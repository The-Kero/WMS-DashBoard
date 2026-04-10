# 🚀 Phase 2 대화 시작 필수 문서

**용도**: 매 대화 시작 시 Claude가 읽고 상황 파악  
**작성일**: 2025-11-16  
**버전**: v2.0 (6일 구조 재정비)  
**상태**: 🔄 진행중

---

## 🔴🔴🔴 Claude 필독! 파일 학습 절대 규칙 🔴🔴🔴

### ⚠️ 심각한 문제 발생 중 - 반드시 준수할 것!

**문제 상황**: 케로님이 명확한 파일 경로를 지정해도 Claude가 파일을 읽지 않고 추측으로 답변하는 심각한 결함이 **6회 이상 반복** 발생

### 🚨🚨🚨 Phase2_진척도.md 특별 규칙 (6번째 실수 후 추가) 🚨🚨🚨

**케로님이 "Phase2_진척도.md 확인해" 라고 하면:**

```
절대 규칙:
1. desktop-commander:read_file 즉시 실행 (말하기 전에!)
2. 파일 전체 읽기 (offset 없으면 기본 1000줄만 읽힘 주의!)
3. 파일이 1000줄 넘으면 반드시 offset=-423 등으로 끝부분도 읽기
4. 읽은 내용만으로 답변 (메모리 추측 절대 금지)
```

**잘못된 예시 (6번 실수):**
```
❌ Claude: "Phase2 진척도 분석 완료"
❌ Claude: "Day 1 완료, Day 2 대기 중"  
❌ (실제로는 파일 안 읽음 - 메모리만 봄)

케로: "파일 확인 안 했지?"
Claude: "😓 죄송합니다" ← 이미 늦음!
```

**올바른 예시:**
```
✅ Claude: [즉시 desktop-commander:read_file 실행]
✅ Claude: [파일 1423줄 확인 → offset으로 전체 읽기]
✅ Claude: "파일 확인 완료! 현재 Day 1 완료..."
```

**Phase2_진척도.md 읽는 방법:**
```python
# 1단계: 파일 크기 확인
read_file(path, offset=0, length=100)  # 첫 100줄 읽기
→ "total: 1423 lines" 확인

# 2단계: 전체 읽기
read_file(path, offset=0, length=1000)  # 1~1000줄
read_file(path, offset=-423)            # 마지막 423줄

# 또는
read_file(path, offset=1000)            # 1000줄부터 끝까지
```

**절대 하지 말 것:**
- ❌ 파일 안 읽고 "아마 Day 1 완료일 것 같습니다"
- ❌ 첫 1000줄만 읽고 "대기 중입니다" (나머지 423줄에 답 있을 수 있음)
- ❌ "Phase2_진척도.md를 확인하겠습니다" 말만 하고 안 읽기

### 🚨 절대 규칙 (위반 시 신뢰도 0%)

#### 규칙 1: 파일 경로 언급 = 무조건 즉시 읽기
```
케로: "C:\...\파일명.md 학습해"
     ↓
Claude: [즉시 desktop-commander:read_file 실행] ← 이것부터!
     ↓
Claude: [파일 내용 기반으로만 답변] ← 추측 절대 금지!
```

**절대 금지 행위:**
- ❌ 메모리만 보고 "아마 ~일 것 같습니다" 답변
- ❌ 파일 읽기 전에 먼저 말하기
- ❌ "~라고 들었습니다", "~인 것으로 보입니다" 같은 추측성 표현
- ❌ 파일 일부만 읽고 나머지는 추측

#### 규칙 2: 학습 완료 증명 필수
파일을 읽었으면 **반드시 이렇게 증명**:
```
✅ 파일 학습 완료: Phase2_진척도.md
📄 파일 정보:
   - 경로: C:\Projects\WMS-DashBoard\docs\official\Phase2_진척도.md
   - 크기: 1,613줄
   - 읽은 범위: 전체 / 1-1000줄 / -100줄(끝부분)
   
🎯 파일에서 확인한 내용 (추측 아님!):
   - Day 1 진척률: 16/80 완료 (20%) ← 파일 1.2.8 체크박스 확인
   - 현재 위치: 1.2.9 python-dotenv 설치 ← 파일 직접 인용
   - 다음 작업: [파일에서 복사한 체크리스트] ← 파일 그대로
```

#### 규칙 3: 의심스러우면 케로님이 재확인 요청
케로: "그거 파일 읽고 말하는 거 맞아?"
     ↓
Claude: [파일 즉시 다시 읽기] → [파일 내용 인용하며 답변]

**올바른 답변 예시:**
```
죄송합니다. 지금 파일을 다시 읽었습니다.

[desktop-commander:read_file 실행 결과]

Phase2_진척도.md 파일 1.2.8 체크박스를 보면:
"- [x] 1.2.8 pandas 설치 완료 확인 (약 1분)"

다음 체크박스 1.2.9는:
"- [ ] 1.2.9 `pip install python-dotenv==1.0.0` 실행"

이것이 파일에 명시된 정확한 내용입니다.
```

#### 규칙 4: 대화 시작 시 필수 파일 자동 읽기
```
케로: "Phase2_대화시작_필수문서.md 학습해"
     ↓
Claude 자동 실행:
  1. ✅ Phase2_대화시작_필수문서.md 읽기
  2. ✅ Phase2_진척도.md 자동으로 읽기 (문서에서 요구함)
  3. ✅ 필요 시 다른 참조 문서도 읽기
  4. 📋 읽은 모든 파일 목록과 핵심 내용 보고
```

#### 규칙 5: 파일 없으면 솔직하게 말하기
파일을 못 찾거나 읽을 수 없으면:
```
❌ 나쁜 답변: "아마 ~인 것 같습니다" (추측)
✅ 좋은 답변: "파일을 찾을 수 없습니다. 경로를 확인해 주세요:
              C:\Projects\WMS-DashBoard\docs\official\파일명.md"
```

### 🔍 자가 점검 체크리스트

Claude는 매 답변 전에 스스로 확인:
- [ ] 케로님이 파일 경로를 언급했는가?
- [ ] 그 파일을 실제로 읽었는가? (도구 호출 확인)
- [ ] 답변이 파일 내용에 기반하는가? (추측 아님)
- [ ] 파일 읽은 증거를 제시했는가? (줄 번호, 인용 등)

**하나라도 No면 → 답변하지 말고 파일부터 읽기!**

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
목표: Flask TV 시스템 구축 (6일)
시작일: 2025-11-16 (토)
완료 예정: 2025-11-28 (금)
진척률: 65.9% (325/493개 완료, Day 1~3 완료)
현재 위치: Day 4 대기
```

---

## 📁 핵심 파일 위치 (절대 경로)

### ⭐ 최우선 참고 문서 (항상 읽기)

#### 1. Phase2_진척도.md
```
경로: C:\Projects\WMS-DashBoard\docs\official\Phase2_진척도.md
내용: 493개 극세분화 체크리스트 (Day 1-6)
용도: 현재 작업 위치 확인, 다음 체크박스 진행
읽는 방법: offset=-100 (최근 100줄) 또는 특정 Day 섹션
```

#### 2. v10_레이아웃_설계서.xml
```
경로: C:\Projects\WMS-DashBoard\docs\official\v10_레이아웃_설계서.xml
내용: v10.html 구조 상세, 카드 1~6 명칭, API 키 매핑
용도: Day 4 API 재설계 시 참조
읽는 방법: 필요한 섹션 검색
```

---

### 📚 보조 참고 문서

#### 3. Phase2_시작가이드.md
```
경로: C:\Projects\WMS-DashBoard\docs\official\2025-11-07_Phase2_시작가이드.md
내용: 전체 일정, Day별 작업 개요
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
- 현재 Day 번호 (1~6)
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

### Day 1 (120개 체크박스) - Flask 환경 + Collector + API ✅ 완료
```
목표: Flask 기본 구조 + Collector 모듈 + 5개 API 엔드포인트
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\app.py
- C:\Projects\WMS-DashBoard\flask_app\api\dashboard.py
- requirements.txt
완료 기준: localhost:5000/api/dashboard 응답
실제 소요: 2.0시간
```

### Day 2 (165개 체크박스) - 통합 API + v9 규칙 적용 ✅ 완료
```
목표: /api/dashboard 완성 + v9 데이터 규칙 적용
핵심 산출물:
- dashboard.py (v9 규칙 적용)
- 에러 처리 + 로깅
완료 기준: /api/dashboard에서 카드 데이터 반환
실제 소요: 4.0시간
```

### Day 3 (40개 체크박스) - pytest 테스트 ✅ 완료
```
목표: Flask API 테스트 커버리지 확보
핵심 산출물:
- C:\Projects\WMS-DashBoard\flask_app\tests\*.py
완료 기준: pytest 100% 통과
실제 소요: 1.3시간
```

### Day 4 (95개 체크박스) - API 재설계 + v10 변환 + 30초 갱신 ⏳ 대기
```
목표: Flask API를 v10.html 구조에 맞게 재설계 + 30초 자동 갱신
핵심 산출물:
- API 응답 구조 재설계 (card1~6)
- card6 API 신규 개발 (금일재고현황 5섹션)
- v10.html → Flask 템플릿 변환
- 30초 자동 갱신 JavaScript
완료 기준: v10 레이아웃 + 30초 갱신 동작
```

### Day 5 (28개 체크박스) - 성능 최적화 + 안정성 ⏳ 대기
```
목표: 24시간 안정 운영 준비
핵심 산출물:
- 메모리 최적화
- 헬스 체크 강화
- 장시간 실행 테스트
완료 기준: 메모리 < 500MB, 24시간 안정성
```

### Day 6 (45개 체크박스) - 배포 + TV 검증 ⏳ 대기
```
목표: 프로덕션 배포 및 Phase 2 완료
핵심 산출물:
- Windows 서비스 (NSSM)
- 100인치 TV 연결 테스트
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
1. Phase2_진척도.md (493개 체크리스트, 6일 구조)
2. v10_레이아웃_설계서.xml (v10.html 구조 상세)
3. Phase2_시작가이드.md (전체 일정)

참고 문서:
4. PROJECT_DIARY.md (작업 일지)
5. PROJECT_STATUS.md (프로젝트 현황)
6. 5개 Collector README (각 모듈 설명)

프로젝트 경로:
백엔드: C:\OSIS_AUTO\
프론트: C:\Projects\WMS-DashBoard\flask_app\
문서: C:\Projects\WMS-DashBoard\docs\official\
일지: C:\diary\
레이아웃: C:\Projects\WMS-DashBoard\Layout\v10.html
```

---

**마지막 업데이트**: 2025-11-26  
**작성자**: WMS 개발팀 (Claude 4인 전문가팀)  
**문서 버전**: v2.0 (6일 구조 재정비)  
**상태**: 🔄 진행중

---

**이 문서를 읽었다면 Phase 2 작업 준비 완료! 🚀**
