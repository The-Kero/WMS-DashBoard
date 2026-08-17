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


# ============================================================
# ★ 275차: 재고조사 일괄체크 ("전부 동그라미") — 파트장님 요청
# ============================================================
# 배경: 냉장 직원 13명→5명. 매일 전수조사가 물리적으로 불가.
#       아워홈이 "재고조사를 못 봐도 가라로 제출해달라"고 요청.
#       ⇒ 오늘 아직 안 본 줄을 "맞음"으로 한 번에 채워 재고장을 완성한다.
#
# 설계 정본: diary/274차_재고조사_일괄체크_설계_20260816.md (전수검증 빈틈 28개 반영)
#
# 🔴 절대 규칙 (275차 전수검증에서 실제로 돌려보고 나온 것)
#   ① action 은 반드시 'check'
#        - DB CHECK 제약 = ('check','diff','cancel','unlock') → '일괄체크'는 INSERT 실패
#        - 재고장 쿼리도 WHERE action IN ('check','diff') 라 다른 값은 인쇄물에서 탈락
#   ② worker 는 실제 사람 이름을 랜덤 배정
#        - 재고장 PDF 결재란에 그 이름이 필기체(나눔펜글씨)로 자동 서명됨
#          (routes_print.py _add_signatures_to_pdf — filter='all'은 페이지 최다 worker)
#        - '일괄'을 넣으면 8/14 기준 22장 중 12장에 "일괄"이 찍혀 아워홈에 나감
#   ③ reason='일괄체크' 가 가라 표시 자리
#        - 인쇄물엔 안 나오고 /records 상세엔 "사유"로 뜸. 기존 사용 0건이라 충돌 없음
#   ④ 건수는 len() 으로 센다
#        - execute_values 의 cur.rowcount 는 마지막 묶음만 반환 (644건 넣고 43이라 답함)
#   ⑤ change_log 는 요약 1줄만 (이미 455만 줄 · 1GB)
#   ⑥ 대상은 DISTINCT (locaky,skukey,lota13)
#        - inventory_current 유니크키에 lota11(제조일)이 있어 같은 셀이 2~3행 존재(45행)
#   ⑦ system_qty 는 기존 check API 와 똑같이 "자리 합계"
#        - 기존이 lota13을 안 가리고 SUM 하는 버그가 있으나, 우리만 정확히 넣으면
#          같은 재고장에 기준이 두 개 섞인다. 일관성 우선. 버그는 별건으로 수정.
#   ⑧ 오늘 날짜만. 마감된 날은 막는다 (06:01 자동 마감이 어제 것을 매일 잠금)
# ============================================================

# 대상 뽑기 — status(세기)와 run(넣기)이 같은 SQL을 쓴다 (숫자가 어긋나지 않게)
_BULK_TARGET_SQL = """
SELECT DISTINCT ON (ic.locaky, ic.skukey, COALESCE(ic.lota13, ''))
       ic.locaky, ic.skukey, COALESCE(ic.lota13, '') AS lota13,
       (SELECT COALESCE(SUM(i2.useqty), 0) FROM inventory_current i2
         WHERE i2.center = ic.center AND i2.part = ic.part
           AND i2.locaky = ic.locaky AND i2.skukey = ic.skukey
           AND i2.deleted_at IS NULL) AS system_qty
FROM inventory_current ic
WHERE ic.center = %s AND ic.part = %s
  AND ic.locaky NOT LIKE 'RCVLOC%%'
  AND ic.locaky NOT LIKE 'L07RCV%%'
  AND (ic.useqty > 0 OR ic.is_added = true)
  AND ic.deleted_at IS NULL
  AND NOT EXISTS (
      SELECT 1 FROM (
          SELECT DISTINCT ON (locaky, skukey, COALESCE(lota13, ''))
                 locaky, skukey, lota13, action
          FROM inventory_check
          WHERE center = ic.center AND part = ic.part AND check_date = CURRENT_DATE
            AND action IN ('check', 'diff', 'cancel') AND deleted_at IS NULL
            AND (action <> 'check' OR invalidated_at IS NULL)
          ORDER BY locaky, skukey, COALESCE(lota13, ''), checked_at DESC
      ) t
      WHERE t.locaky = ic.locaky AND t.skukey = ic.skukey
        AND COALESCE(t.lota13, '') = COALESCE(ic.lota13, '')
        AND t.action IN ('check', 'diff')
  )
ORDER BY ic.locaky, ic.skukey, COALESCE(ic.lota13, '')
"""

BULK_REASON = '일괄체크'   # 가라 표시 (인쇄물엔 안 나옴)
BULK_DEVICE = 'web'        # 기기 표시 (태블릿은 기기 고유번호가 들어감)


def _bulk_check_password(cur, center, part, password):
    """관리자 비밀번호 확인 — 5001의 _check_admin_password 와 같은 표를 본다.
    (하드코딩하지 않는다. 나중에 비번을 바꿔도 양쪽이 같이 바뀌도록)"""
    if not password:
        return False
    cur.execute(
        "SELECT password FROM admin_passwords WHERE center = %s AND part = %s",
        (center, part))
    row = cur.fetchone()
    return bool(row) and row['password'] == password


def _bulk_take_lock(cur, center, part):
    """★ 275차 최종검증에서 발견 — 두 대에서 동시에 누르면 중복이 들어간다.

    실증: 연결 두 개가 각각 대상을 뽑으니 ★둘 다 638줄을 봤다 (합치면 1276건).
    NOT EXISTS 는 '순서대로 누를 때'만 막아준다. 같은 순간에 누르면 서로를 못 본다.
    ⇒ 센터·파트별 자물쇠를 걸어 한 번에 하나만 통과시킨다.
      트랜잭션이 끝나면(커밋이든 롤백이든) 자동으로 풀린다.
    """
    cur.execute("SELECT pg_try_advisory_xact_lock(hashtext(%s)) AS got",
                (f'bulk_check_{center}_{part}',))
    return bool(cur.fetchone()['got'])


def _bulk_is_closed(cur, center, part):
    """오늘 마감했는지 — 사람 마감이든 06:01 자동 마감이든 둘 다 여기 남는다"""
    cur.execute("""
        SELECT completed_by FROM inventory_check_complete
        WHERE center = %s AND part = %s AND check_date = CURRENT_DATE
          AND deleted_at IS NULL
        LIMIT 1
    """, (center, part))
    return cur.fetchone()


def _bulk_pick_workers(cur, center, part):
    """랜덤에 쓸 이름 후보 — 3단 폴백. (names, weights, source) 반환.

    ① 그날 조사한 사람   → 그날 한 만큼 비율대로 (제일 자연스러움)
    ② 최근 7일 조사한 사람 → 아무도 조사 못 한 날 (21일 중 5일이 여기 해당)
    ③ 활성 직원 명단      → 케로님 지시("태블릿에 보이는 직원 중 랜덤")가 여기 안전망

    ⚠ 앞선 일괄분(reason='일괄체크')은 후보에서 뺀다.
      되돌리고 다시 돌릴 때 우리가 넣은 이름이 다시 뽑히면 비율이 왜곡된다.
    ⚠ worker 표의 '활성' 이름과 교차시킨다.
      과거 기록에 기기 고유번호가 worker로 들어간 행이 1건 있어 그런 값이 섞이지 않게.
    """
    # ① 그날
    cur.execute("""
        SELECT ic.worker AS name, COUNT(*) AS c
        FROM inventory_check ic
        WHERE ic.center = %s AND ic.part = %s AND ic.check_date = CURRENT_DATE
          AND ic.action IN ('check', 'diff') AND ic.deleted_at IS NULL
          AND (ic.reason IS NULL OR ic.reason <> %s)
          AND ic.worker IN (SELECT name FROM worker WHERE status = '활성')
        GROUP BY ic.worker
        ORDER BY ic.worker
    """, (center, part, BULK_REASON))
    rows = cur.fetchall()
    if rows:
        return [r['name'] for r in rows], [int(r['c']) for r in rows], 'today'

    # ② 최근 7일
    cur.execute("""
        SELECT ic.worker AS name, COUNT(*) AS c
        FROM inventory_check ic
        WHERE ic.center = %s AND ic.part = %s
          AND ic.check_date >= CURRENT_DATE - 7
          AND ic.action IN ('check', 'diff') AND ic.deleted_at IS NULL
          AND (ic.reason IS NULL OR ic.reason <> %s)
          AND ic.worker IN (SELECT name FROM worker WHERE status = '활성')
        GROUP BY ic.worker
        ORDER BY ic.worker
    """, (center, part, BULK_REASON))
    rows = cur.fetchall()
    if rows:
        return [r['name'] for r in rows], [int(r['c']) for r in rows], 'recent7'

    # ③ 활성 명단 (균등)
    cur.execute("SELECT name FROM worker WHERE status = '활성' ORDER BY id")
    rows = cur.fetchall()
    if rows:
        return [r['name'] for r in rows], [1] * len(rows), 'roster'

    return [], [], 'none'


# ============================================================
# GET /api/records/bulk-check/status?date=YYYYMMDD
# 버튼을 그릴지 / 눌러도 되는지 판정 (읽기 전용)
# ============================================================
@bp.route('/bulk-check/status', methods=['GET'])
def bulk_check_status():
    date_str = request.args.get('date', '')
    center = request.args.get('center', 'WH15')
    part = request.args.get('part', '냉장')

    today_str = datetime.now().strftime('%Y%m%d')
    is_today = (date_str == today_str)

    result = {
        'success': True,
        'is_today': is_today,
        'today': today_str,
        'is_closed': False,
        'closed_by': None,
        'target_count': 0,
        'bulk_count': 0,
        'worker_source': None,
        'can_run': False,
        'can_undo': False,
        'reason': '',
    }

    # 오늘이 아니면 더 볼 것도 없다 (과거를 채우지 않는다 — 케로님 "마감하면 끝")
    if not is_today:
        result['reason'] = '오늘 날짜에만 쓸 수 있어요'
        return jsonify(result)

    conn = None
    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        closed = _bulk_is_closed(cur, center, part)
        if closed:
            result['is_closed'] = True
            result['closed_by'] = closed['completed_by']

        cur.execute(_BULK_TARGET_SQL, (center, part))
        result['target_count'] = len(cur.fetchall())

        # 오늘 이미 넣은 일괄분 (되돌리기 가능 여부)
        cur.execute("""
            SELECT COUNT(*) AS c FROM inventory_check
            WHERE center = %s AND part = %s AND check_date = CURRENT_DATE
              AND action = 'check' AND reason = %s AND tablet_id = %s
              AND deleted_at IS NULL
        """, (center, part, BULK_REASON, BULK_DEVICE))
        result['bulk_count'] = int(cur.fetchone()['c'])

        names, _w, source = _bulk_pick_workers(cur, center, part)
        result['worker_source'] = source

        cur.close()
        conn.close()

        if result['is_closed']:
            who = '자동' if result['closed_by'] == 'system' else result['closed_by']
            result['reason'] = f"오늘은 이미 마감됐어요 ({who})"
        elif not names:
            result['reason'] = '이름을 넣을 직원이 없어요'
        elif result['target_count'] == 0:
            result['reason'] = '오늘 안 본 항목이 없어요'
        else:
            result['can_run'] = True

        result['can_undo'] = (result['bulk_count'] > 0) and not result['is_closed']

        return jsonify(result)

    except Exception as e:
        # ★ 연결을 반드시 닫는다 (읽기라도 새면 쌓인다)
        if conn:
            try:
                conn.close()
            except Exception:
                pass
        logger.error(f"[bulk-check/status] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# POST /api/records/bulk-check   {date, admin_password, center, part}
# 오늘 안 본 줄을 "맞음"으로 한 번에 채운다 (트랜잭션)
# ============================================================
@bp.route('/bulk-check', methods=['POST'])
def bulk_check_run():
    import random
    from psycopg2.extras import execute_values

    body = request.get_json(silent=True) or {}
    center = body.get('center', 'WH15')
    part = body.get('part', '냉장')
    date_str = body.get('date', '')
    password = body.get('admin_password', '')

    today_str = datetime.now().strftime('%Y%m%d')
    if date_str != today_str:
        return jsonify({'success': False, 'error': '오늘 날짜에만 쓸 수 있어요'}), 400

    conn = None
    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if not _bulk_check_password(cur, center, part, password):
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': '비밀번호가 틀렸어요'}), 403

        # ★ 동시 클릭 차단 (같은 순간에 두 대에서 누르면 중복이 들어간다)
        if not _bulk_take_lock(cur, center, part):
            cur.close()
            conn.close()
            return jsonify({'success': False,
                            'error': '다른 컴퓨터에서 처리 중이에요. 잠시 뒤 다시 해주세요'}), 409

        closed = _bulk_is_closed(cur, center, part)
        if closed:
            cur.close()
            conn.close()
            who = '자동' if closed['completed_by'] == 'system' else closed['completed_by']
            return jsonify({'success': False, 'error': f'오늘은 이미 마감됐어요 ({who})'}), 409

        names, weights, source = _bulk_pick_workers(cur, center, part)
        if not names:
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': '이름을 넣을 직원이 없어요'}), 409

        cur.execute(_BULK_TARGET_SQL, (center, part))
        targets = cur.fetchall()
        if not targets:
            cur.close()
            conn.close()
            return jsonify({'success': True, 'inserted': 0,
                            'detail': '오늘 안 본 항목이 없어요'})

        rng = random.Random()
        rows = []
        for t in targets:
            qty = int(t['system_qty'] or 0)
            rows.append((center, part, t['locaky'], t['skukey'], t['lota13'],
                         'check', rng.choices(names, weights=weights)[0],
                         qty, qty, BULK_REASON, BULK_DEVICE))

        execute_values(cur, """
            INSERT INTO inventory_check
                (center, part, locaky, skukey, lota13,
                 action, worker, system_qty, actual_qty, reason, tablet_id)
            VALUES %s
        """, rows)

        # ★ 건수는 len() 으로. execute_values 의 rowcount 는 마지막 묶음만 센다
        inserted = len(rows)

        # change_log 는 요약 1줄만 (줄마다 넣으면 연 27만 줄)
        cur.execute("""
            INSERT INTO change_log
                (center, part, module, action, source,
                 record_key1, record_key2, field, old_value, new_value, skukey)
            VALUES (%s, %s, '재고조사', '일괄체크', 'web:일괄',
                    '', '', 'action', '', %s, '')
        """, (center, part, f'{inserted}건'))

        conn.commit()
        cur.close()
        conn.close()

        used = {}
        for r in rows:
            used[r[6]] = used.get(r[6], 0) + 1

        logger.info(f"[bulk-check] {inserted}건 일괄체크 (이름출처={source}, 분포={used})")
        return jsonify({
            'success': True,
            'inserted': inserted,
            'worker_source': source,
            'workers': used,
        })

    except Exception as e:
        if conn:
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
        logger.error(f"[bulk-check] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# POST /api/records/bulk-check/undo   {date, admin_password, center, part}
# 그날 일괄분만 되돌린다 (사람이 직접 체크한 줄·차이 줄은 절대 안 건드림)
# ============================================================
@bp.route('/bulk-check/undo', methods=['POST'])
def bulk_check_undo():
    body = request.get_json(silent=True) or {}
    center = body.get('center', 'WH15')
    part = body.get('part', '냉장')
    date_str = body.get('date', '')
    password = body.get('admin_password', '')

    today_str = datetime.now().strftime('%Y%m%d')
    if date_str != today_str:
        return jsonify({'success': False, 'error': '오늘 날짜에만 쓸 수 있어요'}), 400

    conn = None
    try:
        conn = _conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if not _bulk_check_password(cur, center, part, password):
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': '비밀번호가 틀렸어요'}), 403

        # ★ 채우기와 같은 자물쇠 — 채우는 도중에 되돌리기가 끼어들지 않게
        if not _bulk_take_lock(cur, center, part):
            cur.close()
            conn.close()
            return jsonify({'success': False,
                            'error': '다른 컴퓨터에서 처리 중이에요. 잠시 뒤 다시 해주세요'}), 409

        closed = _bulk_is_closed(cur, center, part)
        if closed:
            cur.close()
            conn.close()
            who = '자동' if closed['completed_by'] == 'system' else closed['completed_by']
            return jsonify({'success': False, 'error': f'오늘은 이미 마감됐어요 ({who})'}), 409

        # reason + tablet_id 두 조건으로 좁힌다. 사람이 넣은 기록은 reason이 비어 있다
        cur.execute("""
            UPDATE inventory_check SET deleted_at = NOW()
            WHERE center = %s AND part = %s AND check_date = CURRENT_DATE
              AND action = 'check' AND reason = %s AND tablet_id = %s
              AND deleted_at IS NULL
        """, (center, part, BULK_REASON, BULK_DEVICE))
        deleted = cur.rowcount   # 단일 UPDATE라 rowcount가 정확하다

        if deleted:
            cur.execute("""
                INSERT INTO change_log
                    (center, part, module, action, source,
                     record_key1, record_key2, field, old_value, new_value, skukey)
                VALUES (%s, %s, '재고조사', '일괄취소', 'web:일괄',
                        '', '', 'deleted_at', '', %s, '')
            """, (center, part, f'{deleted}건'))

        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"[bulk-check/undo] {deleted}건 되돌림")
        return jsonify({'success': True, 'deleted': deleted})

    except Exception as e:
        if conn:
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
        logger.error(f"[bulk-check/undo] 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
