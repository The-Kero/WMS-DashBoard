# DeleteCollector 상세 가이드

**파일**: `src/data/collectors/delete.py`  
**데이터 소스**: `delete_status_YYYYMMDD.csv`  
**완성 날짜**: 2025-10-27  
**테스트**: 8개 (100% 통과)  
**버전**: v3.0

---

## 📑 목차

1. [개요](#개요)
2. [데이터 소스](#데이터-소스)
3. [18시 이후 삭제 알림](#18시-이후-삭제-알림)
4. [핵심 메트릭](#핵심-메트릭)
5. [BaseCollector 구현](#basecollector-구현)
6. [주요 메서드](#주요-메서드)
7. [사용 예시](#사용-예시)
8. [테스트 가이드](#테스트-가이드)
9. [Edge Case 처리](#edge-case-처리)
10. [관련 문서](#관련-문서)

---

## 📌 개요

**DeleteCollector**는 OSIS 서버에서 수집된 삭제 현황 데이터를 처리하고, 18시 이후 삭제 건을 자동 감지하여 알림을 제공하는 클래스입니다.

### 주요 역할
- ✅ 삭제 처리 현황 추적 및 통계
- ✅ 18시(18:00) 이후 삭제 건 자동 감지
- ✅ 알림여부='Y' 처리 및 알림 시각 기록
- ✅ 배송처별, 상품별 삭제 통계 제공

### 사용 시나리오
1. **18시 이후 긴급 삭제 알림**: 당일 마감 전 처리 필요
2. **배송처별 삭제 패턴 분석**: 특정 배송처 집중 관리
3. **상품별 삭제 빈도 파악**: 문제 상품 조기 발견
4. **라벨출력 추적**: 출력 완료 여부 모니터링

---

## 📊 데이터 소스

### 파일 정보
- **위치**: `C:\OSIS_AUTO\Delete Status\delete_status_YYYYMMDD.csv`
- **형식**: CSV (UTF-8 BOM)
- **갱신 주기**: 1일 4회 (08:00, 12:00, 15:00, 19:00)
- **생성 프로그램**: `delete_status.py` (백엔드)

### 주요 컬럼 (15개)

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|------------|------|------|
| 삭제처리일 | 날짜 (YYYYMMDD) | 삭제 처리 날짜 | 20251024 |
| 삭제처리시간 | 문자열 (HHMMSS) | 삭제 처리 시각 | 181500 (18:15:00) |
| 상품 | 문자열 | 상품 코드 | 41033876 |
| 상품명 | 문자열 | 상품 이름 | 떡볶이양념장(분말) |
| 단위 및 규격 | 문자열 | 포장 단위 | PK, EA |
| 삭제수량 | 숫자 (정수) | 삭제된 수량 | 50 |
| 주문일자 | 날짜 (YYYYMMDD) | 원 주문 날짜 | 20251023 |
| 배송군 | 문자열 | 배송 그룹 코드 | A01 |
| 배송처 | 문자열 | 배송처 코드 | 1001 |
| 배송처명 | 문자열 | 배송처 이름 | 부산물류센터 |
| 라벨출력 | 문자열 (Y/N) | 라벨 출력 여부 | Y, N |
| 출하바코드 | 문자열 | 출하 바코드 | 12345678901234 |
| To로케이션 | 문자열 | 이동 로케이션 | A-01-01-01 |
| 알림여부 | 문자열 (Y/N) | 18시 이후 알림 여부 | Y, N |
| 알림시각 | 날짜시간 | 알림 전송 시각 | 2025-10-24 18:30:00 |

### 데이터 특성
- **18시 이후 알림**: 삭제처리시간 >= 18:00:00 자동 감지
- **알림여부 자동 설정**: 백엔드에서 18시 이후 건을 'Y' 처리
- **배송군 집계**: 배송처별 그룹화 가능
- **라벨출력 추적**: Y/N 상태로 진행 상황 파악

---

## 🚨 18시 이후 삭제 알림

### 알림 판단 기준
```python
삭제처리시간 >= 18:00:00  →  긴급 알림 대상
```

### 알림 처리 흐름
```
1. 백엔드 수집 (delete_status.py)
   ↓
2. 삭제처리시간 >= 18:00:00 확인
   ↓
3. 알림여부 = 'Y' 설정
   ↓
4. 알림시각 = 현재시각 기록
   ↓
5. CSV 파일 저장
   ↓
6. Collector 읽기 (DeleteCollector)
   ↓
7. 대시보드 알림 표시 (🔴 긴급)
```

### 시간 파싱 로직
```python
def _parse_time(self, time_str) -> time:
    """
    HHMMSS → time 객체 변환
    
    예시:
    '181500' → time(18, 15, 0)
    '083000' → time(8, 30, 0)
    """
    try:
        if pd.isna(time_str):
            return time(0, 0, 0)
        
        time_str = str(int(time_str)).zfill(6)  # 6자리 패딩
        hour = int(time_str[0:2])
        minute = int(time_str[2:4])
        second = int(time_str[4:6])
        return time(hour, minute, second)
    except:
        return time(0, 0, 0)
```

### 18시 기준 예시
```
삭제처리시간: 175500 (17:55) → 알림 X
삭제처리시간: 180000 (18:00) → 알림 O (경계값 포함)
삭제처리시간: 181530 (18:15:30) → 알림 O
삭제처리시간: 230045 (23:00:45) → 알림 O
```

---

## 🎯 핵심 메트릭

### 1. 총건수 (total_count)
- **설명**: 전체 삭제 처리 건수
- **계산 방식**: `len(df)`
- **예시**: 127건

### 2. 18시이후삭제 (after_18_count)
- **설명**: 18:00 이후 삭제된 건수 (긴급)
- **계산 방식**: `len(df[df['삭제시각'] >= time(18, 0, 0)])`
- **예시**: 23건

### 3. 알림완료 (alerted_count)
- **설명**: 알림여부='Y' 건수
- **계산 방식**: `len(df[df['알림여부'] == 'Y'])`
- **예시**: 23건

### 4. 알림미완료 (not_alerted_count)
- **설명**: 알림여부='N' 건수
- **계산 방식**: `len(df[df['알림여부'] == 'N'])`
- **예시**: 104건

### 5. 총삭제수량 (total_quantity)
- **설명**: 삭제수량 합계
- **계산 방식**: `df['삭제수량'].sum()`
- **예시**: 3,450개

### 6. 배송처수 (destination_count)
- **설명**: 고유 배송처 개수
- **계산 방식**: `df['배송처명'].nunique()`
- **예시**: 45개

### 7. 상품종류 (product_count)
- **설명**: 고유 상품 개수
- **계산 방식**: `df['상품명'].nunique()`
- **예시**: 87종

### 8. 라벨출력완료 (label_printed_count)
- **설명**: 라벨출력='Y' 건수
- **계산 방식**: `len(df[df['라벨출력'] == 'Y'])`
- **예시**: 115건

### 9. 라벨미출력 (label_not_printed_count)
- **설명**: 라벨출력='N' 건수
- **계산 방식**: `len(df[df['라벨출력'] == 'N'])`
- **예시**: 12건

---

## 🔧 BaseCollector 구현

### 상속 구조
```python
from .base import BaseCollector
from datetime import time

class DeleteCollector(BaseCollector):
    """삭제현황 수집기"""
    
    REQUIRED_COLUMNS = [
        '삭제처리일', '삭제처리시간', '상품', '상품명', '단위 및 규격',
        '삭제수량', '주문일자', '배송군', '배송처', '배송처명',
        '라벨출력', '출하바코드', 'To로케이션', '알림여부', '알림시각'
    ]
```

### 필수 메서드 구현

#### 1. load_data()
```python
def load_data(self) -> pd.DataFrame:
    """CSV 파일에서 삭제현황 데이터 로드"""
    
    if not self.file_exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
    
    # CSV 읽기 (BOM 처리)
    df = pd.read_csv(self.file_path, encoding=self.encoding)
    
    # 데이터 검증
    if not self.validate(df):
        raise ValueError("삭제현황 데이터 검증 실패")
    
    # 데이터 타입 변환
    df['삭제처리일'] = pd.to_datetime(df['삭제처리일'], format='%Y%m%d', errors='coerce')
    df['주문일자'] = pd.to_datetime(df['주문일자'], format='%Y%m%d', errors='coerce')
    df['삭제수량'] = pd.to_numeric(df['삭제수량'], errors='coerce')
    
    # 삭제처리시간을 time 객체로 변환 (HHMMSS → HH:MM:SS)
    df['삭제시각'] = df['삭제처리시간'].apply(self._parse_time)
    
    # 알림시각 변환 (비어있을 수 있음)
    df['알림시각'] = pd.to_datetime(df['알림시각'], errors='coerce')
    
    # 알림여부 빈 값을 'N'으로 처리
    df['알림여부'] = df['알림여부'].fillna('N')
    
    return df
```

**핵심 포인트**:
- HHMMSS 형식을 time 객체로 변환
- 알림여부 빈 값 'N' 처리
- 알림시각은 NaT 허용 (알림 전 상태)

#### 2. validate()
```python
def validate(self, df: pd.DataFrame) -> bool:
    """삭제현황 데이터 유효성 검증"""
    
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
    """삭제현황 데이터 요약 정보"""
    
    df = self.get_data()
    
    # 18시 이후 삭제 건수
    after_18_count = self.count_after_18()
    
    # 알림 관련 통계
    alerted = df[df['알림여부'] == 'Y']
    not_alerted = df[df['알림여부'] == 'N']
    
    return {
        '총건수': len(df),
        '18시이후삭제': after_18_count,
        '알림완료': len(alerted),
        '알림미완료': len(not_alerted),
        '총삭제수량': df['삭제수량'].sum(),
        '배송처수': df['배송처명'].nunique(),
        '상품종류': df['상품명'].nunique(),
        '라벨출력완료': len(df[df['라벨출력'] == 'Y']),
        '라벨미출력': len(df[df['라벨출력'] == 'N']),
        '최근삭제일': df['삭제처리일'].max(),
        '최초삭제일': df['삭제처리일'].min(),
    }
```

**반환 예시**:
```python
{
    '총건수': 127,
    '18시이후삭제': 23,
    '알림완료': 23,
    '알림미완료': 104,
    '총삭제수량': 3450,
    '배송처수': 45,
    '상품종류': 87,
    '라벨출력완료': 115,
    '라벨미출력': 12,
    '최근삭제일': Timestamp('2025-10-24'),
    '최초삭제일': Timestamp('2025-10-24')
}
```

### 2. count_after_18() - 18시 이후 건수
```python
def count_after_18(self) -> int:
    """18시(18:00) 이후 삭제된 건수 계산"""
    
    df = self.get_data()
    cutoff = time(18, 0, 0)  # 18:00:00
    
    # 18시 이후 데이터 필터링
    after_18 = df[df['삭제시각'] >= cutoff]
    return len(after_18)
```

### 3. get_urgent_deletes() - 긴급 삭제 목록
```python
def get_urgent_deletes(self) -> pd.DataFrame:
    """긴급 삭제 알림 목록 (18시 이후 + 알림Y)"""
    
    df = self.get_data()
    cutoff = time(18, 0, 0)
    
    # 18시 이후이면서 알림이 Y인 데이터
    urgent = df[(df['삭제시각'] >= cutoff) & (df['알림여부'] == 'Y')]
    return urgent
```

**반환 예시**:
```
   삭제처리일 삭제시각      상품명  삭제수량 배송처명 알림여부
0  2025-10-24  18:15  떡볶이양념장      50  부산센터     Y
1  2025-10-24  19:30    김밥소스      30  대구센터     Y
2  2025-10-24  20:45  청양고추절임      20  광주센터     Y
```

### 4. get_deletes_by_delivery() - 배송처별 통계
```python
def get_deletes_by_delivery(self) -> pd.DataFrame:
    """배송처별 삭제 통계"""
    
    df = self.get_data()
    
    return (df.groupby('배송처명')
            .agg({
                '상품': 'count',
                '삭제수량': 'sum'
            })
            .rename(columns={'상품': '삭제건수', '삭제수량': '총삭제수량'})
            .sort_values('삭제건수', ascending=False)
            .reset_index())
```

**반환 예시**:
```
     배송처명  삭제건수  총삭제수량
0  부산물류센터       35       850
1  대구물류센터       28       620
2  광주물류센터       22       480
```

### 5. get_deletes_by_product() - 상품별 통계
```python
def get_deletes_by_product(self) -> pd.DataFrame:
    """상품별 삭제 통계"""
    
    df = self.get_data()
    
    return (df.groupby(['상품', '상품명'])
            .agg({
                '삭제처리일': 'count',
                '삭제수량': 'sum'
            })
            .rename(columns={'삭제처리일': '삭제건수', '삭제수량': '총삭제수량'})
            .sort_values('총삭제수량', ascending=False)
            .reset_index())
```

---

## 💡 사용 예시

### 기본 사용 (Streamlit 대시보드)
```python
from src.data.collectors.delete import DeleteCollector

# 1. 인스턴스 생성
file_path = "C:/OSIS_AUTO/Delete Status/delete_status_20251024.csv"
collector = DeleteCollector(file_path=file_path, encoding='utf-8-sig')

# 2. 데이터 로드
try:
    data = collector.get_data()
    print(f"✅ {len(data)}건 로드 성공")
except Exception as e:
    print(f"❌ 오류: {e}")

# 3. 요약 정보
summary = collector.get_summary()
print(f"총 삭제건수: {summary['총건수']}")
print(f"🔴 18시 이후: {summary['18시이후삭제']}건")

# 4. 긴급 삭제 조회
urgent = collector.get_urgent_deletes()
print(f"긴급 알림: {len(urgent)}건")
print(urgent)

# 5. 배송처별 통계
by_delivery = collector.get_deletes_by_delivery()
print(by_delivery.head(10))

# 6. 상품별 통계
by_product = collector.get_deletes_by_product()
print(by_product.head(10))
```

### Flask API 연동 (Phase 2 예정)
```python
from flask import Flask, jsonify
from src.data.collectors.delete import DeleteCollector

app = Flask(__name__)

@app.route('/api/delete')
def get_delete_data():
    """삭제 데이터 API"""
    
    file_path = "C:/OSIS_AUTO/Delete Status/delete_status_20251024.csv"
    collector = DeleteCollector(file_path=file_path, encoding='utf-8-sig')
    
    try:
        # 요약 정보
        summary = collector.get_summary()
        
        # 긴급 삭제
        urgent = collector.get_urgent_deletes().to_dict('records')
        
        # 배송처별 통계
        by_delivery = collector.get_deletes_by_delivery().to_dict('records')
        
        return jsonify({
            'success': True,
            'summary': summary,
            'urgent_deletes': urgent,
            'by_delivery': by_delivery[:10]
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
- **위치**: `tests/test_delete.py`
- **테스트 개수**: 8개
- **커버리지**: 90%

### 테스트 케이스

#### 1. test_load_data_success
```python
def test_load_data_success():
    """데이터 로드 성공 테스트"""
    collector = DeleteCollector(file_path='fixtures/sample_delete.csv')
    df = collector.load_data()
    
    assert not df.empty
    assert '삭제시각' in df.columns
    assert '알림여부' in df.columns
```

#### 2. test_time_parsing
```python
def test_time_parsing():
    """시간 파싱 테스트"""
    collector = DeleteCollector(file_path='fixtures/sample_delete.csv')
    df = collector.load_data()
    
    # time 객체로 변환 확인
    assert df['삭제시각'].dtype == 'object'
    sample_time = df['삭제시각'].iloc[0]
    assert isinstance(sample_time, time)
```

#### 3. test_count_after_18
```python
def test_count_after_18():
    """18시 이후 건수 테스트"""
    collector = DeleteCollector(file_path='fixtures/sample_delete.csv')
    collector.load_data()
    count = collector.count_after_18()
    
    assert isinstance(count, int)
    assert count >= 0
```

#### 4. test_get_summary
```python
def test_get_summary():
    """요약 정보 테스트"""
    collector = DeleteCollector(file_path='fixtures/sample_delete.csv')
    collector.load_data()
    summary = collector.get_summary()
    
    assert '총건수' in summary
    assert '18시이후삭제' in summary
    assert summary['총건수'] > 0
```

#### 5. test_get_urgent_deletes
```python
def test_get_urgent_deletes():
    """긴급 삭제 조회 테스트"""
    collector = DeleteCollector(file_path='fixtures/sample_delete.csv')
    collector.load_data()
    urgent = collector.get_urgent_deletes()
    
    # 모든 레코드가 18시 이후 + 알림Y 확인
    cutoff = time(18, 0, 0)
    assert all(urgent['삭제시각'] >= cutoff)
    assert all(urgent['알림여부'] == 'Y')
```

#### 6. test_get_deletes_by_delivery
```python
def test_get_deletes_by_delivery():
    """배송처별 통계 테스트"""
    collector = DeleteCollector(file_path='fixtures/sample_delete.csv')
    collector.load_data()
    by_delivery = collector.get_deletes_by_delivery()
    
    assert '배송처명' in by_delivery.columns
    assert '삭제건수' in by_delivery.columns
```

#### 7. test_file_not_found
```python
def test_file_not_found():
    """파일 미존재 테스트"""
    collector = DeleteCollector(file_path='nonexistent.csv')
    
    with pytest.raises(FileNotFoundError):
        collector.load_data()
```

#### 8. test_invalid_data
```python
def test_invalid_data():
    """잘못된 데이터 테스트"""
    collector = DeleteCollector(file_path='fixtures/invalid_delete.csv')
    
    with pytest.raises(ValueError):
        collector.load_data()
```

### 테스트 실행
```bash
# 삭제 Collector 테스트만 실행
pytest tests/test_delete.py -v

# 커버리지 확인
pytest tests/test_delete.py --cov=src.data.collectors.delete --cov-report=html
```

---

## ⚠️ Edge Case 처리

### 1. 잘못된 시간 형식
- **상황**: 삭제처리시간이 잘못된 형식 (예: '999999')
- **처리**: `_parse_time()`에서 try-except로 `time(0, 0, 0)` 반환
- **영향**: 00:00:00으로 처리되어 18시 이후 판단 안됨

### 2. 알림여부 빈 값
- **상황**: 알림여부 컬럼이 비어있음 (NaN)
- **처리**: `fillna('N')`으로 'N' 처리
- **의미**: 기본값 'N' (알림 전)

### 3. 알림시각 빈 값
- **상황**: 알림시각이 비어있음 (알림 전 상태)
- **처리**: NaT로 유지 (pandas 자연스러운 처리)
- **영향**: 알림 시각 통계에서 제외

### 4. 18:00:00 경계값
- **상황**: 삭제시각이 정확히 18:00:00
- **처리**: `>=` 연산자로 18시 이후에 포함
- **의미**: 18시 정각도 긴급 알림 대상

### 5. 음수 삭제수량
- **상황**: 삭제수량이 음수 (예: -10)
- **처리**: 데이터 그대로 유지
- **의미**: 취소 또는 시스템 오류
- **대응**: 빨간색 경고

### 6. 라벨출력 빈 값
- **상황**: 라벨출력 컬럼이 비어있음
- **처리**: 데이터 그대로 유지 (NaN)
- **영향**: 라벨 통계에서 제외

---

## 🔗 관련 문서

### 프로젝트 문서
- [../README.md](../README.md) - Collector 전체 개요
- [base.py](base.py) - BaseCollector 추상 클래스
- [../../tests/test_delete.py](../../tests/test_delete.py) - 테스트 코드

### 백엔드 문서
- **WMS_삭제현황_README.md** - 백엔드 사용자 가이드
- **WMS_삭제현황_TECHNICAL_GUIDE.md** - 백엔드 기술 문서
- **WMS_삭제현황_활용방안.md** - 대시보드 활용 방안

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
- UTF-8 BOM 인코딩 필수
- 삭제처리시간은 HHMMSS 형식
- 필수 컬럼 15개 모두 필요
- 18시 기준은 고정 (18:00:00)

---

## 🔄 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1.0 | 2025-10-17 | 초기 버전 (기본 구조) |
| v2.0 | 2025-10-20 | 백엔드 컬럼 반영 |
| - | - | 알림여부, 알림시각 추가 |
| v3.0 | 2025-10-27 | 18시 알림 로직 완성 ✅ |
| - | - | `_parse_time()` 메서드 추가 |
| - | - | `count_after_18()` 메서드 추가 |
| - | - | 8개 테스트 통과 |
| - | - | Phase 1 완료 ✅ |

---

**마지막 업데이트**: 2025-11-07  
**작성자**: WMS 대시보드 개발팀  
**상태**: ✅ Phase 1 완료 → Phase 2 Flask 연동 예정