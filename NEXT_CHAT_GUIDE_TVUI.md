# 다음 대화 시작 가이드 - TV 모니터 대시보드 UI/UX 개선 작업

## 🎯 현재 상태 (2025-10-21 22:05 완료)

### ✅ 완료된 작업

1. **pcap 분석 완료**
   - ourhome.pcapng (10.5MB) 분석
   - 실제 화면 레이아웃 구조 파악
   - 색상 팔레트, 기술 스택 확인

2. **레이아웃 구조 파악**
   - gaugeWrap > gaugeItem 카드 구조
   - 4단 레이아웃: 제목 / 게이지차트 / 큰숫자 / 라인차트
   - ingWarning 경고 클래스
   - 3-column grid (3개씩 한 줄)

3. **프로토타입 제작 완료**
   - HTML Artifact로 실시간 미리보기 제공
   - ourhome 색상/레이아웃 100% 재현
   - TV 모니터용 크기 최적화 (숫자 72pt)

---

## 📋 핵심 정보 요약

### 색상 팔레트 (ourhome 기반)
```javascript
primary: '#1b59f8'      // 메인 파랑
success: '#60CB2E'      // 정상 초록
warning: '#FAB03C'      // 주의 주황
danger: '#F05E5E'       // 위험 빨강
text: '#2C365C'         // 본문 텍스트
textLight: '#56667B'    // 보조 텍스트
background: '#EEF0F5'   // 배경
border: '#E7E8EB'       // 테두리
```

### 레이아웃 구조
```html
<div class="gaugeWrap">
  <div class="gaugeItem [ingWarning]">
    <h2>제목</h2>                      <!-- 32pt -->
    <div class="chartGauge">           <!-- 도넛 차트 -->
    <div class="gaugeTem">
      <em>숫자</em><span>단위</span>   <!-- 72pt -->
    </div>
    <div class="chartLine">            <!-- 라인 차트 -->
  </div>
</div>
```

### 파일 위치
- pcap: `C:\Projects\WMS-DashBoard\ourhome.pcapng`
- HTML: `C:\Projects\WMS-DashBoard\ourhome_page.html`
- 일지: `C:\Projects\WMS-DashBoard\PROJECT_DIARY.md`
- 프로토타입: Artifact `wms_tv_dashboard_prototype`

---

## 🚀 다음 작업 (우선순위)

### 1️⃣ Streamlit 통합 (최우선)
프로토타입을 실제 Streamlit 앱에 적용
- 기존 dashboard/app.py 수정
- HTML/CSS를 st.components.v1.html()로 임베드
- 실제 Collector 데이터 연동

### 2️⃣ 자동 화면 전환
10~30초마다 자동 순환
- 입고 현황 → 출고 현황 → 재고 현황
- JavaScript setInterval 사용

### 3️⃣ 재고 현황 추가
3번째 gaugeWrap 추가
- InventoryCollector 데이터 사용
- 총 상품 / 가용수량 / 위험상품

### 4️⃣ 실시간 데이터 갱신
30초마다 Collector에서 최신 데이터 로드
- 숫자 업데이트
- 차트 업데이트
- 경고 상태 체크

---

## 💡 다음 대화 시작 시

### 확인할 것
1. PROJECT_DIARY.md 끝부분 읽기 (offset=-100)
2. 2025-10-21 22:05 작업 확인
3. Artifact `wms_tv_dashboard_prototype` 참조

### 계속할 작업
- "Streamlit에 프로토타입 통합하기" 또는
- "자동 화면 전환 추가하기" 또는
- "색상/크기 조정하기"

### 말하면 안 되는 것
- DeleteCollector 개발 (아직 안 함!)
- Phase 1 60% 이상 진행 (Day 9까지만 완료)
- 새로운 Collector 추가 (입고/출고/재고만 완성)

---

## 🎨 프로토타입 핵심 특징

### ourhome과 동일한 것
- ✅ gaugeWrap > gaugeItem 구조
- ✅ 4단 카드 레이아웃
- ✅ ingWarning 경고 클래스
- ✅ pageLayer 팝업
- ✅ 색상 팔레트 100% 일치

### TV 모니터용 변경
- 📏 글씨 3~4배 확대
- 📏 차트 2배 확대
- 📏 여백 여유있게

### 작동 기능
- ⏰ 실시간 시계
- 📊 도넛 차트 6개
- 📈 라인 차트 6개
- ⚠️ 경고 애니메이션
- 🔔 자동 팝업

---

## 📝 중요 메모

1. **TV 모니터 사용 환경**
   - 10m 거리에서 봄
   - 24시간 켜져있음
   - 창고 작업자/관리자가 봄
   - 클릭 불가 (자동 전환)

2. **ourhome 레이아웃 유지가 핵심**
   - 단순 크기만 키우는 게 아님
   - 익숙한 레이아웃 유지
   - 색상 팔레트 동일

3. **경고 표시 방식**
   - ingWarning 클래스 추가
   - 배경/테두리 빨간색
   - pulse 애니메이션

---

**다음 대화 시작 시 이 파일을 참고하세요!**
