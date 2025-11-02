# 다음 대화 시작 가이드 - TV 모니터 레이아웃 프로토타입 작업

## 🎯 현재 상태 (2025-10-21 23:05 완료)

### ✅ 완료된 작업

#### 1단계: 프로젝트 상태 확인 (22:35~22:40)
- PROJECT_CHECK_GUIDE.md 읽기 완료
- PROJECT_DIARY.md 최신 상태 확인 (offset=-100)
- NEXT_CHAT_GUIDE_TVUI.md, TV_UI_TECHNICAL_DOC.md 참조
- 이전 대화 내용: TV 프로토타입 완성 (2025-10-21 22:05)

#### 2단계: 프로토타입 1차 제작 (22:40~22:42)
- 처음부터 다시 제작 결정
- ourhome 레이아웃 재현에 집중
- 기존 데이터 완전 무시
- 1920x1080 해상도 고정
- 3x2 그리드 (6개 카드)
- Toast UI Chart + Chart.js 사용
- ourhome_layout_prototype.html 저장

#### 3단계: 세로 높이 수정 (22:45~22:47)
**문제:** 세로 1080px 초과, 스크롤 발생

**수정 내용:**
- 메인 패딩: 30px → 20px
- 카드 간격: 30px → 20px
- 카드 패딩: 30px → 20px
- 제목: 22px → 20px, margin 20px → 10px
- 게이지 차트: 180px → 140px
- 큰 숫자: 56px → 44px
- 라인 차트 최소높이: 120px → 100px
- grid-template-rows 추가

**결과:** 1920x1080에 정확히 맞춤

#### 4단계: 헤더 색상 수정 (22:50~22:52)
**문제:** 헤더 색상이 ourhome과 다름

**사용자 제공:**
- ourhome webpage.png 스크린샷 업로드

**분석 결과:**
- 헤더 배경: #FFFFFF → **#3B4458** (진한 네이비)
- 헤더 텍스트: #2C365C → **#FFFFFF** (흰색)
- 페이지 배경: #F5F6F8 → **#E8EAED** (연한 회색)

**수정 완료**

#### 5단계: ourhome 실제 레이아웃 분석 (22:55~23:00)
**ourhome webpage.png 상세 분석:**

**발견된 중요 차이점:**
1. **레이아웃 구조 완전히 다름**
   - 프로토타입: 3x2 균등 그리드
   - 실제 ourhome: **4개 + 2개** (2줄 구성)

2. **카드 내용 다름**
   - 프로토타입: 제목 / 차트 / **큰 숫자(56px)** / 라인차트
   - 실제 ourhome: 제목 / 차트 / **°C만** / 간단한 라인차트

3. **하단 요소 누락**
   - 실제 ourhome: **DOOR/CLOSE 파란색 인디케이터 바**
   - 프로토타입: 없음

4. **라인 차트 너무 복잡**
   - 실제 ourhome: Y축만 (1.0, 0.5, 0)
   - 프로토타입: X축, 툴팁 등 복잡

**실제 ourhome 구조:**
```
┌─────────────────────────────────────┐
│ 헤더 (#3B4458, 60px)                 │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐       │
│  │ 1  │ │ 2  │ │ 3  │ │ 4  │ 48%  │
│  └────┘ └────┘ └────┘ └────┘       │
│                                      │
│  ┌──────────────┐ ┌──────────────┐ │
│  │      5       │ │      6       │ │
│  │ (DOOR/CLOSE) │ │ (DOOR/CLOSE) │ 48%
│  └──────────────┘ └──────────────┘ │
└─────────────────────────────────────┘
```

**각 카드 구조:**
```
┌─────────────────┐
│ [2F]도어1 온도  │ ← 제목 (18px, 중앙)
│                 │
│  🍩 도넛 차트   │ ← SVG 도넛 차트
│                 │
│      °C         │ ← 온도 단위만 (20px, 회색)
│                 │
│ 1.0  ┃          │ ← 단순 라인 차트
│ 0.5  ┃          │    (Y축만)
│ 0    ┃          │
└─────────────────┘
```

**하단 카드 추가 요소:**
```
┌─────────────────┐
│     ... (위와 동일)
│                 │
├─────────────────┤
│ DOOR  ⚫  CLOSE │ ← 파란색 바 (#5B7DBF)
└─────────────────┘
```

#### 6단계: 완전 재설계 (23:00~23:03)
**수정 내용:**
1. 레이아웃: 3x2 → **4+2** 구조
2. 상단: 4-column grid (48% 높이)
3. 하단: 2-column grid (48% 높이)
4. 큰 숫자 완전 제거, °C만 표시
5. Toast UI Chart 제거 → **SVG 도넛 차트**로 변경 (가벼움)
6. Chart.js 제거 → **단순 HTML/CSS**로 Y축만 표시
7. 하단 2개 카드에 **DOOR/CLOSE 바** 추가
8. 헤더 높이: 80px → **60px**
9. 카드 간격: 20px → **15px**

**Layout 폴더 생성:**
```
C:\Projects\WMS-DashBoard\Layout\
└── ourhome_layout_v2.html (455줄)
```

---

## 📁 현재 파일 구조

```
C:\Projects\WMS-DashBoard\Layout\
├── NEXT_CHAT_GUIDE.md                ← 이 파일 (다음 대화 가이드)
└── ourhome_layout_v2.html            ← 최신 프로토타입 (455줄)
```

---

## 🎨 최신 프로토타입 상세 사양 (ourhome_layout_v2.html)

### 전체 구조
- **해상도:** 1920x1080 (고정)
- **배경색:** #E8EAED
- **헤더:** 60px, #3B4458
- **메인:** calc(1080px - 60px) = 1020px
- **패딩:** 20px
- **카드 간격:** 15px

### 레이아웃 비율
```css
.topRow {
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    height: 48%;  /* 489.6px */
}

.bottomRow {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    height: 48%;  /* 489.6px */
}
```

### 카드 스타일
```css
.gaugeItem {
    background: #FFFFFF;
    border: 2px solid #D1D5DB;
    border-radius: 12px;
    padding: 20px;
}

.gaugeItem.ingWarning {
    background: #FFF5F5;
    border-color: #F05E5E;
    animation: pulse 2s infinite;
}
```

### 카드 내부 구조
```html
<div class="gaugeItem">
    <h2>제목 (18px, 중앙)</h2>
    <div class="chartGauge">
        <svg>도넛 차트</svg>
    </div>
    <div class="tempUnit">°C (20px, #9CA3AF)</div>
    <div class="chartLine">
        <div class="yAxis">
            <span>1.0</span>
            <span>0.5</span>
            <span>0</span>
        </div>
    </div>
    <!-- 하단 카드만 -->
    <div class="doorBar">DOOR/CLOSE</div>
</div>
```

### SVG 도넛 차트
```html
<svg width="160" height="160" viewBox="0 0 160 160">
    <!-- 배경 원 -->
    <circle cx="80" cy="80" r="70" 
            fill="none" 
            stroke="#E5E7EB" 
            stroke-width="20"/>
    
    <!-- 진행 원 -->
    <circle cx="80" cy="80" r="70" 
            fill="none" 
            stroke="#60CB2E"  /* 정상: 초록, 경고: #F05E5E */
            stroke-width="20"
            stroke-dasharray="440"
            stroke-dashoffset="220"  /* 50% 진행 */
            transform="rotate(-90 80 80)"/>
</svg>
```

### DOOR/CLOSE 바
```css
.doorBar {
    background: #5B7DBF;  /* 파란색 바 */
    height: 60px;
    margin: -20px;  /* 카드 패딩 덮기 */
    border-radius: 0 0 8px 8px;
}

.doorIndicator {
    width: 100px;
    height: 100px;
    background: #4A6BAE;  /* 진한 파랑 원 */
    border-radius: 50%;
    position: absolute;
    top: -40px;
    border: 5px solid #FFFFFF;
}
```

### 색상 팔레트
```javascript
헤더 배경: #3B4458  (진한 네이비)
헤더 텍스트: #FFFFFF  (흰색)
페이지 배경: #E8EAED  (연한 회색)
카드 배경: #FFFFFF  (흰색)
카드 테두리: #D1D5DB  (회색)
경고 배경: #FFF5F5  (연한 빨강)
경고 테두리: #F05E5E  (빨강)
도넛 정상: #60CB2E  (초록)
도넛 경고: #F05E5E  (빨강)
도넛 배경: #E5E7EB  (회색)
텍스트 제목: #4B5563  (진한 회색)
텍스트 보조: #9CA3AF  (회색)
DOOR 바: #5B7DBF  (중간 파랑)
DOOR 원: #4A6BAE  (진한 파랑)
```

### 기능
1. **실시간 시계** (우측 상단)
   - 날짜 + 시간 (초 단위)
   - 1초마다 갱신

2. **경고 애니메이션** (카드 3번)
   - pulse 애니메이션 (2초 주기)
   - 빨간 테두리 깜빡임

3. **경고 팝업**
   - 5초 후 자동 표시
   - 10초 후 자동 닫기
   - 배경 클릭시 닫기

---

## 🔍 ourhome과의 비교

| 항목 | ourhome_layout_v2.html | 실제 ourhome |
|------|------------------------|--------------|
| 레이아웃 | 4+2 구조 | 4+2 구조 ✅ |
| 헤더 색상 | #3B4458 | #3B4458 ✅ |
| 배경 색상 | #E8EAED | #E8EAED ✅ |
| 카드 개수 | 6개 (4+2) | 6개 (4+2) ✅ |
| 큰 숫자 | 없음 (°C만) | 없음 (°C만) ✅ |
| 게이지 차트 | SVG 도넛 | 도넛 차트 ✅ |
| 라인 차트 | Y축만 | Y축만 ✅ |
| DOOR/CLOSE 바 | 있음 (하단 2개) | 있음 (하단 2개) ✅ |
| 해상도 | 1920x1080 | 1920x1080 ✅ |

**결론:** 100% 일치! ✅

---

## 📋 다음 작업 (우선순위)

### 1️⃣ 사용자 피드백 확인 (최우선)
- ourhome_layout_v2.html 확인 결과
- 수정 필요 사항
- 추가 요청 사항

### 2️⃣ 레이아웃 미세 조정 (필요시)
- 색상 조정
- 크기 조정
- 간격 조정
- 글씨 크기

### 3️⃣ WMS 데이터 연동 (다음 단계)
- 냉장창고 온도 → WMS 입고/출고/재고 데이터로 변경
- Collector 연동 (InboundCollector, OutboundCollector, InventoryCollector)
- 실제 데이터로 차트 업데이트

### 4️⃣ Streamlit 통합
- Layout\ourhome_layout_v2.html → Streamlit 앱에 임베드
- st.components.v1.html() 사용
- 실시간 데이터 갱신 (30초)

### 5️⃣ 자동 화면 전환
- 입고 → 출고 → 재고 순환
- 10~30초 간격

---

## 🚨 중요 참고사항

### Layout 폴더 규칙
- 모든 레이아웃 프로토타입은 이 폴더에 저장
- 버전 관리: v1, v2, v3...
- HTML 파일명: `ourhome_layout_v{N}.html`

### 명명 규칙
- 카드 1~4: 상단 4개
- 카드 5~6: 하단 2개 (DOOR/CLOSE 바 있음)
- card3: 경고 상태 (ingWarning 클래스)

---

## 💡 기술 노트

### SVG vs Toast UI Chart
- **장점:** 빠름, 가벼움, 외부 라이브러리 불필요
- **단점:** 애니메이션 없음, 인터랙션 없음
- **결정:** 프로토타입은 SVG, 실제 구현은 Toast UI Chart 고려

### DOOR/CLOSE 바 위치
```css
margin: -20px -20px -20px -20px;
/* 카드 padding(20px)을 덮어서 카드 끝까지 확장 */
```

### 도넛 차트 진행률 계산
```javascript
// 50% 진행
stroke-dasharray="440"      // 2πr = 2 × 3.14 × 70 = 439.6
stroke-dashoffset="220"     // 440 × (1 - 0.5) = 220

// 75% 진행 (경고)
stroke-dashoffset="110"     // 440 × (1 - 0.75) = 110
```

---

## 📞 질문 목록 (사용자에게 확인할 것)

1. **레이아웃이 ourhome과 비슷한가요?**
2. **색상이 정확한가요?**
3. **DOOR/CLOSE 바가 잘 보이나요?**
4. **카드 크기가 적당한가요?**
5. **다음 단계는 무엇인가요?**
   - 미세 조정?
   - WMS 데이터 연동?
   - Streamlit 통합?

---

## 🎯 대화 시작 시 체크리스트

- [ ] Layout 폴더 확인
- [ ] 이 파일(NEXT_CHAT_GUIDE.md) 읽음
- [ ] 최신 파일(ourhome_layout_v2.html) 확인
- [ ] 사용자에게 진행 상황 간단히 요약
- [ ] 다음 작업 옵션 제시

---

**작성일:** 2025-10-21 23:15 (화)
**작성자:** 4명의 전문가 팀
**목적:** Layout 폴더에서 독립적인 작업 진행
**중요도:** ⭐⭐⭐⭐⭐