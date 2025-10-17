# 테스트 샘플 데이터

이 폴더는 개발 및 테스트용 샘플 데이터를 포함합니다.

## 파일 목록

- `sample_inbound.csv` - 입고정보 샘플 (5건)
- `sample_outbound.csv` - 출고정보 샘플 (5건)
- `sample_inventory.csv` - 재고정보 샘플 (5건)
- `sample_delete.csv` - 삭제정보 샘플 (3건)
- `sample_irregular.csv` - 비정형오더 샘플 (3건)

## 사용 방법

### 단위 테스트
```python
import pandas as pd

# 샘플 데이터 로드
df = pd.read_csv('tests/fixtures/sample_inbound.csv')
assert len(df) > 0
```

### Collector 테스트
```python
from src.data.collectors.inbound import InboundCollector

config = {'path': 'tests/fixtures/sample_inbound.csv'}
collector = InboundCollector(config)
df = collector.collect()
assert collector.validate(df)
```

## 주의사항

- 모든 파일은 UTF-8 인코딩
- 실제 데이터는 훨씬 많은 레코드 포함
- 테스트 목적으로만 사용