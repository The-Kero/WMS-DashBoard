# -*- coding: utf-8 -*-
"""카드6 배송처 분류 함수 직접 테스트"""

import pandas as pd

# 분류 함수 (dashboard.py에서 복사)
def classify_destination_card6(row):
    출고유형 = row['출고유형']
    배송군 = row['배송군']
    배송처명 = row['배송처명']
    
    # NaN 처리
    if pd.isna(배송군):
        배송군_str = ''
    else:
        배송군_str = str(int(배송군))
    
    if pd.isna(배송처명):
        배송처명 = ''
    
    # 출고유형 05
    if 출고유형 == 5:
        if 배송처명 == '식재':
            return '한익스'
        elif 배송군_str == '3':
            return '키즈'
        elif 배송군_str == '4':
            return '용인3'
        elif 배송군_str == '2':
            return '용인2'
        else:
            return '기타'
    
    # 출고유형 08
    elif 출고유형 == 8:
        if 배송군_str == '3':
            return '키즈'
        elif 배송군_str == '4':
            return '용인3'
        elif 배송군_str == '2':
            return '용인2'
        else:
            return '기타'
    
    # 출고유형 04, 16, 17, 52, 53
    elif 출고유형 in [4, 16, 17, 52, 53]:
        if len(배송군_str) == 4:
            앞자리 = 배송군_str[:2]
            
            # 용인 분기 (01~50)
            if 앞자리.isdigit() and 1 <= int(앞자리) <= 50:
                뒷자리 = 배송군_str[2:]
                
                if 뒷자리 == '01':
                    return '용인1'
                elif 뒷자리 == '02':
                    return '용인2'
                elif 뒷자리 == '03':
                    return '용인3'
                else:
                    return '기타'
            
            # 양산 분기 (51~99)
            elif 앞자리.isdigit() and 51 <= int(앞자리) <= 99:
                return '양산'
            
            else:
                return '기타'
        else:
            return '기타'
    
    else:
        return '기타'

# 데이터 로드
df = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251117.csv', encoding='utf-8-sig')
card6_types = [4, 5, 8, 16, 17, 52, 53]
card6 = df[df['출고유형'].isin(card6_types)].copy()

# 배송처 분류 적용
card6['배송처_분류'] = card6.apply(classify_destination_card6, axis=1)

# 결과 집계
grouped = card6.groupby('배송처_분류').agg({
    '출고유형': 'count',
    '출하금액': 'sum'
}).reset_index()
grouped.columns = ['배송처', '건수', '금액']

print("=" * 60)
print("배송처 분류 결과")
print("=" * 60)
print(grouped)
print()
print(f"총 건수: {grouped['건수'].sum()}건")
print(f"총 금액: {grouped['금액'].sum():,.0f}원")
print()

# 각 배송처별 출고유형 분포
print("배송처별 출고유형 분포:")
for dest in grouped['배송처']:
    dest_data = card6[card6['배송처_분류'] == dest]
    print(f"\n{dest}: {len(dest_data)}건")
    print(dest_data['출고유형'].value_counts().sort_index())
