import pandas as pd

# 데이터 로드
inv_file = 'C:/OSIS_AUTO/inventory_status/inventory_status_20251203.csv'
upper_file = 'C:/OSIS_AUTO/inventory_status/냉장 파레트 적재 로케이션.csv'

inv_df = pd.read_csv(inv_file, encoding='utf-8-sig')
upper_loc_df = pd.read_csv(upper_file, header=None, encoding='utf-8-sig')
upper_loc_set = set(upper_loc_df[0].str.strip())

# 상단/하단 분리
upper_df = inv_df[inv_df['로케이션'].isin(upper_loc_set)].copy()
lower_df = inv_df[~inv_df['로케이션'].isin(upper_loc_set)].copy()

print(f'상단 로케이션 재고: {len(upper_df)}건')
print(f'하단 로케이션 재고: {len(lower_df)}건')
print()

# 상품별 최소 소비기한
upper_min = upper_df.groupby('상품')['소비기한'].min().reset_index()
upper_min.columns = ['상품', 'upper_expiry']

lower_min = lower_df.groupby('상품')['소비기한'].min().reset_index()
lower_min.columns = ['상품', 'lower_expiry']

# 조인 및 위반 찾기
merged = pd.merge(upper_min, lower_min, on='상품', how='inner')
violations = merged[merged['upper_expiry'] < merged['lower_expiry']]

print(f'선입선출 위반: {len(violations)}건')
print()

if len(violations) > 0:
    print('=' * 70)
    print('위반 상품 상세')
    print('=' * 70)
    for _, row in violations.iterrows():
        product_code = row['상품']
        product_info = inv_df[inv_df['상품'] == product_code].iloc[0]
        product_name = product_info['상품명']
        
        # 상단/하단 로케이션 정보
        upper_row = upper_df[upper_df['상품'] == product_code].iloc[0]
        lower_row = lower_df[lower_df['상품'] == product_code].iloc[0]
        
        print(f'상품: {product_name}')
        print(f'상품코드: {product_code}')
        print(f'')
        print(f'  [상단] {upper_row["로케이션"]} - 소비기한: {row["upper_expiry"]} (먼저 출고되어야 함)')
        print(f'  [하단] {lower_row["로케이션"]} - 소비기한: {row["lower_expiry"]} (더 신선함)')
        print(f'')
        print(f'  → 문제: 상단이 {row["upper_expiry"]}인데 하단이 {row["lower_expiry"]}')
        print(f'         상단 유통기한이 더 짧으므로 먼저 출고해야 하는데,')
        print(f'         피킹 시 하단부터 가져가면 FIFO 위반!')
        print('=' * 70)
