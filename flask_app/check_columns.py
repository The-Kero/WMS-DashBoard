import pandas as pd

df = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251119.csv', encoding='utf-8-sig')

print("=== 출고 CSV 컬럼 목록 ===")
for i, col in enumerate(df.columns.tolist(), 1):
    print(f"{i}. {col}")
