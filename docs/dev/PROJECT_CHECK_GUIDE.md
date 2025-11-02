# ⚠️ 프로젝트 상태 확인 필수 가이드

**이 문서는 WMS 대시보드 프로젝트를 다룰 때 가장 먼저 읽어야 할 문서입니다.**

---

## 🚨 중요: 대화 시작 시 필수 절차

### 문제 상황
- PROJECT_DIARY.md 파일이 1783줄로 길어짐
- 최신 작업 내역은 **파일 끝부분**에 있음
- 기본 read_file()은 앞부분 1000줄만 읽음
- **결과:** 이미 완료된 작업을 "다음 작업"이라고 착각하는 치명적 오류 발생

### 올바른 확인 절차

```python
# ✅ 올바른 방법: 끝부분부터 읽기
read_file("PROJECT_DIARY.md", offset=-100)

# ❌ 잘못된 방법: 앞부분만 읽기
read_file("PROJECT_DIARY.md")  # 기본값 = offset=0, length=1000
```

---

## 📋 대화 시작 시 체크리스트

**프로젝트 상태를 확인할 때 반드시 이 순서대로:**

### 1️⃣ PROJECT_DIARY.md 끝부분 확인
```python
# 최신 100줄 읽기
read_file("C:/Projects/WMS-DashBoard/PROJECT_DIARY.md", offset=-100)
```

**확인할 것:**
- 마지막 작업 날짜 (현재: 2025-10-20)
- 마지막 작업 시간 (22:07)
- 마지막 작업 내용 (InventoryCollector 완성)

---

### 2️⃣ Phase 진행률 확인
**현재 정확한 상태 (2025-10-20 22:10 기준):**
- Phase 0: ✅ 100% 완료
- Phase 1: 🚧 60% 완료 (Day 9/15)

---

### 3️⃣ 완료된 Collector 확인
**현재 (3/5 완료):**
- ✅ InboundCollector (입고) - Day 5 완료
- ✅ OutboundCollector (출고) - Day 6-7 완료
- ✅ InventoryCollector (재고) - Day 8-9 완료 ← 최신!
- ⏳ DeleteCollector (삭제) - 다음 작업
- ⏳ IrregularCollector (비정형) - 예정

---

### 4️⃣ 완료된 대시보드 탭 확인
**현재 (3/5 완료):**
- ✅ 입고 현황 탭
- ✅ 출고 현황 탭
- ✅ 재고 현황 탭 ← 최신!
- ⏳ 삭제 현황 탭 - 다음 작업
- ⏳ 비정형 오더 탭 - 예정

---

### 5️⃣ 다음 작업 확인
**다음 작업:**
- Day 10-11: DeleteCollector 개발
- 삭제 대시보드 탭 추가
- 예상 소요 시간: 4-6시간

---

## 🔍 전체 파일 확인이 필요한 경우

파일이 너무 길어서 나눠 읽어야 할 때:

```python
# 1단계: 앞부분 (0~1000줄)
read_file("PROJECT_DIARY.md", offset=0, length=1000)

# 2단계: 뒷부분 (1000~1783줄)
read_file("PROJECT_DIARY.md", offset=1000, length=783)
```

---

## ❌ 하지 말아야 할 것

### 1. 기본 read_file() 사용 금지
```python
# ❌ 이렇게 하면 안 됨!
read_file("PROJECT_DIARY.md")  # 앞부분 1000줄만 읽음
```

**왜?**
- 최신 정보(InventoryCollector 완료)는 1783줄 중 1600줄 이후에 있음
- 앞부분만 읽으면 Day 7 완료 상태만 보임
- "다음은 InventoryCollector 개발입니다" ← 이미 완료됨!

---

### 2. 추측하지 않기
```python
# ❌ 이렇게 하면 안 됨!
"마지막으로 본 게 Day 7이니까... 아마 Day 8이 다음일 거야"
```

**올바른 방법:**
```python
# ✅ 항상 확인하기
read_file("PROJECT_DIARY.md", offset=-100)  # 최신 상태 확인
```

---

### 3. 사용자에게 이미 완료된 작업 제안하지 않기
```python
# ❌ 잘못된 대화:
사용자: "이전 대화 이어서 계속할게"
AI: "InventoryCollector 개발을 시작하시겠어요?" ← 이미 완료됨!

# ✅ 올바른 대화:
사용자: "이전 대화 이어서 계속할게"
AI: [먼저 PROJECT_DIARY.md offset=-100으로 확인]
AI: "InventoryCollector 완료하셨네요! (60% 진행) 다음은 DeleteCollector 개발이에요."
```

---

## 🎯 핵심 원칙

### 📌 원칙 1: 항상 최신부터
```
파일이 길면 끝부터 읽어라!
오래된 정보는 앞에, 최신 정보는 뒤에 있다.
```

### 📌 원칙 2: 추측 금지
```
"아마도", "아마", "~일 것 같다" 금지!
반드시 확인하고 사실만 말한다.
```

### 📌 원칙 3: 의심스러우면 다시 확인
```
확신이 서지 않으면 → 파일 다시 읽기
사용자가 의문을 제기하면 → 즉시 재확인
```

### 📌 원칙 4: 사용자에게 명확히 알리기
```
"PROJECT_DIARY.md 최신 내역 확인했습니다"
"현재 Phase 1 Day 9 완료 (60%) 상태입니다"
"다음 작업은 DeleteCollector 개발입니다"
```

---

## 📊 빠른 참조

### 현재 상태 (2025-10-20 22:10 기준)

| 항목 | 상태 | 비고 |
|------|------|------|
| Phase 0 | ✅ 100% | 완료 |
| Phase 1 | 🚧 60% | Day 9/15 |
| InboundCollector | ✅ 완료 | Day 5 |
| OutboundCollector | ✅ 완료 | Day 6-7 |
| InventoryCollector | ✅ 완료 | Day 8-9 (최신!) |
| DeleteCollector | ⏳ 대기 | Day 10-11 (다음!) |
| IrregularCollector | ⏳ 대기 | Day 12-13 |
| 입고 탭 | ✅ 완료 | |
| 출고 탭 | ✅ 완료 | |
| 재고 탭 | ✅ 완료 | 최신! |
| 삭제 탭 | ⏳ 대기 | 다음! |
| 비정형 탭 | ⏳ 대기 | |

---

## 🔗 관련 문서

- **PROJECT_DIARY.md** - 일별 작업 일지 (1783줄, 끝부터 읽기!)
- **PROJECT_STATUS.md** - 전체 진행 상황 (상세)
- **README.md** - 프로젝트 개요

---

## 💡 재발방지 대책

이 문서를 만든 이유:
1. 2025-10-20 22:07에 오류 발생
2. 대화 시작 시 앞부분만 읽어서 오래된 정보를 현재로 착각
3. 이미 완료된 InventoryCollector를 "다음 작업"이라고 제안
4. 사용자가 "왜 자꾸 이런 오류를 반복하느냐" 지적

**재발 방지:**
- ✅ OpenMemory에 규칙 저장
- ✅ PROJECT_STATUS.md 맨 위에 경고 추가
- ✅ README.md 맨 위에 경고 추가
- ✅ PROJECT_DIARY.md에 오류 분석 기록
- ✅ 이 문서(PROJECT_CHECK_GUIDE.md) 작성

**앞으로:**
- 대화 시작 시 반드시 이 가이드 참조
- PROJECT_DIARY.md는 항상 offset=-100부터
- 의심스러우면 전체 파일 확인
- 사용자에게 명확하고 정확한 정보 제공

---

**작성일:** 2025-10-20 22:15 (일요일)  
**목적:** 프로젝트 상태 확인 오류 재발 방지  
**중요도:** ⭐⭐⭐⭐⭐ (최우선)
