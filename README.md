# 🏭 WMS 대시보드 - 냉장 재고 종합 현황판

창고관리 시스템(WMS) 실시간 현황판

---

## ⚠️ 【중요】프로젝트 상태 확인 필수 절차

**이 프로젝트를 다룰 때 가장 먼저 확인해야 할 것:**

```
1. PROJECT_DIARY.md는 항상 끝부분부터 읽기!
   → read_file(offset=-100) 으로 최신 100줄 먼저 확인

2. 왜 중요한가?
   - 파일이 1783줄로 길어져서 최신 정보는 끝에 있음
   - 앞부분(1000줄)만 읽으면 오래된 정보를 현재로 착각
   - 이미 완료된 작업을 "다음 작업"이라고 착각하는 치명적 오류 발생

3. 반드시 확인할 것:
   - 최신 작업 날짜 (2025-10-20)
   - Phase 진행률 (현재: 60%)
   - 완료된 Collector (현재: 3/5 - Inbound, Outbound, Inventory)
   - 다음 작업 내용 (DeleteCollector 개발)

4. 의심스러우면 전체 파일 나눠 읽기:
   - read_file(offset=0, length=1000)
   - read_file(offset=1000, length=783)
```

**이 규칙을 지키지 않으면:**
- ❌ 완료된 작업을 "다음 작업"이라고 착각
- ❌ 사용자에게 혼란과 불신 초래  
- ❌ 프로젝트 진행에 차질

---

## 📌 프로젝트 개요

물류 현장에서 필요한 **실시간 재고 정보**와 **긴급 알림**을 한 화면에 표시하여,  
작업자들이 신속하게 의사결정할 수 있도록 지원하는 대시보드

- **개발 도구**: Streamlit (Python)
- **개발 기간**: 8주 (40일)
- **개발 팀**: 4명 (풀스택, UX/UI, 데이터, 데브옵스)
- **현재 단계**: Phase 1 - MVP 개발 (60% 완료) ✅
- **최종 업데이트**: 2025-10-20 22:10

---

## 🏗️ 시스템 구조

이 프로젝트는 **두 개의 독립적인 시스템**으로 구성됩니다:

### 🔧 백엔드: 데이터 수집 시스템
**위치:** `C:\OSIS_AUTO\`  
**상태:** ✅ 완성 (100%)

5개 핵심 모듈이 실제 운영 데이터를 자동 수집:
- **Inbound Status** - 입고 정보 수집
- **Outbound Status** - 출고 정보 수집 (10개 타입, 출하금액 계산)
- **inventory_status** - 재고 정보 수집 (422개 상품, 자동 백업)
- **Delete Status** - 삭제 정보 수집 (자동 백업)
- **IrregularOrder Status** - 비정형 오더 수집 (자동 백업)

**백엔드 주요 기능:**
- 날짜 기반 파일명 통일 (예: `inventory_status_YYYYMMDD.csv`)
- 자동 백업 시스템 (같은 날 재실행 시 백업 후 덮어쓰기)
- 출고 출하금액 자동 계산 (재고 단가 연동)
- 실시간 운영 데이터 수집 중

### 🖥️ 프론트엔드: Streamlit 대시보드
**위치:** `C:\Projects\WMS-DashBoard\dashboard\`  
**상태:** 🚧 개발 중 (Phase 1: 60%)

백엔드에서 수집한 데이터를 시각화하는 웹 기반 현황판

**완성된 탭 (3/5):**
- ✅ 📦 입고 현황 - 입고 예정 및 진행 상황
- ✅ 🚚 출고 현황 - 10개 타입 출고 분석 및 출하금액
- ✅ 📊 재고 현황 - 4대 핵심 지표, 유효기한 관리 (2025-10-20 완성!)
- ⏳ 🗑️ 삭제 현황 - 삭제 처리된 오더 추적 (다음 작업)
- ⏳ 📋 비정형 오더 - 특수 오더 관리

---

## 📊 현재 정확한 진행 상황 (2025-10-20 22:10 기준)

### Phase 0: ✅ 100% 완료
- 환경 구축, 샘플 데이터, BaseCollector, InboundCollector 프로토타입

### Phase 1: 🚧 60% 완료 (Day 9/15)

**완료된 작업:**
- ✅ Day 6: OutboundCollector 기본 구조
- ✅ Day 7: OutboundCollector UI 통합 (출고 탭)
- ✅ Day 8-9: InventoryCollector 개발 + 재고 탭 완성 ← 최신!

**완료된 Collector (3/5):**
- ✅ InboundCollector (입고)
- ✅ OutboundCollector (출고)
- ✅ InventoryCollector (재고) ← 최신 완료!

**완료된 대시보드 탭 (3/5):**
- ✅ 입고 현황 탭
- ✅ 출고 현황 탭
- ✅ 재고 현황 탭 ← 최신 완료!

**다음 작업:**
- **Day 10-11: DeleteCollector 개발** (삭제 대시보드) ← 다음!
- Day 12-13: IrregularCollector 개발 (비정형 오더 대시보드)
- Day 14-15: 실제 데이터 연동 + 통합 테스트

### Phase 2: ⏳ 대기 중 (예정)
- 실시간 자동 새로고침, 알림 시스템, 성능 최적화 등

---

## 💡 주요 기능 (Phase 1 - MVP)

### 1. 📦 입고 현황 탭 ✅
**4대 핵심 지표:**
- 총 입고 건수
- 총 입고 수량
- 평균 입고 수량
- 공급처 수

**주요 기능:**
- 공급처별 입고량 TOP 10
- 상품별 입고량 TOP 10
- 입고 데이터 전체 목록

---

### 2. 🚚 출고 현황 탭 ✅
**4대 핵심 지표:**
- 총 출고 건수
- 총 출고 수량
- 총 출하금액 (재고 단가 연동)
- 출고처 수

**10개 출고 타입:**
- 04: 지방 캘리스코 출고
- 05: 한익스, 키즈 출고
- 08: 지방 삼각유부,델리치 50% 출고
- 14: 자사 캘리스코 출고
- 15: 자사 물품 출고
- 16: 지방 (직접 발주 상품) 출고
- 17: 지방 (자동 발주 상품) 출고
- 18: 자사 삼각유부,델리치 50% 출고
- 52: 지방 캘리스코 출고
- 53: 지방 삼각유부,델리치 50% 출고

**주요 기능:**
- 출고처별 출고량 TOP 10
- 상품별 출고량 TOP 10
- 출고유형별 집계 및 차트
- 출하금액 자동 계산 및 통계

---

### 3. 📊 재고 현황 탭 ✅ (최신 완성!)
**4대 핵심 지표:**
- 총 상품 수
- 총 가용수량
- 총 재고금액
- 위험 상품 수 (유효유통비 ≤ 20%)

**주요 기능:**
- 평균 유효유통비 (색상 표시)
- 유효비 구간별 분포 차트
- 위험 상품 목록 (빨간색 강조)
- 가용수량 부족 상품 필터
- 재고금액 TOP 10
- 전체 재고 목록 (필터/정렬 기능)

**완성 날짜:** 2025-10-20

---

### 4. 🗑️ 삭제 현황 탭 ⏳ (다음 작업)
**예정 기능:**
- 삭제 건수 및 금액
- 삭제 사유별 집계
- 삭제 상품 목록

---

### 5. 📋 비정형 오더 탭 ⏳ (예정)
**예정 기능:**
- 비정형 오더 건수
- 처리 상태별 집계
- 특이사항 목록

---

## 🚀 빠른 시작

### 1. 필수 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 2. 설치
```bash
# 저장소 클론
cd C:\Projects\WMS-DashBoard\dashboard

# 가상환경 활성화
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 실행
```bash
# Streamlit 앱 실행
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501` 열림

### 4. 데이터 소스 설정 (Phase 1 Day 14-15에 진행 예정)
```yaml
# config/data_sources.yaml 예시
inbound:
  path: "C:/OSIS_AUTO/Inbound Status/inbound_merged_YYYYMMDD.csv"
  
outbound:
  path: "C:/OSIS_AUTO/Outbound Status/outbound_XX_YYYYMMDD.csv"
  
inventory:
  path: "C:/OSIS_AUTO/inventory_status/inventory_status_YYYYMMDD.csv"
```

---

## 📁 프로젝트 구조

```
C:\Projects\WMS-DashBoard\
│
├── dashboard/                      # Streamlit 대시보드
│   ├── app.py                     # 메인 앱 (3개 탭 완성)
│   ├── requirements.txt           # 패키지 의존성
│   │
│   ├── config/                    # 설정 파일
│   │   ├── config.example.yaml   # 설정 예시
│   │   └── data_sources.yaml     # 데이터 소스 설정
│   │
│   ├── src/                       # 소스 코드
│   │   ├── data/collectors/       # 데이터 수집기
│   │   │   ├── base.py           # 추상 베이스 클래스
│   │   │   ├── inbound.py        # 입고 수집기 ✅
│   │   │   ├── outbound.py       # 출고 수집기 ✅
│   │   │   ├── inventory.py      # 재고 수집기 ✅ (최신!)
│   │   │   ├── delete.py         # 삭제 수집기 (다음 작업)
│   │   │   └── irregular.py      # 비정형 수집기 (예정)
│   │   │
│   │   ├── business/             # 비즈니스 로직
│   │   ├── ui/                   # UI 계층
│   │   │   └── components.py     # Streamlit 컴포넌트
│   │   └── utils/                # 유틸리티
│   │
│   └── tests/                    # 테스트
│       ├── fixtures/             # 샘플 데이터 (5종)
│       └── test_*.py             # 단위 테스트
│
├── docs/                         # 문서
├── scripts/                      # 스크립트
├── PROJECT_STATUS.md             # 진행 상황 (상세)
├── PROJECT_DIARY.md              # 작업 일지 (1783줄)
└── README.md                     # 프로젝트 개요 (이 파일)
```

---

## 🔧 백엔드 시스템 (C:\OSIS_AUTO\)

### 5개 핵심 모듈 상태: ✅ 100% 완성

#### 1. Inbound Status (입고 정보)
- 파일: `inbound_merged_YYYYMMDD.csv`
- 백업 시스템: ✅

#### 2. Outbound Status (출고 정보)
- 파일: `outbound_XX_YYYYMMDD.csv` (10개 타입)
- 출하금액 자동 계산: ✅
- 백업 시스템: ✅
- 최근 데이터: 10,261건, 약 7,942만원

#### 3. inventory_status (재고 정보)
- 파일: `inventory_status_YYYYMMDD.csv`
- 백업 시스템: ✅ (최초 구현)
- 최근 데이터: 422개 상품, 200,847개 재고
- 유효유통비 자동 계산: ✅

#### 4. Delete Status (삭제 정보)
- 파일: `delete_status_YYYYMMDD.csv`
- 백업 시스템: ✅

#### 5. IrregularOrder Status (비정형 오더)
- 파일: `irregular_order_YYYYMMDD.csv`
- 백업 시스템: ✅

---

## 📈 개발 단계별 체크리스트

### Phase 0: 사전 조사 및 환경 구축 ✅ 완료
```
[████████████████████] 100%
```
- [x] 기존 5개 프로그램 분석
- [x] 현장 인터뷰
- [x] Git 저장소 생성
- [x] 샘플 데이터 확보
- [x] BaseCollector 작성
- [x] InboundCollector 프로토타입
- [x] 메인 앱 작성 (app.py)

---

### Phase 1: MVP 개발 🚧 진행 중 (60%)
```
[████████████░░░░░░░░] 60%
```

**완료 (Day 6-9):**
- [x] OutboundCollector 개발 (Day 6)
- [x] OutboundCollector UI 통합 (Day 7)
- [x] InventoryCollector 개발 (Day 8-9) ✅
- [x] 재고 탭 완성 (Day 8-9) ✅

**다음 작업 (Day 10-11):**
- [ ] DeleteCollector 개발
- [ ] 삭제 탭 통합

**예정 (Day 12-15):**
- [ ] IrregularCollector 개발 (Day 12-13)
- [ ] 실제 데이터 연동 (Day 14-15)
- [ ] 통합 테스트 (Day 14-15)

---

### Phase 2: 확장 및 최적화 ⏳ 대기 중
```
[░░░░░░░░░░░░░░░░░░░░] 0%
```
- [ ] 실시간 자동 새로고침
- [ ] 알림 시스템
- [ ] 데이터 필터링 및 검색
- [ ] 엑셀 내보내기
- [ ] 반응형 레이아웃
- [ ] 성능 최적화

---

## 📚 관련 문서

- [PROJECT_STATUS.md](PROJECT_STATUS.md) - 상세 진행 상황 및 작업 내역
- [PROJECT_DIARY.md](PROJECT_DIARY.md) - 일별 작업 일지 (1783줄, **끝부분부터 읽기!**)
- `docs/architecture.md` - 시스템 아키텍처
- `docs/api_reference.md` - API 레퍼런스
- `docs/user_guide.md` - 사용자 가이드

---

## 🤝 기여 가이드

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 통해 남겨주세요.

---

## 🔗 관련 링크

- **GitHub:** https://github.com/The-Kero/WMS-DashBoard.git
- **로컬 경로:** C:\Projects\WMS-DashBoard\
- **백엔드 경로:** C:\OSIS_AUTO\

---

**마지막 업데이트:** 2025-10-20 22:10 (일요일)  
**다음 작업:** DeleteCollector 개발 (Day 10-11)
