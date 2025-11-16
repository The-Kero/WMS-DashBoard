# 📚 Phase 2 참고 문서 가이드 (Claude용)

**작성일**: 2025-11-07  
**용도**: Phase 2 개발 시 Claude가 빠르게 참고  
**버전**: v1.0

---

## 🎯 이 문서의 목적

Phase 2 Flask TV 시스템 개발 중 사용자가 이 문서를 Claude에게 제공하면,  
Claude는 필요한 정보를 빠르게 찾아 정확한 답변과 코드를 제공할 수 있습니다.

---

## 📂 핵심 참고 문서 목록

### 🔥 1순위: 즉시 참고 (3개)

#### 1. Phase 2 시작 가이드 ⭐⭐⭐⭐⭐
```
파일: C:\diary\2025-11-07_Phase2_시작가이드.md
분량: 1,395줄
상태: ✅ 완성

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Day 1-8 상세 개발 계획 (시간별)
✅ Flask 환경 구축 가이드 (명령어 포함)
✅ Collector 재사용 전략 (import 코드)
✅ 6개 API 엔드포인트 설계 (완전한 코드)
✅ HTML 템플릿 구조 (전체 HTML)
✅ JavaScript 30초 갱신 (완전한 JS 코드)
✅ CSS 100인치 TV 최적화 (전체 CSS)
✅ Day별 체크리스트
✅ 배포 가이드 (NSSM, Windows 서비스)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

언제 참고:
├─ Day 1-8 작업 내용 확인
├─ Flask 설치 명령어 필요
├─ API 코드 작성 (복사-붙여넣기)
├─ HTML/CSS/JS 코드 필요
├─ 체크리스트 확인
└─ 막혔을 때 돌아오는 기준점

읽는 방법:
1. 목차로 필요한 섹션 찾기
2. Day별 계획은 순차적으로
3. 코드 예시는 그대로 복사 가능
```

---

#### 2. Phase 1 완료 보고서 ⭐⭐⭐⭐
```
파일: C:\diary\2025-11-07_Phase1_완료보고서_상세.md
분량: 1,201줄
상태: ✅ 완성

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase 1 완성 내역 (5개 Collector)
✅ BaseCollector 패턴 설명
✅ Collector 메서드 목록
   - get_data() → DataFrame 반환
   - get_summary() → dict 반환
   - validate() → bool 반환
✅ 60개 테스트 결과
✅ 코드 통계 (13,350줄)
✅ 인수인계 사항
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

언제 참고:
├─ BaseCollector 패턴 이해 필요
├─ Collector 메서드 확인
├─ Phase 1 결과물 확인
└─ 코드 통계 필요

핵심 정보:
✅ 5개 Collector 완성:
   - InboundCollector
   - OutboundCollector
   - InventoryCollector
   - DeleteCollector
   - IrregularCollector

✅ 공통 메서드:
   - get_data() → pandas.DataFrame
   - get_summary() → dict
   - validate() → bool

✅ 위치:
   C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\
```

---

#### 3. dashboard/README.md ⭐⭐⭐⭐
```
파일: C:\Projects\WMS-DashBoard\dashboard\README.md
분량: 485줄
상태: ✅ 완성

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BaseCollector 패턴 상세
✅ 5개 Collector 사용법
✅ Flask 재사용 예제 코드 (중요!)
✅ import 경로 설정 방법
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

언제 참고:
├─ Collector import 방법
├─ Flask에서 Collector 사용 예제
├─ BaseCollector 메서드 설명
└─ 데이터 소스 경로

Flask 재사용 예제 (핵심!):
```python
# Flask에서 Collector 사용
import sys
from pathlib import Path

# Collector 경로 추가
collector_path = Path(__file__).parent.parent / "dashboard" / "src" / "data" / "collectors"
sys.path.insert(0, str(collector_path))

# Collector 임포트
from inbound import InboundCollector

# 사용
collector = InboundCollector(
    file_path="C:/OSIS_AUTO/Inbound Status/inbound_merged_20251024.csv",
    encoding='utf-8-sig'
)

data = collector.get_data()      # DataFrame
summary = collector.get_summary()  # dict
```

---

### 📖 2순위: 필요 시 참고 (5개)

#### 4. README_inbound.md ⭐⭐⭐
```
파일: C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\README_inbound.md
분량: 555줄

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ InboundCollector 메서드 상세
✅ Flask API 연동 예제 (완전한 코드)
✅ JSON 응답 구조
✅ Edge Case 처리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Flask API 예제:
```python
@app.route('/api/inbound', methods=['GET'])
def get_inbound():
    """입고 현황 API"""
    try:
        today = datetime.now().strftime("%Y%m%d")
        file_path = f"C:/OSIS_AUTO/Inbound Status/inbound_merged_{today}.csv"
        
        collector = InboundCollector(file_path=file_path, encoding='utf-8-sig')
        data = collector.get_data()
        summary = collector.get_summary()
        
        return jsonify({
            'success': True,
            'summary': summary,
            'data': data.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

주요 메서드:
✅ get_summary() 반환값:
   - 총_입고건수: int
   - 평균_진척률: float
   - 완료건수: int
   - 미완료건수: int
   - 공급사_수: int
```

---

#### 5. README_outbound.md ⭐⭐⭐
```
파일: C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\README_outbound.md
분량: 673줄

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ OutboundCollector 메서드 상세
✅ Flask API 연동 예제
✅ 출하금액 계산 로직
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

주요 메서드:
✅ get_summary() 반환값:
   - 총_출하금액: int
   - 총_출하건수: int
   - 배송처_수: int
   - 평균_출하금액: float
   - 상위_배송처: list
```

---

#### 6. README_inventory.md ⭐⭐⭐
```
파일: C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\README_inventory.md
분량: 653줄

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ InventoryCollector 메서드 상세
✅ 유효비 계산 로직
✅ 위험 상품 필터링 (유효비 ≤20%)
✅ 재고 부족 상품 필터링
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

주요 메서드:
✅ get_summary() 반환값:
   - 총_재고금액: int
   - 총_상품수: int
   - 위험_상품수: int (유효비 ≤20%)
   - 재고부족_상품수: int
   - 평균_유효비: float

✅ get_risky_products(threshold=20) → DataFrame
   유효비 ≤ threshold인 상품 반환
```

---

#### 7. README_delete.md ⭐⭐⭐
```
파일: C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\README_delete.md
분량: 668줄

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DeleteCollector 메서드 상세
✅ 18시 이후 삭제 필터링
✅ 알림 여부 체크
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

주요 메서드:
✅ get_summary() 반환값:
   - 총_삭제건수: int
   - 18시이후삭제: int
   - 알림발송건수: int
   - 배송처별_통계: dict

✅ get_after_18_deletes() → DataFrame
   18:00 이후 삭제 건만 반환
```

---

#### 8. README_irregular.md ⭐⭐⭐
```
파일: C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\README_irregular.md
분량: 642줄

핵심 내용:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ IrregularCollector 메서드 상세
✅ 라벨 미출력 필터링
✅ 센터별 통계
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

주요 메서드:
✅ get_summary() 반환값:
   - 총_오더수: int
   - 라벨미출력: int
   - 센터별_통계: dict
   - 최근1시간_오더: int

✅ get_unlabeled_orders() → DataFrame
   라벨 미출력 오더만 반환
```

---

### 📋 3순위: 배경 지식 (3개)

#### 9. 02_기술설명서.md ⭐⭐
```
파일: C:\Projects\WMS-DashBoard\docs\official\02_기술설명서.md
분량: 1,850줄

언제 참고:
├─ 전체 아키텍처 이해
├─ BaseCollector 패턴 깊은 이해
└─ 백엔드 성능 최적화 참고
```

#### 10. PROJECT_STATUS.md ⭐⭐
```
파일: C:\Projects\WMS-DashBoard\docs\official\PROJECT_STATUS.md
분량: 792줄

언제 참고:
├─ 프로젝트 전체 상태 확인
├─ Phase 2-5 로드맵
└─ 타임라인 확인
```

#### 11. README.md (루트) ⭐⭐
```
파일: C:\Projects\WMS-DashBoard\README.md
분량: 540줄

언제 참고:
├─ 프로젝트 전체 개요
├─ Phase 2 아키텍처 그림
└─ 설치 방법
```

---

## 🎯 Phase 2 Day별 참고 문서 매핑

### Day 1: Flask 기본 구조

**참고 순서**:
```
1. Phase 2 시작 가이드 - Day 1 섹션
2. dashboard/README.md - Flask 재사용 예제
3. README_inbound.md - 첫 API 코드
```

**필요한 코드**:
- Flask 설치 명령어
- Collector import 코드
- /api/inbound 엔드포인트 코드

---

### Day 2: 5개 API 완성

**참고 순서**:
```
1. Phase 2 시작 가이드 - Day 2 섹션
2. 5개 Collector README - Flask API 예제
```

**필요한 코드**:
- /api/outbound
- /api/inventory
- /api/delete
- /api/irregular

---

### Day 3: 통합 API + 테스트

**참고 순서**:
```
1. Phase 2 시작 가이드 - Day 3 섹션
2. Phase 1 완료 보고서 - Collector 메서드
```

**필요한 코드**:
- /api/dashboard 통합 API
- pytest 테스트 코드

---

### Day 4-5: HTML 템플릿

**참고 순서**:
```
1. Phase 2 시작 가이드 - Day 4-5 섹션
```

**필요한 코드**:
- dashboard.html (전체 HTML)
- dashboard.css
- dashboard.js

---

### Day 6-7: TV 최적화

**참고 순서**:
```
1. Phase 2 시작 가이드 - Day 6-7 섹션
```

**필요한 코드**:
- CSS 폰트 크기 최적화
- 색상 대비 강화
- 애니메이션

---

### Day 8: 배포

**참고 순서**:
```
1. Phase 2 시작 가이드 - Day 8 섹션
```

**필요한 정보**:
- NSSM 설치 방법
- Windows 서비스 등록
- 방화벽 설정

---

## 🔍 빠른 검색 키워드

### 상황별 찾아야 할 키워드

| 상황 | 키워드 | 문서 |
|------|--------|------|
| Flask 설치 | "Flask 설치", "venv" | Phase 2 시작 가이드 |
| Collector import | "import", "sys.path" | dashboard/README.md |
| API 코드 | "Flask API", "@app.route" | Collector README |
| JSON 응답 | "jsonify", "get_summary" | Collector README |
| HTML 코드 | "dashboard.html", "템플릿" | Phase 2 시작 가이드 |
| CSS 코드 | "dashboard.css", "TV 최적화" | Phase 2 시작 가이드 |
| JavaScript | "dashboard.js", "30초 갱신" | Phase 2 시작 가이드 |
| 에러 처리 | "try-except", "에러" | Phase 2 시작 가이드 |
| 테스트 | "pytest", "테스트" | Phase 2 시작 가이드 |
| 배포 | "NSSM", "Windows 서비스" | Phase 2 시작 가이드 |

---

## 💡 Claude를 위한 빠른 참조 카드

### Phase 2 핵심 정보 요약

#### Collector 재사용 패턴
```python
# 1. 경로 추가
import sys
from pathlib import Path
collector_path = Path(__file__).parent.parent / "dashboard" / "src" / "data" / "collectors"
sys.path.insert(0, str(collector_path))

# 2. Import
from inbound import InboundCollector
from outbound import OutboundCollector
from inventory import InventoryCollector
from delete import DeleteCollector
from irregular import IrregularCollector

# 3. 사용
collector = InboundCollector(
    file_path="C:/OSIS_AUTO/Inbound Status/inbound_merged_20251024.csv",
    encoding='utf-8-sig'
)

# 4. 데이터 가져오기
data = collector.get_data()        # DataFrame
summary = collector.get_summary()  # dict
valid = collector.validate()       # bool
```

---

#### Flask API 기본 패턴
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/inbound', methods=['GET'])
def get_inbound():
    """입고 현황 API"""
    try:
        # 1. Collector 초기화
        collector = InboundCollector(file_path=..., encoding='utf-8-sig')
        
        # 2. 데이터 수집
        data = collector.get_data()
        summary = collector.get_summary()
        
        # 3. JSON 응답
        return jsonify({
            'success': True,
            'summary': summary,
            'data': data.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

#### 6개 카드 데이터 구조
```python
{
    'success': True,
    'cards': [
        {
            'id': 'outbound_amount',
            'title': '당일 출하금액',
            'value': 125450000,
            'unit': '원',
            'change': '+5.2%',
            'trend': 'up'  # up/down/neutral
        },
        {
            'id': 'inbound_progress',
            'title': '입고 진행률',
            'value': 94.5,
            'unit': '%',
            'change': '+2.1%',
            'trend': 'up'
        },
        {
            'id': 'risky_products',
            'title': '피킹 유의 상품',
            'value': 87,
            'unit': '종',
            'change': '-3종',
            'trend': 'down'
        },
        {
            'id': 'low_stock',
            'title': '미할당 상품',
            'value': 12,
            'unit': '종',
            'change': '+1종',
            'trend': 'up'
        },
        {
            'id': 'after_18_delete',
            'title': '18시 이후 삭제',
            'value': 5,
            'unit': '건',
            'change': '0건',
            'trend': 'neutral'
        },
        {
            'id': 'unlabeled_orders',
            'title': '라벨 미출력 오더',
            'value': 3,
            'unit': '건',
            'change': '-2건',
            'trend': 'down'
        }
    ],
    'timestamp': '2025-11-08T10:30:00'
}
```

---

#### JavaScript 30초 갱신 패턴
```javascript
class Dashboard {
    constructor() {
        this.apiUrl = '/api/dashboard';
        this.refreshInterval = 30000;  // 30초
        this.timer = null;
    }
    
    init() {
        this.loadData();              // 첫 로딩
        this.startAutoRefresh();      // 자동 갱신
    }
    
    async loadData() {
        const response = await fetch(this.apiUrl);
        const data = await response.json();
        
        if (data.success) {
            this.updateCards(data.cards);
            this.updateTimestamp();
        }
    }
    
    startAutoRefresh() {
        this.timer = setInterval(() => {
            this.loadData();
        }, this.refreshInterval);
    }
}

const dashboard = new Dashboard();
dashboard.init();
```

---

## 🚨 자주 발생하는 이슈 및 해결

### Issue 1: Collector import 실패
```
에러: ModuleNotFoundError: No module named 'inbound'

해결:
✅ sys.path에 collector 경로 추가 확인
✅ 상대 경로가 아닌 절대 경로 사용
✅ Path(__file__).parent.parent 경로 확인
```

### Issue 2: CSV 파일 없음
```
에러: FileNotFoundError: inbound_merged_20251024.csv

해결:
✅ 날짜 형식 확인 (YYYYMMDD)
✅ C:\OSIS_AUTO\ 경로 확인
✅ 백엔드 프로그램 실행 확인
```

### Issue 3: 한글 깨짐
```
증상: CSV 데이터 한글이 깨짐

해결:
✅ encoding='utf-8-sig' 사용
✅ UTF-8 BOM 인코딩 확인
```

### Issue 4: Flask CORS 에러
```
에러: CORS policy error

해결:
✅ Flask-CORS 설치
✅ CORS(app) 설정 추가
```

---

## 📊 Phase 2 진행 체크리스트

### Day 1 완료 기준
```
□ Flask 서버 실행 성공 (포트 5000)
□ /api/inbound 동작 확인
□ Postman JSON 응답 확인
□ 5개 Collector import 성공
```

### Day 2 완료 기준
```
□ 5개 API 엔드포인트 모두 동작
□ 모든 API 응답 시간 < 1초
□ Postman 테스트 통과
□ 에러 처리 구현
```

### Day 3 완료 기준
```
□ /api/dashboard 통합 API 완성
□ 6개 카드 데이터 정상 반환
□ pytest 15개 테스트 작성
□ 테스트 100% 통과
```

### Day 4-5 완료 기준
```
□ dashboard.html 완성
□ 6개 카드 렌더링 확인
□ 30초 자동 갱신 동작
□ 증감률 표시 정상
```

### Day 6-7 완료 기준
```
□ 폰트 크기 최적화 (5m 가독성)
□ 색상 대비 5:1 이상
□ 애니메이션 부드러움
□ 1920×1080 최적화
```

### Day 8 완료 기준
```
□ Windows 서비스 등록
□ 100인치 TV 연결 테스트
□ 24시간 안정성 확인
□ Phase 2 완료 선언
```

---

## 🎯 Claude를 위한 작업 우선순위

### 사용자가 막혔을 때 확인 순서

**1순위 - 즉시 확인**:
```
1. Phase 2 시작 가이드 해당 Day 섹션
2. 체크리스트 확인
3. 코드 예제 제공
```

**2순위 - 상세 확인**:
```
1. 해당 Collector README
2. Flask API 예제
3. Edge Case 확인
```

**3순위 - 배경 지식**:
```
1. BaseCollector 패턴
2. 전체 아키텍처
3. 성능 최적화
```

---

## 📝 사용자 요청별 참조 문서 매핑

| 요청 유형 | 참고 문서 | 핵심 섹션 |
|----------|----------|----------|
| "Flask 설치해줘" | Phase 2 시작 가이드 | Day 1 - 환경 구축 |
| "첫 API 만들어줘" | Phase 2 시작 가이드, README_inbound.md | Day 1 오후, Flask API 예제 |
| "5개 API 확장" | 5개 Collector README | Flask API 연동 예제 |
| "통합 API 만들어줘" | Phase 2 시작 가이드 | Day 3 - 통합 API |
| "HTML 만들어줘" | Phase 2 시작 가이드 | Day 4 - HTML 템플릿 |
| "30초 갱신 구현" | Phase 2 시작 가이드 | Day 5 - JavaScript |
| "TV 최적화" | Phase 2 시작 가이드 | Day 6 - CSS 최적화 |
| "배포 방법" | Phase 2 시작 가이드 | Day 8 - 배포 가이드 |
| "에러 해결" | Phase 2 시작 가이드 | 에러 처리 섹션 |
| "테스트 작성" | Phase 2 시작 가이드 | Day 3 - pytest |

---

## 🔄 Phase 2 개발 흐름도 (Claude용)

```
사용자 요청
    ↓
Phase 2 시작 가이드 확인 (해당 Day)
    ↓
필요한 코드 예제 찾기
    ↓
코드 제공 (복사-붙여넣기 가능)
    ↓
에러 발생?
    ├─ Yes → Edge Case 확인 → 해결
    └─ No → 다음 단계
    ↓
체크리스트 확인
    ↓
완료!
```

---

## 💡 Claude를 위한 핵심 원칙

### Phase 2 개발 시 항상 기억할 것

**1. Collector는 수정하지 않는다** ✅
```
- Phase 1에서 완성된 5개 Collector
- 코드 수정 0%
- import만으로 100% 재사용
```

**2. 문서에 모든 코드가 있다** ✅
```
- Phase 2 시작 가이드에 모든 코드 예제
- 복사-붙여넣기만 하면 됨
- 즉석에서 코드 작성 필요 없음
```

**3. Day별 순서대로 진행** ✅
```
- Day 1 → Day 2 → ... → Day 8
- 각 Day의 완료 기준 충족
- 체크리스트 하나씩 완료
```

**4. 막히면 문서로 돌아간다** ✅
```
- Phase 2 시작 가이드가 기준점
- 해당 Day 섹션 다시 확인
- 코드 예제 재확인
```

---

## 📞 긴급 참고 (Phase 2 중 막혔을 때)

### Claude가 빠르게 찾아야 할 정보

**Flask 설치**:
```bash
cd C:\Projects\WMS-DashBoard
mkdir flask_app
cd flask_app
python -m venv venv_flask
venv_flask\Scripts\activate
pip install Flask==3.0.0 Flask-CORS==4.0.0 pandas==2.0.3
```

**Collector Import**:
```python
import sys
from pathlib import Path
collector_path = Path(__file__).parent.parent / "dashboard" / "src" / "data" / "collectors"
sys.path.insert(0, str(collector_path))

from inbound import InboundCollector
```

**첫 API**:
```python
@app.route('/api/inbound')
def get_inbound():
    collector = InboundCollector(file_path=..., encoding='utf-8-sig')
    summary = collector.get_summary()
    return jsonify({'success': True, 'summary': summary})
```

**파일 경로**:
```python
today = datetime.now().strftime("%Y%m%d")
file_path = f"C:/OSIS_AUTO/Inbound Status/inbound_merged_{today}.csv"
```

---

## ✅ 이 문서 사용 방법

### 사용자가 Phase 2 진행 중 막혔을 때

**사용자**: "이 문서 보고 도와줘"

**Claude 행동**:
1. ✅ 사용자의 현재 Day 파악
2. ✅ 해당 Day 섹션 확인
3. ✅ 필요한 코드 예제 찾기
4. ✅ 코드 제공 + 설명
5. ✅ 체크리스트 확인

### 효율성

**이 문서의 장점**:
- ✅ 모든 정보가 한 파일에
- ✅ 빠른 검색 키워드 제공
- ✅ 코드 예제 즉시 복사
- ✅ Day별 명확한 가이드
- ✅ 에러 해결 방법 포함

---

**문서 작성 완료**: 2025-11-07  
**작성자**: Claude (4인 전문가 팀)  
**버전**: v1.0  
**상태**: ✅ 완성

**Phase 2에서 Claude의 성공을 기원합니다! 🚀**
