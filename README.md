# 🏭 WMS 대시보드 - 냉장 재고 종합 현황판

창고관리 시스템(WMS) 실시간 현황판

## 📌 프로젝트 개요

물류 현장에서 필요한 **실시간 재고 정보**와 **긴급 알림**을 한 화면에 표시하여,  
작업자들이 신속하게 의사결정할 수 있도록 지원하는 대시보드

- **개발 도구**: Streamlit (Python)
- **개발 기간**: 8주 (40일)
- **개발 팀**: 4명 (풀스택, UX/UI, 데이터, 데브옵스)

---

## 🏗️ 시스템 구조

이 프로젝트는 **두 개의 독립적인 시스템**으로 구성됩니다:

### 🔧 백엔드: 데이터 수집 시스템
**위치:** `C:\OSIS_AUTO\`  
**상태:** ✅ 완성 (100%)

5개 핵심 모듈이 실제 운영 데이터를 자동 수집:
- **Inbound Status** - 입고 정보 수집
- **Outbound Status** - 출고 정보 수집 (10개 타입)
- **inventory_status** - 재고 정보 수집 (422개 상품)
- **Delete Status** - 삭제 정보 수집
- **IrregularOrder Status** - 비정형 오더 수집

### 🖥️ 프론트엔드: Streamlit 대시보드
**위치:** `C:\Projects\WMS-DashBoard\dashboard\`  
**상태:** 🚧 개발 중 (Phase 1: 20%)

백엔드에서 수집한 데이터를 시각화하는 웹 기반 현황판

---

## ✨ 주요 기능

### 1. 4대 핵심 지표 (항시 표시)
- 💰 당일 출하금액 (전일/전주 대비)
- 📦 입고 진행률
- ⚠️ 피킹 유의 상품 (유효비 20% 이하)
- 🚨 미할당 상품 (재고 부족)

### 2. 10종 긴급 알림 (Phase 2 예정)
- 🚨 긴급: 18시 이후 삭제 오더, 선입선출 오류 등
- ⚠️ 중요: 소비기한 임박, 추가 오더 발생 등
- ℹ️ 일반: 유제품 증가, 미출 발생 등

### 3. 시간대별 레이아웃 전환 (Phase 3 예정)
- 🌅 오전: 입고 중심
- ☀️ 오후: 피킹/출고 중심
- 🌆 저녁: 마감 준비
- 🌙 야간: 당일 요약

---

## 🗂️ 프로젝트 구조

```
WMS 대시보드 프로젝트 (전체)
│
├── 🔧 백엔드 데이터 수집 (C:\OSIS_AUTO\)
│   ├── Inbound Status\          ✅ 입고 정보
│   ├── Outbound Status\         ✅ 출고 정보 (10개 타입)
│   ├── inventory_status\        ✅ 재고 정보 (422개 상품)
│   ├── Delete Status\           ✅ 삭제 정보
│   └── IrregularOrder Status\   ✅ 비정형 오더
│
└── 🖥️ 프론트엔드 대시보드 (C:\Projects\WMS-DashBoard\)
    ├── dashboard\               🚧 Streamlit 웹 앱
    │   ├── src\                 
    │   │   ├── data\collectors\ (InboundCollector ✅, OutboundCollector ✅)
    │   │   └── ui\              (UI 컴포넌트)
    │   ├── config\              
    │   └── tests\fixtures\      (샘플 데이터 5개)
    │
    ├── references\              📚 기존 프로그램 레퍼런스
    ├── docs\                    📄 프로젝트 문서
    ├── PROJECT_STATUS.md        📊 진행 상황
    └── PROJECT_DIARY.md         📝 작업 일지
```

---

## 🔗 데이터 소스 (백엔드 모듈)

### ✅ 완성된 5개 데이터 수집 프로그램

| 모듈 | 위치 | 상태 | 설명 |
|------|------|------|------|
| **입고정보** | `C:\OSIS_AUTO\Inbound Status\` | ✅ | 입고 예정/완료 데이터 |
| **출고정보** | `C:\OSIS_AUTO\Outbound Status\` | ✅ | 10개 타입 출고 현황 + 출하금액 |
| **재고정보** | `C:\OSIS_AUTO\inventory_status\` | ✅ | 422개 상품 재고/단가 정보 |
| **삭제정보** | `C:\OSIS_AUTO\Delete Status\` | ✅ | 삭제 오더 |
| **비정형오더** | `C:\OSIS_AUTO\IrregularOrder Status\` | ✅ | 특별 오더 |

### 📦 출고 10개 타입 상세
- **04** - 지방 캘리스코 출고
- **05** - 한익스, 키즈 출고
- **08** - 지방 삼각유부,델리치 50% 출고
- **14** - 자사 캘리스코 출고
- **15** - 자사 물품 출고 ⭐ (전체 출하금액의 82%)
- **16** - 지방 (직접 발주 상품) 출고
- **17** - 지방 (자동 발주 상품) 출고
- **18** - 자사 삼각유부,델리치 50% 출고
- **52** - 지방 캘리스코 출고
- **53** - 지방 삼각유부,델리치 50% 출고

---

## 🚀 빠른 시작

### 개발 환경 설정

```bash
# 1. Clone 저장소
git clone https://github.com/The-Kero/WMS-DashBoard.git
cd WMS-DashBoard/dashboard

# 2. 가상환경 설정
python -m venv venv
venv\Scripts\activate  # Windows

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 설정 파일 생성
copy config\config.example.yaml config\config.yaml
```

### 설정 파일 수정 (config.yaml)

```yaml
data_sources:
  # 백엔드 실제 데이터 경로
  inbound: "C:/OSIS_AUTO/Inbound Status/inbound_merged_*.csv"
  outbound: "C:/OSIS_AUTO/Outbound Status/outbound_all_*.csv"
  inventory: "C:/OSIS_AUTO/inventory_status/inventory_status_*.csv"
  delete: "C:/OSIS_AUTO/Delete Status/delete_status_*.csv"
  irregular: "C:/OSIS_AUTO/IrregularOrder Status/irregular_order_*.csv"
```

### 실행

```bash
# Streamlit 대시보드 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 📚 문서

### 프로젝트 관리
- [📊 프로젝트 진행 상황](PROJECT_STATUS.md) - 최신 진행 상황 및 Phase별 체크리스트
- [📝 프로젝트 작업 일지](PROJECT_DIARY.md) - 일별 작업 내용 및 결과

### 설계 문서 (C:\OSIS_AUTO\)
- [프로젝트 간단 설명서](C:\OSIS_AUTO\01_프로젝트_간단설명서.md)
- [기술 설명서](C:\OSIS_AUTO\02_기술설명서.md)
- [시스템 흐름도](C:\OSIS_AUTO\03_시스템_흐름도.md)
- [전체 개발 계획서](C:\OSIS_AUTO\04_전체개발계획서.md)

---

## 🔧 기술 스택

### 백엔드 (데이터 수집)
- **언어**: Python 3.9+
- **라이브러리**: Pandas, Requests
- **저장**: CSV (하루 단위 스냅샷)
- **특징**: 자동 백업, 출하금액 계산

### 프론트엔드 (대시보드)
- **프레임워크**: Streamlit 1.30.0+
- **데이터 처리**: Pandas, NumPy
- **시각화**: Plotly
- **설정**: YAML

---

## 📅 개발 단계 및 진행 상황

```
Phase 0: 사전 조사 및 환경 구축  ████████████████████ 100% ✅
Phase 1: MVP 개발               ████░░░░░░░░░░░░░░░░  20% 🚧
  └─ InboundCollector           ████████████████████ 100% ✅
  └─ OutboundCollector          ████████████████████ 100% ✅
  └─ InventoryCollector         ░░░░░░░░░░░░░░░░░░░░   0% ⏳
  └─ DeleteCollector            ░░░░░░░░░░░░░░░░░░░░   0% ⏳
  └─ IrregularCollector         ░░░░░░░░░░░░░░░░░░░░   0% ⏳
Phase 2: 알림 기능 개발          ░░░░░░░░░░░░░░░░░░░░   0% ⏳
Phase 3: 시간대별 레이아웃       ░░░░░░░░░░░░░░░░░░░░   0% ⏳
Phase 4: 성능 최적화             ░░░░░░░░░░░░░░░░░░░░   0% ⏳
Phase 5: 배포 및 현장 안착        ░░░░░░░░░░░░░░░░░░░░   0% ⏳
```

**전체 진행률**: 약 24%  
**현재 단계**: Phase 1 MVP 개발 중 (Day 7/15 완료)

---

## 🎯 Phase 1 남은 작업

### ⏳ 진행 예정
- **Day 8-9**: InventoryCollector 개발 (재고 대시보드)
- **Day 10-11**: DeleteCollector 개발 (삭제 대시보드)
- **Day 12-13**: IrregularCollector 개발 (비정형 대시보드)
- **Day 14-15**: 실제 데이터 연동 및 통합 테스트

### ✅ 완료된 작업
- Phase 0: 전체 환경 구축 및 POC 개발
- Phase 1 Day 6: OutboundCollector 개발
- Phase 1 Day 7: 출고 UI 통합 및 2개 탭 시스템 완성
- 백엔드: 5개 모듈 완성 + 출하금액 계산 + 백업 시스템

---

## 📊 주요 성과

### 백엔드 시스템
- ✅ 5개 데이터 수집 모듈 100% 완성
- ✅ 출고 10개 타입 자동 분류 및 수집
- ✅ 출하금액 자동 계산 (재고 단가 연동)
- ✅ 하루 단위 스냅샷 + 자동 백업 시스템
- ✅ 422개 상품 재고 관리

### 프론트엔드 시스템
- ✅ BaseCollector 추상 클래스 (확장 가능한 아키텍처)
- ✅ 입고/출고 대시보드 완성
- ✅ 2개 탭 시스템 (입고/출고)
- ✅ 재사용 가능한 UI 컴포넌트 패키지

---

## 🤝 기여

이 프로젝트는 내부 물류 시스템을 위해 개발되었습니다.

**개발 팀:**
- 풀스택 개발자: 백엔드/프론트엔드 개발
- UX/UI 디자이너: 대시보드 UI/UX 설계
- 데이터 엔지니어: 데이터 파이프라인 구축
- 데브옵스/QA 엔지니어: 배포 및 품질 관리

---

## 📄 라이선스

Internal Use Only

---

## 📞 문의

프로젝트 관련 문의사항은 PROJECT_DIARY.md를 참고하거나,  
개발 팀에게 직접 연락 바랍니다.

---

**최종 업데이트**: 2025-10-19  
**버전**: Phase 1 - MVP 개발 진행 중 (20%)  
**백엔드 상태**: 완성 (100%) ✅  
**프론트엔드 상태**: 개발 중 (24%) 🚧
