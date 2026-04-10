# 🔄 Day 4 신규 진척도 (v10.html 기준 재설계)

**문서 목적**: 기존 Day 4~5를 통합하고, API 재설계 + card6 신규 개발 포함  
**작성일**: 2025-11-26  
**예상 체크박스**: 95개  
**예상 소요시간**: 12~16시간 (2일 분량)

---

## 📊 Day 4 개요

**목표**: Flask API를 v10.html 데이터 구조에 맞게 재설계 + 30초 자동 갱신

**주요 작업**:
1. API 응답 구조 재설계 (card1~6 v10 기준)
2. card6 API 신규 개발 (금일재고현황 5개 섹션)
3. v10.html → Flask 템플릿 변환
4. 30초 자동 갱신 JavaScript 구현
5. 통합 테스트

---

## 🔴 PART 1: API 응답 구조 재설계 (25개)

### 1.1 카드 번호 재매핑 (10개)

**변경 사항:**
- 기존 card2 → card1 (입고현황)
- 기존 card3 → card5 (피킹유의)
- 기존 card5 → card2 (자사출고)
- 기존 card6 → card3 (지방출고)
- 신규 card6 (금일재고현황)

- [ ] 1.1.1 dashboard.py 백업 생성
- [ ] 1.1.2 기존 card2 → card1로 변수명 변경 (입고현황)
- [ ] 1.1.3 기존 card3 → card5로 변수명 변경 (피킹유의)
- [ ] 1.1.4 기존 card5 → card2로 변수명 변경 (자사출고)
- [ ] 1.1.5 기존 card6 → card3로 변수명 변경 (지방출고)
- [ ] 1.1.6 JSON 응답에서 card1 키 사용
- [ ] 1.1.7 JSON 응답에서 card2 키 사용
- [ ] 1.1.8 JSON 응답에서 card3 키 사용
- [ ] 1.1.9 JSON 응답에서 card5 키 사용
- [ ] 1.1.10 카드 번호 매핑 주석 추가

---

### 1.2 키 이름 v10.html에 맞춤 (15개)

**card1 (입고현황) 키 변경:**
- [ ] 1.2.1 totalCount 유지
- [ ] 1.2.2 progressRate 유지
- [ ] 1.2.3 inboundRiskyCount 유지
- [ ] 1.2.4 riskyItems 배열 추가 (기존 API에 없음!)

**card2 (자사출고) 키 변경:**
- [ ] 1.2.5 totalAmount → amount 변경
- [ ] 1.2.6 comparePercent → compare 변경
- [ ] 1.2.7 unpublishedLabel → unprintedLabel 변경
- [ ] 1.2.8 irregularUnpublished → irregularUnprinted 변경

**card3 (지방출고) 키 변경:**
- [ ] 1.2.9 totalAmount → amount 변경
- [ ] 1.2.10 destinations 객체 형태로 변경 (배열 → 객체)
- [ ] 1.2.11 unprintedPicking 필드 추가

**card5 (피킹유의) 키 변경:**
- [ ] 1.2.12 items → riskyItems 변경
- [ ] 1.2.13 riskyItems 내부 키 확인 (location, productCode, productName, expiryDate, stockQty, validityRatio)
- [ ] 1.2.14 totalCount, urgentCount, warningCount 유지
- [ ] 1.2.15 키 변경 완료 테스트

---

## 🔴 PART 2: card6 API 신규 개발 (30개) ⭐ 핵심 작업

### 2.1 card6 데이터 수집 준비 (8개)

**필요한 CSV 파일:**
- inventory_status_{today}.csv → 총재고, 적치율, 선입선출
- outbound_all_{today}.csv → 미출/부분출고
- delete_status_{today}.csv → 삭제현황
- inbound_status_{today}.csv → 미할당

- [ ] 2.1.1 card6 계산용 변수 초기화 블록 추가
- [ ] 2.1.2 inventory_status 파일 경로 설정
- [ ] 2.1.3 outbound_all 파일 경로 설정
- [ ] 2.1.4 delete_status 파일 경로 설정
- [ ] 2.1.5 inbound_status 파일 경로 설정 (이미 있음)
- [ ] 2.1.6 각 CSV 로드 예외 처리
- [ ] 2.1.7 card6 계산 시작 주석 블록
- [ ] 2.1.8 디버그 로그 추가

---

### 2.2 섹션1: 총재고 + 적치율 계산 (5개)

**계산 로직:**
- 총재고 = SUM(가용수량 × 단가)
- 적치율 = (재고있는 상단로케이션 / 524) × 100

- [ ] 2.2.1 총재고 계산 (가용수량 × 단가)
- [ ] 2.2.2 적치율 계산 (L로 시작하는 로케이션)
- [ ] 2.2.3 524 상수 정의 (전체 상단 로케이션 수)
- [ ] 2.2.4 inventory 객체 생성 { total_value }
- [ ] 2.2.5 storageRate 객체 생성 { rate }

---

### 2.3 섹션2: 선입선출 위반 계산 (5개)

**계산 로직:**
- 동일 상품에서 하단(K) 소비기한 > 상단(L) 소비기한인 경우

- [ ] 2.3.1 상단(L) 로케이션 필터링
- [ ] 2.3.2 하단(K) 로케이션 필터링
- [ ] 2.3.3 상품별 소비기한 비교 로직
- [ ] 2.3.4 위반 항목 리스트 생성
- [ ] 2.3.5 fifo 배열 생성 [{ location, productCode, productName, upperExpiry, lowerExpiry }]

---

### 2.4 섹션3: 미출/부분출고 계산 (5개)

**계산 로직:**
- 18시 이후 기준
- 현재 outbound vs 백업 outbound 비교
- 오더수량 < 원주문수량 → 부분출고
- 오더수량 = 0 → 미출

- [ ] 2.4.1 18시 체크 로직 (현재시간 >= 18)
- [ ] 2.4.2 백업 파일 경로 설정
- [ ] 2.4.3 현재 vs 백업 비교 로직
- [ ] 2.4.4 부분출고/미출 분류
- [ ] 2.4.5 partial 배열 생성 [{ delivery_group, delivery_name, product_name, unit, original_qty, order_qty }]

---

### 2.5 섹션4: 삭제현황 계산 (4개)

**계산 로직:**
- delete_status.csv에서 센터별 분리
- 안산 / 음성 구분

- [ ] 2.5.1 안산 삭제 필터링
- [ ] 2.5.2 음성 삭제 필터링
- [ ] 2.5.3 deleteAnsan 배열 생성 [{ name, unit, count }]
- [ ] 2.5.4 deleteEumseong 배열 생성 [{ name, unit, count }]

---

### 2.6 섹션5: 미할당 입고현황 계산 (3개)

**계산 로직:**
- 입고 데이터 중 로케이션 미할당 건

- [ ] 2.6.1 미할당 조건 필터링 (로케이션 비어있음)
- [ ] 2.6.2 센터 정보 추출
- [ ] 2.6.3 unallocated 배열 생성 [{ name, unit, qty, center }]

---

## 🟡 PART 3: v10.html → Flask 템플릿 변환 (15개)

### 3.1 파일 복사 및 구조 변경 (10개)

- [ ] 3.1.1 v10.html 파일 백업
- [ ] 3.1.2 v10.html → flask_app/templates/dashboard.html 복사
- [ ] 3.1.3 templates 폴더 확인
- [ ] 3.1.4 dashboard.html 파일 확인
- [ ] 3.1.5 app.py에 render_template import 확인
- [ ] 3.1.6 루트 라우트 수정 (render_template 사용)
- [ ] 3.1.7 Flask 서버 실행
- [ ] 3.1.8 localhost:5000 접속 테스트
- [ ] 3.1.9 v10 레이아웃 렌더링 확인
- [ ] 3.1.10 기본 스타일 적용 확인

---

### 3.2 정적 파일 설정 (5개)

- [ ] 3.2.1 static/css 폴더 확인
- [ ] 3.2.2 static/js 폴더 확인
- [ ] 3.2.3 로고 이미지 복사 (있다면)
- [ ] 3.2.4 Flask static 경로 테스트
- [ ] 3.2.5 브라우저에서 정적 파일 로드 확인

---

## 🟡 PART 4: 30초 자동 갱신 JavaScript (20개)

### 4.1 API 호출 함수 추가 (10개)

- [ ] 4.1.1 dashboard.html 하단 script 영역 찾기
- [ ] 4.1.2 dashboardData 하드코딩 제거 계획
- [ ] 4.1.3 async function fetchDashboardData() 함수 추가
- [ ] 4.1.4 fetch('/api/dashboard') 호출 로직
- [ ] 4.1.5 response.json() 파싱
- [ ] 4.1.6 에러 처리 try-catch
- [ ] 4.1.7 네트워크 에러 시 재시도 로직
- [ ] 4.1.8 로딩 상태 표시 (선택)
- [ ] 4.1.9 데이터 수신 후 updateCard 함수들 호출
- [ ] 4.1.10 console.log 디버그 메시지

---

### 4.2 30초 주기 갱신 (10개)

- [ ] 4.2.1 REFRESH_INTERVAL = 30000 상수 정의
- [ ] 4.2.2 let refreshTimer = null 변수
- [ ] 4.2.3 function startAutoRefresh() 정의
- [ ] 4.2.4 setInterval(fetchDashboardData, REFRESH_INTERVAL)
- [ ] 4.2.5 function stopAutoRefresh() 정의
- [ ] 4.2.6 clearInterval(refreshTimer)
- [ ] 4.2.7 DOMContentLoaded 이벤트에서 첫 데이터 로드
- [ ] 4.2.8 DOMContentLoaded 이벤트에서 자동 갱신 시작
- [ ] 4.2.9 30초 대기 후 두 번째 갱신 확인
- [ ] 4.2.10 console에서 갱신 로그 확인

---

## 🟢 PART 5: 통합 테스트 (5개)

- [ ] 5.1 Flask 서버 실행 확인
- [ ] 5.2 /api/dashboard 응답 확인 (v10 구조)
- [ ] 5.3 브라우저에서 대시보드 렌더링 확인
- [ ] 5.4 30초 자동 갱신 동작 확인
- [ ] 5.5 Git 커밋

---

## 📊 Day 4 완료 기준 체크

**필수 완료 항목:**
- [ ] API 응답 구조 v10.html에 맞춤
- [ ] card6 (금일재고현황) API 완성
- [ ] v10.html → Flask 템플릿 변환
- [ ] 30초 자동 갱신 JavaScript 동작
- [ ] 통합 테스트 통과
- [ ] Git 커밋 완료

**Day 4 체크박스 총계**: 95개  
**예상 소요시간**: 12~16시간

---

## ⚠️ 주의사항

### API 재설계 시 주의점
1. 기존 pytest 테스트가 깨질 수 있음 → 테스트도 함께 수정 필요
2. 카드 번호 변경 시 모든 참조 확인

### card6 개발 시 주의점
1. 18시 이전/이후 로직 분기 필수
2. CSV 파일 없을 때 빈 배열 반환
3. 선입선출 계산은 상품코드 기준 groupby 필요

### JavaScript 수정 시 주의점
1. 기존 dashboardData 하드코딩 완전 제거
2. fetch 실패 시 마지막 데이터 유지 (TV 화면 빈칸 방지)
3. CORS 설정 확인

---

**작성자**: WMS 개발팀 (4인 전문가팀)  
**문서 버전**: v1.0  
**상태**: 📝 검토 대기
