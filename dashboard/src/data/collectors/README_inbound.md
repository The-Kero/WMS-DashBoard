# InboundCollector 상세 가이드

**파일**: `src/data/collectors/inbound.py`  
**데이터 소스**: `integrated_inbound_YYYYMMDD.csv`  
**완성 날짜**: 2025-11-04  
**테스트**: 8개 (100% 통과)  
**버전**: v1.0

---

## 📑 목차

1. [개요](#개요)
2. [데이터 소스](#데이터-소스)
3. [핵심 메트릭](#핵심-메트릭)
4. [BaseCollector 구현](#basecollector-구현)
5. [주요 메서드](#주요-메서드)
6. [사용 예시](#사용-예시)
7. [테스트 가이드](#테스트-가이드)
8. [Edge Case 처리](#edge-case-처리)
9. [관련 문서](#관련-문서)

---

## 📌 개요

**InboundCollector**는 OSIS 서버에서 수집된 입고 예정 및 실제 입고 데이터를 처리하는 클래스입니다.

### 주요 역할
- ✅ 입고예정정보와 입고실적 데이터 통합 처리
- ✅ 진척률 기반 입고 현황 분석
- ✅ 공급사별, 상품별 입고 통계 제공
- ✅ 입고 완료/진행중/미입고 상태 구분

### 사용 시나리오
1. **입고 진행 모니터링**: 당일 입고 예정 대비 실적 확인
2. **공급사 관리**: 공급사별 입고량 및 진척률 추적
3. **상품 재고 예측**: 입고 예정 수량으로 재고 계획 수립
4. **지연 파악**: 진척률 낮은 입고 건 조기 발견

---

## 📊 데이터 소스

### 파일 정보
- **위치**: `C:\OSIS_AUTO\Inbound Status\integrated_inbound_YYYYMMDD.csv`
- **형식**: CSV (UTF-8 BOM)
- **갱신 주기**: 1일 4회 (08:00, 12:00, 15:00, 19:00)
- **생성 프로그램**: `inbound_status.py` (백엔드)

### 주요 컬럼 (12개)

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| 입고예정일 | 날짜 (YYYYMMDD) | 입고 예정 날짜 | 20251024 |
| 입고예정번호 | 문자열 | 입고 문서 번호 (고유키) | 0003171801 |
| 공급사명 | 문자열 | 공급업체 또는 센터명 | 음성, 주식회사 희푸드 |
| 입고유형 | 숫자 | 입고 타입 코드 | 40, 110 |
| 상품 | 문자열 | 상품 코드 | 41033876 |
| 상품명 | 문자열 | 상품 이름 | 떡볶이양념장(분말) |
| 단위및규격 | 문자열 | 포장 단위 | PK, EA |
| 소비기한 | 날짜 (YYYYMMDD) | 유통기한 | 20260624 |
| 기본로케이션 | 문자열 | 입고 로케이션 | A-01-01-01 |
| 입고예정수량 | 숫자 (정수) | 예정 수량 | 150 |
| 총입고수량 | 숫자 (정수) | 실제 입고된 수량 | 150 |
| 진척률 | 숫자 (실수) | 입고 진척률 (%) | 100.0 |

### 데이터 특성
- **레코드 통합**: 같은 입고예정번호 + 상품 조합을 자동 병합
- **진척률 계산**: (총입고수량 / 입고예정수량) × 100
- **FIFO 관리**: 소비기한 기준 선입선출 검증 가능

---

## 🎯 핵심 메트릭

### 1. 총_입고건수 (total_count)
- **설명**: 입고예정번호 기준 전체 입고 건수
- **계산 방식**: `len(df)`
- **예시**: 57건

### 2. 총_입고예정수량 (total_expected_quantity)
- **설명**: 입고 예정 수량 합계
- **계산 방식**: `df['입고예정수량'].sum()`
- **예시**: 5,420개

### 3. 총_입고수량 (total_actual_quantity)
- **설명**: 실제 입고된 수량 합계
- **계산 방식**: `df['총입고수량'].sum()`
- **예시**: 5,120개

### 4. 평균_진척률 (avg_progress)
- **설명**: 전체 입고 건의 평균 진척률
- **계산 방식**: `df['진척률'].mean()`
- **예시**: 94.5%

### 5. 공급사_수 (supplier_count)
- **설명**: 고유 공급사 개수
- **계산 방식**: `df['공급사명'].nunique()`
- **예시**: 12개

### 6. 상품_종류 (product_count)
- **설명**: 고유 상품 개수
- **계산 방식**: `df['상품'].nunique()`
- **예시**: 45종

---

## 🔧 BaseCollector 구현

### 상속 구조
```python
from .base import BaseCollector

class InboundCollector(BaseCollector):
    """입고정보 수집기"""
    
    REQUIRED_COLUMNS = [
        '입고예정일', '입고예정번호', '공급사명', '입고유형',
        '상품', '상품명', '단위및규격', '소비기한',
        '기본로케이션', '입고예정수량', '총입고수량', '진척률'
    ]
```

### 필수 메서드 구현

#### 1. load_data()
```python
def load_data(self) -> pd.DataFrame:
    """CSV 파일에서 입고 데이터 로드"""
    
    # 파일 존재 확인
    if not self.file_exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
    
    # CSV 읽기 (UTF-8 BOM)
    df = pd.read_csv(self.file_path, encoding=self.encoding)
    
    # 데이터 검증
    if not self.validate(df):
        raise ValueError("입고 데이터 검증 실패")
    
    # 데이터 타입 변환
    df['입고예정일'] = pd.to_datetime(df['입고예정일'], format='%Y%m%d', errors='coerce')
    df['소비기한'] = pd.to_datetime(df['소비기한'], format='%Y%m%d', errors='coerce')
    df['입고예정수량'] = pd.to_numeric(df['입고예정수량'], errors='coerce')
    df['총입고수량'] = pd.to_numeric(df['총입고수량'], errors='coerce')
    df['진척률'] = pd.to_numeric(df['진척률'], errors='coerce')
    
    return df
```

**핵심 포인트**:
- UTF-8 BOM 인코딩 지원 (한글 처리)
- 날짜 형식 자동 변환 (YYYYMMDD → datetime)
- 숫자 형식 안전 변환 (errors='coerce')

#### 2. validate()
```python
def validate(self, df: pd.DataFrame) -> bool:
    """입고 데이터 유효성 검증"""
    
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

**검증 항목**:
1. 필수 컬럼 12개 존재 여부
2. DataFrame이 비어있지 않은지

---

## 💡 주요 메서드

### 1. get_summary() - 요약 정보
```python
def get_summary(self) -> dict:
    """입고 데이터 요약 정보"""
    
    df = self.get_data()
    
    # 진척률 기반 통계
    입고완료 = df[df['진척률'] >= 100.0]
    진행중 = df[(df['진척률'] > 0) & (df['진척률'] < 100.0)]
    미입고 = df[df['진척률'] == 0.0]
    
    return {
        '총_입고건수': len(df),
        '입고완료건수': len(입고완료),
        '진행중건수': len(진행중),
        '미입고건수': len(미입고),
        '총_입고예정수량': df['입고예정수량'].sum(),
        '총_입고수량': df['총입고수량'].sum(),
        '평균_진척률': df['진척률'].mean(),
        '공급사_수': df['공급사명'].nunique(),
        '상품_종류': df['상품'].nunique(),
        '최근_입고예정일': df['입고예정일'].max(),
        '최초_입고예정일': df['입고예정일'].min(),
    }
```

**반환 예시**:
```python
{
    '총_입고건수': 57,
    '입고완료건수': 52,
    '진행중건수': 3,
    '미입고건수': 2,
    '총_입고예정수량': 5420,
    '총_입고수량': 5120,
    '평균_진척률': 94.5,
    '공급사_수': 12,
    '상품_종류': 45,
    '최근_입고예정일': Timestamp('2025-10-24'),
    '최초_입고예정일': Timestamp('2025-10-24')
}
```

### 2. get_top_suppliers() - 상위 공급사
```python
def get_top_suppliers(self, n: int = 5) -> pd.DataFrame:
    """상위 공급사 목록 (입고수량 기준)"""
    
    df = self.get_data()
    return (df.groupby('공급사명')
            .agg({
                '총입고수량': 'sum',
                '입고예정번호': 'count'
            })
            .rename(columns={'입고예정번호': '입고건수'})
            .sort_values('총입고수량', ascending=False)
            .head(n)
            .reset_index())
```

**반환 예시**:
```
       공급사명  총입고수량  입고건수
0          음성     1500      15
1  주식회사 희푸드      980      12
2        이천센터      750       8
```

### 3. get_pending_inbounds() - 미완료 입고
```python
def get_pending_inbounds(self) -> pd.DataFrame:
    """진척률 < 100% 입고 목록"""
    
    df = self.get_data()
    return df[df['진척률'] < 100.0].sort_values('입고예정일')
```

### 4. get_completed_inbounds() - 완료 입고
```python
def get_completed_inbounds(self) -> pd.DataFrame:
    """진척률 100% 입고 목록"""
    
    df = self.get_data()
    return df[df['진척률'] >= 100.0].sort_values('입고예정일', ascending=False)
```

---

## 💡 사용 예시

### 기본 사용 (Streamlit 대시보드)
```python
from src.data.collectors.inbound import InboundCollector

# 1. 인스턴스 생성
file_path = "C:/OSIS_AUTO/Inbound Status/integrated_inbound_20251024.csv"
collector = InboundCollector(file_path=file_path, encoding='utf-8-sig')

# 2. 데이터 로드 및 검증
try:
    data = collector.get_data()
    print(f"✅ {len(data)}건 로드 성공")
except Exception as e:
    print(f"❌ 오류: {e}")

# 3. 요약 정보 조회
summary = collector.get_summary()
print(f"총 입고건수: {summary['총_입고건수']}")
print(f"평균 진척률: {summary['평균_진척률']:.1f}%")

# 4. 상위 공급사 조회
top_suppliers = collector.get_top_suppliers(n=10)
print(top_suppliers)

# 5. 미완료 입고 조회
pending = collector.get_pending_inbounds()
print(f"미완료 입고: {len(pending)}건")
```

### Flask API 연동 (Phase 2 예정)
```python
from flask import Flask, jsonify
from src.data.collectors.inbound import InboundCollector

app = Flask(__name__)

@app.route('/api/inbound')
def get_inbound_data():
    """입고 데이터 API"""
    
    file_path = "C:/OSIS_AUTO/Inbound Status/integrated_inbound_20251024.csv"
    collector = InboundCollector(file_path=file_path, encoding='utf-8-sig')
    
    try:
        # 요약 정보
        summary = collector.get_summary()
        
        # 상위 공급사
        top_suppliers = collector.get_top_suppliers(n=10).to_dict('records')
        
        # 미완료 입고
        pending = collector.get_pending_inbounds().to_dict('records')
        
        return jsonify({
            'success': True,
            'summary': summary,
            'top_suppliers': top_suppliers,
            'pending_inbounds': pending[:20]  # 최대 20건
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**API 응답 예시**:
```json
{
  "success": true,
  "summary": {
    "총_입고건수": 57,
    "평균_진척률": 94.5,
    "공급사_수": 12
  },
  "top_suppliers": [
    {"공급사명": "음성", "총입고수량": 1500, "입고건수": 15},
    {"공급사명": "희푸드", "총입고수량": 980, "입고건수": 12}
  ],
  "pending_inbounds": [...]
}
```

---

## 🧪 테스트 가이드

### 테스트 파일
- **위치**: `tests/test_inbound.py`
- **테스트 개수**: 8개
- **커버리지**: 95%

### 테스트 케이스

#### 1. test_load_data_success
```python
def test_load_data_success():
    """데이터 로드 성공 테스트"""
    collector = InboundCollector(file_path='fixtures/sample_inbound.csv')
    df = collector.load_data()
    
    assert not df.empty
    assert len(df) > 0
    assert '입고예정번호' in df.columns
```

#### 2. test_validate_success
```python
def test_validate_success():
    """데이터 검증 성공 테스트"""
    collector = InboundCollector(file_path='fixtures/sample_inbound.csv')
    df = collector.load_data()
    
    assert collector.validate(df) == True
```

#### 3. test_get_summary
```python
def test_get_summary():
    """요약 정보 테스트"""
    collector = InboundCollector(file_path='fixtures/sample_inbound.csv')
    collector.load_data()
    summary = collector.get_summary()
    
    assert '총_입고건수' in summary
    assert '평균_진척률' in summary
    assert summary['총_입고건수'] > 0
```

#### 4. test_get_top_suppliers
```python
def test_get_top_suppliers():
    """상위 공급사 조회 테스트"""
    collector = InboundCollector(file_path='fixtures/sample_inbound.csv')
    collector.load_data()
    top = collector.get_top_suppliers(n=5)
    
    assert len(top) <= 5
    assert '공급사명' in top.columns
    assert '총입고수량' in top.columns
```

#### 5. test_get_pending_inbounds
```python
def test_get_pending_inbounds():
    """미완료 입고 조회 테스트"""
    collector = InboundCollector(file_path='fixtures/sample_inbound.csv')
    collector.load_data()
    pending = collector.get_pending_inbounds()
    
    # 모든 레코드의 진척률 < 100 확인
    assert all(pending['진척률'] < 100.0)
```

#### 6. test_get_completed_inbounds
```python
def test_get_completed_inbounds():
    """완료 입고 조회 테스트"""
    collector = InboundCollector(file_path='fixtures/sample_inbound.csv')
    collector.load_data()
    completed = collector.get_completed_inbounds()
    
    # 모든 레코드의 진척률 >= 100 확인
    assert all(completed['진척률'] >= 100.0)
```

#### 7. test_file_not_found
```python
def test_file_not_found():
    """파일 미존재 테스트"""
    collector = InboundCollector(file_path='nonexistent.csv')
    
    with pytest.raises(FileNotFoundError):
        collector.load_data()
```

#### 8. test_invalid_data
```python
def test_invalid_data():
    """잘못된 데이터 테스트"""
    collector = InboundCollector(file_path='fixtures/invalid_inbound.csv')
    
    with pytest.raises(ValueError):
        collector.load_data()
```

### 테스트 실행
```bash
# 입고 Collector 테스트만 실행
pytest tests/test_inbound.py -v

# 커버리지 확인
pytest tests/test_inbound.py --cov=src.data.collectors.inbound --cov-report=html
```

---

## ⚠️ Edge Case 처리

### 1. 빈 파일
- **상황**: CSV 파일이 헤더만 있고 데이터가 없음
- **처리**: `validate()` 메서드에서 False 반환
- **응답**: "데이터가 비어있습니다" 오류 메시지

### 2. 필수 컬럼 누락
- **상황**: CSV 파일에 필수 컬럼 일부가 없음
- **처리**: `validate()` 메서드에서 누락된 컬럼 출력 후 False 반환
- **응답**: "누락된 컬럼: {'진척률', '공급사명'}" 오류 메시지

### 3. 날짜 형식 오류
- **상황**: '입고예정일' 컬럼에 잘못된 날짜 (예: '20251399')
- **처리**: `pd.to_datetime(errors='coerce')`로 NaT 변환
- **영향**: 날짜 기반 필터링 시 해당 행 제외

### 4. 음수 진척률
- **상황**: 진척률이 음수값 (예: -10.5)
- **처리**: 데이터 그대로 유지 (비정상 데이터로 표시)
- **대응**: 대시보드에서 빨간색 경고로 표시

### 5. 100% 초과 진척률
- **상황**: 진척률이 100 초과 (예: 105.2%)
- **처리**: 데이터 그대로 유지 (초과 입고 표시)
- **의미**: 입고예정수량보다 많이 입고됨

### 6. 인코딩 문제
- **상황**: 한글 깨짐 (UTF-8 BOM이 아닌 경우)
- **처리**: `encoding='utf-8-sig'` 파라미터로 BOM 처리
- **대안**: 'cp949' 인코딩 시도 가능

---

## 🔗 관련 문서

### 프로젝트 문서
- [../README.md](../README.md) - Collector 전체 개요
- [base.py](base.py) - BaseCollector 추상 클래스
- [../../tests/test_inbound.py](../../tests/test_inbound.py) - 테스트 코드

### 백엔드 문서
- **WMS_입고현황_README.md** - 백엔드 사용자 가이드
- **WMS_입고현황_TECHNICAL_GUIDE.md** - 백엔드 기술 문서
- **WMS_입고현황_활용방안.md** - 대시보드 활용 방안

### 공식 문서
- **PROJECT_STATUS.md** - 프로젝트 현황 (v3.0)
- **02_기술설명서.md** - 기술 스택 (v2.1)

---

## 📊 성능 및 제약사항

### 성능
- **로딩 시간**: 100건 기준 < 0.1초
- **메모리 사용**: 약 2MB (1,000건 기준)
- **권장 데이터 크기**: 최대 10,000건

### 제약사항
- UTF-8 BOM 인코딩 필수 (한글 지원)
- 날짜 형식은 YYYYMMDD 고정
- 필수 컬럼 12개 모두 필요

---

## 🔄 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1.0 | 2025-11-04 | 초기 버전 완성 |
| - | - | BaseCollector 상속 구조 |
| - | - | 8개 테스트 통과 |
| - | - | Phase 1 완료 ✅ |

---

**마지막 업데이트**: 2025-11-07  
**작성자**: WMS 대시보드 개발팀  
**상태**: ✅ Phase 1 완료 → Phase 2 Flask 연동 예정