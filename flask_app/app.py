"""
WMS Dashboard Flask Application
메인 애플리케이션 파일
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_caching import Cache
from datetime import datetime
from pathlib import Path
import logging
from pathlib import Path

# Flask 앱 생성
app = Flask(__name__)

# CORS 설정 (모든 도메인 허용)
CORS(app)

# 캐시 설정 (30초)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 30
cache = Cache(app)

# 로깅 설정
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'app.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(log_file), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================
# API Blueprint 등록
# ============================================================

from api.inbound import bp as inbound_bp
from api.outbound import bp as outbound_bp
from api.inventory import bp as inventory_bp
from api.delete import bp as delete_bp
from api.irregular import bp as irregular_bp
from api.dashboard import bp as dashboard_bp
from api.schedule import bp as schedule_bp
from api.records import bp as records_bp  # ★ 210차 #16: 재고조사 기록 열람

app.register_blueprint(inbound_bp)
app.register_blueprint(outbound_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(irregular_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(records_bp)  # ★ 210차 #16


# ============================================================
# 루트 엔드포인트
# ============================================================

@app.route('/')
def index():
    """메인 페이지 - dashboard.html 렌더링"""
    logger.info("메인 페이지 접근")
    return render_template('dashboard.html')


@app.route('/admin/schedule')
def schedule_admin():
    """스케줄 관리 페이지"""
    logger.info("스케줄 관리 페이지 접근")
    return render_template('schedule_admin.html')


@app.route('/records')
def records_page():
    """★ 210차 #16: 재고조사 기록 열람 페이지"""
    logger.info("재고조사 기록 페이지 접근")
    return render_template('records.html')


@app.route('/api/health')
def health_check():
    """헬스 체크 API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Flask 서버 정상 작동 중'
    })


@app.route('/sound_test')
def sound_test():
    """긴급알림 소리 샘플 테스트 페이지"""
    logger.info("소리 테스트 페이지 접근")
    return render_template('sound_test.html')


@app.route('/sample')
def sample_report():
    """샘플 보고서 페이지 (상부 보고용)"""
    logger.info("샘플 보고서 페이지 접근")
    return render_template('sample_report.html')


# ============================================================
# 에러 핸들러
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """404 에러 처리"""
    logger.warning(f"404 에러: {error}")
    return jsonify({
        'success': False,
        'error': '요청한 리소스를 찾을 수 없습니다',
        'status_code': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 에러 처리"""
    logger.error(f"500 에러: {error}")
    return jsonify({
        'success': False,
        'error': '서버 내부 오류가 발생했습니다',
        'status_code': 500
    }), 500


# ============================================================
# 메인 실행
# ============================================================

if __name__ == '__main__':
    # logs 폴더 생성
    Path('logs').mkdir(exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("Flask 서버 시작")
    logger.info(f"시작 시간: {datetime.now()}")
    logger.info("=" * 60)
    
    # Flask 서버 실행
    app.run(
        host='0.0.0.0',  # 모든 IP에서 접근 가능
        port=5000,
        debug=False  # 2026-06-21: 디스크풀 사건 — 리로더 다중프로세스+로그폭증 차단
    )
