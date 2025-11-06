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
   - 최신 작업 날짜 (2025-11-04)
   - Phase 진행률 (현재: 100% ✅)
   - 완료된 Collector (현재: 5/5 완료!)
   - 다음 작업 내용 (Phase 2 - 실제 데이터 연동)

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

- **개발 도구**: Streamlit + Flask (Python)
- **개발 기간**: Phase 1 완료 (20일) + Phase 2-3 예정 (18일)
- **개발 팀**: 4명 (풀스택, UX/UI, 데이터, 데브옵스)
- **현재 단계**: Phase 1 완료 (100%) ✅ → Phase 2 준비 중
- **최종 업데이트**: 2025-11-07

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
**상태:** ✅ Phase 1 완료 (100%)

백엔드에서 수집한 데이터를 시각화하는 웹 기반 현황판

**완성된 탭 (5/5):**
- ✅ 📦 입고 현황 - 입고 예정 및 진행 상황
- ✅ 🚚 출고 현황 - 10개 타입 출고 분석 및 출하금액
- ✅ 📊 재고 현황 - 4대 핵심 지표, 유효기한 관리
- ✅ 🗑️ 삭제 현황 - 삭제 처리된 오더 추적
- ✅ 📋 비정형 오더 - 특수 오더 관리

**테스트:**
- ✅ 기본 테스트 40개 (100% 통과)
- ✅ Edge Case 테스트 20개 (100% 통과)
- ✅ 테스트 커버리지 80%+

---

## 📊 현재 정확한 진행 상황 (2025-11-04 10:30 기준)

### Phase 0: ✅ 100% 완료
- 환경 구축, 샘플 데이터, BaseCollector, InboundCollector 프로토타입

### Phase 1: ✅ 100% 완료!

**완료된 작업:**
- ✅ Day 6: OutboundCollector 기본 구조
- ✅ Day 7: OutboundCollector UI 통합 (출고 탭)
- ✅ Day 8-9: InventoryCollector 개발 + 재고 탭 완성
- ✅ Day 10-13: DeleteCollector + IrregularCollector 개발
- ✅ Day 14-20: 테스트 60개 개발 및 100% 통과

**완료된 Collector (5/5):**
- ✅ InboundCollector (입고)
- ✅ OutboundCollector (출고)
- ✅ InventoryCollector (재고)
- ✅ DeleteCollector (삭제)
- ✅ IrregularCollector (비정형 오더)

**완료된 대시보드 탭 (5/5):**
- ✅ 입고 현황 탭
- ✅ 출고 현황 탭
- ✅ 재고 현황 탭
- ✅ 삭제 현황 탭
- ✅ 비정형 오더 탭

**완료된 테스트:**
- ✅ test_inbound.py (8개)
- ✅ test_outbound.py (8개)
- ✅ test_inventory_collector.py (8개)
- ✅ test_delete.py (8개)
- ✅ test_irregular.py (8개)
- ✅ test_edge_cases.py (20개)
- **총 60개 테스트 100% 통과**

**다음 작업 (Phase 2):**
- 실제 OSIS 서버 데이터 연동
- 성능 최적화
- 프로덕션 배포

### Phase 2: ⏳ 시작 예정 (2025-11-05~)
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

### 4. 🗑️ 삭제 현황 탭 ✅ 완성!
**5대 핵심 지표:**
- 총 삭제 건수
- 총 삭제 수량
- 18시 이후 삭제 건수
- 라벨출력 건수
- 센터 수

**주요 기능:**
- 배송군별 삭제량 집계
- 삭제 처리 시간 분석
- 삭제 상품 목록
- 알림 여부 추적

---

### 5. 📋 비정형 오더 탭 ✅ 완성!
**주요 지표:**
- 총 오더 건수
- 라벨미출력 건수
- 센터별 집계

**주요 기능:**
- 라벨미출력 오더 필터
- 센터별 오더량 분석
- 비정형 오더 목록

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
│   ├── app.py                     # 메인 앱 (5개 탭 완성)
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
│   │   │   ├── inventory.py      # 재고 수집기 ✅
│   │   │   ├── delete.py         # 삭제 수집기 ✅
│   │   │   └── irregular.py      # 비정형 수집기 ✅
│   │   │
│   │   ├── business/             # 비즈니스 로직
│   │   ├── ui/                   # UI 계층
│   │   │   └── components.py     # Streamlit 컴포넌트
│   │   └── utils/                # 유틸리티
│   │
│   └── tests/                    # 테스트 (60개)
│       ├── fixtures/             # 샘플 데이터
│       │   ├── sample_inbound.csv
│       │   ├── sample_outbound.csv
│       │   ├── sample_inventory.csv
│       │   ├── sample_delete.csv
│       │   ├── sample_irregular.csv
│       │   └── edge_cases/       # Edge Case 샘플 (8개)
│       ├── test_inbound.py       # 8개
│       ├── test_outbound.py      # 8개
│       ├── test_inventory_collector.py  # 8개
│       ├── test_delete.py        # 8개
│       ├── test_irregular.py     # 8개
│       └── test_edge_cases.py    # 20개
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

### Phase 1: MVP 개발 ✅ 완료! (100%)
```
[████████████████████] 100%
```

**완료된 작업:**
- [x] OutboundCollector 개발 (Day 6)
- [x] OutboundCollector UI 통합 (Day 7)
- [x] InventoryCollector 개발 (Day 8-9)
- [x] DeleteCollector 개발 (Day 10-13)
- [x] IrregularCollector 개발 (Day 10-13)
- [x] 5개 탭 UI 완성
- [x] 기본 테스트 40개 작성 (Day 14-15)
- [x] Edge Case 테스트 20개 작성 (Day 16-20)
- [x] 전체 60개 테스트 100% 통과
- [x] Git 커밋 완료
- [x] 문서 업데이트

**완료율:** 100% (15/15 체크박스)

**주요 성과:**
- 5개 Collector 완성
- 5개 대시보드 탭 완성
- 60개 테스트 100% 통과
- 테스트 커버리지 80%+
- 프로덕션 배포 준비 완료

---

### Phase 2: Flask TV 시스템 ⏳ 준비 중 (예정: 8일)
```
[░░░░░░░░░░░░░░░░░░░░] 0%
```

**목표:** 100인치 TV용 자동 갱신 대시보드 구축

**핵심 작업:**
- [ ] Flask API 서버 개발 (Day 1-3)
  - RESTful API 구조 설계
  - 5개 Collector 재사용 (100%)
  - JSON 응답 생성
  
- [ ] 자동 갱신 시스템 (Day 4-5)
  - 30초 주기 데이터 갱신
  - 캐싱 및 성능 최적화
  - 에러 처리 및 복구
  
- [ ] TV 전용 UI (Day 6-7)
  - HTML/CSS/JavaScript 개발
  - 6개 카드 레이아웃
  - 반응형 디자인 (100인치 최적화)
  
- [ ] 배포 및 테스트 (Day 8)
  - 운영 환경 구축
  - 실제 TV 테스트
  - 성능 모니터링

**Flask 아키텍처:**
```
100인치 TV (브라우저)
  ↓ HTTP
Flask API Server (data_server.py)
  ↓ collect()
Collector Layer (5개 재사용 100%)
  ↓ read_csv()
CSV Files (백엔드 출력)
```

**예상 완료일:** 2025-11-15

---

### Phase 3: 알림 시스템 ⏳ 예정 (10일)
```
[░░░░░░░░░░░░░░░░░░░░] 0%
```

**목표:** 10개 실시간 알림 기능 개발

**알림 목록:**
1. 🔴 재고 부족 알림 (가용수량 < 100)
2. 🔴 유효기한 임박 알림 (유효유통비 ≤ 20%)
3. 🔴 18시 이후 삭제 알림
4. 🔴 비정형 라벨미출력 알림
5. 🟡 입고 지연 알림
6. 🟡 출고 급증 알림
7. 🟡 출하금액 급감 알림
8. 🟢 대량 입고 예정
9. 🟢 신규 공급처
10. 🟢 일일 마감 리포트

**예상 완료일:** 2025-11-25

---

### Phase 2: 확장 및 최적화 ⏳ 시작 예정 (2025-11-05~)
```
[░░░░░░░░░░░░░░░░░░░░] 0%
```

**계획된 작업:**
- [ ] 실제 OSIS 데이터 연동 (3일)
- [ ] 성능 최적화 (3일)
- [ ] 운영 환경 구축 (2일)
- [ ] 사용자 피드백 (2일)

**Phase 2 추가 기능:**
- [ ] 실시간 자동 새로고침
- [ ] 알림 시스템
- [ ] 데이터 필터링 및 검색
- [ ] 엑셀 내보내기
- [ ] 반응형 레이아웃
- [ ] 대용량 데이터 처리 최적화

**예상 완료일:** 2025-11-15

---

## 📚 관련 문서

### 📖 공식 문서 (docs/official/)
- [PROJECT_STATUS.md](docs/official/PROJECT_STATUS.md) - 프로젝트 전체 상황 및 Phase별 진행 현황 (v3.0)
- [01_프로젝트_간단설명서.md](docs/official/01_프로젝트_간단설명서.md) - 프로젝트 개요 및 목표 (v2.0)
- [02_기술설명서.md](docs/official/02_기술설명서.md) - 기술 스택 및 아키텍처 상세 (v2.1)
- [03_시스템_흐름도.md](docs/official/03_시스템_흐름도.md) - 시스템 흐름 및 프로세스 (v2.0)
- [04_전체개발계획서.md](docs/official/04_전체개발계획서.md) - Phase 2-3 개발 계획 (v2.0)

### 📝 작업 일지
- [PROJECT_DIARY.md](PROJECT_DIARY.md) - 일별 작업 상세 기록 (⚠️ **끝부분부터 읽기!**)

### 🔧 대시보드 문서
- [dashboard/README.md](dashboard/README.md) - Streamlit 대시보드 설치 및 실행 가이드

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

**마지막 업데이트:** 2025-11-07  
**현재 상태:** Phase 1 완료 (100%) ✅ → Phase 2 준비 중  
**다음 작업:** Flask TV 시스템 개발 (8일) + 알림 시스템 (10일)
