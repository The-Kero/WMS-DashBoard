# 🚀 Phase 2 진척도 관리 (극세분화 v2.0)

**프로젝트**: WMS Dashboard - Flask TV 시스템  
**시작일**: 2025-11-16 (토)  
**예상 완료일**: 2025-11-23 (토)  
**현재 진척률**: 0% (0/417 작업 완료)

---

## 📊 전체 진척도 대시보드

| Day | 날짜 | 주요 작업 | 체크박스 | 완료 | 진척률 | 상태 | 소요시간 |
|-----|------|----------|----------|------|--------|------|----------|
| Day 1 | 2025-11-16 (토) | Flask 환경 + 5개 API | 80개 | 0 | 0% | ⏳ 대기 | - |
| Day 2 | 2025-11-17 (일) | 통합 API + 에러처리 | 50개 | 0 | 0% | ⏳ 대기 | - |
| Day 3 | 2025-11-18 (월) | pytest 테스트 | 40개 | 0 | 0% | ⏳ 대기 | - |
| Day 4 | 2025-11-19 (화) | HTML 템플릿 | 45개 | 0 | 0% | ⏳ 대기 | - |
| Day 5 | 2025-11-20 (수) | JavaScript 30초 갱신 | 50개 | 0 | 0% | ⏳ 대기 | - |
| Day 6 | 2025-11-21 (목) | CSS TV 최적화 | 37개 | 0 | 0% | ⏳ 대기 | - |
| Day 7 | 2025-11-22 (금) | 성능 + 안정성 | 40개 | 0 | 0% | ⏳ 대기 | - |
| Day 8 | 2025-11-23 (토) | 배포 + 검증 | 35개 | 0 | 0% | ⏳ 대기 | - |
| **합계** | **8일** | **Flask TV 시스템** | **377개** | **0** | **0%** | ⏳ | **0시간** |

---

## ✅ Day 1: Flask 기본 구조 (2025-11-16)

**목표**: Flask 환경 구축 + 5개 API 엔드포인트 완성  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/80개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - 환경 구축

#### 1.1 가상환경 생성 (30분)
- [ ] 1.1.1 터미널 열기 (PowerShell 또는 CMD)
- [ ] 1.1.2 `cd C:\Projects\WMS-DashBoard` 이동
- [ ] 1.1.3 `mkdir flask_app` 폴더 생성
- [ ] 1.1.4 `cd flask_app` 이동
- [ ] 1.1.5 `python -m venv venv_flask` 실행
- [ ] 1.1.6 가상환경 생성 완료 대기 (약 1분)
- [ ] 1.1.7 venv_flask 폴더 생성 확인
- [ ] 1.1.8 `venv_flask\Scripts\activate` 활성화
- [ ] 1.1.9 프롬프트에 (venv_flask) 표시 확인
- [ ] 1.1.10 `python --version` 확인 (3.9+ 필요)

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.2 패키지 설치 (30분)
- [ ] 1.2.1 `pip install Flask==3.0.0` 실행
- [ ] 1.2.2 Flask 설치 완료 확인 (약 30초)
- [ ] 1.2.3 `pip install Flask-CORS==4.0.0` 실행
- [ ] 1.2.4 Flask-CORS 설치 완료 확인
- [ ] 1.2.5 `pip install Flask-Caching==2.1.0` 실행
- [ ] 1.2.6 Flask-Caching 설치 완료 확인
- [ ] 1.2.7 `pip install pandas==2.0.3` 실행
- [ ] 1.2.8 pandas 설치 완료 확인 (약 1분)
- [ ] 1.2.9 `pip install python-dotenv==1.0.0` 실행
- [ ] 1.2.10 python-dotenv 설치 완료 확인
- [ ] 1.2.11 `pip list` 로 설치 패키지 확인
- [ ] 1.2.12 필수 패키지 5개 확인 (Flask, Flask-CORS, Flask-Caching, pandas, python-dotenv)
- [ ] 1.2.13 `pip freeze > requirements.txt` 실행
- [ ] 1.2.14 requirements.txt 파일 생성 확인
- [ ] 1.2.15 requirements.txt 열어서 내용 확인

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.3 프로젝트 구조 생성 (30분)
- [ ] 1.3.1 `mkdir api` 폴더 생성
- [ ] 1.3.2 `type nul > api\__init__.py` 생성
- [ ] 1.3.3 api\__init__.py 파일 확인
- [ ] 1.3.4 `mkdir services` 폴더 생성
- [ ] 1.3.5 `type nul > services\__init__.py` 생성
- [ ] 1.3.6 services\__init__.py 파일 확인
- [ ] 1.3.7 `mkdir templates` 폴더 생성
- [ ] 1.3.8 `mkdir static` 폴더 생성
- [ ] 1.3.9 `mkdir static\css` 폴더 생성
- [ ] 1.3.10 `mkdir static\js` 폴더 생성
- [ ] 1.3.11 `mkdir static\images` 폴더 생성
- [ ] 1.3.12 `mkdir logs` 폴더 생성
- [ ] 1.3.13 `mkdir tests` 폴더 생성
- [ ] 1.3.14 `tree /F` 명령으로 폴더 구조 확인
- [ ] 1.3.15 총 7개 폴더 생성 확인

**완료 시간**: ___  
**이슈**: 없음

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - 설정 파일

#### 1.4 .env 파일 생성 (15분)
- [ ] 1.4.1 `type nul > .env` 파일 생성
- [ ] 1.4.2 .env 파일 확인
- [ ] 1.4.3 VS Code (또는 편집기)로 .env 열기
- [ ] 1.4.4 `FLASK_APP=app.py` 입력
- [ ] 1.4.5 `FLASK_ENV=development` 입력
- [ ] 1.4.6 `FLASK_DEBUG=True` 입력
- [ ] 1.4.7 `HOST=0.0.0.0` 입력
- [ ] 1.4.8 `PORT=5000` 입력
- [ ] 1.4.9 `DATA_PATH=C:/OSIS_AUTO` 입력
- [ ] 1.4.10 `CACHE_TYPE=simple` 입력
- [ ] 1.4.11 `CACHE_DEFAULT_TIMEOUT=30` 입력
- [ ] 1.4.12 `LOG_LEVEL=INFO` 입력
- [ ] 1.4.13 `LOG_FILE=logs/app.log` 입력
- [ ] 1.4.14 .env 파일 저장 (Ctrl+S)
- [ ] 1.4.15 .env 파일 내용 재확인 (13줄)

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.5 app.py 기본 구조 (60분)
- [ ] 1.5.1 `type nul > app.py` 파일 생성
- [ ] 1.5.2 VS Code로 app.py 열기
- [ ] 1.5.3 `from flask import Flask, jsonify` import
- [ ] 1.5.4 `from flask_cors import CORS` import
- [ ] 1.5.5 `from flask_caching import Cache` import
- [ ] 1.5.6 `import logging` import
- [ ] 1.5.7 `import os` import
- [ ] 1.5.8 `from datetime import datetime` import
- [ ] 1.5.9 `from dotenv import load_dotenv` import
- [ ] 1.5.10 빈 줄 추가 (import 구분)
- [ ] 1.5.11 `load_dotenv()` 호출 추가
- [ ] 1.5.12 빈 줄 추가
- [ ] 1.5.13 `app = Flask(__name__)` 추가
- [ ] 1.5.14 빈 줄 추가
- [ ] 1.5.15 `CORS(app, resources={r"/api/*": {"origins": "*"}})` 추가
- [ ] 1.5.16 빈 줄 추가
- [ ] 1.5.17 Cache 설정 dict 작성 시작
- [ ] 1.5.18 `cache = Cache(app, config={'CACHE_TYPE': ...})` 완성
- [ ] 1.5.19 빈 줄 추가
- [ ] 1.5.20 logging.basicConfig() 시작
- [ ] 1.5.21 level=logging.INFO 설정
- [ ] 1.5.22 format 문자열 설정
- [ ] 1.5.23 handlers 리스트 설정 (FileHandler, StreamHandler)
- [ ] 1.5.24 logging.basicConfig() 완성
- [ ] 1.5.25 `logger = logging.getLogger(__name__)` 추가
- [ ] 1.5.26 빈 줄 2개 추가
- [ ] 1.5.27 `@app.route('/')` 데코레이터
- [ ] 1.5.28 `def index():` 함수 정의
- [ ] 1.5.29 return 문 작성 (환영 메시지)
- [ ] 1.5.30 빈 줄 2개 추가
- [ ] 1.5.31 `@app.route('/api/health')` 데코레이터
- [ ] 1.5.32 `def health():` 함수 정의
- [ ] 1.5.33 dict 생성 (status, timestamp, version)
- [ ] 1.5.34 `return jsonify(...)` 추가
- [ ] 1.5.35 빈 줄 2개 추가
- [ ] 1.5.36 `@app.errorhandler(404)` 데코레이터
- [ ] 1.5.37 `def not_found(error):` 함수 정의
- [ ] 1.5.38 404 에러 응답 return
- [ ] 1.5.39 빈 줄 2개 추가
- [ ] 1.5.40 `@app.errorhandler(500)` 데코레이터
- [ ] 1.5.41 `def internal_error(error):` 함수 정의
- [ ] 1.5.42 logger.error() 로그 추가
- [ ] 1.5.43 500 에러 응답 return
- [ ] 1.5.44 빈 줄 2개 추가
- [ ] 1.5.45 `if __name__ == '__main__':` 블록
- [ ] 1.5.46 `host = os.getenv('HOST', '0.0.0.0')` 추가
- [ ] 1.5.47 `port = int(os.getenv('PORT', 5000))` 추가
- [ ] 1.5.48 `debug = os.getenv('FLASK_DEBUG', 'False') == 'True'` 추가
- [ ] 1.5.49 빈 줄 추가
- [ ] 1.5.50 logger.info() 시작 메시지 추가
- [ ] 1.5.51 `app.run(host=host, port=port, debug=debug)` 추가
- [ ] 1.5.52 app.py 파일 저장
- [ ] 1.5.53 파일 라인 수 확인 (약 60줄)
- [ ] 1.5.54 `python app.py` 실행
- [ ] 1.5.55 Flask 서버 시작 확인
- [ ] 1.5.56 "Running on http://0.0.0.0:5000" 메시지 확인
- [ ] 1.5.57 새 터미널 열기
- [ ] 1.5.58 브라우저에서 `localhost:5000` 접속
- [ ] 1.5.59 환영 메시지 표시 확인
- [ ] 1.5.60 브라우저에서 `localhost:5000/api/health` 접속
- [ ] 1.5.61 JSON 응답 확인 (status: "ok")
- [ ] 1.5.62 logs 폴더 확인
- [ ] 1.5.63 logs/app.log 파일 생성 확인
- [ ] 1.5.64 app.log 내용 확인 (INFO 로그)
- [ ] 1.5.65 Flask 서버 중지 (Ctrl+C)

**완료 시간**: ___  
**이슈**: 없음

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - Collector 연동

#### 1.6 CollectorService 기본 구조 (45분)
- [ ] 1.6.1 `type nul > services\collector_service.py` 생성
- [ ] 1.6.2 VS Code로 collector_service.py 열기
- [ ] 1.6.3 `import sys` 추가
- [ ] 1.6.4 `from pathlib import Path` 추가
- [ ] 1.6.5 `from datetime import datetime` 추가
- [ ] 1.6.6 `from typing import Dict, Any` 추가
- [ ] 1.6.7 빈 줄 2개 추가
- [ ] 1.6.8 `# Collector 경로 추가` 주석
- [ ] 1.6.9 `collector_path = Path(__file__).parent.parent.parent / ...` 작성
- [ ] 1.6.10 경로 확인 (dashboard/src/data/collectors)
- [ ] 1.6.11 `sys.path.insert(0, str(collector_path))` 추가
- [ ] 1.6.12 빈 줄 2개 추가
- [ ] 1.6.13 `# Collector import` 주석
- [ ] 1.6.14 `from inbound import InboundCollector` 추가
- [ ] 1.6.15 `from outbound import OutboundCollector` 추가
- [ ] 1.6.16 `from inventory import InventoryCollector` 추가
- [ ] 1.6.17 `from delete import DeleteCollector` 추가
- [ ] 1.6.18 `from irregular import IrregularCollector` 추가
- [ ] 1.6.19 빈 줄 2개 추가
- [ ] 1.6.20 `class CollectorService:` 정의
- [ ] 1.6.21 docstring 추가
- [ ] 1.6.22 빈 줄 추가
- [ ] 1.6.23 `def __init__(self, data_path: str = "C:/OSIS_AUTO"):` 작성
- [ ] 1.6.24 `self.data_path = data_path` 추가
- [ ] 1.6.25 `self.collectors = {}` 추가
- [ ] 1.6.26 빈 줄 2개 추가
- [ ] 1.6.27 파일 저장
- [ ] 1.6.28 새 파일 생성: test_import.py
- [ ] 1.6.29 test_import.py에 테스트 코드 작성
- [ ] 1.6.30 `python test_import.py` 실행
- [ ] 1.6.31 import 에러 확인
- [ ] 1.6.32 에러 발생 시 collector_path 경로 수정
- [ ] 1.6.33 import 성공 확인
- [ ] 1.6.34 "All imports successful!" 메시지 확인
- [ ] 1.6.35 test_import.py 삭제

**완료 시간**: ___  
**이슈**: 없음

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 5개 API 엔드포인트

#### 1.7 api/inbound.py 작성 (25분)
- [ ] 1.7.1 `type nul > api\inbound.py` 생성
- [ ] 1.7.2 VS Code로 inbound.py 열기
- [ ] 1.7.3 `from flask import Blueprint, jsonify` import
- [ ] 1.7.4 `from datetime import datetime` import
- [ ] 1.7.5 `import sys` import
- [ ] 1.7.6 `from pathlib import Path` import
- [ ] 1.7.7 빈 줄 2개 추가
- [ ] 1.7.8 collector_path 경로 설정
- [ ] 1.7.9 `sys.path.insert(0, str(collector_path))` 추가
- [ ] 1.7.10 `from inbound import InboundCollector` import
- [ ] 1.7.11 빈 줄 2개 추가
- [ ] 1.7.12 `bp = Blueprint('inbound', __name__, url_prefix='/api')` 생성
- [ ] 1.7.13 빈 줄 2개 추가
- [ ] 1.7.14 `@bp.route('/inbound', methods=['GET'])` 데코레이터
- [ ] 1.7.15 `def get_inbound():` 함수 정의
- [ ] 1.7.16 docstring 추가
- [ ] 1.7.17 `try:` 블록 시작
- [ ] 1.7.18 `today = datetime.now().strftime("%Y%m%d")` 추가
- [ ] 1.7.19 file_path 문자열 작성
- [ ] 1.7.20 `collector = InboundCollector(file_path=..., encoding='utf-8-sig')` 추가
- [ ] 1.7.21 빈 줄 추가
- [ ] 1.7.22 `if not collector.validate():` 조건문
- [ ] 1.7.23 에러 응답 return
- [ ] 1.7.24 빈 줄 추가
- [ ] 1.7.25 `summary = collector.get_summary()` 추가
- [ ] 1.7.26 `data = collector.get_data()` 추가
- [ ] 1.7.27 빈 줄 추가
- [ ] 1.7.28 성공 응답 dict 작성
- [ ] 1.7.29 `return jsonify(...)` 추가
- [ ] 1.7.30 빈 줄 추가
- [ ] 1.7.31 `except FileNotFoundError:` 블록
- [ ] 1.7.32 404 에러 응답 return
- [ ] 1.7.33 `except Exception as e:` 블록
- [ ] 1.7.34 500 에러 응답 return
- [ ] 1.7.35 파일 저장

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.8 api/outbound.py 작성 (20분)
- [ ] 1.8.1 `type nul > api\outbound.py` 생성
- [ ] 1.8.2 inbound.py 내용 복사
- [ ] 1.8.3 Blueprint 이름 'outbound'로 변경
- [ ] 1.8.4 import OutboundCollector로 변경
- [ ] 1.8.5 route '/outbound'로 변경
- [ ] 1.8.6 함수명 get_outbound로 변경
- [ ] 1.8.7 file_path 경로 수정 (Outbound Status/outbound_all_)
- [ ] 1.8.8 OutboundCollector 사용으로 변경
- [ ] 1.8.9 docstring 수정
- [ ] 1.8.10 파일 저장

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.9 api/inventory.py 작성 (20분)
- [ ] 1.9.1 `type nul > api\inventory.py` 생성
- [ ] 1.9.2 inbound.py 내용 복사
- [ ] 1.9.3 Blueprint 이름 'inventory'로 변경
- [ ] 1.9.4 import InventoryCollector로 변경
- [ ] 1.9.5 route '/inventory'로 변경
- [ ] 1.9.6 함수명 get_inventory로 변경
- [ ] 1.9.7 file_path 경로 수정 (inventory_status/inventory_status_)
- [ ] 1.9.8 InventoryCollector 사용으로 변경
- [ ] 1.9.9 `risky = collector.get_risky_products(threshold=20)` 추가
- [ ] 1.9.10 응답에 risky_products 추가
- [ ] 1.9.11 docstring 수정
- [ ] 1.9.12 파일 저장

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.10 api/delete.py 작성 (20분)
- [ ] 1.10.1 `type nul > api\delete.py` 생성
- [ ] 1.10.2 inbound.py 내용 복사
- [ ] 1.10.3 Blueprint 이름 'delete'로 변경
- [ ] 1.10.4 import DeleteCollector로 변경
- [ ] 1.10.5 route '/delete'로 변경
- [ ] 1.10.6 함수명 get_delete로 변경
- [ ] 1.10.7 file_path 경로 수정 (Delete Status/delete_status_)
- [ ] 1.10.8 DeleteCollector 사용으로 변경
- [ ] 1.10.9 `after_18 = collector.get_after_18_deletes()` 추가
- [ ] 1.10.10 응답에 after_18_deletes 추가
- [ ] 1.10.11 docstring 수정
- [ ] 1.10.12 파일 저장

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.11 api/irregular.py 작성 (20분)
- [ ] 1.11.1 `type nul > api\irregular.py` 생성
- [ ] 1.11.2 inbound.py 내용 복사
- [ ] 1.11.3 Blueprint 이름 'irregular'로 변경
- [ ] 1.11.4 import IrregularCollector로 변경
- [ ] 1.11.5 route '/irregular'로 변경
- [ ] 1.11.6 함수명 get_irregular로 변경
- [ ] 1.11.7 file_path 경로 수정 (IrregularOrder Status/irregular_order_)
- [ ] 1.11.8 IrregularCollector 사용으로 변경
- [ ] 1.11.9 `unlabeled = collector.get_unlabeled_orders()` 추가
- [ ] 1.11.10 응답에 unlabeled_orders 추가
- [ ] 1.11.11 docstring 수정
- [ ] 1.11.12 파일 저장

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.12 app.py에 Blueprint 등록 (15분)
- [ ] 1.12.1 app.py 열기
- [ ] 1.12.2 logger 정의 다음에 빈 줄 2개 추가
- [ ] 1.12.3 `# API 블루프린트 등록` 주석 추가
- [ ] 1.12.4 `from api.inbound import bp as inbound_bp` import
- [ ] 1.12.5 `from api.outbound import bp as outbound_bp` import
- [ ] 1.12.6 `from api.inventory import bp as inventory_bp` import
- [ ] 1.12.7 `from api.delete import bp as delete_bp` import
- [ ] 1.12.8 `from api.irregular import bp as irregular_bp` import
- [ ] 1.12.9 빈 줄 추가
- [ ] 1.12.10 `app.register_blueprint(inbound_bp)` 추가
- [ ] 1.12.11 `app.register_blueprint(outbound_bp)` 추가
- [ ] 1.12.12 `app.register_blueprint(inventory_bp)` 추가
- [ ] 1.12.13 `app.register_blueprint(delete_bp)` 추가
- [ ] 1.12.14 `app.register_blueprint(irregular_bp)` 추가
- [ ] 1.12.15 파일 저장

**완료 시간**: ___  
**이슈**: 없음

---

### 🌆 오후 3부 (17:00-18:00) - 테스트 및 Git

#### 1.13 Flask 서버 실행 및 테스트 (30분)
- [ ] 1.13.1 터미널에서 가상환경 활성화 확인
- [ ] 1.13.2 `python app.py` 실행
- [ ] 1.13.3 서버 시작 확인
- [ ] 1.13.4 에러 메시지 없는지 확인
- [ ] 1.13.5 브라우저에서 `localhost:5000/api/inbound` 접속
- [ ] 1.13.6 JSON 응답 확인 (또는 404)
- [ ] 1.13.7 `localhost:5000/api/outbound` 접속
- [ ] 1.13.8 JSON 응답 확인
- [ ] 1.13.9 `localhost:5000/api/inventory` 접속
- [ ] 1.13.10 JSON 응답 확인
- [ ] 1.13.11 `localhost:5000/api/delete` 접속
- [ ] 1.13.12 JSON 응답 확인
- [ ] 1.13.13 `localhost:5000/api/irregular` 접속
- [ ] 1.13.14 JSON 응답 확인
- [ ] 1.13.15 logs/app.log 확인
- [ ] 1.13.16 API 호출 로그 확인
- [ ] 1.13.17 에러 없는지 확인
- [ ] 1.13.18 서버 중지 (Ctrl+C)

**완료 시간**: ___  
**이슈**: 없음

---

#### 1.14 Git 커밋 (30분)
- [ ] 1.14.1 서버 중지 확인
- [ ] 1.14.2 `cd C:\Projects\WMS-DashBoard` 이동
- [ ] 1.14.3 `git status` 확인
- [ ] 1.14.4 flask_app 폴더 확인
- [ ] 1.14.5 .gitignore에 venv_flask 추가 여부 확인
- [ ] 1.14.6 .gitignore에 logs/ 추가 여부 확인
- [ ] 1.14.7 .gitignore에 .env 추가 여부 확인
- [ ] 1.14.8 `git add flask_app/` 실행
- [ ] 1.14.9 `git status` 재확인
- [ ] 1.14.10 추가된 파일 확인
- [ ] 1.14.11 `git commit -m "Phase 2 Day 1: Flask 환경 + 5개 API 완성"` 실행
- [ ] 1.14.12 커밋 성공 확인
- [ ] 1.14.13 커밋 해시 확인
- [ ] 1.14.14 `git log --oneline -5` 확인
- [ ] 1.14.15 최신 커밋 확인

**완료 시간**: ___  
**이슈**: 없음

---

## 📊 Day 1 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ Flask 서버 정상 실행 (localhost:5000)
- [ ] ✅ 가상환경 활성화 상태
- [ ] ✅ requirements.txt 생성 완료 (Flask 3.0.0 등)
- [ ] ✅ .env 파일 설정 완료 (13개 환경변수)
- [ ] ✅ app.py 메인 파일 완성 (약 70줄)
- [ ] ✅ /api/health 응답 정상 (status: "ok")
- [ ] ✅ 5개 API 엔드포인트 모두 동작
  - [ ] /api/inbound
  - [ ] /api/outbound
  - [ ] /api/inventory
  - [ ] /api/delete
  - [ ] /api/irregular
- [ ] ✅ JSON 응답 구조 정상 (success, summary, data)
- [ ] ✅ logs/app.log 파일 생성 확인
- [ ] ✅ 에러 로그 없음
- [ ] ✅ Git 커밋 완료

**Day 1 최종 완료율**: ___% (___/80개 완료)  
**실제 소요시간**: ___ 시간  
**완료 시각**: ___

---

## ✅ Day 2: 통합 API + 에러처리 (2025-11-17)

**목표**: /api/dashboard 통합 API 완성 + 고급 에러 처리  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/50개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - 대시보드 통합 API

#### 2.1 api/dashboard.py 기본 구조 (30분)
- [ ] 2.1.1 `type nul > api\dashboard.py` 생성
- [ ] 2.1.2 VS Code로 dashboard.py 열기
- [ ] 2.1.3 `from flask import Blueprint, jsonify` import
- [ ] 2.1.4 `from datetime import datetime` import
- [ ] 2.1.5 `import sys, os` import
- [ ] 2.1.6 `from pathlib import Path` import
- [ ] 2.1.7 빈 줄 추가
- [ ] 2.1.8 collector_path 경로 설정
- [ ] 2.1.9 `sys.path.insert(0, str(collector_path))` 추가
- [ ] 2.1.10 5개 Collector 모두 import
- [ ] 2.1.11 빈 줄 추가
- [ ] 2.1.12 `bp = Blueprint('dashboard', __name__, url_prefix='/api')` 생성
- [ ] 2.1.13 빈 줄 추가
- [ ] 2.1.14 `@bp.route('/dashboard', methods=['GET'])` 데코레이터
- [ ] 2.1.15 `def get_dashboard():` 함수 정의

**완료 시간**: ___

---

#### 2.2 6개 카드 데이터 수집 (60분)
- [ ] 2.2.1 try 블록 시작
- [ ] 2.2.2 `today = datetime.now().strftime("%Y%m%d")` 추가
- [ ] 2.2.3 `data_path = os.getenv('DATA_PATH', 'C:/OSIS_AUTO')` 추가
- [ ] 2.2.4 빈 줄 추가
- [ ] 2.2.5 `# 입고 데이터` 주석
- [ ] 2.2.6 inbound_file 경로 작성
- [ ] 2.2.7 InboundCollector 인스턴스 생성
- [ ] 2.2.8 inbound_summary = collector.get_summary()
- [ ] 2.2.9 빈 줄 추가
- [ ] 2.2.10 `# 출고 데이터` 주석
- [ ] 2.2.11 outbound_file 경로 작성
- [ ] 2.2.12 OutboundCollector 인스턴스 생성
- [ ] 2.2.13 outbound_summary = collector.get_summary()
- [ ] 2.2.14 빈 줄 추가
- [ ] 2.2.15 `# 재고 데이터` 주석
- [ ] 2.2.16 inventory_file 경로 작성
- [ ] 2.2.17 InventoryCollector 인스턴스 생성
- [ ] 2.2.18 inventory_summary = collector.get_summary()
- [ ] 2.2.19 risky_products = collector.get_risky_products(threshold=20)
- [ ] 2.2.20 빈 줄 추가
- [ ] 2.2.21 `# 삭제 데이터` 주석
- [ ] 2.2.22 delete_file 경로 작성
- [ ] 2.2.23 DeleteCollector 인스턴스 생성
- [ ] 2.2.24 delete_summary = collector.get_summary()
- [ ] 2.2.25 빈 줄 추가
- [ ] 2.2.26 `# 비정형 데이터` 주석
- [ ] 2.2.27 irregular_file 경로 작성
- [ ] 2.2.28 IrregularCollector 인스턴스 생성
- [ ] 2.2.29 irregular_summary = collector.get_summary()

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - 응답 구조 작성

#### 2.3 6개 카드 JSON 응답 (75분)
- [ ] 2.3.1 빈 줄 추가
- [ ] 2.3.2 `# 응답 구성` 주석
- [ ] 2.3.3 `response = { 'success': True, 'cards': [] }` 시작
- [ ] 2.3.4 카드2 (입고) dict 작성
- [ ] 2.3.5 카드2 data 필드 (totalCount, progressRate) 추가
- [ ] 2.3.6 cards 리스트에 추가
- [ ] 2.3.7 빈 줄 추가
- [ ] 2.3.8 카드3 (재고) dict 작성
- [ ] 2.3.9 카드3 data 필드 (totalCount, urgentCount) 추가
- [ ] 2.3.10 risky_products Top 10 추가
- [ ] 2.3.11 cards 리스트에 추가
- [ ] 2.3.12 빈 줄 추가
- [ ] 2.3.13 카드5 (자사출고) dict 작성
- [ ] 2.3.14 카드5 data 필드 (amount, totalLabel) 추가
- [ ] 2.3.15 irregular 데이터 추가
- [ ] 2.3.16 cards 리스트에 추가
- [ ] 2.3.17 빈 줄 추가
- [ ] 2.3.18 카드6 (지방출고) dict 작성
- [ ] 2.3.19 카드6 data 필드 (amount, destinations) 추가
- [ ] 2.3.20 cards 리스트에 추가
- [ ] 2.3.21 빈 줄 추가
- [ ] 2.3.22 timestamp 필드 추가
- [ ] 2.3.23 `return jsonify(response)` 추가

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - 에러 처리 강화

#### 2.4 고급 에러 처리 (90분)
- [ ] 2.4.1 except FileNotFoundError 블록 추가
- [ ] 2.4.2 파일명 포함 에러 메시지 작성
- [ ] 2.4.3 404 응답 return
- [ ] 2.4.4 빈 줄 추가
- [ ] 2.4.5 except ValueError 블록 추가
- [ ] 2.4.6 데이터 검증 실패 메시지 작성
- [ ] 2.4.7 400 응답 return
- [ ] 2.4.8 빈 줄 추가
- [ ] 2.4.9 except Exception as e 블록 추가
- [ ] 2.4.10 일반 에러 메시지 작성
- [ ] 2.4.11 logger.error() 추가
- [ ] 2.4.12 500 응답 return
- [ ] 2.4.13 파일 저장
- [ ] 2.4.14 app.py에 dashboard_bp import 추가
- [ ] 2.4.15 app.py에 register_blueprint 추가
- [ ] 2.4.16 app.py 저장

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 캐싱 및 성능

#### 2.5 Flask-Caching 적용 (60분)
- [ ] 2.5.1 api/dashboard.py 열기
- [ ] 2.5.2 `from flask import current_app` import 추가
- [ ] 2.5.3 get_dashboard 함수 위에 빈 줄 추가
- [ ] 2.5.4 `@cache.cached(timeout=30, key_prefix='dashboard')` 데코레이터 추가
- [ ] 2.5.5 cache import 추가 (app에서)
- [ ] 2.5.6 나머지 5개 API에도 캐싱 추가
- [ ] 2.5.7 각 API마다 key_prefix 다르게 설정
- [ ] 2.5.8 timeout=30 확인
- [ ] 2.5.9 파일 저장
- [ ] 2.5.10 Flask 서버 재실행
- [ ] 2.5.11 /api/dashboard 두 번 호출
- [ ] 2.5.12 두 번째 호출이 빠른지 확인
- [ ] 2.5.13 로그에서 캐시 히트 확인

**완료 시간**: ___

---

#### 2.6 로깅 강화 (60분)
- [ ] 2.6.1 각 API 시작 부분에 logger.info() 추가
- [ ] 2.6.2 "API 호출: /api/inbound" 형식 로그
- [ ] 2.6.3 각 API 성공 시 logger.info() 추가
- [ ] 2.6.4 "API 응답: /api/inbound - 성공" 형식 로그
- [ ] 2.6.5 각 API 에러 시 logger.error() 추가
- [ ] 2.6.6 에러 내용 포함
- [ ] 2.6.7 dashboard.py에도 동일하게 적용
- [ ] 2.6.8 파일 저장
- [ ] 2.6.9 Flask 서버 재실행
- [ ] 2.6.10 모든 API 호출
- [ ] 2.6.11 logs/app.log 확인
- [ ] 2.6.12 로그 포맷 확인

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - 테스트 및 Git

#### 2.7 통합 테스트 (30분)
- [ ] 2.7.1 Flask 서버 실행
- [ ] 2.7.2 /api/dashboard 호출
- [ ] 2.7.3 6개 카드 데이터 확인
- [ ] 2.7.4 JSON 구조 확인
- [ ] 2.7.5 success: true 확인
- [ ] 2.7.6 cards 배열 4개 확인
- [ ] 2.7.7 timestamp 확인
- [ ] 2.7.8 30초 후 재호출
- [ ] 2.7.9 캐싱 동작 확인
- [ ] 2.7.10 서버 중지

**완료 시간**: ___

---

#### 2.8 Git 커밋 (30분)
- [ ] 2.8.1 `git status` 확인
- [ ] 2.8.2 변경 파일 확인
- [ ] 2.8.3 `git add .` 실행
- [ ] 2.8.4 `git commit -m "Phase 2 Day 2: 통합 API + 에러처리 + 캐싱 완성"` 실행
- [ ] 2.8.5 커밋 성공 확인
- [ ] 2.8.6 `git log --oneline -3` 확인

**완료 시간**: ___

---

## 📊 Day 2 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ /api/dashboard 엔드포인트 완성
- [ ] ✅ 6개 카드 데이터 모두 반환
- [ ] ✅ JSON 응답 구조 정상
- [ ] ✅ 고급 에러 처리 (FileNotFoundError, ValueError, Exception)
- [ ] ✅ Flask-Caching 적용 (30초)
- [ ] ✅ 로깅 강화 완료
- [ ] ✅ 통합 테스트 통과
- [ ] ✅ Git 커밋 완료

**Day 2 최종 완료율**: ___% (___/50개 완료)  
**실제 소요시간**: ___ 시간  
**완료 시각**: ___

---

## ✅ Day 3: pytest 테스트 작성 (2025-11-18)

**목표**: Flask API 전체 테스트 커버리지 확보  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/40개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - 테스트 환경 구축

#### 3.1 pytest 설치 및 설정 (30분)
- [ ] 3.1.1 가상환경 활성화 확인
- [ ] 3.1.2 `pip install pytest==7.4.3` 실행
- [ ] 3.1.3 `pip install pytest-cov==4.1.0` 실행
- [ ] 3.1.4 pytest 설치 확인
- [ ] 3.1.5 `type nul > pytest.ini` 생성
- [ ] 3.1.6 pytest.ini 편집
- [ ] 3.1.7 [pytest] 섹션 추가
- [ ] 3.1.8 testpaths = tests 추가
- [ ] 3.1.9 python_files = test_*.py 추가
- [ ] 3.1.10 파일 저장

**완료 시간**: ___

---

#### 3.2 conftest.py 작성 (60분)
- [ ] 3.2.1 `type nul > tests\conftest.py` 생성
- [ ] 3.2.2 VS Code로 conftest.py 열기
- [ ] 3.2.3 `import pytest` import
- [ ] 3.2.4 `import sys` import
- [ ] 3.2.5 `from pathlib import Path` import
- [ ] 3.2.6 빈 줄 추가
- [ ] 3.2.7 프로젝트 경로 추가 코드 작성
- [ ] 3.2.8 `from app import app` import
- [ ] 3.2.9 빈 줄 추가
- [ ] 3.2.10 `@pytest.fixture` 데코레이터
- [ ] 3.2.11 `def client():` 함수 정의
- [ ] 3.2.12 `app.config['TESTING'] = True` 설정
- [ ] 3.2.13 `with app.test_client() as client:` 컨텍스트
- [ ] 3.2.14 `yield client` 추가
- [ ] 3.2.15 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - API 테스트 작성

#### 3.3 test_api.py 기본 테스트 (75분)
- [ ] 3.3.1 `type nul > tests\test_api.py` 생성
- [ ] 3.3.2 VS Code로 test_api.py 열기
- [ ] 3.3.3 `import pytest` import
- [ ] 3.3.4 빈 줄 추가
- [ ] 3.3.5 `def test_health(client):` 함수 작성
- [ ] 3.3.6 response = client.get('/api/health')
- [ ] 3.3.7 assert response.status_code == 200
- [ ] 3.3.8 data = response.get_json()
- [ ] 3.3.9 assert data['status'] == 'ok'
- [ ] 3.3.10 빈 줄 2개 추가
- [ ] 3.3.11 `def test_dashboard(client):` 함수 작성
- [ ] 3.3.12 response 받기
- [ ] 3.3.13 status_code 확인
- [ ] 3.3.14 JSON 파싱
- [ ] 3.3.15 success 필드 확인
- [ ] 3.3.16 cards 필드 확인
- [ ] 3.3.17 cards 개수 확인 (4개)
- [ ] 3.3.18 파일 저장

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - 5개 API 개별 테스트

#### 3.4 5개 API 테스트 함수 (90분)
- [ ] 3.4.1 `def test_inbound(client):` 작성
- [ ] 3.4.2 200 응답 확인
- [ ] 3.4.3 success 필드 확인
- [ ] 3.4.4 summary 필드 확인
- [ ] 3.4.5 빈 줄 추가
- [ ] 3.4.6 `def test_outbound(client):` 작성
- [ ] 3.4.7 동일한 패턴으로 작성
- [ ] 3.4.8 빈 줄 추가
- [ ] 3.4.9 `def test_inventory(client):` 작성
- [ ] 3.4.10 risky_products 필드 추가 확인
- [ ] 3.4.11 빈 줄 추가
- [ ] 3.4.12 `def test_delete(client):` 작성
- [ ] 3.4.13 after_18_deletes 필드 확인
- [ ] 3.4.14 빈 줄 추가
- [ ] 3.4.15 `def test_irregular(client):` 작성
- [ ] 3.4.16 unlabeled_orders 필드 확인
- [ ] 3.4.17 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 에러 케이스 테스트

#### 3.5 에러 테스트 작성 (60분)
- [ ] 3.5.1 `def test_404_error(client):` 작성
- [ ] 3.5.2 존재하지 않는 경로 호출
- [ ] 3.5.3 404 응답 확인
- [ ] 3.5.4 빈 줄 추가
- [ ] 3.5.5 `def test_file_not_found(client, monkeypatch):` 작성
- [ ] 3.5.6 잘못된 날짜로 파일 경로 변경
- [ ] 3.5.7 404 또는 500 응답 확인
- [ ] 3.5.8 파일 저장

**완료 시간**: ___

---

#### 3.6 pytest 실행 및 검증 (60분)
- [ ] 3.6.1 터미널에서 가상환경 활성화
- [ ] 3.6.2 `cd tests` 이동
- [ ] 3.6.3 `pytest -v` 실행
- [ ] 3.6.4 테스트 실행 확인
- [ ] 3.6.5 모든 테스트 PASSED 확인
- [ ] 3.6.6 실패한 테스트 수정
- [ ] 3.6.7 재실행
- [ ] 3.6.8 `pytest --cov=api` 실행
- [ ] 3.6.9 커버리지 확인
- [ ] 3.6.10 80% 이상 확인

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - 문서화 및 Git

#### 3.7 테스트 문서 작성 (30분)
- [ ] 3.7.1 `type nul > tests\README.md` 생성
- [ ] 3.7.2 테스트 실행 방법 작성
- [ ] 3.7.3 커버리지 확인 방법 작성
- [ ] 3.7.4 파일 저장

**완료 시간**: ___

---

#### 3.8 Git 커밋 (30분)
- [ ] 3.8.1 `git add .` 실행
- [ ] 3.8.2 `git commit -m "Phase 2 Day 3: pytest 테스트 15개 완성"` 실행
- [ ] 3.8.3 커밋 확인

**완료 시간**: ___

---

## 📊 Day 3 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ pytest 설치 완료
- [ ] ✅ conftest.py 작성
- [ ] ✅ 15개 테스트 함수 작성
- [ ] ✅ 모든 테스트 PASSED
- [ ] ✅ 커버리지 80% 이상
- [ ] ✅ 테스트 문서 작성
- [ ] ✅ Git 커밋 완료

**Day 3 최종 완료율**: ___% (___/40개 완료)

---

## ✅ Day 4: HTML 템플릿 (2025-11-19)

**목표**: dashboard.html 기본 구조 완성  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/45개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - HTML 기본 구조

#### 4.1 dashboard.html 생성 (90분)
- [ ] 4.1.1 `type nul > templates\dashboard.html` 생성
- [ ] 4.1.2 VS Code로 dashboard.html 열기
- [ ] 4.1.3 `<!DOCTYPE html>` 선언
- [ ] 4.1.4 `<html lang="ko">` 태그
- [ ] 4.1.5 `<head>` 섹션 시작
- [ ] 4.1.6 `<meta charset="UTF-8">` 추가
- [ ] 4.1.7 viewport meta 태그 추가
- [ ] 4.1.8 `<title>` 태그 추가
- [ ] 4.1.9 CSS 링크 추가
- [ ] 4.1.10 `</head>` 닫기
- [ ] 4.1.11 `<body>` 시작
- [ ] 4.1.12 헤더 div 추가
- [ ] 4.1.13 h1 타이틀 추가
- [ ] 4.1.14 lastUpdate span 추가
- [ ] 4.1.15 메인 div 추가
- [ ] 4.1.16 cardsSection div 추가
- [ ] 4.1.17 6개 카드 div 추가
- [ ] 4.1.18 JavaScript 스크립트 링크
- [ ] 4.1.19 `</body>` 닫기
- [ ] 4.1.20 `</html>` 닫기
- [ ] 4.1.21 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - 카드 마크업

#### 4.2 6개 카드 상세 마크업 (75분)
- [ ] 4.2.1 카드2 (입고) 마크업 시작
- [ ] 4.2.2 카드 헤더 추가
- [ ] 4.2.3 카드 바디 추가
- [ ] 4.2.4 데이터 표시 영역 추가
- [ ] 4.2.5 카드3 (재고) 마크업
- [ ] 4.2.6 위험 상품 리스트 영역
- [ ] 4.2.7 카드5 (자사출고) 마크업
- [ ] 4.2.8 출하금액 영역
- [ ] 4.2.9 라벨 정보 영역
- [ ] 4.2.10 카드6 (지방출고) 마크업
- [ ] 4.2.11 배송처 정보 영역
- [ ] 4.2.12 파일 저장

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - CSS 기본 스타일

#### 4.3 dashboard.css 작성 (90분)
- [ ] 4.3.1 `type nul > static\css\dashboard.css` 생성
- [ ] 4.3.2 VS Code로 dashboard.css 열기
- [ ] 4.3.3 CSS 리셋 코드 작성
- [ ] 4.3.4 body 스타일 작성
- [ ] 4.3.5 헤더 스타일 작성
- [ ] 4.3.6 그리드 레이아웃 작성 (4+2)
- [ ] 4.3.7 카드 공통 스타일 작성
- [ ] 4.3.8 카드 hover 효과
- [ ] 4.3.9 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - Flask 라우팅 연결

#### 4.4 app.py 라우트 추가 (30분)
- [ ] 4.4.1 app.py 열기
- [ ] 4.4.2 render_template import 추가
- [ ] 4.4.3 @app.route('/') 수정
- [ ] 4.4.4 render_template('dashboard.html') return
- [ ] 4.4.5 파일 저장

**완료 시간**: ___

---

#### 4.5 렌더링 테스트 (60분)
- [ ] 4.5.1 Flask 서버 실행
- [ ] 4.5.2 브라우저에서 localhost:5000 접속
- [ ] 4.5.3 HTML 렌더링 확인
- [ ] 4.5.4 6개 카드 표시 확인
- [ ] 4.5.5 CSS 적용 확인
- [ ] 4.5.6 레이아웃 확인
- [ ] 4.5.7 서버 중지

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - Git 커밋

#### 4.6 Git 커밋 (30분)
- [ ] 4.6.1 `git add .` 실행
- [ ] 4.6.2 `git commit -m "Phase 2 Day 4: HTML 템플릿 + CSS 기본"` 실행
- [ ] 4.6.3 커밋 확인

**완료 시간**: ___

---

## 📊 Day 4 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ dashboard.html 완성
- [ ] ✅ 6개 카드 마크업 완료
- [ ] ✅ dashboard.css 기본 스타일
- [ ] ✅ Flask 렌더링 성공
- [ ] ✅ Git 커밋 완료

**Day 4 최종 완료율**: ___% (___/45개 완료)

---

## ✅ Day 5: JavaScript 30초 갱신 (2025-11-20)

**목표**: AJAX 자동 갱신 + 데이터 바인딩 완성  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/50개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - JavaScript 기본 구조

#### 5.1 dashboard.js 클래스 생성 (90분)
- [ ] 5.1.1 `type nul > static\js\dashboard.js` 생성
- [ ] 5.1.2 VS Code로 dashboard.js 열기
- [ ] 5.1.3 `const API_BASE_URL = 'http://localhost:5000/api';` 추가
- [ ] 5.1.4 `const REFRESH_INTERVAL = 30000;` 추가
- [ ] 5.1.5 빈 줄 추가
- [ ] 5.1.6 `class Dashboard {` 클래스 정의
- [ ] 5.1.7 `constructor() {}` 작성
- [ ] 5.1.8 this.refreshTimer = null 초기화
- [ ] 5.1.9 this.isLoading = false 초기화
- [ ] 5.1.10 빈 줄 추가
- [ ] 5.1.11 `init() {}` 메서드 정의
- [ ] 5.1.12 init 내부 로직 작성
- [ ] 5.1.13 빈 줄 추가
- [ ] 5.1.14 `async loadData() {}` 메서드 정의
- [ ] 5.1.15 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - AJAX 데이터 로드

#### 5.2 loadData 메서드 완성 (75분)
- [ ] 5.2.1 isLoading 체크 로직
- [ ] 5.2.2 this.isLoading = true 설정
- [ ] 5.2.3 try 블록 시작
- [ ] 5.2.4 `const response = await fetch(...)` 추가
- [ ] 5.2.5 `const data = await response.json()` 추가
- [ ] 5.2.6 data.success 체크
- [ ] 5.2.7 this.updateCards(data.cards) 호출
- [ ] 5.2.8 this.updateTimestamp() 호출
- [ ] 5.2.9 catch 블록 추가
- [ ] 5.2.10 에러 로그 추가
- [ ] 5.2.11 finally 블록
- [ ] 5.2.12 this.isLoading = false 설정
- [ ] 5.2.13 파일 저장

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - 카드 업데이트 로직

#### 5.3 updateCards 메서드 작성 (90분)
- [ ] 5.3.1 `updateCards(cards) {}` 메서드 정의
- [ ] 5.3.2 cards.forEach() 루프 시작
- [ ] 5.3.3 card.id로 switch 문
- [ ] 5.3.4 case 'card2': 입고 업데이트 로직
- [ ] 5.3.5 totalCount 업데이트
- [ ] 5.3.6 progressRate 업데이트
- [ ] 5.3.7 break
- [ ] 5.3.8 case 'card3': 재고 업데이트 로직
- [ ] 5.3.9 위험상품 리스트 렌더링
- [ ] 5.3.10 break
- [ ] 5.3.11 case 'card5': 자사출고 업데이트
- [ ] 5.3.12 출하금액 업데이트
- [ ] 5.3.13 break
- [ ] 5.3.14 case 'card6': 지방출고 업데이트
- [ ] 5.3.15 break
- [ ] 5.3.16 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 자동 갱신 구현

#### 5.4 30초 자동 갱신 (60분)
- [ ] 5.4.1 `startAutoRefresh() {}` 메서드 정의
- [ ] 5.4.2 `this.refreshTimer = setInterval(...)` 추가
- [ ] 5.4.3 REFRESH_INTERVAL 사용
- [ ] 5.4.4 콜백에서 this.loadData() 호출
- [ ] 5.4.5 console.log 추가
- [ ] 5.4.6 빈 줄 추가
- [ ] 5.4.7 `stopAutoRefresh() {}` 메서드 정의
- [ ] 5.4.8 clearInterval 호출
- [ ] 5.4.9 파일 저장

**완료 시간**: ___

---

#### 5.5 유틸리티 메서드 (60분)
- [ ] 5.5.1 `formatNumber(num) {}` 메서드
- [ ] 5.5.2 천 단위 콤마 로직
- [ ] 5.5.3 return 추가
- [ ] 5.5.4 빈 줄 추가
- [ ] 5.5.5 `updateTimestamp() {}` 메서드
- [ ] 5.5.6 현재 시각 가져오기
- [ ] 5.5.7 DOM 업데이트
- [ ] 5.5.8 빈 줄 추가
- [ ] 5.5.9 `showError(message) {}` 메서드
- [ ] 5.5.10 에러 표시 로직
- [ ] 5.5.11 파일 저장

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - 테스트 및 Git

#### 5.6 Dashboard 인스턴스 생성 (15분)
- [ ] 5.6.1 파일 하단에 빈 줄 2개 추가
- [ ] 5.6.2 `const dashboard = new Dashboard();` 추가
- [ ] 5.6.3 빈 줄 추가
- [ ] 5.6.4 `window.addEventListener('DOMContentLoaded', ...)` 추가
- [ ] 5.6.5 콜백에서 dashboard.init() 호출
- [ ] 5.6.6 파일 저장

**완료 시간**: ___

---

#### 5.7 자동 갱신 테스트 (30분)
- [ ] 5.7.1 Flask 서버 실행
- [ ] 5.7.2 브라우저에서 localhost:5000 접속
- [ ] 5.7.3 F12 개발자 도구 열기
- [ ] 5.7.4 Console 탭 확인
- [ ] 5.7.5 첫 데이터 로드 확인
- [ ] 5.7.6 30초 대기
- [ ] 5.7.7 자동 갱신 로그 확인
- [ ] 5.7.8 데이터 업데이트 확인
- [ ] 5.7.9 서버 중지

**완료 시간**: ___

---

#### 5.8 Git 커밋 (15분)
- [ ] 5.8.1 `git add .` 실행
- [ ] 5.8.2 `git commit -m "Phase 2 Day 5: JavaScript 30초 자동갱신 완성"` 실행
- [ ] 5.8.3 커밋 확인

**완료 시간**: ___

---

## 📊 Day 5 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ dashboard.js 클래스 완성
- [ ] ✅ AJAX 데이터 로드 동작
- [ ] ✅ 6개 카드 데이터 바인딩
- [ ] ✅ 30초 자동 갱신 동작
- [ ] ✅ 에러 처리 완료
- [ ] ✅ Git 커밋 완료

**Day 5 최종 완료율**: ___% (___/50개 완료)

---

## ✅ Day 6: CSS TV 최적화 (2025-11-21)

**목표**: 100인치 TV 전용 스타일 완성  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/37개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - 폰트 최적화

#### 6.1 대형 폰트 적용 (90분)
- [ ] 6.1.1 dashboard.css 열기
- [ ] 6.1.2 h1 폰트 크기 48px로 변경
- [ ] 6.1.3 카드 타이틀 32px로 변경
- [ ] 6.1.4 카드 값 72px로 변경
- [ ] 6.1.5 카드 단위 28px로 변경
- [ ] 6.1.6 서브텍스트 24px로 변경
- [ ] 6.1.7 파일 저장
- [ ] 6.1.8 브라우저에서 확인
- [ ] 6.1.9 가독성 테스트 (5m 거리)
- [ ] 6.1.10 필요 시 조정

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - 색상 대비 강화

#### 6.2 고대비 색상 시스템 (75분)
- [ ] 6.2.1 배경색 #1a1a1a로 변경
- [ ] 6.2.2 텍스트 #ffffff로 변경
- [ ] 6.2.3 긍정 색상 #4caf50 설정
- [ ] 6.2.4 부정 색상 #f44336 설정
- [ ] 6.2.5 중립 색상 #2196f3 설정
- [ ] 6.2.6 경고 색상 #ff9800 설정
- [ ] 6.2.7 대비 비율 5:1 확인
- [ ] 6.2.8 파일 저장

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - 레이아웃 조정

#### 6.3 TV 전용 레이아웃 (90분)
- [ ] 6.3.1 그리드 갭 30px로 확대
- [ ] 6.3.2 카드 패딩 40px로 증가
- [ ] 6.3.3 카드 보더 radius 20px
- [ ] 6.3.4 카드 shadow 강화
- [ ] 6.3.5 1920×1080 최적화
- [ ] 6.3.6 전체 화면 여백 조정
- [ ] 6.3.7 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 애니메이션

#### 6.4 부드러운 애니메이션 (60분)
- [ ] 6.4.1 카드 hover 효과 추가
- [ ] 6.4.2 transform: translateY(-5px)
- [ ] 6.4.3 transition 0.3s ease
- [ ] 6.4.4 값 변경 시 pulse 애니메이션
- [ ] 6.4.5 @keyframes pulse 정의
- [ ] 6.4.6 페이드 효과 추가
- [ ] 6.4.7 파일 저장

**완료 시간**: ___

---

#### 6.5 반응형 디자인 (60분)
- [ ] 6.5.1 @media (min-width: 3840px) 추가
- [ ] 6.5.2 4K용 폰트 크기 조정
- [ ] 6.5.3 4K용 레이아웃 조정
- [ ] 6.5.4 파일 저장
- [ ] 6.5.5 1920×1080 테스트
- [ ] 6.5.6 스케일링 확인

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - 최종 검증

#### 6.6 TV 화면 테스트 (45분)
- [ ] 6.6.1 Flask 서버 실행
- [ ] 6.6.2 전체 화면 모드 (F11)
- [ ] 6.6.3 5m 거리 가독성 확인
- [ ] 6.6.4 색상 대비 확인
- [ ] 6.6.5 애니메이션 확인
- [ ] 6.6.6 서버 중지

**완료 시간**: ___

---

#### 6.7 Git 커밋 (15분)
- [ ] 6.7.1 `git add .` 실행
- [ ] 6.7.2 `git commit -m "Phase 2 Day 6: CSS TV 최적화 완성"` 실행
- [ ] 6.7.3 커밋 확인

**완료 시간**: ___

---

## 📊 Day 6 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ 폰트 크기 최적화 (5m 가독성)
- [ ] ✅ 색상 대비 5:1 이상
- [ ] ✅ 레이아웃 1920×1080 최적화
- [ ] ✅ 애니메이션 부드러움
- [ ] ✅ 전체 화면 테스트 통과
- [ ] ✅ Git 커밋 완료

**Day 6 최종 완료율**: ___% (___/37개 완료)

---

## ✅ Day 7: 성능 + 안정성 (2025-11-22)

**목표**: 24시간 안정 운영 준비  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/40개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - 성능 최적화

#### 7.1 파일 최소화 (60분)
- [ ] 7.1.1 CSS 압축 (불필요한 공백 제거)
- [ ] 7.1.2 JavaScript 압축
- [ ] 7.1.3 이미지 최적화
- [ ] 7.1.4 파일 저장

**완료 시간**: ___

---

#### 7.2 메모리 최적화 (30분)
- [ ] 7.2.1 dashboard.js 메모리 누수 확인
- [ ] 7.2.2 이벤트 리스너 정리 로직 추가
- [ ] 7.2.3 타이머 정리 확인
- [ ] 7.2.4 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - 안정성 강화

#### 7.3 헬스 체크 강화 (75분)
- [ ] 7.3.1 app.py 열기
- [ ] 7.3.2 /api/health 엔드포인트 수정
- [ ] 7.3.3 시스템 상태 체크 추가
- [ ] 7.3.4 메모리 사용량 체크
- [ ] 7.3.5 응답에 추가 정보 포함
- [ ] 7.3.6 파일 저장

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - 24시간 테스트

#### 7.4 장시간 실행 테스트 (90분)
- [ ] 7.4.1 Flask 서버 실행
- [ ] 7.4.2 메모리 사용량 기록 (초기)
- [ ] 7.4.3 1시간 후 메모리 확인
- [ ] 7.4.4 2시간 후 메모리 확인
- [ ] 7.4.5 4시간 후 메모리 확인
- [ ] 7.4.6 메모리 누수 없는지 확인
- [ ] 7.4.7 CPU 사용률 확인

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 모니터링

#### 7.5 로그 모니터링 시스템 (60분)
- [ ] 7.5.1 로그 순환 설정 추가
- [ ] 7.5.2 에러 로그 별도 파일
- [ ] 7.5.3 성능 로그 추가
- [ ] 7.5.4 파일 저장

**완료 시간**: ___

---

#### 7.6 문서 작성 (60분)
- [ ] 7.6.1 운영 가이드 작성
- [ ] 7.6.2 트러블슈팅 가이드
- [ ] 7.6.3 성능 튜닝 가이드
- [ ] 7.6.4 파일 저장

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - Git 커밋

#### 7.7 Git 커밋 (30분)
- [ ] 7.7.1 `git add .` 실행
- [ ] 7.7.2 `git commit -m "Phase 2 Day 7: 성능+안정성 완성"` 실행
- [ ] 7.7.3 커밋 확인

**완료 시간**: ___

---

## 📊 Day 7 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ 파일 최소화 완료
- [ ] ✅ 메모리 최적화 완료
- [ ] ✅ 24시간 안정성 확인
- [ ] ✅ 모니터링 시스템 구축
- [ ] ✅ 운영 문서 작성
- [ ] ✅ Git 커밋 완료

**Day 7 최종 완료율**: ___% (___/40개 완료)

---

## ✅ Day 8: 배포 + 검증 (2025-11-23)

**목표**: 프로덕션 배포 및 Phase 2 완료  
**예상 소요**: 8시간  
**실제 소요**: ___ 시간  
**완료율**: 0% (0/35개 완료)

---

### 🌅 오전 1부 (09:00-10:30) - 프로덕션 환경

#### 8.1 환경 설정 (90분)
- [ ] 8.1.1 .env.production 파일 생성
- [ ] 8.1.2 FLASK_ENV=production 설정
- [ ] 8.1.3 FLASK_DEBUG=False 설정
- [ ] 8.1.4 LOG_LEVEL=WARNING 설정
- [ ] 8.1.5 파일 저장

**완료 시간**: ___

---

### ☕ 휴식 (10:30-10:45)

---

### 🌅 오전 2부 (10:45-12:00) - Windows 서비스

#### 8.2 NSSM 설치 및 설정 (75분)
- [ ] 8.2.1 NSSM 다운로드
- [ ] 8.2.2 C:\Program Files\NSSM 폴더 생성
- [ ] 8.2.3 NSSM 압축 해제
- [ ] 8.2.4 관리자 PowerShell 열기
- [ ] 8.2.5 `nssm install WMS-Flask-Dashboard` 실행
- [ ] 8.2.6 Application Path 설정
- [ ] 8.2.7 Startup directory 설정
- [ ] 8.2.8 Arguments 설정
- [ ] 8.2.9 서비스 생성 완료
- [ ] 8.2.10 `nssm start WMS-Flask-Dashboard` 실행
- [ ] 8.2.11 서비스 시작 확인

**완료 시간**: ___

---

### 🍽️ 점심 (12:00-13:00)

---

### 🌆 오후 1부 (13:00-14:30) - TV 연결

#### 8.3 100인치 TV 테스트 (90분)
- [ ] 8.3.1 TV IP 확인 (10.60.27.130)
- [ ] 8.3.2 네트워크 연결 확인
- [ ] 8.3.3 Chrome 전체화면 바로가기 생성
- [ ] 8.3.4 --kiosk 모드 설정
- [ ] 8.3.5 TV에서 브라우저 실행
- [ ] 8.3.6 localhost:5000 접속
- [ ] 8.3.7 전체 화면 확인
- [ ] 8.3.8 가독성 테스트 (5m 거리)
- [ ] 8.3.9 30초 자동 갱신 확인
- [ ] 8.3.10 6개 카드 데이터 확인

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 최종 검증

#### 8.4 전체 기능 검증 (90분)
- [ ] 8.4.1 /api/health 동작 확인
- [ ] 8.4.2 /api/dashboard 동작 확인
- [ ] 8.4.3 5개 개별 API 동작 확인
- [ ] 8.4.4 30초 갱신 정확도 확인
- [ ] 8.4.5 에러 처리 확인
- [ ] 8.4.6 로그 기록 확인
- [ ] 8.4.7 성능 측정 (페이지 로딩 < 2초)
- [ ] 8.4.8 메모리 사용량 확인 (< 500MB)

**완료 시간**: ___

---

#### 8.5 Phase 2 완료 보고서 (30분)
- [ ] 8.5.1 완료 항목 체크리스트 작성
- [ ] 8.5.2 성능 지표 정리
- [ ] 8.5.3 트러블슈팅 이력 정리
- [ ] 8.5.4 다음 단계 (Phase 3) 준비사항
- [ ] 8.5.5 파일 저장

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - Git 최종 커밋

#### 8.6 Git 최종 커밋 및 태그 (30분)
- [ ] 8.6.1 `git add .` 실행
- [ ] 8.6.2 `git commit -m "Phase 2 완료: Flask TV 시스템 배포"` 실행
- [ ] 8.6.3 `git tag -a v2.0 -m "Phase 2 완료"` 실행
- [ ] 8.6.4 `git push origin main` 실행
- [ ] 8.6.5 `git push origin v2.0` 실행
- [ ] 8.6.6 GitHub에서 태그 확인

**완료 시간**: ___

---

## 📊 Day 8 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ 프로덕션 환경 설정
- [ ] ✅ Windows 서비스 등록
- [ ] ✅ 100인치 TV 연결 성공
- [ ] ✅ 전체 기능 검증 통과
- [ ] ✅ Phase 2 완료 보고서 작성
- [ ] ✅ Git 태그 v2.0 생성
- [ ] ✅ 24/7 운영 준비 완료

**Day 8 최종 완료율**: ___% (___/35개 완료)

---

## 🎯 Phase 2 전체 완료 요약

**총 작업일**: 8일  
**총 체크박스**: 377개  
**현재 완료**: ___개 (___%)  
**실제 소요시간**: ___ 시간  
**최종 완료일**: ___

---

### ✅ 주요 성과

**백엔드:**
- [ ] Flask 서버 안정 운영
- [ ] 6개 API 엔드포인트 완성
- [ ] Collector 100% 재사용
- [ ] Flask-Caching 30초 적용
- [ ] 에러 처리 완벽

**프론트엔드:**
- [ ] HTML 템플릿 완성
- [ ] CSS TV 최적화 (1920×1080)
- [ ] JavaScript 자동 갱신 (30초)
- [ ] 6개 카드 데이터 바인딩
- [ ] 애니메이션 부드러움

**테스트:**
- [ ] pytest 15개 테스트
- [ ] 커버리지 80% 이상
- [ ] 24시간 안정성 확인

**배포:**
- [ ] Windows 서비스 등록
- [ ] 100인치 TV 연결
- [ ] 프로덕션 운영 준비

---

### 🚀 다음 단계 (Phase 3)

**Phase 3 알람 시스템 (10일)**:
- [ ] 10개 알람 규칙 구현
- [ ] Telegram 알림 연동
- [ ] 알람 로그 관리
- [ ] 알람 설정 UI

---

**마지막 업데이트**: 2025-11-16  
**작성자**: WMS 개발팀 (Claude 4인 전문가팀)  
**문서 버전**: v2.0 (극세분화 완전판)  
**상태**: ✅ 완성

---

**Phase 2 완료를 축하합니다! 🎉**
