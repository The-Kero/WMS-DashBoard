# OutboundCollector 수정 확인 가이드

## 작성일: 2025-10-20

---

## ✅ 확인 방법 1: 자동 테스트 실행 (가장 쉬움)

### 명령어
```powershell
python C:\Projects\WMS-DashBoard\test_outbound_collector.py
```

### 확인 항목
- ✅ `[OK] Data loaded` - 데이터 로드 성공
- ✅ `[SUCCESS] Sample data test passed!` - 샘플 테스트 성공
- ✅ `[SUCCESS] Real data test passed!` - 실제 데이터 테스트 성공

### 예상 결과
```
총 출고건수: 4,312건
총 오더수량: 30,065개
총 출하금액: 45,725,984원
출하금액 유효건수: 2,481건
출하금액 N/A건수: 1,831건
```

---

## ✅ 확인 방법 2: 직접 코드 열어서 확인

### 1. 파일 열기
```
C:\Projects\WMS-DashBoard\dashboard\src\data\collectors\outbound.py
```

### 2. REQUIRED_COLUMNS 확인 (17줄)
```python
# 올바른 버전 (수정 완료)
REQUIRED_COLUMNS = [
    '출하바코드',      # ✅ (출고번호 → 출하바코드)
    '출고일자',        # ✅
    '상품',            # ✅ (상품코드 → 상품)
    '상품명',          # ✅
    '오더수량*',       # ✅ (출하수량 → 오더수량*)
    '출하금액',        # ✅
    '배송처'           # ✅
]

# 잘못된 버전 (수정 전)
REQUIRED_COLUMNS = [
    '출고번호',    # ❌ (백엔드에 없음)
    '출고일자', 
    '상품코드',    # ❌ (백엔드에 없음)
    '상품명',
    '출하수량',    # ❌ (백엔드에 없음)
    '출하금액',
    '배송처'
]
```

### 3. load_data() 확인 (47~49줄)
```python
# 올바른 버전 (수정 완료)
df['오더수량*'] = pd.to_numeric(df['오더수량*'], errors='coerce')  # ✅

# 출하금액 N/A 처리
df['출하금액'] = df['출하금액'].replace('N/A', pd.NA)  # ✅
df['출하금액'] = pd.to_numeric(df['출하금액'], errors='coerce')  # ✅

# 잘못된 버전 (수정 전)
df['출하수량'] = pd.to_numeric(df['출하수량'], errors='coerce')  # ❌
```

### 4. get_summary() 확인 (76~79줄)
```python
# 올바른 버전 (수정 완료)
'총_오더수량': int(df['오더수량*'].sum()),  # ✅
'출하금액_유효건수': int(valid_amount),     # ✅ 신규
'출하금액_N/A건수': len(df) - int(valid_amount),  # ✅ 신규

# 잘못된 버전 (수정 전)
'총_출하수량': df['출하수량'].sum(),  # ❌
'상품_종류': df['상품코드'].nunique(),  # ❌
```

---

## ✅ 확인 방법 3: 백엔드 데이터와 비교

### 1. 백엔드 CSV 파일 열기
```
C:\OSIS_AUTO\Outbound Status\outbound_all_20251020.csv
```

### 2. 컬럼명 확인
엑셀이나 메모장으로 열어서 첫 줄 확인:
```csv
출고유형,출고유형명,출고일자,라벨 출력시간,피킹리스트 출력시간,라벨출력,피킹 리스트,배송군,배송처,배송처명,출하타입구분,보관온도,상품,상품명,단위및규격,문서상태명,원주문수량,오더수량*,할당수량**,재고수량,가용재고,비고,출고제한일,출하바코드,출하금액
```

### 3. 확인 체크리스트
- ✅ `출하바코드` 컬럼 존재 (출고번호 없음)
- ✅ `상품` 컬럼 존재 (상품코드 없음)
- ✅ `오더수량*` 컬럼 존재 (출하수량 없음)
- ✅ `출하금액` 컬럼 존재 (N/A 값 포함)

---

## ✅ 확인 방법 4: 샘플 데이터 확인

### 1. 샘플 파일 열기
```
C:\Projects\WMS-DashBoard\dashboard\tests\fixtures\sample_outbound.csv
```

### 2. 확인 사항
- ✅ 20개 레코드 존재
- ✅ 25개 컬럼 존재 (이전 7개 → 25개)
- ✅ 백엔드와 동일한 컬럼 구조

---

## ✅ 확인 방법 5: Python으로 직접 확인 (고급)

### 코드 실행
```python
import sys
sys.path.append('C:/Projects/WMS-DashBoard/dashboard/src')

from data.collectors.outbound import OutboundCollector

# 1. REQUIRED_COLUMNS 확인
print("REQUIRED_COLUMNS:")
print(OutboundCollector.REQUIRED_COLUMNS)

# 2. 실제 데이터 로드 테스트
collector = OutboundCollector(
    file_path='C:/OSIS_AUTO/Outbound Status/outbound_all_20251020.csv'
)

# 3. 데이터 확인
df = collector.get_data()
print(f"\n총 레코드: {len(df):,}개")
print(f"컬럼 수: {len(df.columns)}개")

# 4. 요약 정보
summary = collector.get_summary()
print(f"\n총 오더수량: {summary['총_오더수량']:,}개")
print(f"총 출하금액: {summary['총_출하금액']:,}원")
print(f"출하금액 유효건수: {summary['출하금액_유효건수']:,}건")
print(f"출하금액 N/A건수: {summary['출하금액_N/A건수']:,}건")
```

### 예상 출력
```
REQUIRED_COLUMNS:
['출하바코드', '출고일자', '상품', '상품명', '오더수량*', '출하금액', '배송처']

총 레코드: 4,312개
컬럼 수: 25개

총 오더수량: 30,065개
총 출하금액: 45,725,984원
출하금액 유효건수: 2,481건
출하금액 N/A건수: 1,831건
```

---

## 📊 수정 전후 비교

| 항목 | 수정 전 | 수정 후 | 상태 |
|------|---------|---------|------|
| 출고번호 | ✅ 사용 | ❌ 제거 → 출하바코드 | 🔄 변경 |
| 상품코드 | ✅ 사용 | ❌ 제거 → 상품 | 🔄 변경 |
| 출하수량 | ✅ 사용 | ❌ 제거 → 오더수량* | 🔄 변경 |
| 출하금액 | ✅ 사용 | ✅ 유지 (N/A 처리 추가) | ✅ 개선 |
| 출하금액 유효건수 | ❌ 없음 | ✅ 추가 | ✅ 신규 |
| 출하금액 N/A건수 | ❌ 없음 | ✅ 추가 | ✅ 신규 |
| 출고유형별 집계 | ❌ 없음 | ✅ 추가 (get_by_type) | ✅ 신규 |
| 백엔드 호환성 | ❌ 불가 | ✅ 완벽 | ✅ 수정 |

---

## 🎯 최종 확인 체크리스트

### 필수 확인 사항
- [ ] 1. 테스트 스크립트 실행 성공 (`[SUCCESS]` 2개 출력)
- [ ] 2. outbound.py 파일에서 REQUIRED_COLUMNS 확인
- [ ] 3. 백엔드 CSV 파일의 컬럼명과 일치 확인
- [ ] 4. 샘플 데이터가 25개 컬럼 구조인지 확인
- [ ] 5. 실제 데이터 4,312건 정상 로드 확인

### 선택 확인 사항
- [ ] 6. 출하금액 N/A 처리 정상 작동 확인
- [ ] 7. 출고유형별 집계 정상 작동 확인
- [ ] 8. 상위 배송처/상품 집계 정상 작동 확인

---

## 💡 문제 발생 시

### 오류가 발생하면
```python
# 오류 메시지 확인
❌ 누락된 컬럼: {'출고번호', '상품코드', '출하수량'}
```
→ 아직 수정 전 버전입니다. outbound.py를 다시 확인하세요.

### 성공 메시지
```python
[SUCCESS] Sample data test passed!
[SUCCESS] Real data test passed!
```
→ 수정이 완벽하게 완료되었습니다! ✅

---

## 📞 추가 도움이 필요하면

- GitHub 커밋 확인: https://github.com/The-Kero/WMS-DashBoard/commit/b0c2cd7
- 커밋 해시: b0c2cd7
- 커밋 시간: 2025-10-20 13:29

---

**작성자:** 4명의 가상 전문가 팀  
**최종 업데이트:** 2025-10-20 13:29
