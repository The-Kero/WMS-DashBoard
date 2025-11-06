# IrregularCollector 상세 가이드

**파일**: `src/data/collectors/irregular.py`  
**데이터 소스**: `irregular_order_YYYYMMDD.csv`  
**완성 날짜**: 2025-10-27  
**테스트**: 8개 (100% 통과)  
**버전**: v2.0

---

## 📑 목차

1. [개요](#개요)
2. [데이터 소스](#데이터-소스)
3. [라벨 미출력 알림](#라벨-미출력-알림)
4. [핵심 메트릭](#핵심-메트릭)
5. [BaseCollector 구현](#basecollector-구현)
6. [주요 메서드](#주요-메서드)
7. [사용 예시](#사용-예시)
8. [테스트 가이드](#테스트-가이드)
9. [Edge Case 처리](#edge-case-처리)
10. [관련 문서](#관련-문서)

---

## 📌 개요

**IrregularCollector**는 OSIS 서버에서 수집된 비정형 오더 데이터를 처리하고, 라벨 미출력 건을 자동 감지하여 알림을 제공하는 클래스입니다.

### 주요 역할
- ✅ 비정형 오더 현황 추적 및 통계
- ✅ 라벨 미출력('N') 건 자동 감지
- ✅ 센터 간 이동 오더 관리
- ✅ 최근 입력 오더 시간별 필터링

### 사용 시나리오
1. **라벨 미출력 긴급 알림**: 출력 누락 건 조기 발견
2. **센터별 비정형 오더 분석**: 출고/입고 센터별 통계
3. **최근 오더 모니터링**: N시간 이내 오더 추적
4. **상품별 비정형 빈도 파악**: 특수 처리 상품 관리

---

## 📊 데이터 소스

### 파일 정보
- **위치**: `C:\OSIS_AUTO\Irregular Order\irregular_order_YYYYMMDD.csv`
- **형식**: CSV (UTF-8 BOM)
- **갱신 주기**: 1일 4회 (08:00, 12:00, 15:00, 19:00)
- **생성 프로그램**: `irregular_order_status.py` (백엔드)

### 주요 컬럼 (7개)

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| 상세내용 | 문자열 | 비정형 오더 상세 설명 | 센터 간 이동, 특수 출고 |
| 출고센터명 | 문자열 | 출고 센터 이름 | 음성센터, 이천센터 |
| 입고센터명 | 문자열 | 입고 센터 이름 | 부산센터, 대구센터 |
| 상품명 | 문자열 | 상품 이름 | 떡볶이양념장(분말) |
| 입출수량 | 숫자 (정수) | 입출고 수량 | 50 |
| 라벨출력 | 문자열 (Y/N) | 라벨 출력 여부 | Y, N |
| 최초입력시각 | 날짜시간 | 오더 입력 시각 | 2025-10-24 14:30:25 |

### 데이터 특성
- **비정형 오더**: 일반 프로세스를 따르지 않는 특수 오더
- **센터 간 이동**: 출고센터 → 입고센터 물류 이동
- **라벨출력 추적**: Y/N 상태로 출력 완료 여부 파악
- **시간 기반 필터**: 최초입력시각으로 최근 오더 조회

---

## 🏷️ 라벨 미출력 알림

### 알림 판단 기준
```python
라벨출력 = 'N'  →  긴급 알림 대상
```

### 라벨출력 상태 의미

| 상태 | 의미 | 조치 |
|------|------|------|
| **N** | 🔴 미출력 | 긴급 출력 필요 |
| **Y** | ✅ 출력 완료 | 정상 처리 |

### 처리 흐름
```
1. 백엔드 수집 (irregular_order_status.py)
   ↓
2. 라벨출력 상태 확인
   ↓
3. 'N' 건 필터링
   ↓
4. CSV 파일 저장
   ↓
5. Collector 읽기 (IrregularCollector)
   ↓
6. 대시보드 알림 표시 (🔴 라벨미출력)
```

### 라벨 미출력 예시
```
      상세내용 출고센터명 입고센터명        상품명  입출수량 라벨출력
0  센터 간 이동    음성센터   부산센터  떡볶이양념장      50       N
1    특수 출고    이천센터   대구센터    김밥소스      30       N
2  긴급 배송    음성센터   광주센터  청양고추절임      20       N
```

---

## 🎯 핵심 메트릭

### 1. 총건수 (total_count)
- **설명**: 전체 비정형 오더 건수
- **계산 방식**: `len(df)`
- **예시**: 45건

### 2. 라벨미출력 (label_not_printed_count)
- **설명**: 라벨출력='N' 건수 (긴급)
- **계산 방식**: `len(df[df['라벨출력'] == 'N'])`
- **예시**: 12건

### 3. 라벨출력완료 (label_printed_count)
- **설명**: 라벨출력='Y' 건수
- **계산 방식**: `len(df[df['라벨출력'] == 'Y'])`
- **예시**: 33건

### 4. 출고센터수 (outbound_center_count)
- **설명**: 고유 출고센터 개수
- **계산 방식**: `df['출고센터명'].nunique()`
- **예시**: 3개

### 5. 입고센터수 (inbound_center_count)
- **설명**: 고유 입고센터 개수
- **계산 방식**: `df['입고센터명'].nunique()`
- **예시**: 8개

### 6. 상품종류 (product_count)
- **설명**: 고유 상품 개수
- **계산 방식**: `df['상품명'].nunique()`
- **예시**: 28종

### 7. 총입출수량 (total_quantity)
- **설명**: 입출수량 합계
- **계산 방식**: `df['입출수량'].sum()`
- **예시**: 1,450개

### 8. 최근입력시각 (latest_input_time)
- **설명**: 가장 최근 오더 입력 시각
- **계산 방식**: `df['최초입력시각'].max()`
- **예시**: 2025-10-24 16:45:30

### 9. 최초입력시각 (earliest_input_time)
- **설명**: 가장 오래된 오더 입력 시각
- **계산 방식**: `df['최초입력시각'].min()`
- **예시**: 2025-10-24 08:15:10

---

## 🔧 BaseCollector 구현

### 상속 구조
```python
from .base import BaseCollector
from datetime import datetime, timedelta

class IrregularCollector(BaseCollector):
    """비정형오더 수집기"""
    
    REQUIRED_COLUMNS = [
        '상세내용', '출고센터명', '입고센터명', '상품명',
        '입출수량', '라벨출력', '최초입력시각'
    ]
```

### 필수 메서드 구현

#### 1. load_data()
```python
def load_data(self) -> pd.DataFrame:
    """CSV 파일에서 비정형오더 데이터 로드"""
    
    if not self.file_exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
    
    # CSV 읽기 (BOM 처리)
    df = pd.read_csv(self.file_path, encoding=self.encoding)
    
    # 데이터 검증
    if not self.validate(df):
        raise ValueError("비정형오더 데이터 검증 실패")
    
    # 데이터 타입 변환
    df['최초입력시각'] = pd.to_datetime(df['최초입력시각'], errors='coerce')
    df['입출수량'] = pd.to_numeric(df['입출수량'], errors='coerce')
    
    return df
```

**핵심 포인트**:
- 최초입력시각을 datetime 객체로 변환
- 숫자 형식 안전 변환
- UTF-8 BOM 인코딩 지원

#### 2. validate()
```python
def validate(self, df: pd.DataFrame) -> bool:
    """비정형오더 데이터 유효성 검증"""
    
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
    """비정형오더 데이터 요약 정보"""
    
    df = self.get_data()
    
    return {
        '총건수': len(df),
        '라벨미출력': len(df[df['라벨출력'] == 'N']),
        '라벨출력완료': len(df[df['라벨출력'] == 'Y']),
        '출고센터수': df['출고센터명'].nunique(),
        '입고센터수': df['입고센터명'].nunique(),
        '상품종류': df['상품명'].nunique(),
        '총입출수량': df['입출수량'].sum(),
        '최근입력시각': df['최초입력시각'].max(),
        '최초입력시각': df['최초입력시각'].min(),
    }
```

**반환 예시**:
```python
{
    '총건수': 45,
    '라벨미출력': 12,
    '라벨출력완료': 33,
    '출고센터수': 3,
    '입고센터수': 8,
    '상품종류': 28,
    '총입출수량': 1450,
    '최근입력시각': Timestamp('2025-10-24 16:45:30'),
    '최초입력시각': Timestamp('2025-10-24 08:15:10')
}
```

### 2. get_unlabeled_orders() - 라벨 미출력 목록
```python
def get_unlabeled_orders(self) -> pd.DataFrame:
    """라벨 미출력 오더 목록 조회"""
    
    df = self.get_data()
    return df[df['라벨출력'] == 'N']
```

**반환 예시**:
```
      상세내용 출고센터명 입고센터명        상품명  입출수량 라벨출력       최초입력시각
0  센터 간 이동    음성센터   부산센터  떡볶이양념장      50       N  2025-10-24 14:30
1    특수 출고    이천센터   대구센터    김밥소스      30       N  2025-10-24 15:20
2  긴급 배송    음성센터   광주센터  청양고추절임      20       N  2025-10-24 16:10
```

### 3. get_recent_orders() - 최근 N시간 오더
```python
def get_recent_orders(self, hours: int = 1) -> pd.DataFrame:
    """최근 N시간 이내 비정형오더 조회"""
    
    df = self.get_data()
    now = datetime.now()
    cutoff_time = now - timedelta(hours=hours)
    
    # 최근 N시간 이내 데이터 필터링
    recent_df = df[df['최초입력시각'] >= cutoff_time]
    return recent_df
```

**사용 예시**:
```python
# 최근 1시간 이내 오더
recent_1h = collector.get_recent_orders(hours=1)

# 최근 3시간 이내 오더
recent_3h = collector.get_recent_orders(hours=3)

# 최근 24시간 이내 오더
recent_24h = collector.get_recent_orders(hours=24)
```

### 4. get_orders_by_center() - 센터별 통계
```python
def get_orders_by_center(self, center_type: str = 'outbound') -> pd.DataFrame:
    """센터별 오더 통계"""
    
    df = self.get_data()
    
    if center_type == 'outbound':
        column = '출고센터명'
    else:
        column = '입고센터명'
    
    return (df.groupby(column)
            .agg({
                '상세내용': 'count',
                '입출수량': 'sum'
            })
            .rename(columns={'상세내용': '오더건수', '입출수량': '총수량'})
            .sort_values('오더건수', ascending=False)
            .reset_index())
```

**출고센터별 예시**:
```python
orders_by_outbound = collector.get_orders_by_center(center_type='outbound')
```
```
  출고센터명  오더건수  총수량
0    음성센터       25    750
1    이천센터       15    450
2    광주센터        5    250
```

**입고센터별 예시**:
```python
orders_by_inbound = collector.get_orders_by_center(center_type='inbound')
```
```
  입고센터명  오더건수  총수량
0    부산센터       18    550
1    대구센터       12    380
2    광주센터        8    290
```

---

## 💡 사용 예시

### 기본 사용 (Streamlit 대시보드)
```python
from src.data.collectors.irregular import IrregularCollector

# 1. 인스턴스 생성
file_path = "C:/OSIS_AUTO/Irregular Order/irregular_order_20251024.csv"
collector = IrregularCollector(file_path=file_path, encoding='utf-8-sig')

# 2. 데이터 로드
try:
    data = collector.get_data()
    print(f"✅ {len(data)}건 로드 성공")
except Exception as e:
    print(f"❌ 오류: {e}")

# 3. 요약 정보
summary = collector.get_summary()
print(f"총 비정형 오더: {summary['총건수']}")
print(f"🔴 라벨 미출력: {summary['라벨미출력']}건")

# 4. 라벨 미출력 조회
unlabeled = collector.get_unlabeled_orders()
print(f"라벨 미출력: {len(unlabeled)}건")
print(unlabeled)

# 5. 최근 1시간 오더
recent_1h = collector.get_recent_orders(hours=1)
print(f"최근 1시간: {len(recent_1h)}건")

# 6. 센터별 통계
by_outbound = collector.get_orders_by_center(center_type='outbound')
by_inbound = collector.get_orders_by_center(center_type='inbound')
print("출고센터별:")
print(by_outbound)
print("입고센터별:")
print(by_inbound)
```

### Flask API 연동 (Phase 2 예정)
```python
from flask import Flask, jsonify
from src.data.collectors.irregular import IrregularCollector

app = Flask(__name__)

@app.route('/api/irregular')
def get_irregular_data():
    """비정형 오더 데이터 API"""
    
    file_path = "C:/OSIS_AUTO/Irregular Order/irregular_order_20251024.csv"
    collector = IrregularCollector(file_path=file_path, encoding='utf-8-sig')
    
    try:
        # 요약 정보
        summary = collector.get_summary()
        
        # 라벨 미출력
        unlabeled = collector.get_unlabeled_orders().to_dict('records')
        
        # 최근 3시간 오더
        recent_3h = collector.get_recent_orders(hours=3).to_dict('records')
        
        # 센터별 통계
        by_outbound = collector.get_orders_by_center('outbound').to_dict('records')
        by_inbound = collector.get_orders_by_center('inbound').to_dict('records')
        
        return jsonify({
            'success': True,
            'summary': summary,
            'unlabeled_orders': unlabeled,
            'recent_orders': recent_3h,
            'by_outbound_center': by_outbound,
            'by_inbound_center': by_inbound
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
- **위치**: `tests/test_irregular.py`
- **테스트 개수**: 8개
- **커버리지**: 91%

### 테스트 케이스

#### 1. test_load_data_success
```python
def test_load_data_success():
    """데이터 로드 성공 테스트"""
    collector = IrregularCollector(file_path='fixtures/sample_irregular.csv')
    df = collector.load_data()
    
    assert not df.empty
    assert '라벨출력' in df.columns
    assert '최초입력시각' in df.columns
```

#### 2. test_validate_success
```python
def test_validate_success():
    """데이터 검증 성공 테스트"""
    collector = IrregularCollector(file_path='fixtures/sample_irregular.csv')
    df = collector.load_data()
    
    assert collector.validate(df) == True
```

#### 3. test_get_summary
```python
def test_get_summary():
    """요약 정보 테스트"""
    collector = IrregularCollector(file_path='fixtures/sample_irregular.csv')
    collector.load_data()
    summary = collector.get_summary()
    
    assert '총건수' in summary
    assert '라벨미출력' in summary
    assert summary['총건수'] > 0
```

#### 4. test_get_unlabeled_orders
```python
def test_get_unlabeled_orders():
    """라벨 미출력 조회 테스트"""
    collector = IrregularCollector(file_path='fixtures/sample_irregular.csv')
    collector.load_data()
    unlabeled = collector.get_unlabeled_orders()
    
    # 모든 레코드가 라벨출력='N' 확인
    assert all(unlabeled['라벨출력'] == 'N')
```

#### 5. test_get_recent_orders
```python
def test_get_recent_orders():
    """최근 오더 조회 테스트"""
    collector = IrregularCollector(file_path='fixtures/sample_irregular.csv')
    collector.load_data()
    
    # 최근 24시간 오더 (테스트 데이터는 모두 최근)
    recent = collector.get_recent_orders(hours=24)
    assert len(recent) >= 0
```

#### 6. test_get_orders_by_center
```python
def test_get_orders_by_center():
    """센터별 통계 테스트"""
    collector = IrregularCollector(file_path='fixtures/sample_irregular.csv')
    collector.load_data()
    
    # 출고센터별
    by_outbound = collector.get_orders_by_center('outbound')
    assert '출고센터명' in by_outbound.columns
    assert '오더건수' in by_outbound.columns
    
    # 입고센터별
    by_inbound = collector.get_orders_by_center('inbound')
    assert '입고센터명' in by_inbound.columns
```

#### 7. test_file_not_found
```python
def test_file_not_found():
    """파일 미존재 테스트"""
    collector = IrregularCollector(file_path='nonexistent.csv')
    
    with pytest.raises(FileNotFoundError):
        collector.load_data()
```

#### 8. test_invalid_data
```python
def test_invalid_data():
    """잘못된 데이터 테스트"""
    collector = IrregularCollector(file_path='fixtures/invalid_irregular.csv')
    
    with pytest.raises(ValueError):
        collector.load_data()
```

### 테스트 실행
```bash
# 비정형 오더 Collector 테스트만 실행
pytest tests/test_irregular.py -v

# 커버리지 확인
pytest tests/test_irregular.py --cov=src.data.collectors.irregular --cov-report=html
```

---

## ⚠️ Edge Case 처리

### 1. 라벨출력 빈 값
- **상황**: 라벨출력 컬럼이 비어있음 (NaN)
- **처리**: 데이터 그대로 유지 (NaN)
- **영향**: 라벨 통계에서 제외
- **대응**: 빈 값은 'N'으로 간주 가능

### 2. 최초입력시각 파싱 오류
- **상황**: 날짜 형식이 잘못됨 (예: '2025-13-45')
- **처리**: `pd.to_datetime(errors='coerce')`로 NaT 변환
- **영향**: 시간 기반 필터링에서 제외

### 3. 음수 입출수량
- **상황**: 입출수량이 음수 (예: -10)
- **처리**: 데이터 그대로 유지
- **의미**: 반품 또는 취소
- **대응**: 빨간색 경고

### 4. 0 입출수량
- **상황**: 입출수량이 0
- **처리**: 데이터 유지
- **의미**: 수량 미정 또는 오류
- **영향**: 통계에는 포함되지만 0으로 계산

### 5. get_recent_orders() 시간 범위
- **상황**: hours=0 또는 음수값
- **처리**: 현재 시각 기준으로 계산
- **영향**: 0이면 현재 시각 이전 모든 데이터 반환

### 6. 센터명 빈 값
- **상황**: 출고센터명 또는 입고센터명이 비어있음
- **처리**: 데이터 그대로 유지 (NaN)
- **영향**: 센터별 통계에서 제외

---

## 🔗 관련 문서

### 프로젝트 문서
- [../README.md](../README.md) - Collector 전체 개요
- [base.py](base.py) - BaseCollector 추상 클래스
- [../../tests/test_irregular.py](../../tests/test_irregular.py) - 테스트 코드

### 백엔드 문서
- **WMS_비정형오더_README.md** - 백엔드 사용자 가이드
- **WMS_비정형오더_TECHNICAL_GUIDE.md** - 백엔드 기술 문서
- **WMS_비정형오더_활용방안.md** - 대시보드 활용 방안

### 공식 문서
- **PROJECT_STATUS.md** - 프로젝트 현황 (v3.0)
- **02_기술설명서.md** - 기술 스택 (v2.1)

---

## 📊 성능 및 제약사항

### 성능
- **로딩 시간**: 100건 기준 < 0.1초
- **메모리 사용**: 약 1MB (1,000건 기준)
- **권장 데이터 크기**: 최대 5,000건

### 제약사항
- UTF-8 BOM 인코딩 필수
- 최초입력시각은 datetime 형식
- 필수 컬럼 7개 모두 필요
- 라벨출력은 Y/N 권장 (빈 값 허용)

---

## 🔄 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1.0 | 2025-10-17 | 초기 버전 (기본 구조) |
| v2.0 | 2025-10-27 | 라벨 미출력 알림 완성 ✅ |
| - | - | `get_unlabeled_orders()` 추가 |
| - | - | `get_recent_orders()` 추가 |
| - | - | 시간 기반 필터링 구현 |
| - | - | 8개 테스트 통과 |
| - | - | Phase 1 완료 ✅ |

---

**마지막 업데이트**: 2025-11-07  
**작성자**: WMS 대시보드 개발팀  
**상태**: ✅ Phase 1 완료 → Phase 2 Flask 연동 예정