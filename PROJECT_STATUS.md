# 🚀 WMS 대시보드 프로젝트 진행 상황

## 📅 최종 업데이트: 2025-10-17

---

## 📊 Phase 0: 사전 조사 및 환경 구축 (5일)

### ✅ 완료 항목 (Day 1-4)
- [x] 기존 5개 프로그램 데이터 구조 파악
- [x] 현장 인터뷰 완료
- [x] 정보 우선순위 매트릭스 작성
- [x] Git 저장소 생성
- [x] 확장 가능한 폴더 구조 설계
- [x] GitHub 폴더 구조 생성
- [x] 레퍼런스 문서 5개 업로드
- [x] 샘플 데이터 5종 확보 (입고/출고/재고/삭제/비정형)
- [x] 설정 파일 템플릿 작성 (config.example.yaml, data_sources.yaml)
- [x] requirements.txt 작성

### ⏳ 대기 중 (Day 5)
- [ ] POC 개발 (CSV 읽기 + 화면 표시)
- [ ] 기술 스택 최종 검증
- [ ] 데이터 수집 모듈 프로토타입

---

## 📦 주요 결정 사항

### 아키텍처
- **GitHub**: 개발 코드 + 문서 + 레퍼런스
- **운영환경**: C:\OSIS_AUTO\냉장현황판
- **확장성**: 플러그인 아키텍처 (BaseCollector + Registry)

### 기술 스택
- **개발 도구**: Streamlit (Python)
- **데이터 처리**: Pandas, NumPy
- **설정 관리**: YAML
- **데이터베이스**: SQLite (설정/이력)

### 데이터 소스 (확장 가능)
1. 입고정보 (inbound_status)
2. 출고정보 (outbound_status)
3. 재고정보 (inventory_status)
4. 삭제정보 (delete_status)
5. 비정형오더 (irregular_order)

---

## 🎯 Phase 0 완료 기준

```
✅ 5개 프로그램 데이터 구조 파악
✅ 샘플 데이터 5종 확보
✅ 현장 인터뷰 3명 이상 완료
✅ 정보 우선순위 매트릭스 작성
✅ 개발 환경 정상 작동 (Git + 폴더 구조)
⏳ POC 성공 (데이터 읽기 + 표시)
⏳ 기술 스택 합의 완료
```

**진행률**: 5/7 완료 (71%)

---

## 📅 작업 이력

**Day 4 완료 (2025-10-17):**
- ✅ PROJECT_STATUS.md 생성
- ✅ README.md 업데이트
- ✅ .gitignore 설정
- ✅ 폴더 구조 생성 (9개 폴더)
- ✅ 레퍼런스 문서 5개 작성
- ✅ 샘플 CSV 데이터 5종 생성
- ✅ 설정 템플릿 파일 작성

**Day 5 계획:**
1. POC 개발 (CSV → DataFrame → Streamlit 표시)
2. BaseCollector 추상 클래스 작성
3. InboundCollector 프로토타입
4. 기술 스택 검증

---

## 📁 GitHub 저장소 구조

```
WMS-DashBoard/
├── PROJECT_STATUS.md        ✅
├── README.md                ✅
├── .gitignore               ✅
├── dashboard/               ✅
│   ├── src/ (구조)         ✅
│   ├── config/ (템플릿)     ✅
│   ├── tests/fixtures/      ✅ (5개 CSV)
│   ├── requirements.txt     ✅
│   └── README.md            ✅
├── references/              ✅
│   └── modules/ (5개)       ✅
└── docs/                    ✅
```

---

## 📝 메모

### 폴더 구조 특징
- `references/`: 기존 5개 프로그램 문서 (학습용)
- `dashboard/`: 새로 개발할 현황판
- 확장 가능: 새 모듈 추가 시 Collector 클래스만 추가

### 주의사항
- 민감 정보 (login.txt, CSV 파일) .gitignore 처리
- 운영 환경과 GitHub 환경 분리
- 설정 파일은 .example 템플릿 제공

### 다음 마일스톤
- Day 5 완료 시 → Phase 0 완료 (100%)
- Phase 1 시작 → MVP 개발 (4대 지표)
