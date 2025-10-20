# Collector 수정 계획서

## 작성 일시: 2025-10-20
## 목적: 백엔드 데이터 변경사항을 프론트엔드 Collector에 반영

---

## 📊 전체 현황

| Collector | 현재 상태 | 수정 필요 | 우선순위 |
|-----------|----------|----------|---------|
| InboundCollector | ✅ 정상 | ❌ 없음 | N/A |
| OutboundCollector | ❌ 작동불가 | ✅ 긴급 | 🔴 HIGH |
| InventoryCollector | ⚠️ 미개발 | ✅ 필요 | 🟡 MEDIUM |
| DeleteCollector | ⚠️ 미개발 | ✅ 필요 | 🟡 MEDIUM |
| IrregularCollector | ⚠️ 미개발 | ✅ 필요 | 🟡 MEDIUM |

---

## 1. InboundCollector ✅

### 현재 상태
```python
REQUIRED_COLUMNS = [
    '입고예정번호', '공급사', '공급사명', '입고유형',
    '입고예정일', '로케이션', '상품', '상품명',
    '단위및규격', '소비기한', '입고수량'
]
```

### 백엔드 컬럼 (11개)
```
입고예정번호, 공급사, 공급사명, 입고유형, 입고예정일, 
로케이션, 상품, 상품명, 단위및규격, 소비기한, 입고수량
```

### 결론
✅ **수정 불필요** - 모든 컬럼 완벽히 일치

---

## 2. OutboundCollector 🔴

### 현재 상태 (작동 불가)
```python
REQUIRED_COLUMNS = [
    '출고번호',    # ❌ 백엔드에 없음
    '출고일자',    # ✅ 존재
    '상품코드',    # ❌ 백엔드에 없음 → '상품'으로 변경됨
    '상품명',      # ✅ 존재
    '출하수량',    # ❌ 백엔드에 없음 → '오더수량*'으로 변경됨
    '출하금액',    # ✅ 신규 추가됨
    '배송처'       # ✅ 존재
]
```

### 백엔드 컬럼 (25개)
```
출고유형, 출고유형명, 출고일자, 라벨 출력시간, 피킹리스트 출력시간,
라벨출력, 피킹 리스트, 배송군, 배송처, 배송처명, 출하타입구분,
보관온도, 상품, 상품명, 단위및규격, 문서상태명, 원주문수량,
오더수량*, 할당수량**, 재고수량, 가용재고, 비고, 출고제한일,
출하바코드, 출하금액
```

### 수정 계획

#### Step 1: REQUIRED_COLUMNS 수정
```python
REQUIRED_COLUMNS = [
    '출하바코드',     # 출고번호 대체 (고유 식별자)
    '출고일자',       # 유지
    '상품',           # 상품코드 → 상품
    '상품명',         # 유지
    '오더수량*',      # 출하수량 → 오더수량*
    '출하금액',       # 신규 추가 (유지)
    '배송처'          # 유지
]
```

#### Step 2: 추가 유용 컬럼 (선택사항)
```python
# 대시보드에 유용한 추가 컬럼
OPTIONAL_COLUMNS = [
    '출고유형',       # 08, 15, 16, 17 등 타입 구분
    '출고유형명',     # 타입 설명
    '배송처명',       # 배송처 이름
    '보관온도',       # 실온/냉장/냉동
    '문서상태명',     # 할당/미할당 상태
    '할당수량**',     # 실제 할당된 수량
]
```

#### Step 3: load_data() 수정
```python
def load_data(self) -> pd.DataFrame:
    # ... (기존 코드)
    
    # 데이터 타입 변환
    df['출고일자'] = pd.to_datetime(df['출고일자'], format='%Y%m%d', errors='coerce')
    df['오더수량*'] = pd.to_numeric(df['오더수량*'], errors='coerce')  # 변경
    
    # 출하금액 처리 (N/A → NaN)
    df['출하금액'] = df['출하금액'].replace('N/A', pd.NA)
    df['출하금액'] = pd.to_numeric(df['출하금액'], errors='coerce')
    
    return df
```

#### Step 4: get_summary() 수정
```python
def get_summary(self) -> dict:
    df = self.get_data()
    
    return {
        '총_출고건수': len(df),
        '총_오더수량': df['오더수량*'].sum(),  # 변경
        '총_출하금액': df['출하금액'].sum(),
        '총_출하금액_유효': df['출하금액'].notna().sum(),  # N/A 제외
        '배송처_수': df['배송처'].nunique(),
        '상품_종류': df['상품'].nunique(),  # 변경
        '최근_출고일자': df['출고일자'].max(),
        '최초_출고일자': df['출고일자'].min(),
        '출고유형_분포': df['출고유형'].value_counts().to_dict(),  # 신규
    }
```

#### Step 5: 기존 함수 수정
```python
def get_top_products(self, n: int = 5) -> pd.DataFrame:
    df = self.get_data()
    return (df.groupby(['상품', '상품명'])['오더수량*']  # 변경
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .reset_index())
```

#### Step 6: 샘플 데이터 교체
- `sample_outbound.csv` 삭제
- 백엔드 `outbound_all_20251020.csv`에서 20개 레코드 추출하여 새로운 샘플 생성

---

## 3. InventoryCollector 🟡

### 백엔드 컬럼 (12개)
```
로케이션, 상품, 상품명, 단위및규격, 소비기한, 입수량,
가용수량, 가용박스수량, 가용잔량, 재고수량,
유효유통비(%), 단가
```

### 수정 계획

#### REQUIRED_COLUMNS
```python
REQUIRED_COLUMNS = [
    '로케이션',
    '상품',
    '상품명',
    '단위및규격',
    '소비기한',
    '가용수량',
    '재고수량',
    '유효유통비(%)',
    '단가'
]
```

#### 주요 기능
```python
def get_summary(self) -> dict:
    df = self.get_data()
    
    return {
        '총_상품수': df['상품'].nunique(),
        '총_재고수량': df['재고수량'].sum(),
        '총_가용수량': df['가용수량'].sum(),
        '총_재고금액': (df['재고수량'] * df['단가']).sum(),
        '위험_상품수': len(df[df['유효유통비(%)'] <= 20]),  # 유효비 20% 이하
        '평균_유효비': df['유효유통비(%)'].mean(),
    }

def get_low_stock(self, threshold: int = 10) -> pd.DataFrame:
    """재고 부족 상품 (가용수량 기준)"""
    df = self.get_data()
    return df[df['가용수량'] <= threshold].sort_values('가용수량')

def get_expiring_soon(self, threshold: int = 20) -> pd.DataFrame:
    """유효기한 임박 상품 (유효비 20% 이하)"""
    df = self.get_data()
    return df[df['유효유통비(%)'] <= threshold].sort_values('유효유통비(%)')
```

---

## 4. DeleteCollector 🟡

### 백엔드 컬럼 (13개)
```
삭제처리일, 삭제처리시간, 상품, 상품명, 규격 및 입고,
주문수량, 주문일자, 배송군, 배송처, 배송처명,
현황, 출하바코드, To로케이션
```

### 수정 계획

#### REQUIRED_COLUMNS
```python
REQUIRED_COLUMNS = [
    '삭제처리일',
    '삭제처리시간',
    '상품',
    '상품명',
    '주문수량',
    '주문일자',
    '배송처',
    '배송처명',
    '현황',
    '출하바코드'
]
```

#### 주요 기능
```python
def get_summary(self) -> dict:
    df = self.get_data()
    
    return {
        '총_삭제건수': len(df),
        '총_삭제수량': df['주문수량'].sum(),
        '배송처_수': df['배송처'].nunique(),
        '상품_종류': df['상품'].nunique(),
        '최근_삭제일': df['삭제처리일'].max(),
    }
```

---

## 5. IrregularCollector 🟡

### 백엔드 컬럼 (6개)
```
상세내역, 공급처명, 입고처명, 상품명, 오더수량, 현황
```

### 수정 계획

#### REQUIRED_COLUMNS
```python
REQUIRED_COLUMNS = [
    '상세내역',
    '공급처명',
    '입고처명',
    '상품명',
    '오더수량',
    '현황'
]
```

#### 주요 기능
```python
def get_summary(self) -> dict:
    df = self.get_data()
    
    return {
        '총_비정형건수': len(df),
        '총_오더수량': df['오더수량'].sum(),
        '공급처_수': df['공급처명'].nunique(),
        '입고처_수': df['입고처명'].nunique(),
        '현황_분포': df['현황'].value_counts().to_dict(),
    }
```

---

## 📋 작업 순서 (우선순위)

### 🔴 HIGH - 즉시 수정 필요
1. **OutboundCollector 수정** (1-2시간)
   - REQUIRED_COLUMNS 변경
   - load_data() 수정
   - get_summary() 수정
   - 모든 메서드 테스트
   - 샘플 데이터 교체

### 🟡 MEDIUM - 순차 개발
2. **InventoryCollector 개발** (3-4시간)
   - 신규 Collector 작성
   - UI 컴포넌트 개발
   - 재고 탭 추가

3. **DeleteCollector 개발** (2-3시간)
   - 신규 Collector 작성
   - UI 컴포넌트 개발
   - 삭제 탭 추가

4. **IrregularCollector 개발** (2-3시간)
   - 신규 Collector 작성
   - UI 컴포넌트 개발
   - 비정형 탭 추가

---

## 🔍 검증 계획

### 각 Collector별 검증 항목
1. ✅ 백엔드 CSV 파일 읽기 성공
2. ✅ 필수 컬럼 검증 통과
3. ✅ 데이터 타입 변환 정상
4. ✅ get_summary() 정상 작동
5. ✅ UI 컴포넌트에서 데이터 표시 정상

### 통합 테스트
- 5개 탭 모두 정상 작동
- 실제 백엔드 데이터로 테스트
- 샘플 데이터로도 테스트

---

## 📝 예상 소요 시간

| 작업 | 소요 시간 | 상태 |
|------|----------|------|
| OutboundCollector 수정 | 1-2시간 | ⏳ 대기 |
| InventoryCollector 개발 | 3-4시간 | ⏳ 대기 |
| DeleteCollector 개발 | 2-3시간 | ⏳ 대기 |
| IrregularCollector 개발 | 2-3시간 | ⏳ 대기 |
| 통합 테스트 | 1-2시간 | ⏳ 대기 |
| **총 예상 시간** | **9-14시간** | |

---

## ✅ 완료 후 상태

- 5개 Collector 모두 백엔드 데이터 구조와 완벽히 일치
- 실제 운영 데이터로 정상 작동
- Phase 1 완료 준비 완료
- Phase 2 (실제 데이터 연동) 준비 완료

---

## 작성자: 4명의 가상 전문가 팀
- 풀스택 개발자
- UX/UI 디자이너
- 데이터 엔지니어
- 데브옵스/QA 엔지니어
