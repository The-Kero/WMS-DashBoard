# 🚀 WMS 대시보드 프로젝트 진행 상황

## 📅 최종 업데이트: 2025-11-19

---

## ⚠️ 【중요】프로젝트 상태 확인 필수 절차

**대화 시작 시 반드시 준수해야 할 규칙:**

```
1. PROJECT_DIARY.md는 항상 끝부분부터 읽기
   → read_file(offset=-100) 으로 최신 100줄 먼저 확인

2. 왜? 파일이 1783줄로 길어져서 최신 정보는 끝에 있음
   → 앞부분(1000줄)만 읽으면 오래된 정보를 현재로 착각

3. 확인할 것:
   - 최신 작업 날짜
   - Phase 진행률 (현재: 60%)
   - 완료된 Collector 개수 (현재: 3/5)
   - 다음 작업 내용

4. 의심스러우면 전체 파일 나눠 읽기:
   - read_file(offset=0, length=1000)
   - read_file(offset=1000, length=783)
```

**이 규칙을 지키지 않으면:**
- ❌ 이미 완료된 작업을 "다음 작업"이라고 착각
- ❌ 사용자에게 혼란과 불신 초래
- ❌ 프로젝트 진행에 차질

---

## 🏗️ 프로젝트 전체 구조

이 프로젝트는 **두 개의 독립적인 시스템**으로 구성되어 있습니다:

### 🔧 백엔드: 데이터 수집 시스템
**위치:** `C:\OSIS_AUTO\`

5개 핵심 모듈이 실제 운영 데이터를 자동 수집합니다.

### 🖥️ 프론트엔드: Streamlit 대시보드
**위치:** `C:\Projects\WMS-DashBoard\dashboard\`

백엔드에서 수집한 데이터를 시각화하는 웹 기반 현황판입니다.

---

## 📦 백엔드 시스템 상태 (C:\OSIS_AUTO\)

### 🔄 공통 기능 (모든 모듈 적용)

#### 1. 변화 감지 시스템 (SHA256)

**목적**: 불필요한 저장 방지, 성능 최적화

**작동 원리**:
1. 새 데이터의 SHA256 해시 계산
2. 기존 .hash 파일의 해시와 비교
3. 동일하면 저장 생략 (⏭️)
4. 변경되면 백업 후 저장 (💾)

**효과**:
- 디스크 I/O: 50~97% 감소
- 백업 파일: 80% 감소
- 처리 시간: 40~94% 단축

**적용 모듈**:
- ✅ 출고현황 v2.0
- ✅ 재고현황 v2.0

---

#### 2. 스마트 백업 시스템

**백업 트리거**:
- 데이터 변경 감지 시 자동 백업
- 같은 날 재실행 시에도 안전

**백업 파일 명명 규칙**:
```
원본: inventory_status_20251030.csv
백업: inventory_status_20251030_143052_backup.csv
      ^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^ ^^^^^^
      원본명                  시간   식별자
```

**백업 폴더 구조**:
```
C:\OSIS_AUTO\inventory_status\
├── inventory_status_20251030.csv    (현재)
└── backup/
    ├── inventory_status_20251030_100532.csv
    ├── inventory_status_20251030_140215.csv
    └── inventory_status_20251030_143052.csv
```

**적용 모듈**: 모든 모듈 (v2.0 이상)

---

#### 3. UTF-8 BOM 인코딩

**목적**: 엑셀에서 한글 정상 표시

**적용**: 모든 CSV 파일

---

#### 4. 자동 실행 스케줄

**지원**: 모든 모듈

**방법**: Windows 작업 스케줄러 연동

---

### 📈 성능 개선 요약

| 모듈 | 버전 | 주요 개선 | 개선율 | 시간 단축 |
|------|------|----------|--------|-----------|
| 입고현황 | v3.0 | 레코드 통합, Pandas 최적화 | 61% | 1.1초 → 0.7초 |
| 출고현황 | v2.0 | 통합 파일, 변화 감지 | 94% | 80초 → 4.6초 |
| 재고현황 | v2.0 | 변화 감지, 스마트 저장 | 50~70% | 디스크 I/O 감소 |
| 삭제현황 | v3.0 | 누적 방식 | - | 이력 추적 가능 |
| 비정형오더 | v2.0 | 누적 방식, 시각 보존 | - | 실시간 모니터링 |

**전체 효과**:
- ✅ 디스크 I/O: 평균 70% 감소
- ✅ 백업 파일 수: 80% 감소
- ✅ 실행 시간: 평균 60% 단축
- ✅ 데이터 정확도: 100% 보장

---

### ✅ 5개 핵심 모듈 완성 (100%)


#### 1. ✅ 입고현황 (v3.0)

**위치**: `C:\OSIS_AUTO\Inbound Status\`  
**파일명**: `inbound_merged_YYYYMMDD.csv`  
**완성일**: 2025-10-26

**v3.0 주요 기능**:
- ✅ 레코드 통합 기능 (8개 키 그룹화)
- ✅ 입고예정수량 정확 합산
- ✅ 진척률 0~100% 보장
- ✅ Pandas FutureWarning 해결
- ✅ 성능 61% 향상 (1.1초 → 0.7초)

**8개 그룹화 키**:
1. 입고예정번호
2. 상품
3. 소비기한
4. 로케이션
5. 입고센터
6. 공급사명
7. 입고유형
8. 최초입력시각

**수집 데이터**:
- 입고예정번호, 상품코드, 상품명
- 입고예정수량, 입고수량, 진척률
- 소비기한, 로케이션
- 입고센터, 공급사명, 입고유형

**통계 (최근 데이터)**:
- 총 레코드: 57건
- 총 입고예정수량: 5,398개
- 총 입고수량: 5,398개
- 진척률: 100.0%

**관련 문서**:
- WMS_입고현황_README.md
- WMS_입고현황_TECHNICAL_GUIDE.md
- WMS_입고현황_활용방안.md

---

#### 2. ✅ 출고현황 (v2.0)

**위치**: `C:\OSIS_AUTO\Outbound Status\`  
**파일명**: `outbound_all_YYYYMMDD.csv`  
**완성일**: 2025-10-29

**v2.0 주요 기능**:
- ✅ 10개 파일 → 1개 통합 파일
- ✅ 변화 감지 시스템 (SHA256)
- ✅ 출하금액 자동 계산
- ✅ 타입별 파일 자동 정리
- ✅ 성능 94% 향상 (80초 → 4.6초)

**10개 출고 타입**:

| 타입 | 명칭 | date_offset |
|------|------|-------------|
| 04 | 지방 캘리스코 출고 | +1 |
| 05 | 한익스, 키즈 출고 | +1 |
| 08 | 지방 삼각유부,델리치 50% | +1 |
| 14 | 자사 캘리스코 출고 | +1 |
| 15 | 자사 물품 출고 | +1 |
| 16 | 지방 (직접 발주) | 0 |
| 17 | 지방 (자동 발주) | +1 |
| 18 | 자사 삼각유부,델리치 50% | +1 |
| 52 | 지방 캘리스코 출고 | 0 |
| 53 | 지방 삼각유부,델리치 50% | 0 |

**수집 데이터**:
- 출하바코드, 상품, 상품명
- 오더수량, 출하금액 (자동 계산)
- 출고지, 출고유형
- 오더일시

**통계 (최근 데이터)**:
- 총 출하금액: 약 7,942만원
- 타입별 금액 범위: 7만원 ~ 6,483만원

**관련 문서**:
- WMS_출고현황_README.md
- WMS_출고현황_TECHNICAL_GUIDE.md
- WMS_출고현황_활용방안.md

---

#### 3. ✅ 재고현황 (v2.0)

**위치**: `C:\OSIS_AUTO\inventory_status\`  
**파일명**: `inventory_status_YYYYMMDD.csv`  
**완성일**: 2025-10-29

**v2.0 주요 기능**:
- ✅ 변화 감지 시스템 (SHA256)
- ✅ 스마트 저장 (변화 시에만)
- ✅ 유효유통비 자동 계산
- ✅ 백업 파일 80% 감소
- ✅ 디스크 I/O 50~70% 감소

**유효유통비 계산식**:
```
유효유통비 = (소비기한 - 오늘) / (소비기한 - 제조일) × 100
```

**수집 데이터**:
- 로케이션, 상품, 상품명
- 재고수량, 가용수량
- 유효유통비 (자동 계산)
- 소비기한, 제조일, 입고일
- 단가, 재고금액

**통계 (최근 데이터)**:
- 총 상품: 422개
- 총 재고수량: 200,847개
- 평균 유효유통비: 85%
- 위험 상품 (≤20%): 7개

**관련 문서**:
- WMS_재고현황_README.md
- WMS_재고현황_TECHNICAL_GUIDE.md
- WMS_재고현황_활용방안.md

---

#### 4. ✅ 삭제현황 (v3.0)

**위치**: `C:\OSIS_AUTO\Delete Status\`  
**파일명**: `delete_status_YYYYMMDD.csv`  
**완성일**: 2025-10-27

**v3.0 주요 기능**:
- ✅ 누적 데이터 관리 (당일 데이터 유지)
- ✅ 알림 시스템 통합 (Y/N)
- ✅ 18시 이후 자동 알림 설정
- ✅ 출하바코드 기준 중복 제거
- ✅ 알림 정보 보존 (N→Y 변경 시에도)

**누적 방식 특징**:
- 기존 데이터 + 신규 데이터 통합
- 출하바코드 기준 중복 제거
- 최초입력시각 자동 추적
- 알림여부 보존

**수집 데이터**:
- 삭제일시, 출하바코드
- 상품, 상품명, 삭제수량
- 삭제센터, 삭제사유
- 알림여부, 알림시각 (18시 이후)

**알림 로직**:
- 18시 이전: 알림여부 = '' (일반)
- 18시 이후: 알림여부 = 'Y' (긴급)

**관련 문서**:
- WMS_삭제현황_README.md
- WMS_삭제현황_TECHNICAL_GUIDE.md
- WMS_삭제현황_활용방안.md

---

#### 5. ✅ 비정형오더 (v2.0)

**위치**: `C:\OSIS_AUTO\IrregularOrder Status\`  
**파일명**: `irregular_order_YYYYMMDD.csv`  
**완성일**: 2025-10-27

**v2.0 주요 기능**:
- ✅ 실시간 모니터링 (1분 주기)
- ✅ 라벨출력 추적
- ✅ 즉시 알림 시스템
- ✅ 변화 감지 시스템
- ✅ 상세내용 기준 중복 제거

**누적 방식 특징**:
- 상세내용(상품코드+수량) 기준 중복 제거
- 최초입력시각 보존 (N→Y 변경 시에도)
- 라벨 N/Y 건수 실시간 표시

**수집 데이터**:
- 상세내용 (상품 정보)
- 출고센터명, 입고센터명
- 상품명, 입출수량
- 라벨출력 (N/Y)
- 최초입력시각

**알림 로직**:
- 라벨출력 = 'N': 🚨 즉시 알림
- 라벨출력 = 'Y': ✅ 정상

**관련 문서**:
- WMS_비정형오더_README.md
- WMS_비정형오더_TECHNICAL_GUIDE.md
- WMS_비정형오더_활용방안.md

---


## 📊 현재 정확한 진행 상황 (2025-11-05 기준)

### Phase 0: ✅ 100% 완료
### Phase 1: ✅ 100% 완료 (2025-11-04 완료)

**완료된 Collector (5/5):**
- ✅ InboundCollector (입고)
- ✅ OutboundCollector (출고)
- ✅ InventoryCollector (재고)
- ✅ DeleteCollector (삭제) ← 2025-10-30 완성
- ✅ IrregularCollector (비정형) ← 2025-10-30 완성

**완료된 대시보드 탭 (5/5):**
- ✅ 입고 현황 탭
- ✅ 출고 현황 탭
- ✅ 재고 현황 탭
- ✅ 삭제 현황 탭
- ✅ 비정형 오더 탭

**완료된 테스트:**
- ✅ 기본 테스트 40개 (100% 통과)
  * test_inbound.py (8개)
  * test_outbound.py (8개)
  * test_inventory.py (8개)
  * test_delete.py (8개)
  * test_irregular.py (8개)

- ✅ Edge Case 테스트 20개 (100% 통과)
  * 파일 관련 (4개)
  * 데이터 품질 (4개)
  * 에러 처리 (4개)
  * 성능 (4개)
  * 통합 (4개)

- ✅ 총 60개 테스트 완료
- ✅ 테스트 커버리지 80%+

**Phase 1 완료 시각:** 2025-11-04 10:30

**다음 단계:**
- Phase 2: TV 모니터 시스템 구축 (8일 예정)
- Phase 3: 알림 10개 개발 (10일 예정)

---

## 📊 Phase 0: 사전 조사 및 환경 구축 ✅ 완료

### ✅ 완료 항목 (Day 1-5)
- [x] 기존 5개 프로그램 데이터 구조 파악
- [x] 현장 인터뷰 완료
- [x] 정보 우선순위 매트릭스 작성
- [x] Git 저장소 생성
- [x] 확장 가능한 폴더 구조 설계
- [x] GitHub 폴더 구조 생성
- [x] 레퍼런스 문서 5개 업로드
- [x] 샘플 데이터 5종 확보 (입고/출고/재고/삭제/비정형)
- [x] 설정 파일 템플릿 작성
- [x] requirements.txt 작성
- [x] **POC 개발 완료** (CSV → DataFrame → Streamlit)
- [x] **BaseCollector 추상 클래스 작성**
- [x] **InboundCollector 프로토타입 구현**
- [x] **UI 컴포넌트 개발**
- [x] **메인 앱 작성 (app.py)**

**진행률**: 100% ✅

---

## 📊 Phase 1: MVP 개발 ✅ 완료

**전체 기간:** 19일 (2025-10-17 ~ 2025-11-04)  
**완료 날짜:** 2025-11-04 10:30  
**진행률:** 100% ✅

### ✅ Day 6 완료 (2025-10-17)

**OutboundCollector 기본 구조 개발**
- [x] outbound.py 파일 생성 (185 lines)
- [x] 필수 컬럼 7개 정의
- [x] load_data() 구현
- [x] validate() 구현
- [x] get_summary() 구현
- [x] get_top_destinations() 구현
- [x] get_top_products() 구현
- [x] get_by_type() 구현 (출고유형별 집계)
- [x] 기본 단위 테스트 작성 및 통과

---

### ✅ Day 7 완료 (2025-10-17~18)

**OutboundCollector UI 통합**
- [x] OutboundCollector UI 컴포넌트 4개 추가
- [x] display_outbound_metrics() 구현
- [x] display_outbound_summary_cards() 구현
- [x] display_top_destinations() 구현
- [x] display_top_outbound_products() 구현
- [x] app.py에 출고 탭 통합
- [x] 2개 탭 시스템 완성 (입고/출고)
- [x] 통합 테스트 통과

**결과:**
- Streamlit 대시보드에서 입고/출고 데이터를 2개 탭으로 완벽하게 시각화
- 샘플 데이터 기반으로 모든 기능 정상 작동 확인

---

### ✅ Day 8-9 완료 (2025-10-20)

**InventoryCollector 개발 및 재고 대시보드 통합**

**Collector 개발:**
- [x] inventory.py 파일 생성 (203 lines)
- [x] 필수 컬럼 5개 정의 (상품, 상품명, 가용수량, 유효유통비(%), 단가)
- [x] load_data() 구현 (UTF-8 BOM 지원)
- [x] validate() 구현
- [x] get_summary() 구현 (6개 지표)
- [x] get_risky_products() 구현 (유효비 ≤20%)
- [x] get_low_stock_products() 구현 (가용수량 부족)
- [x] get_top_value_products() 구현 (재고금액 TOP N)
- [x] calculate_total_value() 구현 (총 재고금액)

**UI 컴포넌트 개발 (5개):**
- [x] display_inventory_metrics() - 4대 지표 카드
- [x] display_inventory_summary() - 평균 유효비 + 구간별 분포
- [x] display_risky_products_table() - 위험 상품 테이블
- [x] display_inventory_table() - 전체 재고 목록
- [x] display_low_stock_table() - 가용수량 부족 상품

**대시보드 통합:**
- [x] app.py에 재고 탭 추가 (3번째 탭)
- [x] 절대 경로 수정으로 파일 로딩 문제 해결
- [x] 샘플 데이터 테스트 통과 (17개 상품)
- [x] 실제 데이터 테스트 통과 (917개 상품)
- [x] 3개 탭 모두 정상 작동 확인

**결과:**
- Phase 1 진행률: 40% → 60%
- Collector: 3/5 완성 ✅
- 대시보드 탭: 3/5 완성 ✅

---

### ✅ Day 10-13 완료 (2025-10-28 ~ 2025-10-30)

**DeleteCollector 개발**
- [x] delete.py 파일 생성
- [x] 삭제 오더 데이터 수집
- [x] 18시 이후 알림 로직
- [x] CSV 파일 생성
- [x] 테스트 8개 작성

**IrregularCollector 개발**
- [x] irregular.py 파일 생성
- [x] 비정형 오더 데이터 수집
- [x] 라벨출력 정보 처리
- [x] CSV 파일 생성
- [x] 테스트 8개 작성

---

### ✅ Day 14-16 완료 (2025-10-31 ~ 2025-11-02)

**삭제 탭 UI 개발**
- [x] Streamlit 탭 구현
- [x] 18시 이후 삭제 필터링
- [x] 삭제 사유별 차트
- [x] 삭제 상품 테이블

**비정형 탭 UI 개발**
- [x] Streamlit 탭 구현
- [x] 라벨출력='N' 필터링
- [x] 출고지시방법별 차트
- [x] 비정형 오더 테이블

---

### ✅ Day 17-20 완료 (2025-11-03 ~ 2025-11-04)

**Edge Case 테스트 개발**
- [x] test_edge_cases.py 작성 (20개)
- [x] 파일 관련 테스트 (4개)
- [x] 데이터 품질 테스트 (6개)
- [x] 경계값 테스트 (5개)
- [x] 비즈니스 로직 테스트 (5개)
- [x] 100% 통과 확인

**샘플 데이터 생성**
- [x] edge_cases/ 폴더 생성
- [x] 8개 CSV 샘플 파일
- [x] 다양한 시나리오 커버

**Phase 1 완료 선언**
- [x] 2025-11-04 10:30 완료
- [x] Git 커밋 2개 완료
- [x] 문서 업데이트 준비

---

### 🎊 Phase 1 완료 선언

**상태:** ✅ **Phase 1 MVP 개발 100% 완료**

**완료 시간:** 2025-10-17 ~ 2025-11-04 (19일)

**주요 산출물:**

1. **백엔드 5개 모듈 (100%)**
   - inbound_status.py (v3.0)
   - collect_outbound_status.py (v3.0)
   - inventory_status.py (v3.0)
   - delete_status.py (v1.0)
   - irregular_order_status.py (v1.0)

2. **프론트엔드 5개 Collector (100%)**
   - InboundCollector
   - OutboundCollector
   - InventoryCollector
   - DeleteCollector
   - IrregularCollector

3. **테스트 60개 (100% 통과)**
   - 기본 테스트 40개
   - Edge Case 테스트 20개
   - 테스트 커버리지 80%+

4. **문서 및 인프라**
   - README 작성
   - 기술 문서 작성
   - Git 버전 관리
   - 샘플 데이터 13개 (기본 5 + edge 8)

**프로덕션 준비도:** 85%

---

### 🚧 Day 10-11 예정 (다음 작업)

**DeleteCollector 개발 및 삭제 대시보드 통합**

**예상 작업:**
1. delete.py 개발
   - 필수 컬럼 정의
   - load_data() 구현
   - validate() 구현
   - get_summary() 구현
   - 삭제 사유별 집계
   - 삭제 금액 계산

2. UI 컴포넌트 개발
   - 삭제 지표 카드
   - 삭제 사유별 차트
   - 삭제 상품 테이블

3. 대시보드 통합
   - app.py에 삭제 탭 추가 (4번째 탭)
   - 샘플 데이터 테스트
   - 실제 데이터 테스트

**예상 소요 시간:** 4-6시간

---

### 🚧 Day 12-13 예정

**IrregularCollector 개발 및 비정형 오더 대시보드 통합**

**예상 작업:**
1. irregular.py 개발
2. UI 컴포넌트 개발
3. 대시보드 통합 (5번째 탭)

**예상 소요 시간:** 4-6시간

---

### 🚧 Day 14-15 예정

**실제 데이터 연동 및 통합 테스트**

**예상 작업:**
1. 백엔드(C:\OSIS_AUTO\)와 프론트엔드 연동
2. 실제 데이터 경로 설정
3. 5개 탭 모두 실제 데이터로 테스트
4. 성능 최적화
5. 오류 처리 강화
6. 최종 문서 업데이트

**예상 소요 시간:** 6-8시간

---

## 📈 Phase 1 완료 기준

- [x] InboundCollector 완성 ✅
- [x] OutboundCollector 완성 ✅
- [x] InventoryCollector 완성 ✅
- [x] DeleteCollector 완성 ✅
- [x] IrregularCollector 완성 ✅
- [x] 입고 탭 UI 완성 ✅
- [x] 출고 탭 UI 완성 ✅
- [x] 재고 탭 UI 완성 ✅
- [x] 삭제 탭 UI 완성 ✅
- [x] 비정형 탭 UI 완성 ✅
- [x] 60개 테스트 100% 통과 ✅
- [x] 샘플 데이터 13개 생성 ✅
- [x] Git 커밋 완료 ✅

**완료율:** 100% (13/13 체크박스) ✅

---

## 🚀 Phase 2: Flask TV 시스템 (진행중)

**전체 기간:** 8일 (2025-11-16 ~ 2025-11-23)  
**현재 진척률:** Day 3/8 완료 (61.8%)  
**완료 날짜:** 진행중

---

### ✅ Day 1 완료 (2025-11-16)

**Flask 기본 구조 + Collector 모듈**

#### 1.1 가상환경 생성
- [x] 터미널 열기 및 디렉토리 이동
- [x] `python -m venv venv_flask` 실행
- [x] 가상환경 활성화
- [x] Python 버전 확인 (3.9+)

#### 1.2 패키지 설치
- [x] Flask==3.0.0 설치
- [x] Flask-CORS==4.0.0 설치
- [x] Flask-Caching==2.1.0 설치
- [x] pandas==2.0.3 설치
- [x] python-dotenv==1.0.0 설치
- [x] requirements.txt 생성

#### 1.3 프로젝트 구조 생성
- [x] api/ 폴더 생성
- [x] services/ 폴더 생성
- [x] templates/ 폴더 생성
- [x] static/ 폴더 생성 (css, js, images)
- [x] logs/ 폴더 생성
- [x] tests/ 폴더 생성

#### 1.4 app.py 기본 구조
- [x] Flask, CORS, Cache, logging 설정
- [x] / 루트 엔드포인트
- [x] /api/health 헬스체크
- [x] 404, 500 에러 핸들러
- [x] 서버 실행 확인

#### 1.5 Collector 모듈 작성 (신규)
- [x] BaseCollector 클래스 작성 (74줄)
- [x] InboundCollector 작성 (54줄)
- [x] OutboundCollector 작성 (56줄)
- [x] InventoryCollector 작성 (91줄)
- [x] DeleteCollector 작성 (58줄)
- [x] IrregularCollector 작성 (33줄)

#### 1.6 5개 API 엔드포인트
- [x] api/inbound.py 작성 (73줄)
- [x] api/outbound.py 작성 (55줄)
- [x] api/inventory.py 작성 (55줄)
- [x] api/delete.py 작성 (55줄)
- [x] api/irregular.py 작성 (55줄)

#### 1.7 Flask 서버 테스트
- [x] 서버 정상 실행 (포트 5000)
- [x] /api/health 200 OK
- [x] 5개 API 모두 동작 확인
- [x] CORS 헤더 확인
- [x] 로그 파일 생성 확인

**완료 시간**: 2025-11-16  
**실제 소요**: 2.0시간 (예상 10시간 대비 80% 단축)

---

### ✅ Day 2 완료 (2025-11-19)

**통합 API + v9 규칙 적용**

#### 2.1 api/dashboard.py 기본 구조
- [x] dashboard.py 생성
- [x] Blueprint 설정
- [x] CollectorService import
- [x] /api/dashboard 엔드포인트 정의

#### 2.2 5개 Collector 데이터 수집
- [x] 입고 데이터 수집
- [x] 출고 데이터 수집
- [x] 재고 데이터 수집
- [x] 삭제 데이터 수집 (현재 미사용)
- [x] 비정형 오더 데이터 수집
- [x] DataFrame 수집 완료 확인

#### 2.3 카드2 계산 - 입고유의상품
- [x] 총 건수 계산
- [x] 평균 진척률 계산
- [x] 입고 소비기한 집계
- [x] 재고 소비기한 집계
- [x] 데이터 병합
- [x] 입고유의상품 필터링 (입고 < 재고)

#### 2.4 카드3 계산 - L07 제외 + 영문키
- [x] 유효유통비 ≤20% 필터링
- [x] L07 로케이션 제외
- [x] 긴급/주의 구분 (10% 기준)
- [x] 유효비 오름차순 정렬
- [x] JSON 변환 (영문 키)

#### 2.5 카드5 계산 - 자사출고 + 라벨 + 비정형
- [x] 자사 출고 타입 필터링 (14, 15, 18)
- [x] 총 출하금액 계산
- [x] 라벨 건수 (총/미발행)
- [x] 비정형 오더 (총/미출력)
- [x] 전일 대비 계산 (D-1~D-10 탐색)

#### 2.6 카드6 계산 - 배송처 분류 + destinations
- [x] classify_destination_card6() 함수 정의
- [x] 05 타입 특수 규칙
- [x] 08 타입 규칙
- [x] 기타 타입 (04, 16, 17, 52, 53) 규칙
- [x] 지방 출고 타입 필터링
- [x] 배송처 분류 적용
- [x] 13개 배송처 집계

#### 2.7 JSON 응답 구조 작성
- [x] response 기본 구조
- [x] card2 데이터 (totalCount, progressRate, riskyCount)
- [x] card3 데이터 (totalCount, urgentCount, warningCount, items)
- [x] card5 데이터 (totalAmount, comparePercent, labels, irregular)
- [x] card6 데이터 (totalCount, totalAmount, destinations)
- [x] timestamp, data_counts 포함

#### 2.8 고급 에러 처리
- [x] FileNotFoundError 처리
- [x] ValueError 처리
- [x] KeyError 처리
- [x] Exception 통합 처리

#### 2.9 통합 테스트
- [x] Flask 서버 실행
- [x] /api/dashboard 호출
- [x] HTTP 200 OK 확인
- [x] JSON 구조 확인
- [x] 카드2~6 데이터 정확성 검증
- [x] 카드6 미발행 피킹리스트 확인
- [x] 서버 중지

#### 2.10 리팩토링 (Service 제거)
- [x] CollectorService 삭제
- [x] Collector 직접 호출로 변경
- [x] 코드 간소화
- [x] yesterday → today 수정

#### 2.11 Git 커밋
- [x] git add . 실행
- [x] git commit 실행
- [x] 커밋 성공 확인

**완료 시간**: 2025-11-19 22:12  
**실제 소요**: 4.0시간 (예상 12시간 대비 67% 단축)  
**커밋 해시**: 03dc291

---

### ✅ Day 3 완료 (2025-11-20)

**pytest 테스트 작성**

**목표**: Flask API 전체 테스트 커버리지 확보  
**완료 시간**: 2025-11-20 15:15  
**실제 소요**: 1.3시간 (예상 4-5시간 대비 74% 단축)  
**테스트 결과**: pytest 37개 PASSED  
**완료율**: 100% (44/44개 완료)

**완료 작업:**
- [x] pytest 환경 구축
- [x] BaseCollector 테스트 (8개)
- [x] 5개 Collector 단위 테스트 (29개)
- [x] 6개 API 엔드포인트 테스트 (30개)
- [x] 통합 테스트 시나리오 (5개)
- [x] 테스트 커버리지 80% 이상
- [x] Git 커밋

---

### 📊 Phase 2 진행 요약

| Day | 날짜 | 주요 작업 | 체크박스 | 완료 | 진척률 | 상태 | 소요시간 |
|-----|------|----------|----------|------|--------|------|----------|
| Day 1 | 2025-11-16 | Flask 환경 + Collector + API | 120개 | 120 | 100% | ✅ 완료 | 2.0시간 |
| Day 2 | 2025-11-19 | 통합 API + v9 규칙 적용 | 165개 | 165 | 100% | ✅ 완료 | 4.0시간 |
| Day 3 | 2025-11-20 | pytest 테스트 | 44개 | 44 | 100% | ✅ 완료 | 1.3시간 |
| Day 4 | 2025-11-20 | HTML 템플릿 | 45개 | 0 | 0% | ⏳ 대기 | - |
| Day 5 | 2025-11-21 | JavaScript 30초 갱신 | 50개 | 0 | 0% | ⏳ 대기 | - |
| Day 6 | 2025-11-22 | CSS TV 최적화 | 37개 | 0 | 0% | ⏳ 대기 | - |
| Day 7 | 2025-11-23 | 성능 + 안정성 | 40개 | 0 | 0% | ⏳ 대기 | - |
| Day 8 | 2025-11-24 | 배포 + 검증 | 35개 | 0 | 0% | ⏳ 대기 | - |
| **합계** | **8일** | **Flask TV 시스템** | **532개** | **329** | **61.8%** | 🔄 | **7.3시간** |

---

### ✅ Phase 2 완료 기준

**필수 완료 항목:**
- [x] Flask 서버 정상 실행 ✅
- [x] 5개 Collector 모듈 작성 ✅
- [x] 6개 API 엔드포인트 구현 ✅
- [x] /api/dashboard 통합 API ✅
- [x] v9 데이터 규칙 100% 적용 ✅
- [ ] pytest 테스트 커버리지 80% 이상
- [ ] HTML 템플릿 완성
- [ ] JavaScript 30초 자동 갱신
- [ ] CSS TV 최적화 (1920×1080)
- [ ] 100인치 TV 현장 테스트
- [ ] Windows 서비스 등록
- [ ] 24/7 운영 준비

**현재 완료율**: 35% (5/14개 필수 항목)

---

## ⏳ Phase 3: 알림 10개 개발 (예정)

**기간:** 10일 예상 (Phase 2 완료 후)  
**목표:** 10개 알림 규칙 정확 구현, 우선순위별 시각화

### 알림 10개 개요
- 긴급 알림 3개 (빨강 🔴)
- 중요 알림 4개 (주황 🟠)
- 일반 알림 3개 (파랑 🔵)

**상세 계획:** 04_전체개발계획서.md의 Phase 3 섹션 참조

---

## 📁 프로젝트 구조

```
C:\Projects\WMS-DashBoard\
│
├── flask_app/                      # 🆕 Flask API 서버 (Phase 2)
│   ├── app.py                     # Flask 메인 (102줄)
│   ├── requirements.txt           # 패키지 의존성
│   ├── venv_flask/                # 가상환경
│   │
│   ├── api/                       # API 엔드포인트
│   │   ├── __init__.py
│   │   ├── inbound.py             # 입고 API (73줄)
│   │   ├── outbound.py            # 출고 API (55줄)
│   │   ├── inventory.py           # 재고 API (55줄)
│   │   ├── delete.py              # 삭제 API (55줄)
│   │   ├── irregular.py           # 비정형 API (55줄)
│   │   └── dashboard.py           # 통합 API (v9 규칙 적용)
│   │
│   ├── templates/                 # HTML 템플릿 (Day 4 예정)
│   ├── static/                    # CSS/JS (Day 5-6 예정)
│   │   ├── css/
│   │   └── js/
│   │
│   ├── logs/                      # 로그 파일
│   │   └── app.log
│   │
│   └── tests/                     # pytest 테스트 (Day 3 예정)
│       ├── conftest.py
│       ├── unit/
│       └── integration/
│
├── dashboard/                      # Streamlit 대시보드 (Phase 1)
│   ├── app.py                     # 메인 앱 (5개 탭 완성)
│   ├── requirements.txt           # 패키지 의존성
│   ├── README.md                  # 프로젝트 설명
│   │
│   ├── config/                    # 설정 파일
│   │   ├── config.example.yaml   # 설정 예시
│   │   └── data_sources.yaml     # 데이터 소스 설정
│   │
│   ├── src/                       # 소스 코드
│   │   ├── data/                  # 데이터 계층
│   │   │   └── collectors/        # 데이터 수집기
│   │   │       ├── base.py        # 추상 베이스 클래스
│   │   │       ├── inbound.py     # 입고 수집기 ✅
│   │   │       ├── outbound.py    # 출고 수집기 ✅
│   │   │       ├── inventory.py   # 재고 수집기 ✅
│   │   │       ├── delete.py      # 삭제 수집기 ✅
│   │   │       └── irregular.py   # 비정형 수집기 ✅
│   │   │
│   │   ├── business/              # 비즈니스 로직
│   │   │   └── analytics.py       # 분석 로직
│   │   │
│   │   ├── ui/                    # UI 계층
│   │   │   └── components.py      # Streamlit 컴포넌트
│   │   │
│   │   └── utils/                 # 유틸리티
│   │       ├── file_utils.py      # 파일 처리
│   │       └── date_utils.py      # 날짜 처리
│   │
│   └── tests/                     # 테스트
│       ├── fixtures/              # 테스트 데이터
│       │   ├── sample_inbound.csv
│       │   ├── sample_outbound.csv
│       │   ├── sample_inventory.csv
│       │   ├── sample_delete.csv
│       │   └── sample_irregular.csv
│       └── test_*.py              # 단위 테스트
│
├── docs/                          # 문서
│   ├── official/                  # 공식 프로젝트 문서
│   │   ├── README.md             # 문서 가이드
│   │   ├── PROJECT_STATUS.md     # 프로젝트 진행 상황
│   │   ├── 01_프로젝트_간단설명서.md
│   │   ├── 02_기술설명서.md
│   │   ├── 03_시스템_흐름도.md
│   │   └── 04_전체개발계획서.md
│   ├── dev/                       # 개발 가이드
│   │   ├── PROJECT_CHECK_GUIDE.md
│   │   └── V3_개발_현황.md
│   ├── backup/                    # 백업
│   └── updates/                   # 업데이트 기록
│
├── scripts/                       # 스크립트
│   └── setup.py                   # 초기 설정 스크립트
│
├── PROJECT_STATUS.md              # 프로젝트 진행 상황 (루트)
├── PROJECT_DIARY.md               # 작업 일지
└── README.md                      # 프로젝트 개요
```

---

## 🔗 관련 저장소

- **GitHub:** https://github.com/The-Kero/WMS-DashBoard.git
- **로컬:** C:\Projects\WMS-DashBoard\

---

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 통해 남겨주세요.

---

## 📅 문서 이력

| 버전 | 날짜 | 주요 변경 | 담당자 |
|------|------|-----------|--------|
| v1.0 | 2025-10-17 | 초안 작성 | 개발팀 |
| v2.0 | 2025-10-20 | Phase 1 진행 상황 (60%) | 개발팀 |
| v3.0 | 2025-10-30 | 백엔드 v2.0~v3.0 완성 반영 | 개발팀 |
| v4.0 | 2025-11-05 | Phase 1 완료 (100%) 반영 | 개발팀 |
| **v5.0** | **2025-11-19** | **• Phase 2 Day 1-2 완료 반영 (53.6%)**<br>**• Flask 환경 구축 완료**<br>**• BaseCollector 패턴 확립**<br>**• /api/dashboard 통합 API 완성**<br>**• v9 데이터 규칙 100% 적용**<br>**• Service 제거 리팩토링 완료** | **개발팀** |

---

**마지막 업데이트**: 2025-11-19  
**다음 업데이트**: Phase 2 Day 3 완료 시 (2025-11-20 예정)  
**작성자**: WMS 개발팀
