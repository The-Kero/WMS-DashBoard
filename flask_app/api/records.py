# -*- coding: utf-8 -*-
"""
재고조사 기록 열람 API (210차 #16)
============================================================
재고조사 결과를 엑셀 포맷 그대로 웹에서 조회.
엑셀 재고표..xlsx를 계승한 월별 매트릭스 + 셀 상세 모달.

엔드포인트:
  GET /api/records/matrix?month=YYYY-MM&center=WH15&part=냉장
  GET /api/records/detail?locaky=&skukey=&lota13=&date=YYYY-MM-DD&...

데이터 소스:
  - inventory_check (메인) — DISTINCT ON 으로 같은 상품/날짜 최신 diff
  - product_master (LEFT JOIN) — 상품명/규격

설계 원칙 (6원칙):
  ①OPS톤(반투명/유리질감) ②7원칙(현장3초/✓기호) ③정합성(엑셀 1:1)
  ④확장성(month/center/part 파라미터) ⑤안정성(읽기 전용 SELECT)
  ⑥무결성(inventory_check DB 그대로)
"""

# ★ 210차 #16: 시즌1 Flask venv_flask는 core.settings 의존성(cryptography) 없으므로
# DB_CONFIG 직접 정의 (CLAUDE.md §3-5 PostgreSQL wms / 1004)
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'wms_db',  # ★ core/settings.py와 동일 (CLAUDE.md 3-5 오타 주의)
    'user': 'postgres',
    'password': '1004',
}

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from calendar import monthrange
import logging

bp = Blueprint('records', __name__, url_prefix='/api/records')
logger = logging.getLogger(__name__)


def _conn():
    conn = psycopg2.connect(**DB_CONFIG)
    # ★ 210차 #16: Windows cp949 로캐일 환경에서 UTF8 강제 (한글 part '냉장' 파라미터)
    conn.set_client_encoding('UTF8')
    return conn


# ============================================================
# GET /api/records/matrix?month=YYYY-MM
# 월별 매트릭스 — 상품×날짜 격자 (엑셀 포맷 계승)
# ============================================================
@bp.route('/matrix', methods=['GET'])
def get_matrix():
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    center = request.args.get('center', 'WH15')
    part = request.args.get('part', '냉장')

    try:
        year, mon = map(int, month.split('-'))
    except ValueError:
        return jsonify({'success': False, 'error': 'month 형식 YYYY-MM'}), 400

    start_date = datetime(year, mon, 1).date()
    last_day = monthrange(year, mon)[1]
    end_date = datetime(year, mon, last_day).date()

    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # ★ 211차 B안(스냅샷): inventory_check 단독 기준 — 과거 기록이 시간 흘러도 동일 표시
        # ★ 211차 cancel 최신 행 버그 수정: 'cancel' 포함해서 DISTINCT ON 최신 뽑고, 외부 WHERE 'diff'로 자동 제외
        # INNER JOIN inventory_current 제거 (현재 재고 여부가 과거 기록 표시 결정하면 안 됨)
        cur.execute("""
            SELECT ic.locaky, ic.skukey, ic.lota13, ic.check_date,
                   ic.actual_qty, ic.system_qty, ic.note,
                   ic.worker, ic.resolved, ic.reason, ic.action,
                   pm.product_name, pm.spec, pm.category
            FROM (
                SELECT DISTINCT ON (locaky, skukey, COALESCE(lota13, ''), check_date)
                    center, part, locaky, skukey, lota13, check_date,
                    action, actual_qty, system_qty, note, worker, resolved, reason
                FROM inventory_check
                WHERE center = %s AND part = %s
                  AND check_date BETWEEN %s AND %s
                  AND action IN ('check', 'diff', 'cancel')
                  AND deleted_at IS NULL
                ORDER BY locaky, skukey, COALESCE(lota13, ''), check_date, checked_at DESC
            ) ic
            LEFT JOIN product_master pm
                ON pm.center_code = ic.center AND pm.part = ic.part
                AND pm.product_code = ic.skukey AND pm.deleted_at IS NULL
            WHERE ic.action = 'diff'
              -- ★ 212차: 현재 재고 있는 셀만 (태블릿 화면과 일치)
              AND EXISTS (
                  SELECT 1 FROM inventory_current invc2
                  WHERE invc2.center = ic.center AND invc2.part = ic.part
                    AND invc2.locaky = ic.locaky AND invc2.skukey = ic.skukey
                    AND COALESCE(invc2.lota13, '') = COALESCE(ic.lota13, '')
                    AND invc2.locaky NOT LIKE 'RCVLOC%%' AND invc2.locaky NOT LIKE 'L07RCV%%'
                    AND invc2.deleted_at IS NULL
                    AND (invc2.useqty > 0 OR invc2.is_added = true)
              )
        """, (center, part, start_date, end_date))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # 상품 기준 그룹화 → 매트릭스
        matrix = {}
        for r in rows:
            key = (r['locaky'], r['skukey'], r['lota13'] or '')
            if key not in matrix:
                matrix[key] = {
                    'locaky': r['locaky'],
                    'skukey': r['skukey'],
                    'lota13': r['lota13'] or '',
                    'product_name': r['product_name'] or '',
                    'spec': r['spec'] or '',
                    'category': r['category'] or '',
                    'days': {}
                }
            diff = (r['actual_qty'] or 0) - (r['system_qty'] or 0)
            matrix[key]['days'][r['check_date'].day] = {
                'diff': diff,
                'note': r['note'] or '',
                'worker': r['worker'] or '',
                'resolved': r['resolved'],
            }

        items = sorted(matrix.values(),
                       key=lambda x: (x['locaky'], x['skukey'], x['lota13']))

        logger.info(f"[records/matrix] {month} {part}: {len(items)}건 상품 매트릭스")
        return jsonify({
            'success': True,
            'month': month,
            'last_day': last_day,
            'center': center,
            'part': part,
            'items': items,
            'total': len(items),
            'timestamp': datetime.now().isoformat(),
        })

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"[records/matrix] 실패: {e}\n{tb}")
        return jsonify({'success': False, 'error': str(e), 'traceback': tb}), 500


# ============================================================
# GET /api/records/detail?locaky=&skukey=&lota13=&date=YYYY-MM-DD
# 셀 클릭 → 해당 상품×날짜 전체 이력 (모달용)
# ============================================================
@bp.route('/detail', methods=['GET'])
def get_detail():
    locaky = request.args.get('locaky', '')
    skukey = request.args.get('skukey', '')
    lota13 = request.args.get('lota13', '')
    date_str = request.args.get('date', '')
    center = request.args.get('center', 'WH15')
    part = request.args.get('part', '냉장')

    if not locaky or not skukey or not date_str:
        return jsonify({'success': False, 'error': 'locaky/skukey/date 필수'}), 400

    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT action, worker, actual_qty, system_qty, note, reason,
                   resolved, checked_at
            FROM inventory_check
            WHERE center=%s AND part=%s AND locaky=%s AND skukey=%s
              AND (COALESCE(lota13, '') = %s)
              AND DATE(checked_at) = %s
              AND deleted_at IS NULL
            ORDER BY checked_at
        """, (center, part, locaky, skukey, lota13, date_str))
        events = []
        for r in cur.fetchall():
            events.append({
                'action': r['action'],
                'worker': r['worker'],
                'system_qty': r['system_qty'],
                'actual_qty': r['actual_qty'],
                'diff': (r['actual_qty'] or 0) - (r['system_qty'] or 0),
                'note': r['note'] or '',
                'reason': r['reason'] or '',
                'resolved': r['resolved'],
                'time': r['checked_at'].strftime('%H:%M:%S') if r['checked_at'] else '',
            })
        cur.close()
        conn.close()

        return jsonify({
            'success': True,
            'locaky': locaky, 'skukey': skukey,
            'lota13': lota13, 'date': date_str,
            'events': events,
            'count': len(events),
        })

    except Exception as e:
        logger.error(f"[records/detail] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# POST /api/records/print
# 태블릿 양식 PDF 미리보기 프록시 (5000 → 5001 /api/print/inventory?preview=true)
# 211차 추가: 매트릭스 날짜 헤더 클릭 시 그 날짜의 태블릿 양식으로 인쇄
# Body: {date: YYYYMMDD, filter: 'diff'|'all'|'caution', center, part}
# 반환: application/pdf (PDF 바이트 그대로)
# ============================================================
@bp.route('/print', methods=['POST'])
def proxy_print_inventory():
    """5001 재고장 인쇄 API 프록시 — 브라우저 CORS 회피용. venv_flask에 requests 없어 urllib 사용"""
    import urllib.request
    import urllib.error
    import json as _json
    from flask import Response

    body = request.get_json(silent=True) or {}
    # ★ silent=True 파싱 실패(인코딩 꼬임 등) 폴백 — 유효한 JSON 구조만 있으면 살림
    if not body:
        try:
            import json as __j
            body = __j.loads(request.data.decode('utf-8', errors='replace')) if request.data else {}
        except Exception as _e:
            logger.warning(f"[proxy_print] JSON parse fallback failed: {_e}")
            body = {}
    body['preview'] = True  # ★ 강제: 프린터 전송 안 함, PDF 반환만
    logger.info(f"[proxy_print] date={body.get('date')} filter={body.get('filter')} part={body.get('part')}")

    try:
        req = urllib.request.Request(
            'http://10.60.27.130:5001/api/print/inventory',
            data=_json.dumps(body, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
            ct = r.headers.get('Content-Type', '')
            cd = r.headers.get('Content-Disposition', 'inline; filename="재고장.pdf"')
            content = r.read()

        if 'application/pdf' in ct:
            return Response(content, mimetype='application/pdf', headers={
                'Content-Disposition': cd
            })
        return Response(content, mimetype=ct, status=status)

    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')[:500]
        return jsonify({'success': False, 'error': f'5001 HTTP {e.code}', 'detail': detail}), e.code
    except Exception as e:
        logger.error(f"[records/print] 프록시 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# ★ 222차 #45: 상품 자동완성 (태블릿 search-product와 동일 스펙, 독립 구현)
# GET /api/records/search-product?q=검색어&center=WH15&part=냉장
# 2글자 이상 필수, 최대 20건
# ============================================================
@bp.route('/search-product', methods=['GET'])
def search_product():
    q = request.args.get('q', '').strip()
    center = request.args.get('center', 'WH15')
    part = request.args.get('part', '냉장')

    if len(q) < 2:
        return jsonify({'success': False, 'error': '2글자 이상 입력'}), 400

    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # product_master ILIKE 부분 매칭 + inventory_current에서 qtduom 조회 (태블릿 동일 스펙)
        cur.execute("""
            SELECT pm.product_code, pm.product_name, pm.spec, pm.stock_location,
                   COALESCE((SELECT ic.qtduom FROM inventory_current ic
                             WHERE ic.center = pm.center_code AND ic.part = pm.part
                               AND ic.skukey = pm.product_code AND ic.deleted_at IS NULL
                             LIMIT 1), 0) as qtduom
            FROM product_master pm
            WHERE pm.center_code = %s AND pm.part = %s AND pm.deleted_at IS NULL
              AND (pm.product_name ILIKE %s OR pm.product_code ILIKE %s)
            ORDER BY pm.product_name
            LIMIT 20
        """, (center, part, f"%{q}%", f"%{q}%"))
        products = cur.fetchall()
        cur.close()
        conn.close()

        logger.info(f"[records/search-product] q={q!r} → {len(products)}건")
        return jsonify({
            'success': True,
            'products': [dict(p) for p in products],
            'count': len(products),
        })
    except Exception as e:
        logger.error(f"[records/search-product] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# ★ 222차 #45: 상품별 재고조사 이력 (최근 N일)
# GET /api/records/product-history?skukey=&days=7&center=WH15&part=냉장
# 모든 action(check/diff/cancel/unlock/add_item) 포함, 시간역순
# ============================================================
@bp.route('/product-history', methods=['GET'])
def product_history():
    skukey = request.args.get('skukey', '').strip()
    center = request.args.get('center', 'WH15')
    part = request.args.get('part', '냉장')
    try:
        days = int(request.args.get('days', '7'))
        if days < 1 or days > 365:
            days = 7
    except ValueError:
        days = 7

    if not skukey:
        return jsonify({'success': False, 'error': 'skukey 필수'}), 400

    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # 상품 기본 정보 (상품명/규격/기본로케)
        cur.execute("""
            SELECT product_code, product_name, spec, stock_location
            FROM product_master
            WHERE center_code = %s AND part = %s AND product_code = %s AND deleted_at IS NULL
            LIMIT 1
        """, (center, part, skukey))
        pm = cur.fetchone()

        # 기간 내 재고조사 이벤트 — 매트릭스(get_matrix)와 동일 DISTINCT ON 패턴
        # ★ 222차 #45-3: 같은 (날짜, 로케, 소비기한) 조합은 최신 1건만 (중간 cancel/note 스킵)
        # 내부: DISTINCT ON (check_date, locaky, lota13) + checked_at DESC → 각 조합 최신
        # 외부: check_date ASC, locaky ASC, checked_at ASC → 시선 흐름 위→아래
        cur.execute("""
            SELECT * FROM (
                SELECT DISTINCT ON (ic.check_date, ic.locaky, COALESCE(ic.lota13, ''))
                    ic.checked_at, ic.check_date, ic.locaky, ic.skukey, ic.lota13,
                    ic.action, ic.worker, ic.system_qty, ic.actual_qty,
                    ic.note, ic.reason, ic.resolved, ic.is_added
                FROM inventory_check ic
                WHERE ic.center = %s AND ic.part = %s AND ic.skukey = %s
                  AND ic.check_date >= CURRENT_DATE - INTERVAL '%s days'
                  AND ic.deleted_at IS NULL
                ORDER BY ic.check_date, ic.locaky, COALESCE(ic.lota13, ''), ic.checked_at DESC
            ) sub
            ORDER BY check_date ASC, locaky ASC, checked_at ASC
            LIMIT 500
        """, (center, part, skukey, days))

        events = []
        for r in cur.fetchall():
            diff = (r['actual_qty'] or 0) - (r['system_qty'] or 0) if r['action'] == 'diff' else 0
            events.append({
                'check_date': r['check_date'].strftime('%Y-%m-%d') if r['check_date'] else '',
                'time': r['checked_at'].strftime('%H:%M:%S') if r['checked_at'] else '',
                'locaky': r['locaky'],
                'lota13': r['lota13'] or '',
                'action': r['action'],
                'worker': r['worker'] or '',
                'system_qty': r['system_qty'] or 0,
                'actual_qty': r['actual_qty'] or 0,
                'diff': diff,
                'note': r['note'] or '',
                'reason': r['reason'] or '',
                'resolved': r['resolved'],
                'is_added': r['is_added'] or False,
            })
        cur.close()
        conn.close()

        logger.info(f"[records/product-history] skukey={skukey} days={days} → {len(events)}건")
        return jsonify({
            'success': True,
            'product': {
                'skukey': skukey,
                'product_name': pm['product_name'] if pm else '',
                'spec': pm['spec'] if pm else '',
                'stock_location': pm['stock_location'] if pm else '',
            } if pm else {'skukey': skukey, 'product_name': '', 'spec': '', 'stock_location': ''},
            'days': days,
            'events': events,
            'count': len(events),
        })
    except Exception as e:
        logger.error(f"[records/product-history] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# ★ 222차 #45-4: 긴 형식 CSV 다운로드용 (엑셀 필터/피벗 분석 최적)
# GET /api/records/export-csv?month=YYYY-MM&center=WH15&part=냉장
# 매트릭스와 동일 스코프 (월별 + diff만 + 현재 재고 있는 셀만)
# 18컬럼: 날짜/요일/시간/로케/기본로케/상품코드/상품명/규격/소비기한/
#        액션/작업자/가용/실사/차이/비고/사유/해결/항목추가
# ============================================================
@bp.route('/export-csv', methods=['GET'])
def export_csv():
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    center = request.args.get('center', 'WH15')
    part = request.args.get('part', '냉장')

    try:
        year, mon = map(int, month.split('-'))
    except ValueError:
        return jsonify({'success': False, 'error': 'month 형식 YYYY-MM'}), 400

    start_date = datetime(year, mon, 1).date()
    last_day = monthrange(year, mon)[1]
    end_date = datetime(year, mon, last_day).date()

    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # 매트릭스 쿼리(L76~106)와 동일 + checked_at/is_added/stock_location 추가
        cur.execute("""
            SELECT ic.locaky, ic.skukey, ic.lota13, ic.check_date, ic.checked_at,
                   ic.actual_qty, ic.system_qty, ic.note,
                   ic.worker, ic.resolved, ic.reason, ic.action, ic.is_added,
                   pm.product_name, pm.spec, pm.stock_location
            FROM (
                SELECT DISTINCT ON (locaky, skukey, COALESCE(lota13, ''), check_date)
                    center, part, locaky, skukey, lota13, check_date, checked_at,
                    action, actual_qty, system_qty, note, worker, resolved, reason, is_added
                FROM inventory_check
                WHERE center = %s AND part = %s
                  AND check_date BETWEEN %s AND %s
                  AND action IN ('check', 'diff', 'cancel')
                  AND deleted_at IS NULL
                ORDER BY locaky, skukey, COALESCE(lota13, ''), check_date, checked_at DESC
            ) ic
            LEFT JOIN product_master pm
                ON pm.center_code = ic.center AND pm.part = ic.part
                AND pm.product_code = ic.skukey AND pm.deleted_at IS NULL
            WHERE ic.action = 'diff'
              AND EXISTS (
                  SELECT 1 FROM inventory_current invc2
                  WHERE invc2.center = ic.center AND invc2.part = ic.part
                    AND invc2.locaky = ic.locaky AND invc2.skukey = ic.skukey
                    AND COALESCE(invc2.lota13, '') = COALESCE(ic.lota13, '')
                    AND invc2.locaky NOT LIKE 'RCVLOC%%' AND invc2.locaky NOT LIKE 'L07RCV%%'
                    AND invc2.deleted_at IS NULL
                    AND (invc2.useqty > 0 OR invc2.is_added = true)
              )
            ORDER BY ic.check_date, ic.locaky, ic.skukey
        """, (center, part, start_date, end_date))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        events = []
        for r in rows:
            events.append({
                'check_date': r['check_date'].strftime('%Y-%m-%d') if r['check_date'] else '',
                'time': r['checked_at'].strftime('%H:%M:%S') if r['checked_at'] else '',
                'locaky': r['locaky'],
                'skukey': r['skukey'],
                'product_name': r['product_name'] or '',
                'spec': r['spec'] or '',
                'stock_location': r['stock_location'] or '',
                'lota13': r['lota13'] or '',
                'action': r['action'],
                'worker': r['worker'] or '',
                'system_qty': r['system_qty'] or 0,
                'actual_qty': r['actual_qty'] or 0,
                'note': r['note'] or '',
                'reason': r['reason'] or '',
                'resolved': r['resolved'],
                'is_added': r['is_added'] or False,
            })

        logger.info(f"[records/export-csv] {month} {part}: {len(events)}건")
        return jsonify({
            'success': True,
            'month': month,
            'center': center,
            'part': part,
            'events': events,
            'count': len(events),
        })
    except Exception as e:
        logger.error(f"[records/export-csv] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
