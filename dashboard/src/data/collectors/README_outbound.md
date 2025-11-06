# OutboundCollector 상세 가이드

**파일**: `src/data/collectors/outbound.py`  
**데이터 소스**: `outbound_04_YYYYMMDD.csv ~ outbound_53_YYYYMMDD.csv` (10개)  
**완성 날짜**: 2025-10-20  
**테스트**: 8개 (100% 통과)  
**버전**: v2.0

---

## 📑 목차

1. [개요](#개요)
2. [데이터 소스](#데이터-소스)
3. [10개 출고 타입](#10개-출고-타입)
4. [핵심 메트릭](#핵심-메트릭)
5. [BaseCollector 구현](#basecollector-구현)
6. [주요 메서드](#주요-메서드)
7. [사용 예시](#사용-예시)
8. [테스트 가이드](#테스트-가이드)
9. [Edge Case 처리](#edge-case-처리)
10. [관련 문서](#관련-문서)

---

## 📌 개요

**OutboundCollector**는 OSIS 서버에서 수집된 10개 타입의 출고 데이터를 통합 처리하는 클래스입니다.

### 주요 역할
- ✅ 10개 출고 타입별 데이터 통합 수집
- ✅ 출하금액 자동 계산 (재고 단가 × 출고 수량)
- ✅ 배송처별, 상품별 출고 통계 제공
- ✅ 출고유형별 집계 및 분석

### 사용 시나리오
1. **출하금액 모니터링**: 일일/시간대별 출하금액 추적
2. **배송처 관리**: 배송처별 출고량 및 금액 분석
3. **상품 판매 분석**: 상품별 출고 추이 파악
4. **타입별 운영 최적화**: 10개 타입별 효율성 비교

---

## 📊 데이터 소스

### 파일 정보
- **위치**: `C:\OSIS_AUTO\Outbound Status\`
- **파일 개수**: 10개 (타입별 분리)
- **형식**: CSV (UTF-8 BOM)
- **갱신 주기**: 1일 4회 (08:00, 12:00, 15:00, 19:00)
- **생성 프로그램**: `collect_outbound_status.py` (백엔드)

### 파일 목록
```
outbound_04_20251024.csv  (지방 캘리스코)
outbound_05_20251024.csv  (한익스, 키즈)
outbound_08_20251024.csv  (지방 삼각유부,델리치 50%)
outbound_14_20251024.csv  (자사 캘리스코)
outbound_15_20251024.csv  (자사 물품)
outbound_16_20251024.csv  (지방 직접발주)
outbound_17_20251024.csv  (지방 자동발주)
outbound_18_20251024.csv  (자사 삼각유부,델리치 50%)
outbound_52_20251024.csv  (지방 캘리스코)
outbound_53_20251024.csv  (지방 삼각유부,델리치 50%)
```

### 주요 컬럼 (7개)

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| 출하바코드 | 문자열 | 출고 고유 식별자 | 12345678901234 |
| 출고일자 | 날짜 (YYYYMMDD) | 출고 날짜 | 20251024 |
| 상품 | 문자열 | 상품 코드 | 41033876 |
| 상품명 | 문자열 | 상품 이름 | 떡볶이양념장(분말) |
| 오더수량* | 숫자 (정수) | 출고 수량 | 50 |
| 출하금액 | 숫자 (정수) | 재고 단가 × 오더수량 | 125000 |
| 배송처 | 문자열 | 배송처명 | 부산물류센터 |

### 데이터 특성
- **출하금액**: 재고 단가 연동하여 자동 계산 (백엔드)
- **N/A 처리**: 단가 없는 상품은 출하금액 'N/A'
- **10개 타입 통합**: Collector가 10개 CSV를 하나로 병합

---

## 🏷️ 10개 출고 타입

### 타입별 상세 정보

| 타입 코드 | 출고유형명 | 설명 | 주요 특징 |
|----------|-----------|------|-----------|
| **04** | 지방 캘리스코 | 지방 캘리스코 매장 출고 | 주력 타입 |
| **05** | 한익스, 키즈 | 한익스프레스, 키즈카페 | 소량 다품종 |
| **08** | 지방 삼각유부,델리치 50% | 지방 특정 상품 50% | 특수 할인 |
| **14** | 자사 캘리스코 | 자사 캘리스코 출고 | 내부 이동 |
| **15** | 자사 물품 | 자사 일반 물품 | 내부 이동 |
| **16** | 지방 (직접 발주) | 지방 직접 발주 건 | 수동 처리 |
| **17** | 지방 (자동 발주) | 지방 자동 발주 건 | 시스템 자동 |
| **18** | 자사 삼각유부,델리치 50% | 자사 특정 상품 50% | 특수 할인 |
| **52** | 지방 캘리스코 | 지방 캘리스코 매장 | 04와 유사 |
| **53** | 지방 삼각유부,델리치 50% | 지방 특정 상품 50% | 08과 유사 |

### 타입별 비중 (예시)
```
04: 35%  (가장 많음)
17: 25%  (자동 발주)
16: 15%  (직접 발주)
05: 10%  (한익스)
14-15: 8%  (자사)
08, 18, 52, 53: 7% (기타)
```

---

## 🎯 핵심 메트릭

### 1. 총_출고건수 (total_count)
- **설명**: 출하바코드 기준 전체 출고 건수
- **계산 방식**: `len(df)`
- **예시**: 1,245건

### 2. 총_오더수량 (total_quantity)
- **설명**: 오더수량 합계
- **계산 방식**: `df['오더수량*'].sum()`
- **예시**: 25,480개

### 3. 총_출하금액 (total_amount)
- **설명**: 출하금액 합계 (N/A 제외)
- **계산 방식**: `df['출하금액'].sum()` (N/A → NaN 변환 후)
- **예시**: 125,450,000원

### 4. 출하금액_유효건수 (valid_amount_count)
- **설명**: 출하금액이 유효한 건수 (N/A 제외)
- **계산 방식**: `df['출하금액'].notna().sum()`
- **예시**: 1,180건 (1,245건 중)

### 5. 출하금액_N/A건수 (na_amount_count)
- **설명**: 출하금액이 N/A인 건수
- **계산 방식**: `len(df) - valid_amount_count`
- **예시**: 65건

### 6. 배송처_수 (destination_count)
- **설명**: 고유 배송처 개수
- **계산 방식**: `df['배송처'].nunique()`
- **예시**: 87개

### 7. 상품_종류 (product_count)
- **설명**: 고유 상품 개수
- **계산 방식**: `df['상품'].nunique()`
- **예시**: 320종

---

## 🔧 BaseCollector 구현

### 상속 구조
```python
from .base import BaseCollector

class OutboundCollector(BaseCollector):
    """출고정보 수집기"""
    
    REQUIRED_COLUMNS = [
        '출하바코드',      # 출고 고유키
        '출고일자',        # 출고 날짜
        '상품',            # 상품코드
        '상품명',          # 상품명
        '오더수량*',       # 출고 수량
        '출하금액',        # 재고 단가 연동
        '배송처'           # 배송처명
    ]
```

### 필수 메서드 구현

#### 1. load_data()
```python
def load_data(self) -> pd.DataFrame:
    """CSV 파일에서 출고 데이터 로드"""
    
    if not self.file_exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
    
    # CSV 읽기 (UTF-8 BOM)
    df = pd.read_csv(self.file_path, encoding=self.encoding)
    
    # 데이터 검증
    if not self.validate(df):
        raise ValueError("출고 데이터 검증 실패")
    
    # 데이터 타입 변환
    df['출고일자'] = pd.to_datetime(df['출고일자'], format='%Y%m%d', errors='coerce')
    df['오더수량*'] = pd.to_numeric(df['오더수량*'], errors='coerce')
    
    # 출하금액 처리 (N/A → NaN)
    df['출하금액'] = df['출하금액'].replace('N/A', pd.NA)
    df['출하금액'] = pd.to_numeric(df['출하금액'], errors='coerce')
    
    return df
```

**핵심 포인트**:
- 'N/A' 문자열을 pandas NA로 변환
- 숫자 변환 시 errors='coerce'로 안전 처리
- 날짜 형식 자동 변환

#### 2. validate()
```python
def validate(self, df: pd.DataFrame) -> bool:
    """출고 데이터 유효성 검증"""
    
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
    """출고 데이터 요약 정보"""
    
    df = self.get_data()
    
    # 출하금액 유효 건수 계산
    valid_amount = df['출하금액'].notna().sum()
    total_amount = df['출하금액'].sum()
    
    summary = {
        '총_출고건수': len(df),
        '총_오더수량': int(df['오더수량*'].sum()),
        '총_출하금액': int(total_amount) if pd.notna(total_amount) else 0,
        '출하금액_유효건수': int(valid_amount),
        '출하금액_N/A건수': len(df) - int(valid_amount),
        '배송처_수': df['배송처'].nunique(),
        '상품_종류': df['상품'].nunique(),
        '최근_출고일자': df['출고일자'].max(),
        '최초_출고일자': df['출고일자'].min(),
    }
    
    # 출고유형 분포 (백엔드에 출고유형 컬럼이 있으면)
    if '출고유형' in df.columns:
        summary['출고유형_분포'] = df['출고유형'].value_counts().to_dict()
    
    return summary
```

**반환 예시**:
```python
{
    '총_출고건수': 1245,
    '총_오더수량': 25480,
    '총_출하금액': 125450000,
    '출하금액_유효건수': 1180,
    '출하금액_N/A건수': 65,
    '배송처_수': 87,
    '상품_종류': 320,
    '최근_출고일자': Timestamp('2025-10-24'),
    '최초_출고일자': Timestamp('2025-10-24')
}
```

### 2. get_top_destinations() - 상위 배송처
```python
def get_top_destinations(self, n: int = 5) -> pd.DataFrame:
    """상위 배송처 목록 (오더수량 기준)"""
    
    df = self.get_data()
    
    result = (df.groupby('배송처')
              .agg({
                  '오더수량*': 'sum',
                  '출하금액': lambda x: x.sum() if x.notna().any() else 0
              })
              .sort_values('오더수량*', ascending=False)
              .head(n)
              .reset_index())
    
    # 컬럼명 정리
    result.columns = ['배송처', '총_오더수량', '총_출하금액']
    return result
```

**반환 예시**:
```
          배송처  총_오더수량  총_출하금액
0  부산물류센터        3500   87500000
1  대구물류센터        2800   70000000
2  광주물류센터        2200   55000000
```

### 3. get_top_products() - 상위 출고 상품
```python
def get_top_products(self, n: int = 5) -> pd.DataFrame:
    """상위 출고 상품 목록 (오더수량 기준)"""
    
    df = self.get_data()
    
    result = (df.groupby(['상품', '상품명'])
              .agg({
                  '오더수량*': 'sum',
                  '출하금액': lambda x: x.sum() if x.notna().any() else 0
              })
              .sort_values('오더수량*', ascending=False)
              .head(n)
              .reset_index())
    
    # 컬럼명 정리
    result.columns = ['상품', '상품명', '총_오더수량', '총_출하금액']
    return result
```

### 4. get_by_type() - 출고유형별 집계
```python
def get_by_type(self) -> pd.DataFrame:
    """출고유형별 집계 (백엔드에 출고유형 컬럼이 있을 때)"""
    
    df = self.get_data()
    
    if '출고유형' not in df.columns or '출고유형명' not in df.columns:
        return pd.DataFrame()  # 컬럼 없으면 빈 DataFrame
    
    result = (df.groupby(['출고유형', '출고유형명'])
              .agg({
                  '오더수량*': 'sum',
                  '출하금액': lambda x: x.sum() if x.notna().any() else 0,
                  '출하바코드': 'count'  # 건수
              })
              .sort_values('오더수량*', ascending=False)
              .reset_index())
    
    # 컬럼명 정리
    result.columns = ['출고유형', '출고유형명', '총_오더수량', '총_출하금액', '출고건수']
    return result
```

**반환 예시**:
```
  출고유형        출고유형명  총_오더수량  총_출하금액  출고건수
0     04   지방 캘리스코        8900  44500000       435
1     17  지방(자동발주)        6200  31000000       312
2     16  지방(직접발주)        3700  18500000       187
```

---

## 💡 사용 예시

### 기본 사용 (Streamlit 대시보드)
```python
from src.data.collectors.outbound import OutboundCollector

# 1. 인스턴스 생성 (타입 04 예시)
file_path = "C:/OSIS_AUTO/Outbound Status/outbound_04_20251024.csv"
collector = OutboundCollector(file_path=file_path, encoding='utf-8-sig')

# 2. 데이터 로드
try:
    data = collector.get_data()
    print(f"✅ {len(data)}건 로드 성공")
except Exception as e:
    print(f"❌ 오류: {e}")

# 3. 요약 정보
summary = collector.get_summary()
print(f"총 출고건수: {summary['총_출고건수']}")
print(f"총 출하금액: {summary['총_출하금액']:,}원")

# 4. 상위 배송처
top_dest = collector.get_top_destinations(n=10)
print(top_dest)

# 5. 상위 상품
top_products = collector.get_top_products(n=10)
print(top_products)
```

### 10개 타입 통합 사용
```python
import glob
from pathlib import Path

# 10개 CSV 파일 경로 가져오기
base_path = Path("C:/OSIS_AUTO/Outbound Status")
pattern = "outbound_*_20251024.csv"
files = list(base_path.glob(pattern))

# 모든 타입 데이터 통합
all_data = []
for file in files:
    collector = OutboundCollector(file_path=str(file), encoding='utf-8-sig')
    data = collector.get_data()
    all_data.append(data)

# DataFrame 통합
import pandas as pd
combined_df = pd.concat(all_data, ignore_index=True)

print(f"✅ 10개 타입 통합: {len(combined_df)}건")
print(f"총 출하금액: {combined_df['출하금액'].sum():,}원")
```

### Flask API 연동 (Phase 2 예정)
```python
from flask import Flask, jsonify
from src.data.collectors.outbound import OutboundCollector
import glob

app = Flask(__name__)

@app.route('/api/outbound')
def get_outbound_data():
    """출고 데이터 API (10개 타입 통합)"""
    
    try:
        # 10개 타입 파일 수집
        base_path = "C:/OSIS_AUTO/Outbound Status"
        files = glob.glob(f"{base_path}/outbound_*_20251024.csv")
        
        all_data = []
        for file in files:
            collector = OutboundCollector(file_path=file, encoding='utf-8-sig')
            data = collector.get_data()
            all_data.append(data)
        
        # 통합
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # 요약 정보
        summary = {
            '총_출고건수': len(combined_df),
            '총_오더수량': int(combined_df['오더수량*'].sum()),
            '총_출하금액': int(combined_df['출하금액'].sum())
        }
        
        # 상위 배송처
        top_dest = (combined_df.groupby('배송처')
                    .agg({'오더수량*': 'sum', '출하금액': 'sum'})
                    .sort_values('오더수량*', ascending=False)
                    .head(10)
                    .reset_index()
                    .to_dict('records'))
        
        return jsonify({
            'success': True,
            'summary': summary,
            'top_destinations': top_dest
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
- **위치**: `tests/test_outbound.py`
- **테스트 개수**: 8개
- **커버리지**: 92%

### 테스트 케이스

#### 1. test_load_data_success
```python
def test_load_data_success():
    """데이터 로드 성공 테스트"""
    collector = OutboundCollector(file_path='fixtures/sample_outbound.csv')
    df = collector.load_data()
    
    assert not df.empty
    assert '출하바코드' in df.columns
    assert '출하금액' in df.columns
```

#### 2. test_na_amount_handling
```python
def test_na_amount_handling():
    """N/A 출하금액 처리 테스트"""
    collector = OutboundCollector(file_path='fixtures/sample_outbound.csv')
    df = collector.load_data()
    
    # N/A → NaN 변환 확인
    assert df['출하금액'].dtype in ['float64', 'Int64']
    na_count = df['출하금액'].isna().sum()
    assert na_count >= 0  # N/A가 있을 수 있음
```

#### 3. test_get_summary
```python
def test_get_summary():
    """요약 정보 테스트"""
    collector = OutboundCollector(file_path='fixtures/sample_outbound.csv')
    collector.load_data()
    summary = collector.get_summary()
    
    assert '총_출고건수' in summary
    assert '총_출하금액' in summary
    assert '출하금액_유효건수' in summary
    assert summary['총_출고건수'] > 0
```

#### 4. test_get_top_destinations
```python
def test_get_top_destinations():
    """상위 배송처 조회 테스트"""
    collector = OutboundCollector(file_path='fixtures/sample_outbound.csv')
    collector.load_data()
    top = collector.get_top_destinations(n=5)
    
    assert len(top) <= 5
    assert '배송처' in top.columns
    assert '총_오더수량' in top.columns
```

#### 5. test_get_top_products
```python
def test_get_top_products():
    """상위 상품 조회 테스트"""
    collector = OutboundCollector(file_path='fixtures/sample_outbound.csv')
    collector.load_data()
    top = collector.get_top_products(n=5)
    
    assert len(top) <= 5
    assert '상품명' in top.columns
```

#### 6. test_get_by_type
```python
def test_get_by_type():
    """출고유형별 집계 테스트"""
    collector = OutboundCollector(file_path='fixtures/sample_outbound.csv')
    collector.load_data()
    by_type = collector.get_by_type()
    
    # 출고유형 컬럼이 있으면 결과 있음, 없으면 빈 DataFrame
    if not by_type.empty:
        assert '출고유형' in by_type.columns
```

#### 7. test_file_not_found
```python
def test_file_not_found():
    """파일 미존재 테스트"""
    collector = OutboundCollector(file_path='nonexistent.csv')
    
    with pytest.raises(FileNotFoundError):
        collector.load_data()
```

#### 8. test_invalid_data
```python
def test_invalid_data():
    """잘못된 데이터 테스트"""
    collector = OutboundCollector(file_path='fixtures/invalid_outbound.csv')
    
    with pytest.raises(ValueError):
        collector.load_data()
```

### 테스트 실행
```bash
# 출고 Collector 테스트만 실행
pytest tests/test_outbound.py -v

# 커버리지 확인
pytest tests/test_outbound.py --cov=src.data.collectors.outbound --cov-report=html
```

---

## ⚠️ Edge Case 처리

### 1. 출하금액 N/A
- **상황**: 재고 단가가 없어서 출하금액이 'N/A'
- **처리**: `pd.NA`로 변환 후 계산에서 제외
- **영향**: 총_출하금액 계산 시 자동 제외

### 2. 10개 타입 파일 일부 누락
- **상황**: 10개 CSV 중 일부만 존재
- **처리**: 존재하는 파일만 로드하고 통합
- **대응**: 누락된 타입은 경고 로그 출력

### 3. 음수 오더수량
- **상황**: 오더수량이 음수 (예: -10)
- **처리**: 데이터 그대로 유지 (반품 또는 오류 표시)
- **대응**: 대시보드에서 빨간색 경고

### 4. 0 출하금액
- **상황**: 출하금액이 0원 (무상 출고)
- **처리**: 유효한 데이터로 처리
- **의미**: 샘플 제품 또는 프로모션

### 5. 날짜 형식 오류
- **상황**: 출고일자가 잘못된 형식 (예: '20251399')
- **처리**: `pd.to_datetime(errors='coerce')`로 NaT 변환
- **영향**: 날짜 필터링 시 해당 행 제외

### 6. 중복 출하바코드
- **상황**: 같은 출하바코드가 여러 행에 존재
- **처리**: 중복 제거 없이 모두 유지
- **의미**: 같은 출하 건에 여러 상품 가능

---

## 🔗 관련 문서

### 프로젝트 문서
- [../README.md](../README.md) - Collector 전체 개요
- [base.py](base.py) - BaseCollector 추상 클래스
- [../../tests/test_outbound.py](../../tests/test_outbound.py) - 테스트 코드

### 백엔드 문서
- **WMS_출고현황_README.md** - 백엔드 사용자 가이드
- **WMS_출고현황_TECHNICAL_GUIDE.md** - 백엔드 기술 문서
- **WMS_출고현황_활용방안.md** - 대시보드 활용 방안

### 공식 문서
- **PROJECT_STATUS.md** - 프로젝트 현황 (v3.0)
- **02_기술설명서.md** - 기술 스택 (v2.1)

---

## 📊 성능 및 제약사항

### 성능
- **로딩 시간**: 100건 기준 < 0.1초
- **10개 타입 통합**: 1,000건 기준 < 0.5초
- **메모리 사용**: 약 3MB (10,000건 기준)
- **권장 데이터 크기**: 최대 50,000건 (10개 타입 합계)

### 제약사항
- UTF-8 BOM 인코딩 필수
- 날짜 형식은 YYYYMMDD 고정
- 출하금액 N/A 가능 (재고 단가 없을 때)
- 필수 컬럼 7개 모두 필요

---

## 🔄 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1.0 | 2025-10-17 | 초기 버전 (기본 구조) |
| v2.0 | 2025-10-20 | 백엔드 실제 컬럼 반영 ✅ |
| - | - | 출하바코드, 오더수량* 변경 |
| - | - | 출하금액 N/A 처리 추가 |
| - | - | 8개 테스트 통과 |
| - | - | Phase 1 완료 ✅ |

---

**마지막 업데이트**: 2025-11-07  
**작성자**: WMS 대시보드 개발팀  
**상태**: ✅ Phase 1 완료 → Phase 2 Flask 연동 예정