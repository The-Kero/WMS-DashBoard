import pandas as pd

# 백엔드 실제 데이터 읽기
df = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251020.csv')

print(f"Original data: {len(df)} records, {len(df.columns)} columns")

# 다양한 출고유형을 포함한 샘플 추출
sample_df = df.head(20)

# 샘플 데이터 저장
output_path = 'C:/Projects/WMS-DashBoard/dashboard/tests/fixtures/sample_outbound.csv'
sample_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\nSample data created: {len(sample_df)} records")
print(f"Columns: {len(sample_df.columns)}")
print(f"File saved to: {output_path}")
print("\nSample record check:")
print(sample_df[['출고유형', '출고일자', '상품', '상품명', '오더수량*', '출하금액', '배송처']].head(3))
