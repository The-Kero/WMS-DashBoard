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

        # ★ 210차 최종: 인쇄 API (routes_print.py)와 100% 동일 논리
        # 1) inventory_check: 같은 키의 check_date 내 최신 action이 'diff'인 것
        # 2) inventory_current: HAVING SUM(useqty) > 0 (현재 재고 있는 것만)
        # → "미해결 차이 + 현재 재고 있음" = 어제 재고조사 10건과 정확히 일치
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
                  AND action IN ('check', 'diff')
                  AND deleted_at IS NULL
                ORDER BY locaky, skukey, COALESCE(lota13, ''), check_date, checked_at DESC
            ) ic
            INNER JOIN (
                SELECT locaky, skukey, COALESCE(lota13, '') AS lota13_norm
                FROM inventory_current
                WHERE center = %s AND part = %s
                  AND locaky NOT LIKE 'RCVLOC%%' AND locaky NOT LIKE 'L07RCV%%'
                  AND deleted_at IS NULL
                GROUP BY locaky, skukey, lota13
                HAVING SUM(useqty) > 0
            ) inv
                ON inv.locaky = ic.locaky AND inv.skukey = ic.skukey
                AND inv.lota13_norm = COALESCE(ic.lota13, '')
            LEFT JOIN product_master pm
                ON pm.center_code = ic.center AND pm.part = ic.part
                AND pm.product_code = ic.skukey AND pm.deleted_at IS NULL
            WHERE ic.action = 'diff'
        """, (center, part, start_date, end_date, center, part))
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
