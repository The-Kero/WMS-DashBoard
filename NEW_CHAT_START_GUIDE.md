# 🚀 새 대화에서 프로젝트 이어하기 가이드

## 📋 새 대화 시작 시 명령어

새로운 Claude 대화에서 이 프로젝트를 계속 진행하려면, 아래 명령어를 **첫 메시지로** 보내주세요:

```
질문에 답할 때, 당신은 4명의 가상 전문가로 구성된 팀을 만들어 주세요:

1. 풀스택 개발자
창고관리 시스템(WMS)의 핵심 로직과 데이터베이스를 구축하고, 프론트엔드와 백엔드를 모두 담당하며 전체 시스템을 유기적으로 연결합니다. 자동화 장비 및 외부 시스템과의 연동을 담당하는 기술적 핵심 인력입니다.

2. UX/UI 디자이너
창고 작업자와 관리자의 관점에서 직관적이고 효율적인 사용자 경험을 설계합니다. 특히 현황판의 데이터를 명확하게 시각화하고, 작업자들이 편리하게 사용할 수 있는 인터페이스를 디자인합니다.

3. 데이터 엔지니어
물류 데이터를 효율적으로 수집, 처리, 저장하고 관리하는 데이터 파이프 라인을 구축합니다. 물류 데이터의 정확성과 신뢰성을 확보하며, AI 기술을 활용한 재고 예측 및 최적화 기능을 개발합니다.

4. 데브옵스/QA 엔지니어
개발된 프로그램을 배포하고 안정적으로 운영될 수 있도록 시스템을 관리합니다. 물류 현장의 다양한 시나리오에 대한 테스트를 진행하여 프로그램의 오류를 찾아내고, 전체적인 품질과 안정성을 확보합니다.

각 전문가가 내 질문을 자신의 관점에서 분석하고, 서로의 의견을 검토한 다음, 최종적으로 모든 의견을 종합한 답변을 단계적으로 해서 제공해 주세요.

답변을 할 때 프로그램이나 코드를 만들어야 한다면 꼭 다시 실행 여부를 물어봐 주세요.

프로그램 개발 진행 상태를 작업이 끝날 때 마다 파일에 기록해 주세요. 기록에 4명의 팀원이 대화한 내용이 들어갈 필요는 없습니다. 종합 의견이나 어떤 작업을 했는지 아주 간략하게 기록해주고 기록 시간을 시스템 시간으로 분까지 꼭 넣어주세요. 저 혼자 볼 것이기 때문에 쉽고 친근하게 기록해 주세요. 기록 위치는 C:\Projects\WMS-DashBoard\PROJECT_DIARY.md 입니다

대화는 openmemory MCP 활용해서 기억해 주세요.

프로젝트 진행 상황과 내가 어디서부터 시작하면 좋을지 C:\OSIS_AUTO, C:\Projects\WMS-DashBoard, 깃허브, 메모리를 자세히 참고해서 말해줘
```

---

## 📂 주요 참고 파일

Claude가 자동으로 다음 파일들을 확인하여 프로젝트 상황을 파악합니다:

### 1. 프로젝트 현황
- `C:\Projects\WMS-DashBoard\PROJECT_DIARY.md` - 일별 작업 일지 (가장 중요!)
- `C:\Projects\WMS-DashBoard\PROJECT_STATUS.md` - 전체 진행 상황
- `C:\Projects\WMS-DashBoard\PHASE1_DAY9_REPORT.md` - 최신 완료 보고서
- `C:\Projects\WMS-DashBoard\README.md` - 프로젝트 개요

### 2. 백엔드 시스템
- `C:\OSIS_AUTO\` - 5개 데이터 수집 모듈 (완성)
  - Inbound Status
  - Outbound Status
  - inventory_status
  - Delete Status
  - IrregularOrder Status

### 3. 프론트엔드 시스템
- `C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\` - Collector 클래스들
- `C:\Projects\WMS-DashBoard\dashboard\app.py` - 메인 앱
- `C:\Projects\WMS-DashBoard\dashboard\src\ui\components.py` - UI 컴포넌트

### 4. GitHub
- 저장소: https://github.com/The-Kero/WMS-DashBoard
- 최신 커밋: 7db45c2 (2025-10-20 17:35)
- 브랜치: main

### 5. OpenMemory
- Claude가 자동으로 이전 대화 내용 검색
- Phase 1 Day 9 완료 상황 저장됨
- 다음 작업: DeleteCollector 개발

---

## 🎯 현재 진행 상황 (2025-10-20 17:35 기준)

### ✅ 완료된 작업
- Phase 0: 100% 완료 ✅
- Phase 1: 60% 완료 (Day 9/15)
  - ✅ BaseCollector (추상 클래스)
  - ✅ InboundCollector (입고 대시보드)
  - ✅ OutboundCollector (출고 대시보드)
  - ✅ InventoryCollector (재고 대시보드) - **2025-10-20 완성**

### ⏳ 다음 작업
- **DeleteCollector 개발 (Day 10-11)**
  - 예상 소요 시간: 2-3시간
  - 백엔드 데이터: C:\OSIS_AUTO\Delete Status\delete_status_YYYYMMDD.csv
  - 13개 컬럼 (삭제처리일, 상품, 주문수량, 배송처, 출하바코드 등)

### 🚀 작업 시작 명령어
다음 작업을 시작할 준비가 되면:
```
준비됐어. 1,2,3,4 차례대로 차근차근 준비해줘
```

---

## 💡 자주 사용하는 명령어

### 진행 상황 확인
```
현재 프로젝트 진행 상황 알려줘
```

### 다음 작업 시작
```
준비됐어. 1,2,3,4 차례대로 차근차근 준비해줘
```

### GitHub 업데이트
```
다른 대화에서 이어서 할수 있게 C:\OSIS_AUTO, C:\Projects, 메모리, 깃허브 업데이트 해줘
```

### 백엔드 데이터 수집
```
백엔드 5개 모듈 실행해서 최신 데이터 수집해줘
```

### 테스트 실행
```
[Collector명] 테스트 실행해줘
```

---

## 📝 작업 패턴

Claude는 항상 **4단계 프로세스**로 작업합니다:

### 1단계: 파일 생성
- Collector 클래스 개발 (200-300줄)
- 백엔드 데이터 구조 반영

### 2단계: 백엔드 테스트
- 실제 데이터로 테스트
- 모든 메서드 검증

### 3단계: UI 컴포넌트
- components.py에 UI 함수 추가
- 차트, 테이블, 카드 구현

### 4단계: app.py 통합
- render_XXX_tab() 함수 추가
- 탭 시스템에 통합
- Streamlit 앱 실행 확인

---

## 🔄 작업 완료 후

매 작업 완료 시 Claude가 자동으로:
1. PROJECT_DIARY.md 업데이트
2. GitHub 커밋 및 푸시
3. OpenMemory 업데이트
4. 다음 작업 안내

---

## ⚠️ 주의사항

1. **절대 경로 사용**
   - 모든 파일 경로는 절대 경로 사용
   - 예: `C:\Projects\WMS-DashBoard\dashboard\app.py`

2. **백엔드 데이터 구조 확인**
   - 각 Collector 개발 전 백엔드 CSV 구조 확인 필수
   - 컬럼명과 데이터 타입 정확히 반영

3. **가상환경 활성화**
   - Streamlit 실행 시 가상환경 필요
   - 경로: `C:\Projects\WMS-DashBoard\dashboard\venv\`

4. **인코딩**
   - 백엔드 CSV: `utf-8-sig` (BOM 처리)
   - Python 파일: `# -*- coding: utf-8 -*-`

---

## 📊 프로젝트 구조 요약

```
WMS 대시보드 프로젝트
├── 백엔드 (C:\OSIS_AUTO\) - 100% 완성 ✅
│   ├── 5개 데이터 수집 모듈
│   └── 하루 단위 CSV + 자동 백업
│
└── 프론트엔드 (C:\Projects\WMS-DashBoard\) - 60% 완성 🚧
    ├── 3/5 Collector 완성 ✅
    ├── 3/5 탭 완성 ✅
    └── DeleteCollector 개발 예정 ⏳
```

---

**작성일**: 2025-10-20  
**최종 업데이트**: Phase 1 Day 9 완료  
**다음 작업**: DeleteCollector 개발 (Day 10-11)
