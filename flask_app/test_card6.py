# -*- coding: utf-8 -*-
"""카드6 배송처 분류 검증 스크립트"""

import pandas as pd

# 데이터 로드 (어제 날짜)
df = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251117.csv', encoding='utf-8-sig')

# 카드6 타입 필터링
card6_types = [4, 5, 8, 16, 17, 52, 53]
card6 = df[df['출고유형'].isin(card6_types)].copy()

print("=" * 60)
print("카드6 지방 출고 데이터 분석")
print("=" * 60)
print(f"\n총 건수: {len(card6)}건\n")

print("출고유형별 건수:")
print(card6['출고유형'].value_counts().sort_index())
print()

print("출고유형 05 데이터 (배송군 2, 3, 4 확인):")
type05 = card6[card6['출고유형'] == 5]
print(f"  - 총 {len(type05)}건")
if len(type05) > 0:
    print(f"  - 배송군 2: {len(type05[type05['배송군'] == 2])}건")
    print(f"  - 배송군 3: {len(type05[type05['배송군'] == 3])}건")
    print(f"  - 배송군 4: {len(type05[type05['배송군'] == 4])}건")
    print(f"  - 식재: {len(type05[type05['배송처명'] == '식재'])}건")
print()

print("출고유형 08 데이터 (배송군 2, 3, 4 확인):")
type08 = card6[card6['출고유형'] == 8]
print(f"  - 총 {len(type08)}건")
if len(type08) > 0:
    print(f"  - 배송군 2: {len(type08[type08['배송군'] == 2])}건")
    print(f"  - 배송군 3: {len(type08[type08['배송군'] == 3])}건")
    print(f"  - 배송군 4: {len(type08[type08['배송군'] == 4])}건")
print()

print("배송군 4자리 데이터 확인:")
card6['배송군_str'] = card6['배송군'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
card6_4digit = card6[card6['배송군_str'].str.len() == 4]
print(f"  - 4자리 배송군: {len(card6_4digit)}건")
if len(card6_4digit) > 0:
    print(f"  - 샘플 배송군: {card6_4digit['배송군_str'].head(10).tolist()}")
print()

print("샘플 데이터 (처음 10건):")
print(card6[['출고유형', '배송군', '배송처명', '출하금액']].head(10))
