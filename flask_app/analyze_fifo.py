# -*- coding: utf-8 -*-
import pandas as pd

# 데이터 로드
inv = pd.read_csv('C:/OSIS_AUTO/inventory_status/inventory_status_20251203.csv', encoding='utf-8-sig')
upper_loc = pd.read_csv('C:/OSIS_AUTO/inventory_status/냉장 파레트 적재 로케이션.csv', header=None, encoding='utf-8-sig')
upper_set = set(upper_loc[0].str.strip())

print("=" * 80)
print("FIFO 위반 분석 - 아워홈 칼칼한 돼지김치찌개(실온)")
print("=" * 80)

# 해당 상품 데이터
p = inv[inv['상품'] == 41067307][['로케이션', '소비기한', '가용수량']]
print("\n[1] 원본 데이터:")
for _, r in p.iterrows():
    loc_type = "UPPER(CSV에 있음)" if r['로케이션'] in upper_set else "LOWER(CSV에 없음)"
    print(f"  {r['로케이션']}: {loc_type} | 소비기한:{r['소비기한']} | 가용수량:{r['가용수량']}")

# 현재 코드 로직대로 계산
print("\n[2] 현재 코드 로직:")
upper_df = inv[inv['로케이션'].isin(upper_set)]
lower_df = inv[~inv['로케이션'].isin(upper_set)]

upper_product = upper_df[upper_df['상품'] == 41067307]
lower_product = lower_df[lower_df['상품'] == 41067307]

upper_min_exp = upper_product['소비기한'].min()
lower_min_exp = lower_product['소비기한'].min()

print(f"  상단(UPPER) 최소 소비기한: {upper_min_exp}")
print(f"  하단(LOWER) 최소 소비기한: {lower_min_exp}")
print(f"  위반 조건 (upper < lower): {upper_min_exp} < {lower_min_exp} = {upper_min_exp < lower_min_exp}")

# 로케이션 찾기 (현재 코드)
upper_loc_row = upper_product.iloc[0]
lower_loc_row = lower_product.iloc[0]
print(f"\n[3] 화면 표시용 로케이션 (iloc[0] = 첫번째 행):")
print(f"  상단 로케이션: {upper_loc_row['로케이션']} (실제 소비기한: {upper_loc_row['소비기한']})")
print(f"  하단 로케이션: {lower_loc_row['로케이션']} (실제 소비기한: {lower_loc_row['소비기한']})")

print(f"\n[4] 화면에 표시되는 결과:")
print(f"  [하단] {lower_loc_row['로케이션']} ({lower_min_exp}) -> [상단] {upper_loc_row['로케이션']} ({upper_min_exp})")
print(f"  *** 문제: {upper_loc_row['로케이션']}의 실제 소비기한은 {upper_loc_row['소비기한']}인데 {upper_min_exp}으로 표시됨!")

# 가용수량 0 제외하면?
print("\n[5] 가용수량 > 0인 것만 계산하면:")
upper_product_valid = upper_product[upper_product['가용수량'] > 0]
lower_product_valid = lower_product[lower_product['가용수량'] > 0]

if len(upper_product_valid) > 0 and len(lower_product_valid) > 0:
    upper_min_valid = upper_product_valid['소비기한'].min()
    lower_min_valid = lower_product_valid['소비기한'].min()
    print(f"  상단 최소 소비기한: {upper_min_valid}")
    print(f"  하단 최소 소비기한: {lower_min_valid}")
    print(f"  위반 여부: {upper_min_valid} < {lower_min_valid} = {upper_min_valid < lower_min_valid}")
else:
    print("  상단 또는 하단에 가용수량 > 0인 재고 없음")
