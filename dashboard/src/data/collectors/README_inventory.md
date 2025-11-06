# InventoryCollector 상세 가이드

**파일**: `src/data/collectors/inventory.py`  
**데이터 소스**: `inventory_status_YYYYMMDD.csv`  
**완성 날짜**: 2025-10-20  
**테스트**: 8개 (100% 통과)  
**버전**: v2.0

---

## 📑 목차

1. [개요](#개요)
2. [데이터 소스](#데이터-소스)
3. [유효유통비 계산 로직](#유효유통비-계산-로직)
4. [핵심 메트릭](#핵심-메트릭)
5. [BaseCollector 구현](#basecollector-구현)
6. [주요 메서드](#주요-메서드)
7. [사용 예시](#사용-예시)
8. [테스트 가이드](#테스트-가이드)
9. [Edge Case 처리](#edge-case-처리)
10. [관련 문서](#관련-문서)

---

## 📌 개요

**InventoryCollector**는 OSIS 서버에서 수집된 재고 현황 데이터를 처리하고, 유효유통비를 기반으로 위험 상품을 파악하는 클래스입니다.

### 주요 역할
- ✅ 가용수량 기반 재고 현황 관리
- ✅ 유효유통비(%) 계산 및 위험 상품 판단
- ✅ 재고금액 자동 계산 (가용수량 × 단가)
- ✅ 유효비 구간별 상품 분포 분석

### 사용 시나리오
1. **위험 상품 관리**: 유효유통비 ≤ 20% 상품 조기 발견
2. **재고금액 모니터링**: 고가 재고 집중 관리
3. **재고 부족 알림**: 가용수량 낮은 상품 파악
4. **선입선출(FIFO) 관리**: 유효비 기준 출고 순서 결정

---

## 📊 데이터 소스

### 파일 정보
- **위치**: `C:\OSIS_AUTO\Inventory Status\inventory_status_YYYYMMDD.csv`
- **형식**: CSV (UTF-8 BOM)
- **갱신 주기**: 1일 4회 (08:00, 12:00, 15:00, 19:00)
- **생성 프로그램**: `inventory_status.py` (백엔드)

### 주요 컬럼 (5개 + α)

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| 상품 | 문자열 | 상품 코드 | 41033876 |
| 상품명 | 문자열 | 상품 이름 | 떡볶이양념장(분말) |
| 가용수량 | 숫자 (정수) | 실제 사용 가능한 재고 | 500 |
| 유효유통비(%) | 숫자 (실수) | 백엔드에서 계산된 유효비 | 35.5 |
| 단가 | 숫자 (정수) | 상품 단가 (원) | 2500 |

**추가 컬럼 (백엔드에서 제공 가능)**:
- 제조일자 (YYYYMMDD)
- 유효기한 (YYYYMMDD)
- 로케이션
- 창고코드

### 데이터 특성
- **가용수량**: 예약/할당 제외한 실제 사용 가능 재고
- **유효유통비**: 백엔드에서 자동 계산 (제조일~유효기한 기준)
- **단가**: 재고금액 계산에 사용
- **동일 상품 여러 로케이션**: 로케이션별 분리 가능

---

## 🧮 유효유통비 계산 로직

### 계산 공식 (백엔드)
```
유효유통비(%) = (유효기한 - 현재일) / (유효기한 - 제조일) × 100
```

### 예시
```
제조일: 2025-01-01
유효기한: 2026-01-01  (365일)
현재일: 2025-10-24   (296일 경과)

잔여일수 = 2026-01-01 - 2025-10-24 = 69일
전체일수 = 2026-01-01 - 2025-01-01 = 365일

유효유통비 = 69 / 365 × 100 = 18.9%  (위험!)
```

### 유효비 구간별 의미

| 구간 | 상태 | 색상 | 조치 |
|------|------|------|------|
| **0-20%** | 🔴 위험 | 빨간색 | 긴급 출고 필요 |
| 21-40% | 🟠 주의 | 주황색 | 조기 출고 권장 |
| 41-60% | 🟡 보통 | 노란색 | 정상 출고 |
| 61-80% | 🟢 양호 | 연두색 | 여유 있음 |
| 81-100% | 🔵 최상 | 파란색 | 신선 상품 |

### 위험 상품 기준
- **InventoryCollector 기준**: 유효유통비 ≤ 20%
- **대시보드 알림**: 빨간색 경고 표시
- **조치 필요**: 48시간 내 출고 권장

---

## 🎯 핵심 메트릭

### 1. 총_상품수 (total_product_count)
- **설명**: 고유 상품 코드 개수
- **계산 방식**: `df['상품'].nunique()`
- **예시**: 1,245종

### 2. 총_가용수량 (total_available_quantity)
- **설명**: 전체 가용수량 합계
- **계산 방식**: `df['가용수량'].sum()`
- **예시**: 125,480개

### 3. 총_재고금액 (total_inventory_value)
- **설명**: (가용수량 × 단가) 합계
- **계산 방식**: `(df['가용수량'] * df['단가']).sum()`
- **예시**: 312,450,000원

### 4. 위험_상품수 (risk_product_count)
- **설명**: 유효유통비 ≤ 20% 상품 개수
- **계산 방식**: `len(df[df['유효유통비(%)'] <= 20])`
- **예시**: 87종

### 5. 평균_유효비 (avg_validity_ratio)
- **설명**: 전체 상품의 평균 유효유통비
- **계산 방식**: `df['유효유통비(%)'].mean()`
- **예시**: 52.3%

### 6. 유효비_구간별_분포 (distribution_by_validity)
- **설명**: 구간별 상품 개수 딕셔너리
- **계산 방식**: `pd.cut()` 사용하여 구간 분류
- **예시**:
```python
{
    '위험(≤20%)': 87,
    '주의(21-50%)': 423,
    '정상(51-100%)': 735
}
```

---

## 🔧 BaseCollector 구현

### 상속 구조
```python
from .base import BaseCollector

class InventoryCollector(BaseCollector):
    """재고정보 수집기"""
    
    REQUIRED_COLUMNS = [
        '상품',           # 상품코드
        '상품명',         # 상품명
        '가용수량',       # 가용수량
        '유효유통비(%)',  # 유효유통비 (백엔드 계산)
        '단가'           # 단가 (금액 계산용)
    ]
```

### 필수 메서드 구현

#### 1. load_data()
```python
def load_data(self) -> pd.DataFrame:
    """CSV 파일에서 재고 데이터 로드"""
    
    if not self.file_exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
    
    # CSV 읽기 (UTF-8 BOM)
    df = pd.read_csv(self.file_path, encoding=self.encoding)
    
    # 데이터 검증
    if not self.validate(df):
        raise ValueError("재고 데이터 검증 실패")
    
    # 데이터 타입 변환
    df['가용수량'] = pd.to_numeric(df['가용수량'], errors='coerce')
    df['유효유통비(%)'] = pd.to_numeric(df['유효유통비(%)'], errors='coerce')
    df['단가'] = pd.to_numeric(df['단가'], errors='coerce')
    
    return df
```

**핵심 포인트**:
- 유효유통비는 백엔드에서 계산되어 제공
- 숫자 형식 안전 변환 (errors='coerce')
- UTF-8 BOM 인코딩 지원

#### 2. validate()
```python
def validate(self, df: pd.DataFrame) -> bool:
    """재고 데이터 유효성 검증"""
    
    # 필수 컬럼 확인
    missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        print(f"❌ 누락된 컬럼: {missing_columns}")
        return False
    
    # 빈 데이터 확인
    if df.empty:
        print("❌ 데이터가 비어있습니다")
        return False
    
    return True
```

---

## 💡 주요 메서드

### 1. get_summary() - 요약 정보
```python
def get_summary(self) -> dict:
    """재고 데이터 요약 정보"""
    
    df = self.get_data()
    
    # 총 재고 금액 계산
    df['재고금액'] = df['가용수량'] * df['단가']
    total_value = df['재고금액'].sum()
    
    # 유효비 위험 상품 (≤ 20%)
    risky_count = len(df[df['유효유통비(%)'] <= 20])
    
    # 유효비 구간별 분포
    bins = [0, 20, 50, 100]
    labels = ['위험(≤20%)', '주의(21-50%)', '정상(51-100%)']
    df['유효비구간'] = pd.cut(df['유효유통비(%)'], bins=bins, labels=labels, include_lowest=True)
    distribution = df['유효비구간'].value_counts().to_dict()
    
    summary = {
        '총_상품수': df['상품'].nunique(),
        '총_가용수량': int(df['가용수량'].sum()),
        '총_재고금액': int(total_value),
        '위험_상품수': risky_count,
        '평균_유효비': round(df['유효유통비(%)'].mean(), 2),
        '유효비_구간별_분포': distribution
    }
    
    return summary
```

**반환 예시**:
```python
{
    '총_상품수': 1245,
    '총_가용수량': 125480,
    '총_재고금액': 312450000,
    '위험_상품수': 87,
    '평균_유효비': 52.3,
    '유효비_구간별_분포': {
        '위험(≤20%)': 87,
        '주의(21-50%)': 423,
        '정상(51-100%)': 735
    }
}
```

### 2. get_risky_products() - 위험 상품 목록
```python
def get_risky_products(self) -> pd.DataFrame:
    """유효비 위험 상품 목록 (≤ 20%)"""
    
    df = self.get_data()
    
    # 유효비 20% 이하 필터링
    risky = df[df['유효유통비(%)'] <= 20].copy()
    
    # 재고금액 계산
    risky['재고금액'] = risky['가용수량'] * risky['단가']
    
    # 필요한 컬럼만 선택 및 정렬
    result = risky[['상품', '상품명', '가용수량', '유효유통비(%)', '단가', '재고금액']]
    result = result.sort_values('유효유통비(%)', ascending=True)
    
    return result
```

**반환 예시**:
```
     상품              상품명  가용수량  유효유통비(%)  단가   재고금액
0  41033876  떡볶이양념장(분말)      500         8.5  2500  1250000
1  41044521     김밥천국소스      320        12.3  1800   576000
2  41055632      청양고추절임      180        15.7  3200   576000
```

### 3. get_low_stock_products() - 재고 부족 상품
```python
def get_low_stock_products(self, threshold: int = 10) -> pd.DataFrame:
    """가용수량 부족 상품 목록"""
    
    df = self.get_data()
    
    # 가용수량 부족 필터링
    low_stock = df[df['가용수량'] <= threshold].copy()
    
    # 재고금액 계산
    low_stock['재고금액'] = low_stock['가용수량'] * low_stock['단가']
    
    # 필요한 컬럼만 선택 및 정렬
    result = low_stock[['상품', '상품명', '가용수량', '유효유통비(%)', '단가', '재고금액']]
    result = result.sort_values('가용수량', ascending=True)
    
    return result
```

### 4. get_top_value_products() - 재고금액 상위 상품
```python
def get_top_value_products(self, n: int = 10) -> pd.DataFrame:
    """재고금액 상위 상품 목록"""
    
    df = self.get_data()
    
    # 재고금액 계산
    df['재고금액'] = df['가용수량'] * df['단가']
    
    # 상품별 집계 (같은 상품이 여러 로케이션에 있을 수 있음)
    result = (df.groupby(['상품', '상품명'])
              .agg({
                  '가용수량': 'sum',
                  '재고금액': 'sum',
                  '유효유통비(%)': 'mean',  # 평균 유효비
                  '단가': 'first'  # 첫 번째 단가
              })
              .sort_values('재고금액', ascending=False)
              .head(n)
              .reset_index())
    
    # 유효비 반올림
    result['유효유통비(%)'] = result['유효유통비(%)'].round(2)
    
    return result
```

**반환 예시**:
```
     상품          상품명  가용수량  재고금액  유효유통비(%)  단가
0  41077788  프리미엄소고기     2500  87500000       65.3  35000
1  41066432    참치캔세트     5800  69600000       72.1  12000
2  41055211      연어필렛     1200  60000000       58.7  50000
```

### 5. calculate_total_value() - 총 재고 금액
```python
def calculate_total_value(self) -> int:
    """총 재고 금액 계산"""
    
    df = self.get_data()
    total = (df['가용수량'] * df['단가']).sum()
    return int(total)
```

---

## 💡 사용 예시

### 기본 사용 (Streamlit 대시보드)
```python
from src.data.collectors.inventory import InventoryCollector

# 1. 인스턴스 생성
file_path = "C:/OSIS_AUTO/Inventory Status/inventory_status_20251024.csv"
collector = InventoryCollector(file_path=file_path, encoding='utf-8-sig')

# 2. 데이터 로드
try:
    data = collector.get_data()
    print(f"✅ {len(data)}건 로드 성공")
except Exception as e:
    print(f"❌ 오류: {e}")

# 3. 요약 정보
summary = collector.get_summary()
print(f"총 상품수: {summary['총_상품수']}")
print(f"위험 상품수: {summary['위험_상품수']}")
print(f"총 재고금액: {summary['총_재고금액']:,}원")

# 4. 위험 상품 조회
risky = collector.get_risky_products()
print(f"🔴 위험 상품: {len(risky)}종")
print(risky.head(10))

# 5. 재고 부족 상품
low_stock = collector.get_low_stock_products(threshold=50)
print(f"⚠️ 재고 부족: {len(low_stock)}종")

# 6. 재고금액 TOP 10
top_value = collector.get_top_value_products(n=10)
print(top_value)
```

### Flask API 연동 (Phase 2 예정)
```python
from flask import Flask, jsonify
from src.data.collectors.inventory import InventoryCollector

app = Flask(__name__)

@app.route('/api/inventory')
def get_inventory_data():
    """재고 데이터 API"""
    
    file_path = "C:/OSIS_AUTO/Inventory Status/inventory_status_20251024.csv"
    collector = InventoryCollector(file_path=file_path, encoding='utf-8-sig')
    
    try:
        # 요약 정보
        summary = collector.get_summary()
        
        # 위험 상품
        risky = collector.get_risky_products().to_dict('records')
        
        # 재고 부족 상품
        low_stock = collector.get_low_stock_products(threshold=50).to_dict('records')
        
        # 재고금액 TOP 10
        top_value = collector.get_top_value_products(n=10).to_dict('records')
        
        return jsonify({
            'success': True,
            'summary': summary,
            'risky_products': risky[:20],  # 최대 20건
            'low_stock': low_stock[:20],
            'top_value': top_value
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 🧪 테스트 가이드

### 테스트 파일
- **위치**: `tests/test_inventory_collector.py`
- **테스트 개수**: 8개
- **커버리지**: 94%

### 테스트 케이스

#### 1. test_load_data_success
```python
def test_load_data_success():
    """데이터 로드 성공 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    df = collector.load_data()
    
    assert not df.empty
    assert '유효유통비(%)' in df.columns
    assert '가용수량' in df.columns
```

#### 2. test_validate_success
```python
def test_validate_success():
    """데이터 검증 성공 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    df = collector.load_data()
    
    assert collector.validate(df) == True
```

#### 3. test_get_summary
```python
def test_get_summary():
    """요약 정보 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    collector.load_data()
    summary = collector.get_summary()
    
    assert '총_상품수' in summary
    assert '위험_상품수' in summary
    assert '총_재고금액' in summary
    assert summary['총_상품수'] > 0
```

#### 4. test_get_risky_products
```python
def test_get_risky_products():
    """위험 상품 조회 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    collector.load_data()
    risky = collector.get_risky_products()
    
    # 모든 레코드의 유효비 ≤ 20 확인
    assert all(risky['유효유통비(%)'] <= 20)
```

#### 5. test_get_low_stock_products
```python
def test_get_low_stock_products():
    """재고 부족 상품 조회 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    collector.load_data()
    low_stock = collector.get_low_stock_products(threshold=10)
    
    # 모든 레코드의 가용수량 ≤ 10 확인
    assert all(low_stock['가용수량'] <= 10)
```

#### 6. test_get_top_value_products
```python
def test_get_top_value_products():
    """재고금액 TOP 상품 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    collector.load_data()
    top = collector.get_top_value_products(n=5)
    
    assert len(top) <= 5
    assert '재고금액' in top.columns
    # 내림차순 정렬 확인
    assert top['재고금액'].is_monotonic_decreasing
```

#### 7. test_calculate_total_value
```python
def test_calculate_total_value():
    """총 재고 금액 계산 테스트"""
    collector = InventoryCollector(file_path='fixtures/sample_inventory.csv')
    collector.load_data()
    total = collector.calculate_total_value()
    
    assert isinstance(total, int)
    assert total > 0
```

#### 8. test_file_not_found
```python
def test_file_not_found():
    """파일 미존재 테스트"""
    collector = InventoryCollector(file_path='nonexistent.csv')
    
    with pytest.raises(FileNotFoundError):
        collector.load_data()
```

### 테스트 실행
```bash
# 재고 Collector 테스트만 실행
pytest tests/test_inventory_collector.py -v

# 커버리지 확인
pytest tests/test_inventory_collector.py --cov=src.data.collectors.inventory --cov-report=html
```

---

## ⚠️ Edge Case 처리

### 1. 음수 유효유통비
- **상황**: 유효유통비가 음수 (예: -5.2%)
- **처리**: 데이터 그대로 유지
- **의미**: 유효기한 경과 (폐기 대상)
- **대응**: 대시보드에서 긴급 알림

### 2. 100% 초과 유효비
- **상황**: 유효유통비가 100 초과 (예: 105%)
- **처리**: 데이터 그대로 유지
- **의미**: 계산 오류 또는 데이터 이상
- **대응**: 데이터 검증 필요

### 3. 0 가용수량
- **상황**: 가용수량이 0
- **처리**: 데이터 유지 (재고 소진 표시)
- **영향**: 재고 부족 알림 대상

### 4. 음수 가용수량
- **상황**: 가용수량이 음수 (예: -10)
- **처리**: 데이터 그대로 유지
- **의미**: 초과 할당 또는 시스템 오류
- **대응**: 빨간색 경고

### 5. 0원 단가
- **상황**: 단가가 0원
- **처리**: 재고금액 0원으로 계산
- **의미**: 무상 제품 또는 데이터 누락
- **영향**: 재고금액 통계에서 제외 가능

### 6. 유효비 구간 경계값
- **상황**: 유효비가 정확히 20.0%
- **처리**: `pd.cut(include_lowest=True)`로 위험 구간 포함
- **의미**: 20% 이하를 위험으로 판단

---

## 🔗 관련 문서

### 프로젝트 문서
- [../README.md](../README.md) - Collector 전체 개요
- [base.py](base.py) - BaseCollector 추상 클래스
- [../../tests/test_inventory_collector.py](../../tests/test_inventory_collector.py) - 테스트 코드

### 백엔드 문서
- **WMS_재고현황_README.md** - 백엔드 사용자 가이드
- **WMS_재고현황_TECHNICAL_GUIDE.md** - 백엔드 기술 문서
- **WMS_재고현황_활용방안.md** - 대시보드 활용 방안

### 공식 문서
- **PROJECT_STATUS.md** - 프로젝트 현황 (v3.0)
- **02_기술설명서.md** - 기술 스택 (v2.1)

---

## 📊 성능 및 제약사항

### 성능
- **로딩 시간**: 1,000건 기준 < 0.2초
- **메모리 사용**: 약 2MB (10,000건 기준)
- **권장 데이터 크기**: 최대 50,000건

### 제약사항
- UTF-8 BOM 인코딩 필수
- 유효유통비는 백엔드에서 계산되어 제공
- 필수 컬럼 5개 모두 필요
- 가용수량과 단가는 0 이상 권장

---

## 🔄 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1.0 | 2025-10-17 | 초기 버전 (기본 구조) |
| v2.0 | 2025-10-20 | 백엔드 유효비 연동 ✅ |
| - | - | 유효비 구간별 분포 추가 |
| - | - | 위험 상품 판단 로직 (≤20%) |
| - | - | 8개 테스트 통과 |
| - | - | Phase 1 완료 ✅ |

---

**마지막 업데이트**: 2025-11-07  
**작성자**: WMS 대시보드 개발팀  
**상태**: ✅ Phase 1 완료 → Phase 2 Flask 연동 예정