# 🚀 Phase 2 대화 시작 필수 문서

**용도**: 매 대화 시작 시 Claude가 읽고 상황 파악  
**작성일**: 2025-11-16  
**버전**: v1.0  
**상태**: ✅ 완성

---

## 📋 이 문서의 목적

Phase 2 작업 중 **새로운 대화를 시작할 때마다** Claude가 이 문서를 읽고:
1. 현재 프로젝트 상태 파악
2. 다음 작업 내용 확인
3. 필요한 참고 문서 위치 파악
4. 즉시 작업 시작 가능

---

## 🎯 프로젝트 현황 (2025-11-16 기준)

### Phase 1 완료 현황 ✅
```
백엔드 5개 Collector: 100% 완성
├─ InboundCollector (입고 현황)
├─ OutboundCollector (출고 현황)
├─ InventoryCollector (재고 현황)
├─ DeleteCollector (삭제 현황)
└─ IrregularCollector (비정형 오더)

위치: C:\OSIS_AUTO\*.py
상태: 프로덕션 운영 중 (매 5분 데이터 수집)
성능: 최적화 완료 (50-97% 개선)
```

### Phase 2 현재 상황 ⏳
```
목표: Flask TV 시스템 구축 (8일)
시작일: 2025-11-16 (토)
완료 예정: 2025-11-23 (토)
진척률: 확인 필요 (Phase2_진척도.md 참조)
```

---

## 📁 핵심 파일 위치 (절대 경로)

### ⭐ 최우선 참고 문서 (항상 읽기)

#### 1. Phase2_진척도.md
```
경로: C:\Projects\WMS-DashBoard\docs\official\Phase2_진척도.md
내용: 377개 극세분화 체크리스트 (Day 1-8)
용도: 현재 작업 위치 확인, 다음 체크박스 진행
읽는 방법: offset=-100 (최근 100줄) 또는 특정 Day 섹션
```

#### 2. Phase2_완전가이드_백엔드포함.md
```
경로: C:\diary\2025-11-13_Phase2_완전가이드_백엔드포함.md
내용: Flask 전체 코드, API 설계, HTML/CSS/JS 전체
용도: 코드 참고 (복사-붙여넣기)
읽는 방법: 검색 키워드로 필요한 섹션 찾기
```

---

### 📚 보조 참고 문서

#### 3. Phase2_시작가이드.md
```
경로: C:\Projects\WMS-DashBoard\docs\official\2025-11-07_Phase2_시작가이드.md
내용: 8일 전체 일정, Day별 작업 개요
용도: 큰 그림 파악
```

#### 4. 5개 Collector 위치
```
InboundCollector: C:\OSIS_AUTO\inbound_status.py
OutboundCollector: C:\OSIS_AUTO\collect_outbound_status.py
InventoryCollector: C:\OSIS_AUTO\inventory_status.py
DeleteCollector: C:\OSIS_AUTO\delete_status.py
IrregularCollector: C:\OSIS_AUTO\irregular_order_status.py
```

#### 5. Flask 프로젝트 경로
```
루트: C:\Projects\WMS-DashBoard\flask_app\
(처음 시작 시 이 폴더는 없을 수 있음 - Day 1에서 생성)
```

---

## 🔄 대화 시작 시 필수 절차

### Step 1: 문서 읽기 (30초)
```python
# 항상 이 순서로 읽기
1. 이 문서 (Phase2_대화시작_필수문서.md) ✅ 지금 읽는 중
2. Phase2_진척도.md (최근 100줄 또는 현재 Day)
3. 필요 시 Phase2_완전가이드 특정 섹션
```

### Step 2: 현재 위치 파악 (10초)
```python
Phase2_진척도.md에서 확인:
- 현재 Day 번호 (1~8)
- 완료된 체크박스 개수
- 다음 진행할 체크박스 번호
- 예상 소요 시간
```

### Step 3: 사용자에게 확인 (즉시)
```python
케로님께 보고:
"Phase 2 Day X 작업 재개합니다.
 현재 위치: X.X.X (체크박스 이름)
 완료율: XX% (XX/총개수)
 다음 작업: (체크박스 내용)
 
 계속 진행하시겠습니까?"
```

---

## 📊 Day별 작업 요약

### Day 1 (80개 체크박스) - Flask 환경 + 5개 API
```
목표: Flask 기본 구조 + 5개 API 엔드포인트
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\app.py
- C:\Projects\WMS-DashBoard\flask_app\api\*.py (5개)
- requirements.txt
완료 기준: localhost:5000/api/health 응답, 5개 API 동작
```

### Day 2 (50개 체크박스) - 통합 API
```
목표: /api/dashboard 완성 + 에러처리
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\api\dashboard.py
- 고급 에러 처리 + 로깅
완료 기준: /api/dashboard에서 6개 카드 데이터 반환
```

### Day 3 (40개 체크박스) - pytest
```
목표: Flask API 테스트 커버리지 확보
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\tests\*.py
- 15개 테스트 함수
완료 기준: pytest 100% 통과, 커버리지 80%+
```

### Day 4 (45개 체크박스) - HTML
```
목표: dashboard.html 기본 구조
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\templates\dashboard.html
- C:\Projects\WMS-DashBoard\flask_app\static\css\dashboard.css
완료 기준: 6개 카드 렌더링 성공
```

### Day 5 (50개 체크박스) - JavaScript
```
목표: 30초 자동 갱신 구현
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\static\js\dashboard.js
완료 기준: 30초마다 자동 갱신, 데이터 바인딩
```

### Day 6 (37개 체크박스) - CSS 최적화
```
목표: 100인치 TV 전용 스타일
핵심 산출물:
- dashboard.css (TV 최적화)
완료 기준: 5m 거리 가독성, 색상 대비 5:1+
```

### Day 7 (40개 체크박스) - 성능
```
목표: 24시간 안정 운영 준비
핵심 산출물:
- 성능 최적화, 로그 모니터링
완료 기준: 메모리 < 500MB, 24시간 안정성
```

### Day 8 (35개 체크박스) - 배포
```
목표: 프로덕션 배포
핵심 산출물:
- Windows 서비스, 100인치 TV 연결
완료 기준: 24/7 운영 가능, Phase 2 완료
```

---

## 💡 중요 원칙 (Claude 필수 숙지)

### 1. Collector는 절대 수정 금지 ⛔
```
Phase 1에서 완성된 5개 Collector:
- 코드 수정 0%
- import만으로 100% 재사용
- Flask에서 sys.path 추가 후 import
```

### 2. 체크박스 순서대로 진행 ✅
```
Phase2_진척도.md:
- 순서 건너뛰기 금지
- 한 번에 하나씩 완료
- 완료 시간 기록
- 이슈 발생 시 메모
```

### 3. 매 작업 후 검증 필수 ✅
```
코드 작성 후:
1. 파일 저장 확인
2. 실행 테스트
3. 에러 확인
4. 로그 확인
5. 다음 체크박스 진행
```

### 4. Git 커밋 규칙 📝
```
각 Day 완료 시:
- git add .
- git commit -m "Phase 2 Day X: (작업 내용)"
- git log --oneline -3 확인
```

---

## 🔍 빠른 참조 - Collector Import 패턴

### Flask에서 Collector 사용 (핵심!)
```python
# 1. 경로 추가
import sys
from pathlib import Path

collector_path = Path(__file__).parent.parent.parent / "dashboard" / "src" / "data" / "collectors"
sys.path.insert(0, str(collector_path))

# 2. Import
from inbound import InboundCollector
from outbound import OutboundCollector
from inventory import InventoryCollector
from delete import DeleteCollector
from irregular import IrregularCollector

# 3. 사용
today = datetime.now().strftime("%Y%m%d")
file_path = f"C:/OSIS_AUTO/Inbound Status/inbound_merged_{today}.csv"

collector = InboundCollector(file_path=file_path, encoding='utf-8-sig')

if collector.validate():
    summary = collector.get_summary()  # dict
    data = collector.get_data()        # DataFrame
```

---

## 🔍 빠른 참조 - Flask API 기본 패턴

### API 엔드포인트 템플릿
```python
from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint('inbound', __name__, url_prefix='/api')

@bp.route('/inbound', methods=['GET'])
def get_inbound():
    """입고 현황 API"""
    try:
        today = datetime.now().strftime("%Y%m%d")
        file_path = f"C:/OSIS_AUTO/Inbound Status/inbound_merged_{today}.csv"
        
        collector = InboundCollector(file_path=file_path, encoding='utf-8-sig')
        
        if not collector.validate():
            return jsonify({'success': False, 'error': '데이터 검증 실패'}), 400
        
        summary = collector.get_summary()
        data = collector.get_data()
        
        return jsonify({
            'success': True,
            'summary': summary,
            'data': data.to_dict('records'),
            'timestamp': datetime.now().isoformat()
        })
    
    except FileNotFoundError:
        return jsonify({'success': False, 'error': '파일 없음'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

---

## 🚨 자주 발생하는 이슈 & 해결

### Issue 1: ModuleNotFoundError: No module named 'inbound'
```
원인: sys.path에 collector 경로 미추가
해결:
1. collector_path 경로 확인
2. sys.path.insert(0, str(collector_path)) 확인
3. Path(__file__).parent 경로 재확인
```

### Issue 2: FileNotFoundError: inbound_merged_YYYYMMDD.csv
```
원인: CSV 파일 없음 또는 날짜 형식 오류
해결:
1. C:\OSIS_AUTO\ 경로 확인
2. 날짜 형식 확인 (YYYYMMDD)
3. 백엔드 프로그램 실행 확인
```

### Issue 3: 한글 깨짐
```
원인: 인코딩 문제
해결:
1. encoding='utf-8-sig' 사용 (BOM 제거)
2. CSV 파일 인코딩 확인
```

### Issue 4: PowerShell && 연산자 에러
```
원인: PowerShell은 && 미지원
해결:
1. && 대신 ; (세미콜론) 사용
2. 예: cd path; command1; command2
```

---

## 📞 긴급 상황 대응

### 작업 중단 시 (컨텍스트 부족, 에러 등)
```
1. 현재 상태 PROJECT_DIARY.md에 기록
2. Phase2_진척도.md 완료율 업데이트
3. 문제 상황 상세 메모
4. 다음 대화에서 이어서 진행
```

### 다음 대화 재개 시
```
1. 이 문서 다시 읽기
2. Phase2_진척도.md에서 마지막 완료 지점 확인
3. PROJECT_DIARY.md 최근 항목 확인
4. 작업 재개
```

---

## ✅ 대화 시작 체크리스트

**Claude가 대화 시작 시 반드시 확인:**

- [ ] 1. Phase2_대화시작_필수문서.md 읽기 ✅
- [ ] 2. Phase2_진척도.md에서 현재 Day 확인
- [ ] 3. 현재 완료율 파악 (완료/377 × 100)
- [ ] 4. 다음 체크박스 번호 확인
- [ ] 5. 필요한 참고 문서 확인
- [ ] 6. 케로님께 현재 상태 보고
- [ ] 7. 작업 진행 의사 확인
- [ ] 8. 즉시 작업 시작 준비 완료

---

## 🎯 케로님께 보고 템플릿

```
Phase 2 작업 재개 준비 완료!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 현재 위치
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day: X (총 8일)
진척률: XX% (XX/377개 완료)
다음 작업: X.X.X (체크박스 이름)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 오늘 목표
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
(Day X의 주요 작업 내용)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 예상 소요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
남은 체크박스: XX개
예상 시간: X시간

바로 시작하시겠습니까?
```

---

## 🔗 관련 문서 링크

```
필수 문서:
1. Phase2_진척도.md (377개 체크리스트)
2. Phase2_완전가이드_백엔드포함.md (전체 코드)
3. Phase2_시작가이드.md (8일 일정)

참고 문서:
4. PROJECT_DIARY.md (작업 일지)
5. PROJECT_STATUS.md (프로젝트 현황)
6. 5개 Collector README (각 모듈 설명)

프로젝트 경로:
백엔드: C:\OSIS_AUTO\
프론트: C:\Projects\WMS-DashBoard\flask_app\
문서: C:\Projects\WMS-DashBoard\docs\official\
일지: C:\diary\
```

---

**마지막 업데이트**: 2025-11-16  
**작성자**: WMS 개발팀 (Claude 4인 전문가팀)  
**문서 버전**: v1.0  
**상태**: ✅ 완성

---

**이 문서를 읽었다면 Phase 2 작업 준비 완료! 🚀**
