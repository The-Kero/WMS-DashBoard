# 새로운 대화 시작 시 효과적인 명령 가이드

## 작성일: 2025-10-20 15:20

---

## 🎯 가장 효과적인 명령 방법 (우선순위)

### ⭐ **방법 1: 구체적 + 맥락 제공** (가장 추천!)

```
"이전 대화에서 OutboundCollector 수정과 Config 날짜 자동화를 완료했어.
이제 InventoryCollector 개발을 시작해줘.
백엔드는 C:/OSIS_AUTO/inventory_status/inventory_status_20251020.csv 파일이고
12개 컬럼 구조야."
```

**장점:**
- ✅ 이전 작업 명시 → 메모리 검색 쉬움
- ✅ 다음 작업 명확 → 바로 시작 가능
- ✅ 필요한 정보 제공 → 추가 질문 최소화

---

### ⭐ **방법 2: 파일 참조** (효율적!)

```
"C:\Projects\WMS-DashBoard\PROJECT_DIARY.md 읽고
마지막 작업 이어서 InventoryCollector 개발 시작해줘"
```

**장점:**
- ✅ 정확한 정보 → 파일에서 직접 확인
- ✅ 간결함 → 짧은 명령
- ✅ 명확한 참조점 → 오해 없음

---

### ⭐ **방법 3: 메모리 검색 요청** (안전!)

```
"메모리에서 OutboundCollector와 Config 관련 작업을 찾아보고
다음 작업인 InventoryCollector 개발을 시작해줘"
```

**장점:**
- ✅ 명시적 메모리 검색 → 저장된 정보 활용
- ✅ 맥락 파악 → 이전 대화 이해
- ✅ 자연스러운 연결 → 작업 흐름 유지

---

## 📝 구체적인 명령 예시

### 예시 1: 다음 단계 작업 시작

#### ❌ **좋지 않은 방법:**
```
"InventoryCollector 만들어줘"
```
→ 이전 작업 모름, 구조 모름, 백엔드 경로 모름

#### ✅ **좋은 방법:**
```
"이전 대화에서 OutboundCollector 수정 완료했어.
이제 InventoryCollector 개발 시작해줘.
COLLECTOR_修正_PLAN.md 파일에 계획이 있어."
```
→ 맥락 명확, 참조 문서 명시, 바로 시작 가능

---

### 예시 2: 오류 수정

#### ❌ **좋지 않은 방법:**
```
"OutboundCollector 에러나"
```
→ 어떤 에러인지, 언제 발생했는지 불명확

#### ✅ **좋은 방법:**
```
"이전에 수정한 OutboundCollector (커밋 b0c2cd7)에서
실제 데이터 로드할 때 에러가 발생해.
test_outbound_collector.py 실행 결과 확인해줘."
```
→ 특정 커밋, 상황, 테스트 파일까지 명시

---

### 예시 3: 이전 작업 확인 후 진행

#### ❌ **좋지 않은 방법:**
```
"작업 계속해줘"
```
→ 어떤 작업인지 불명확

#### ✅ **좋은 방법:**
```
"PROJECT_DIARY.md의 마지막 작업을 확인하고
다음 단계를 진행해줘"
```
→ 명확한 참조점, 자동으로 다음 단계 파악

---

## 🎯 핵심 키워드 (검색 잘 되는 단어들)

### ✅ **효과적인 키워드**
- "이전 대화에서"
- "메모리 검색해서"
- "PROJECT_DIARY.md 확인하고"
- "커밋 b0c2cd7"
- "OutboundCollector 수정"
- "Config 날짜 자동화"
- "InventoryCollector 개발"
- "COLLECTOR_修正_PLAN.md 참고"

### ❌ **피해야 할 애매한 표현**
- "저번에"
- "그거"
- "작업"
- "계속"
- "이어서"

---

## 📋 상황별 명령 템플릿

### 상황 1: 새로운 모듈 개발 시작

```
"이전 대화에서 [완료한 작업]을 마쳤어.
이제 [새로운 작업]을 시작할게.
[참고 문서/파일]을 확인해서 진행해줘."
```

**예시:**
```
"이전 대화에서 OutboundCollector 수정을 완료했어.
이제 InventoryCollector 개발을 시작할게.
COLLECTOR_修正_PLAN.md를 확인해서 진행해줘."
```

---

### 상황 2: 오류 발생 시

```
"[작업명] (커밋 [해시])에서 오류가 발생했어.
[오류 상황] 상황이야.
[테스트 파일/로그]를 확인해서 해결해줘."
```

**예시:**
```
"OutboundCollector (커밋 b0c2cd7)에서 오류가 발생했어.
실제 데이터 로드할 때 컬럼명 불일치 오류야.
test_outbound_collector.py를 확인해서 해결해줘."
```

---

### 상황 3: 이전 작업 확인 필요 시

```
"PROJECT_DIARY.md (또는 [문서명])를 읽고
마지막 작업 상태를 파악한 다음
다음 단계를 진행해줘."
```

**예시:**
```
"PROJECT_DIARY.md를 읽고
마지막 작업 상태를 파악한 다음
InventoryCollector 개발을 시작해줘."
```

---

### 상황 4: 특정 기능 추가 시

```
"[모듈명] (파일: [경로])에
[기능 설명] 기능을 추가해줘.
[참고 문서]를 참고해서 진행해."
```

**예시:**
```
"OutboundCollector (파일: dashboard/src/data/collectors/outbound.py)에
출고유형별 금액 합계 기능을 추가해줘.
BACKEND_COLUMN_ANALYSIS.md를 참고해서 진행해."
```

---

## 🔍 Claude가 자동으로 확인하는 순서

새로운 대화 시작 시 제가 자동으로 확인하는 순서:

1. **메모리 검색** (openmemory)
   - 명령어의 키워드로 관련 메모리 검색
   
2. **프로젝트 파일 확인**
   - PROJECT_DIARY.md (최근 작업)
   - COLLECTOR_修正_PLAN.md (계획)
   - 기타 문서들

3. **GitHub 상태 확인**
   - 최근 커밋 확인
   - 변경사항 확인

4. **작업 시작**

---

## ✅ 최고의 명령 방법 (종합)

### 🌟 **완벽한 명령 예시:**

```
"이전 대화에서 OutboundCollector 수정(커밋 b0c2cd7)과 
Config 날짜 자동화(커밋 7cc1d7e)를 완료했어.

이제 InventoryCollector 개발을 시작할게.
- 백엔드: C:/OSIS_AUTO/inventory_status/inventory_status_20251020.csv
- 컬럼: 12개 (COLLECTOR_修正_PLAN.md 참고)
- 작업 시간: 3-4시간 예상

PROJECT_DIARY.md와 COLLECTOR_修正_PLAN.md를 확인하고
개발 시작해줘."
```

**이 명령이 완벽한 이유:**
1. ✅ 이전 작업 명시 (커밋 해시까지!)
2. ✅ 다음 작업 명확
3. ✅ 필요한 정보 제공
4. ✅ 참고 문서 명시
5. ✅ 예상 시간 언급

---

## 💡 추가 팁

### 1. 커밋 해시 활용
```
"커밋 b0c2cd7 이후 작업을 이어서 해줘"
```
→ 정확한 시점 지정 가능

### 2. 파일 경로 명시
```
"dashboard/src/data/collectors/outbound.py 파일을 수정해줘"
```
→ 정확한 파일 지정

### 3. 문서 참조
```
"BACKEND_COLUMN_ANALYSIS.md를 참고해서 작업해줘"
```
→ 필요한 정보 위치 명시

### 4. 작업 단계 명시
```
"Step 1: 분석, Step 2: 코드 작성, Step 3: 테스트 순서로 진행해줘"
```
→ 작업 흐름 명확

---

## 📌 저장해두면 좋은 정보

### 최근 커밋 해시
- OutboundCollector: `b0c2cd7`
- Config 날짜 자동화: `7cc1d7e`
- 최종 업데이트: `fb25d2e`

### 주요 파일 경로
- 작업 일지: `C:\Projects\WMS-DashBoard\PROJECT_DIARY.md`
- 수정 계획: `C:\Projects\WMS-DashBoard\COLLECTOR_修正_PLAN.md`
- 컬럼 분석: `C:\Projects\WMS-DashBoard\BACKEND_COLUMN_ANALYSIS.md`

### 다음 작업
- InventoryCollector 개발 (3-4시간)
- DeleteCollector 개발 (2-3시간)
- IrregularCollector 개발 (2-3시간)

---

## 🎯 결론

**가장 효과적인 명령 공식:**

```
"[이전 작업] + [커밋 해시] + [다음 작업] + [참고 문서]"
```

**예시:**
```
"이전 대화에서 OutboundCollector 수정(b0c2cd7) 완료.
InventoryCollector 개발 시작.
COLLECTOR_修正_PLAN.md 참고."
```

간결하면서도 필요한 정보를 모두 포함!

---

작성: 4명의 가상 전문가 팀  
작성 일시: 2025-10-20 15:20  
목적: 새로운 대화 시작 시 효율적인 소통
