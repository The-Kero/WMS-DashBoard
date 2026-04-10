import pandas as pd

file_path = 'C:/OSIS_AUTO/inventory_status/inventory_status_20251203.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 현재 조건
risky = df[df['유효유통비(%)'] <= 20].copy()
risky2 = risky[~risky['로케이션'].str.startswith('L07', na=False)].copy()
risky2 = risky2.sort_values('유효유통비(%)')

# 가용수량 0인 항목
zero = risky2[risky2['가용수량'] == 0]
new = risky2[risky2['가용수량'] != 0]

# 제외될 항목 저장
zero[['로케이션', '상품명', '유효유통비(%)', '가용수량']].to_csv(
    'C:/Projects/WMS-DashBoard/flask_app/temp_excluded.csv', 
    index=False, encoding='utf-8-sig'
)

# 변경 후 남는 항목 저장
new[['로케이션', '상품명', '유효유통비(%)', '가용수량']].head(12).to_csv(
    'C:/Projects/WMS-DashBoard/flask_app/temp_remaining.csv', 
    index=False, encoding='utf-8-sig'
)

print(f'현재: {len(risky2)}건, 제외: {len(zero)}건, 변경후: {len(new)}건')
print('CSV 저장 완료')
