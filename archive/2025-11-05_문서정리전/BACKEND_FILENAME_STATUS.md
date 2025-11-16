# 백엔드 CSV 파일명 방식 변경 현황

## 확인 일시: 2025-10-20 13:35

---

## ✅ 백엔드 모듈 (5/5 완료)

| 모듈 | 파일명 방식 | 백업 시스템 | 상태 |
|------|------------|------------|------|
| Inbound Status | ✅ `inbound_merged_YYYYMMDD.csv` | ✅ 있음 (7개) | ✅ 완료 |
| Outbound Status | ✅ `outbound_all_YYYYMMDD.csv` | ✅ 있음 (8개) | ✅ 완료 |
| Inventory Status | ✅ `inventory_status_YYYYMMDD.csv` | ✅ 있음 (11개) | ✅ 완료 |
| Delete Status | ✅ `delete_status_YYYYMMDD.csv` | ✅ 있음 (1개) | ✅ 완료 |
| IrregularOrder Status | ✅ `irregular_order_YYYYMMDD.csv` | ✅ 있음 (2개) | ✅ 완료 |

**결과:** 백엔드 5개 모듈 모두 날짜 방식 + 백업 시스템 적용 완료! ✅

---

## ❌ Collector (프론트엔드) - 반영 안됨

### 현재 상황

**파일:** `dashboard/config/config.example.yaml`

**현재 설정 (와일드카드 방식):**
```yaml
data_sources:
  inbound: "C:/OSIS_AUTO/입고정보/inbound_merged_*.csv"
  outbound: "C:/OSIS_AUTO/출고정보/outbound_*.csv"
  inventory: "C:/OSIS_AUTO/재고정보/inventory_status_*.csv"
  delete: "C:/OSIS_AUTO/삭제정보/delete_status_*.csv"
  irregular: "C:/OSIS_AUTO/비정형오더/irregular_order_*.csv"
```

**문제점:**
1. ❌ 폴더 경로가 틀림 (입고정보 → Inbound Status)
2. ❌ 와일드카드 패턴 사용 중 (`*`)
3. ❌ 날짜 자동화 로직 없음

---

## 🔧 필요한 수정 사항

### 1. config.yaml 수정 필요

**수정 후:**
```yaml
data_sources:
  inbound: "C:/OSIS_AUTO/Inbound Status/inbound_merged_{date}.csv"
  outbound: "C:/OSIS_AUTO/Outbound Status/outbound_all_{date}.csv"
  inventory: "C:/OSIS_AUTO/inventory_status/inventory_status_{date}.csv"
  delete: "C:/OSIS_AUTO/Delete Status/delete_status_{date}.csv"
  irregular: "C:/OSIS_AUTO/IrregularOrder Status/irregular_order_{date}.csv"
```

### 2. 날짜 자동 치환 로직 추가 필요

**현재:** 없음  
**필요:** config 파일을 읽을 때 `{date}`를 오늘 날짜로 자동 치환

**예시 코드:**
```python
from datetime import datetime

def load_config():
    # config.yaml 읽기
    config = yaml.safe_load(...)
    
    # 오늘 날짜로 치환
    today = datetime.now().strftime("%Y%m%d")
    for key, path in config['data_sources'].items():
        config['data_sources'][key] = path.replace('{date}', today)
    
    return config
```

---

## 📊 영향 범위

### ✅ 영향 없는 부분
- `test_outbound_collector.py` - 직접 경로 지정 방식이라 정상 작동 ✅

### ❌ 영향 있는 부분
- 실제 대시보드 실행 시 config.yaml 사용하는 부분
- 현재는 와일드카드로 최신 파일 찾는 로직이 필요함

---

## 🎯 수정 계획

### Option 1: 와일드카드 유지 (간단)
```python
# glob으로 최신 파일 찾기
import glob
files = glob.glob("C:/OSIS_AUTO/Inbound Status/inbound_merged_*.csv")
latest_file = max(files, key=os.path.getctime)
```

**장점:** 코드 수정 최소화  
**단점:** 타임스탬프 파일 남아있으면 혼란

### Option 2: 날짜 치환 방식 (권장) ⭐
```yaml
# config.yaml
inbound: "C:/OSIS_AUTO/Inbound Status/inbound_merged_{date}.csv"
```

```python
# Python
today = datetime.now().strftime("%Y%m%d")
path = config['inbound'].replace('{date}', today)
```

**장점:** 명확하고 안전  
**단점:** 코드 약간 수정 필요

---

## ✅ 결론

**백엔드는 완료, Collector는 미반영**

**다음 작업:**
1. config.yaml 경로 수정 (폴더명 변경)
2. 날짜 치환 로직 추가 (Option 2 권장)
3. Collector 코드에서 config 읽기 부분 수정

**예상 소요 시간:** 20-30분

---

작성: 4명의 가상 전문가 팀  
확인 일시: 2025-10-20 13:35
