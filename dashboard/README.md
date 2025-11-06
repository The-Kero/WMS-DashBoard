# WMS 대시보드 (Streamlit) - Phase 1 완료 ✅

**상태:** Phase 1 완료 (100%)  
**완료일:** 2025-11-04  
**최종 업데이트:** 2025-11-07  
**다음 단계:** Phase 2 Flask TV 시스템 (8일)

---

## 📊 Phase 1 완료 현황

### ✅ 5개 Collector 완성
모든 Collector는 `BaseCollector` 추상 클래스를 상속하여 일관된 인터페이스를 제공합니다.

| Collector | 상태 | 파일 | 기능 |
|-----------|------|------|------|
| InboundCollector | ✅ | `src/data/collectors/inbound.py` | 입고 데이터 수집 및 분석 |
| OutboundCollector | ✅ | `src/data/collectors/outbound.py` | 10개 타입 출고 분석 |
| InventoryCollector | ✅ | `src/data/collectors/inventory.py` | 재고 현황 및 유효기한 관리 |
| DeleteCollector | ✅ | `src/data/collectors/delete.py` | 삭제 처리 추적 |
| IrregularCollector | ✅ | `src/data/collectors/irregular.py` | 비정형 오더 관리 |

### ✅ 60개 테스트 통과
| 테스트 파일 | 개수 | 커버리지 | 상태 |
|------------|------|---------|------|
| test_inbound.py | 8개 | 95% | ✅ 100% |
| test_outbound.py | 8개 | 92% | ✅ 100% |
| test_inventory_collector.py | 8개 | 94% | ✅ 100% |
| test_delete.py | 8개 | 90% | ✅ 100% |
| test_irregular.py | 8개 | 91% | ✅ 100% |
| test_edge_cases.py | 20개 | - | ✅ 100% |
| **총계** | **60개** | **평균 80%+** | **✅ 100%** |

### ✅ 5개 대시보드 탭 완성
- 📦 입고 현황 - 4대 핵심 지표 + TOP 10 차트
- 🚚 출고 현황 - 10개 타입 분석 + 출하금액 계산
- 📊 재고 현황 - 유효유통비 관리 + 위험 상품 알림
- 🗑️ 삭제 현황 - 18시 이후 삭제 추적
- 📋 비정형 오더 - 라벨미출력 필터링

---

## 🏗️ BaseCollector 패턴

모든 데이터 수집기는 `BaseCollector` 추상 클래스를 상속하여 다음 메서드를 구현합니다:

### 추상 메서드 (필수 구현)
```python
class BaseCollector(ABC):
    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        """CSV 파일에서 데이터 로드"""
        pass
    
    @abstractmethod
    def collect(self) -> Dict[str, Any]:
        """핵심 지표 수집 및 계산"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """데이터 유효성 검증"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, float]:
        """주요 메트릭 반환"""
        pass
```

### 구현 예시: InboundCollector
```python
class InboundCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        return {
            'total_count': len(self.df),
            'total_quantity': self.df['수량'].sum(),
            'avg_quantity': self.df['수량'].mean(),
            'supplier_count': self.df['공급처코드'].nunique()
        }
```

### 장점
- ✅ **일관성**: 모든 Collector가 동일한 인터페이스 제공
- ✅ **확장성**: 새 Collector 추가 시 BaseCollector만 상속
- ✅ **재사용성**: Phase 2 Flask API에서 100% 재사용 가능
- ✅ **테스트 용이성**: 공통 테스트 패턴 적용 가능

---

## 🔮 Phase 2 계획 (Flask TV 시스템)

### 목표
100인치 TV용 자동 갱신 대시보드 구축 (8일)

### 아키텍처
```
100인치 TV (브라우저)
  ↓ HTTP GET /api/data
Flask API Server (data_server.py)
  ↓ collect()
5개 Collector (Phase 1에서 100% 재사용)
  ↓ read_csv()
CSV Files (백엔드 출력)
```

### 핵심 기능
- **30초 자동 갱신**: JavaScript setInterval
- **6개 카드 레이아웃**: 입고/출고/재고/삭제/비정형/알림
- **RESTful API**: `/api/data` 엔드포인트
- **JSON 응답**: 실시간 데이터 전송
- **캐싱**: 성능 최적화

### Collector 재사용
Phase 1에서 개발한 5개 Collector를 **코드 수정 없이** Flask 서버에서 그대로 사용:
```python
# Flask API에서 Collector 사용 예시
from src.data.collectors.inbound import InboundCollector

@app.route('/api/data')
def get_data():
    inbound = InboundCollector(sample_mode=False)
    data = inbound.collect()
    return jsonify(data)
```

---

## 📦 설치

### 1. 저장소 복제
```bash
git clone https://github.com/The-Kero/WMS-DashBoard.git
cd WMS-DashBoard/dashboard
```

### 2. 가상환경 설정
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 설정 파일 생성
```bash
# Windows
copy config\config.example.yaml config\config.yaml

# Linux/Mac
cp config/config.example.yaml config/config.yaml
```

### 5. 설정 파일 수정
`config/config.yaml` 파일을 열어 실제 데이터 경로로 수정:
```yaml
data_sources:
  inbound: "C:/OSIS_AUTO/Inbound Status/inbound_merged_YYYYMMDD.csv"
  outbound: "C:/OSIS_AUTO/Outbound Status/outbound_XX_YYYYMMDD.csv"
  inventory: "C:/OSIS_AUTO/inventory_status/inventory_status_YYYYMMDD.csv"
  delete: "C:/OSIS_AUTO/Delete Status/delete_status_YYYYMMDD.csv"
  irregular: "C:/OSIS_AUTO/IrregularOrder Status/irregular_order_YYYYMMDD.csv"
```

---

## 🚀 실행

### 개발 모드 (Streamlit)
```bash
# 기본 실행
streamlit run app.py

# 포트 지정
streamlit run app.py --server.port 8501

# 외부 접속 허용
streamlit run app.py --server.address 0.0.0.0
```

브라우저에서 자동으로 `http://localhost:8501` 열림

### 테스트 실행
```bash
# 전체 테스트 실행
pytest tests/ -v

# 특정 테스트만 실행
pytest tests/test_inbound.py -v

# 커버리지 확인
pytest tests/ --cov=src --cov-report=html
```

---

## 📁 프로젝트 구조

```
dashboard/
├── app.py                          # Streamlit 메인 앱 ✅
├── requirements.txt                # 패키지 의존성
├── README.md                       # 이 파일
│
├── config/                         # 설정 파일
│   ├── config.example.yaml        # 설정 예시
│   └── config.yaml                # 실제 설정 (gitignore)
│
├── src/                            # 소스 코드
│   ├── data/                      # 데이터 레이어
│   │   └── collectors/            # 데이터 수집기 ✅
│   │       ├── base.py           # BaseCollector 추상 클래스
│   │       ├── inbound.py        # 입고 Collector ✅
│   │       ├── outbound.py       # 출고 Collector ✅
│   │       ├── inventory.py      # 재고 Collector ✅
│   │       ├── delete.py         # 삭제 Collector ✅
│   │       └── irregular.py      # 비정형 Collector ✅
│   │
│   ├── business/                  # 비즈니스 로직
│   ├── ui/                        # UI 컴포넌트
│   │   └── components.py         # Streamlit 컴포넌트
│   └── utils/                     # 유틸리티
│
└── tests/                         # 테스트 (60개) ✅
    ├── fixtures/                  # 샘플 데이터
    │   ├── sample_inbound.csv
    │   ├── sample_outbound.csv
    │   ├── sample_inventory.csv
    │   ├── sample_delete.csv
    │   ├── sample_irregular.csv
    │   └── edge_cases/            # Edge Case 샘플
    │
    ├── test_inbound.py            # 8개 ✅
    ├── test_outbound.py           # 8개 ✅
    ├── test_inventory_collector.py # 8개 ✅
    ├── test_delete.py             # 8개 ✅
    ├── test_irregular.py          # 8개 ✅
    └── test_edge_cases.py         # 20개 ✅
```

---

## ⚙️ 주요 기능 (Phase 1)

### 1. 📦 입고 현황 탭
- **4대 핵심 지표**: 총 건수, 총 수량, 평균 수량, 공급처 수
- **TOP 10 차트**: 공급처별/상품별 입고량
- **전체 목록**: 필터 및 정렬 기능

### 2. 🚚 출고 현황 탭
- **4대 핵심 지표**: 총 건수, 총 수량, 총 출하금액, 출고처 수
- **10개 타입 분석**: 지방/자사/캘리스코 등
- **출하금액 계산**: 재고 단가 연동
- **TOP 10 차트**: 출고처별/상품별 출고량

### 3. 📊 재고 현황 탭
- **4대 핵심 지표**: 총 상품 수, 총 가용수량, 총 재고금액, 위험 상품 수
- **유효유통비 관리**: ≤20% 빨간색 알림
- **위험 상품 목록**: 자동 필터링
- **재고금액 TOP 10**: 고가 상품 관리

### 4. 🗑️ 삭제 현황 탭
- **5대 핵심 지표**: 총 건수, 총 수량, 18시 이후, 라벨출력, 센터 수
- **18시 이후 알림**: 긴급 삭제 추적
- **배송군별 집계**: 패턴 분석

### 5. 📋 비정형 오더 탭
- **주요 지표**: 총 건수, 라벨미출력, 센터별 집계
- **라벨미출력 필터**: 긴급 처리 대상
- **센터별 분석**: 오더량 추적

---

## 🐛 문제 해결

### 1. 모듈을 찾을 수 없음
```bash
# PYTHONPATH 설정 (Windows)
set PYTHONPATH=%PYTHONPATH%;%CD%

# PYTHONPATH 설정 (Linux/Mac)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 2. 데이터 파일을 찾을 수 없음
- `config/config.yaml`의 경로 확인
- 백엔드 5개 프로그램 정상 실행 확인
- CSV 파일 존재 여부 확인

### 3. 포트 충돌
```bash
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

### 4. 가상환경 활성화 안됨
```bash
# Windows에서 실행 정책 오류 시
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🧪 테스트 가이드

### 전체 테스트 실행
```bash
pytest tests/ -v
```

### 특정 Collector 테스트
```bash
pytest tests/test_inbound.py -v
pytest tests/test_outbound.py -v
pytest tests/test_inventory_collector.py -v
pytest tests/test_delete.py -v
pytest tests/test_irregular.py -v
```

### Edge Case 테스트
```bash
pytest tests/test_edge_cases.py -v
```

### 커버리지 확인
```bash
# HTML 리포트 생성
pytest tests/ --cov=src --cov-report=html

# 브라우저에서 htmlcov/index.html 열기
```

---

## 📚 관련 문서

### 상위 프로젝트 문서
- [../README.md](../README.md) - 프로젝트 전체 개요
- [../docs/official/PROJECT_STATUS.md](../docs/official/PROJECT_STATUS.md) - 프로젝트 상태 (v3.0)
- [../docs/official/02_기술설명서.md](../docs/official/02_기술설명서.md) - 기술 스택 및 아키텍처 (v2.1)
- [../docs/official/03_시스템_흐름도.md](../docs/official/03_시스템_흐름도.md) - 시스템 흐름 (v2.0)

### 모듈별 문서 (Phase 5 예정)
- `collectors/README_inbound.md` - 입고 Collector 상세
- `collectors/README_outbound.md` - 출고 Collector 상세
- `collectors/README_inventory.md` - 재고 Collector 상세
- `collectors/README_delete.md` - 삭제 Collector 상세
- `collectors/README_irregular.md` - 비정형 Collector 상세

---

## 🤝 기여 가이드

새로운 Collector를 추가하려면:

1. `BaseCollector`를 상속하는 새 클래스 생성
2. 필수 메서드 구현 (`load_data`, `collect`, `validate`, `get_metrics`)
3. 테스트 파일 작성 (최소 8개 + Edge Case)
4. `app.py`에 새 탭 추가
5. Pull Request 생성

---

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 통해 남겨주세요.

---

**마지막 업데이트:** 2025-11-07  
**Phase 1 상태:** ✅ 완료 (100%)  
**Phase 2 예정:** Flask TV 시스템 (8일)  
**Phase 3 예정:** 알림 시스템 (10일)