import pandas as pd

df = pd.read_csv('C:/OSIS_AUTO/Inbound Status/integrated_inbound_20251204.csv', encoding='utf-8-sig')
result = df[df['상품'] == 41006641][['상품', '상품명', '공급사명', '입고예정수량', '진척률']]
print(result.to_string())
print(f"\n합계: {result['입고예정수량'].sum()}")
