"""
WMS 대시보드 v9 실제 데이터 계산 스크립트

5개 핵심모듈 CSV → dashboardData JSON 생성
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
import os

# ========================================
# 경로 설정
# ========================================
BASE_PATH = Path('C:/OSIS_AUTO')
TODAY = datetime.now().strftime("%Y%m%d")

print("=" * 100)
print(f"WMS 대시보드 v9 데이터 계산 ({TODAY})")
print("=" * 100)
print()

# ========================================
# 카드2: 입고 현황
# ========================================
print("📦 카드2 - 입고 현황")
print("-" * 100)

try:
    inbound_file = BASE_PATH / 'Inbound Status' / f'integrated_inbound_{TODAY}.csv'
    if not inbound_file.exists():
        print(f"❌ 파일 없음: {inbound_file}")
        card2_data = {
            "totalCount": 0,
            "progressRate": 0.0,
            "inboundRiskyCount": 0,
            "riskyItems": [],
            "testMode": True
        }
    else:
        inbound = pd.read_csv(inbound_file, encoding='utf-8-sig')
        inventory_file = BASE_PATH / 'inventory_status' / f'inventory_status_{TODAY}.csv'
        
        card2_total = len(inbound)
        card2_progress = float(inbound['진척률'].mean()) if '진척률' in inbound.columns else 0.0
        
        # 입고유의상품 계산
        if inventory_file.exists():
            inventory = pd.read_csv(inventory_file, encoding='utf-8-sig')
            
            inbound_exp = inbound.groupby('상품')['소비기한'].min().reset_index()
            inbound_exp.columns = ['상품', '입고_소비기한']
            
            inv_exp = inventory.groupby('상품')['소비기한'].min().reset_index()
            inv_exp.columns = ['상품', '재고_소비기한']
            
            merged = pd.merge(inbound_exp, inv_exp, on='상품', how='inner')
            risky_inbound = merged[merged['입고_소비기한'] < merged['재고_소비기한']]
            card2_risky = len(risky_inbound)
        else:
            card2_risky = 0
        
        card2_data = {
            "totalCount": int(card2_total),
            "progressRate": round(card2_progress, 1),
            "inboundRiskyCount": int(card2_risky),
            "riskyItems": [],
            "testMode": False
        }
        
        print(f"✅ totalCount: {card2_total}")
        print(f"✅ progressRate: {card2_progress:.1f}")
        print(f"✅ inboundRiskyCount: {card2_risky}")

except Exception as e:
    print(f"❌ 에러: {e}")
    card2_data = {
        "totalCount": 0,
        "progressRate": 0.0,
        "inboundRiskyCount": 0,
        "riskyItems": [],
        "testMode": True
    }

print()

# ========================================
# 카드3: 피킹 유의상품
# ========================================
print("📋 카드3 - 피킹 유의상품")
print("-" * 100)

try:
    inventory_file = BASE_PATH / 'inventory_status' / f'inventory_status_{TODAY}.csv'
    if not inventory_file.exists():
        print(f"❌ 파일 없음: {inventory_file}")
        card3_data = {
            "totalCount": 0,
            "urgentCount": 0,
            "warningCount": 0,
            "riskyItems": []
        }
    else:
        inventory = pd.read_csv(inventory_file, encoding='utf-8-sig')
        
        # 유효유통비 20% 이하 필터링
        risky = inventory[inventory['유효유통비(%)'] <= 20].copy()
        
        # L07 로케이션 제외
        risky_filtered = risky[~risky['로케이션'].str.startswith('L07')].copy()
        
        card3_total = len(risky_filtered)
        card3_urgent = len(risky_filtered[risky_filtered['유효유통비(%)'] <= 10])
        card3_warning = len(risky_filtered[risky_filtered['유효유통비(%)'] > 10])
        
        # 유효비 오름차순 정렬
        risky_filtered = risky_filtered.sort_values('유효유통비(%)')
        
        # 상위 10개 항목
        card3_items = []
        for _, row in risky_filtered.head(10).iterrows():
            item = {
                "location": row['로케이션'],
                "productCode": str(row['상품']),
                "productName": row['상품명'],
                "expiryDate": str(row['소비기한']),
                "stockQty": int(row['재고수량']),
                "validityRatio": float(row['유효유통비(%)'])
            }
            card3_items.append(item)
        
        card3_data = {
            "totalCount": int(card3_total),
            "urgentCount": int(card3_urgent),
            "warningCount": int(card3_warning),
            "riskyItems": card3_items
        }
        
        print(f"✅ totalCount: {card3_total}")
        print(f"✅ urgentCount: {card3_urgent}")
        print(f"✅ warningCount: {card3_warning}")
        print(f"✅ riskyItems: {len(card3_items)}개")

except Exception as e:
    print(f"❌ 에러: {e}")
    card3_data = {
        "totalCount": 0,
        "urgentCount": 0,
        "warningCount": 0,
        "riskyItems": []
    }

print()

# ========================================
# 카드5: 자사 출고
# ========================================
print("🚚 카드5 - 자사 출고")
print("-" * 100)

try:
    outbound_file = BASE_PATH / 'Outbound Status' / f'outbound_all_{TODAY}.csv'
    if not outbound_file.exists():
        print(f"❌ 파일 없음: {outbound_file}")
        card5_data = {
            "amount": 0,
            "compare": 0.0,
            "totalLabel": 0,
            "unprintedLabel": 0,
            "irregularTotal": 0,
            "irregularUnprinted": 0
        }
    else:
        outbound = pd.read_csv(outbound_file, encoding='utf-8-sig')
        
        # 자사 출고 타입 (14, 15, 18)
        card5_types = [14, 15, 18]
        card5_data_df = outbound[outbound['출고유형'].isin(card5_types)].copy()
        
        card5_amount = int(card5_data_df['출하금액'].sum())
        card5_total_label = len(card5_data_df)
        card5_unpublished_label = len(card5_data_df[card5_data_df['라벨출력'] == 'N'])
        
        # 비정형 오더
        irregular_file = BASE_PATH / 'IrregularOrder Status' / f'irregular_order_{TODAY}.csv'
        if irregular_file.exists():
            irregular = pd.read_csv(irregular_file, encoding='utf-8-sig')
            card5_irregular_total = len(irregular)
            
            if '라벨출력' in irregular.columns:
                card5_irregular_unpublished = len(irregular[irregular['라벨출력'] == 'N'])
            else:
                card5_irregular_unpublished = 0
        else:
            card5_irregular_total = 0
            card5_irregular_unpublished = 0
        
        # 전일 대비 계산
        outbound_dir = BASE_PATH / 'Outbound Status'
        compare_file = None
        
        for days_ago in range(1, 11):
            check_date = (datetime.strptime(TODAY, '%Y%m%d') - timedelta(days=days_ago)).strftime('%Y%m%d')
            check_file = outbound_dir / f'outbound_all_{check_date}.csv'
            if check_file.exists():
                compare_file = check_file
                break
        
        if compare_file:
            compare_data = pd.read_csv(compare_file, encoding='utf-8-sig')
            compare_card5 = compare_data[compare_data['출고유형'].isin(card5_types)]
            compare_amount = int(compare_card5['출하금액'].sum())
            card5_compare = ((card5_amount - compare_amount) / compare_amount * 100) if compare_amount > 0 else 0.0
        else:
            card5_compare = 0.0
        
        card5_data = {
            "amount": card5_amount,
            "compare": round(card5_compare, 1),
            "totalLabel": card5_total_label,
            "unprintedLabel": card5_unpublished_label,
            "irregularTotal": card5_irregular_total,
            "irregularUnprinted": card5_irregular_unpublished
        }
        
        print(f"✅ amount: {card5_amount:,}")
        print(f"✅ compare: {card5_compare:+.1f}%")
        print(f"✅ totalLabel: {card5_total_label}")
        print(f"✅ unprintedLabel: {card5_unpublished_label}")
        print(f"✅ irregularTotal: {card5_irregular_total}")
        print(f"✅ irregularUnprinted: {card5_irregular_unpublished}")

except Exception as e:
    print(f"❌ 에러: {e}")
    card5_data = {
        "amount": 0,
        "compare": 0.0,
        "totalLabel": 0,
        "unprintedLabel": 0,
        "irregularTotal": 0,
        "irregularUnprinted": 0
    }

print()

# ========================================
# 카드6: 지방 출고
# ========================================
print("🚛 카드6 - 지방 출고")
print("-" * 100)

def classify_destination_card6(row):
    """배송처 분류 로직"""
    출고유형 = row['출고유형']
    배송군_str = str(row['배송군'])
    배송처명 = row['배송처명']
    
    배송군_4자리 = len(배송군_str) == 4
    
    # 05 타입 특수 분류
    if 출고유형 == 5:
        if 배송처명 == '식재':
            return '한익스'
        elif 배송군_4자리 and 배송군_str[0] == '3':
            return '키즈'
        elif 배송군_4자리 and 배송군_str[0] == '4':
            return '용인3'
        elif 배송군_4자리 and 배송군_str[0] == '2':
            return '용인2'
    
    # 08 타입
    elif 출고유형 == 8:
        if 배송군_4자리 and 배송군_str[0] == '4':
            return '용인3'
        elif 배송군_4자리 and 배송군_str[0] == '2':
            return '용인2'
    
    # 기타 지방 출고
    elif 출고유형 in [4, 16, 17, 52, 53]:
        if '용인' in 배송처명:
            if 배송군_4자리 and 배송군_str[0] == '4':
                return '용인3'
            else:
                return '용인2'
        elif 배송처명 == '양산':
            return '양산'
        elif 배송처명 == '양산2':
            return '양산2'
        else:
            return 배송처명
    
    return 배송처명

try:
    outbound_file = BASE_PATH / 'Outbound Status' / f'outbound_all_{TODAY}.csv'
    if not outbound_file.exists():
        print(f"❌ 파일 없음: {outbound_file}")
        card6_data = {
            "amount": 0,
            "compare": 0.0,
            "unprintedPicking": 0,
            "destinations": {
                "jeju": 0, "jecheon": 0, "honam": 0, "gumi": 0,
                "gyeryong": 0, "eumseong": 0, "yongin2": 0, "yongin3": 0,
                "ansan": 0, "yangsan": 0, "yangsan2": 0, "hanex": 0, "kids": 0
            }
        }
    else:
        outbound = pd.read_csv(outbound_file, encoding='utf-8-sig')
        
        # 지방 출고 타입 (4, 5, 8, 16, 17, 52, 53)
        card6_types = [4, 5, 8, 16, 17, 52, 53]
        card6_data_df = outbound[outbound['출고유형'].isin(card6_types)].copy()
        
        card6_amount = int(card6_data_df['출하금액'].sum())
        card6_unpublished_picking = len(card6_data_df[card6_data_df['피킹 리스트'] == 'N'])
        
        # 배송처별 분류
        card6_data_df['배송처_분류'] = card6_data_df.apply(classify_destination_card6, axis=1)
        dest_summary = card6_data_df.groupby('배송처_분류')['오더수량*'].sum().to_dict()
        
        # 12개 배송처 기본값 0
        card6_destinations = {
            'jeju': int(dest_summary.get('제주', 0)),
            'jecheon': int(dest_summary.get('제천', 0)),
            'honam': int(dest_summary.get('호남', 0)),
            'gumi': int(dest_summary.get('구미', 0)),
            'gyeryong': int(dest_summary.get('계룡', 0)),
            'eumseong': int(dest_summary.get('음성', 0)),
            'yongin2': int(dest_summary.get('용인2', 0)),
            'yongin3': int(dest_summary.get('용인3', 0)),
            'ansan': int(dest_summary.get('안산', 0)),
            'yangsan': int(dest_summary.get('양산', 0)),
            'yangsan2': int(dest_summary.get('양산2', 0)),
            'hanex': int(dest_summary.get('한익스', 0)),
            'kids': int(dest_summary.get('키즈', 0))
        }
        
        # 전일 대비 계산
        outbound_dir = BASE_PATH / 'Outbound Status'
        compare_file = None
        
        for days_ago in range(1, 11):
            check_date = (datetime.strptime(TODAY, '%Y%m%d') - timedelta(days=days_ago)).strftime('%Y%m%d')
            check_file = outbound_dir / f'outbound_all_{check_date}.csv'
            if check_file.exists():
                compare_file = check_file
                break
        
        if compare_file:
            compare_data = pd.read_csv(compare_file, encoding='utf-8-sig')
            compare_card6 = compare_data[compare_data['출고유형'].isin(card6_types)]
            compare_amount = int(compare_card6['출하금액'].sum())
            card6_compare = ((card6_amount - compare_amount) / compare_amount * 100) if compare_amount > 0 else 0.0
        else:
            card6_compare = 0.0
        
        card6_data = {
            "amount": card6_amount,
            "compare": round(card6_compare, 1),
            "unprintedPicking": card6_unpublished_picking,
            "destinations": card6_destinations
        }
        
        print(f"✅ amount: {card6_amount:,}")
        print(f"✅ compare: {card6_compare:+.1f}%")
        print(f"✅ unprintedPicking: {card6_unpublished_picking}")
        print(f"✅ destinations: {sum(card6_destinations.values())}개")

except Exception as e:
    print(f"❌ 에러: {e}")
    card6_data = {
        "amount": 0,
        "compare": 0.0,
        "unprintedPicking": 0,
        "destinations": {
            "jeju": 0, "jecheon": 0, "honam": 0, "gumi": 0,
            "gyeryong": 0, "eumseong": 0, "yongin2": 0, "yongin3": 0,
            "ansan": 0, "yangsan": 0, "yangsan2": 0, "hanex": 0, "kids": 0
        }
    }

print()

# ========================================
# JSON 생성
# ========================================
print("=" * 100)
print("📊 dashboardData JSON 생성")
print("=" * 100)

dashboard_data = {
    "date": TODAY,
    "card2": card2_data,
    "card3": card3_data,
    "card5": card5_data,
    "card6": card6_data
}

# JSON 파일 저장
output_file = Path(__file__).parent / 'dashboard_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=4)

print(f"✅ JSON 저장 완료: {output_file}")
print()

# JSON 출력 (복사용)
print("=" * 100)
print("📋 복사용 JSON (v9 HTML에 붙여넣기)")
print("=" * 100)
print()
print(json.dumps(dashboard_data, ensure_ascii=False, indent=4))
print()

print("=" * 100)
print("✅ 모든 작업 완료!")
print("=" * 100)
