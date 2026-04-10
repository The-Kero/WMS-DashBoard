"""
카드6 샘플 데이터 추출 스크립트
실제 CSV에서 10개 레이아웃 샘플 데이터 생성
"""
import pandas as pd
import json
from datetime import datetime

# UTF-8 출력 설정
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("카드6 샘플 데이터 추출 시작")
print("=" * 60)

# ========================================
# 1. CSV 파일 읽기
# ========================================
print("\n[1단계] CSV 파일 로드 중...")
df1 = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251116.csv', encoding='utf-8-sig')
df2 = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251119.csv', encoding='utf-8-sig')

print(f"  ✅ 파일1 (20251116): {len(df1):,}행")
print(f"  ✅ 파일2 (20251119): {len(df2):,}행")

# ========================================
# 2. 섹션4: 금일 특판 출하
# ========================================
print("\n[2단계] 섹션4 - 금일 특판 출하 추출...")

# 특판 배송처명 패턴
special_patterns = ['이랜드', '쿠팡', '군납']
special_data = df1[df1['배송처명'].str.contains('|'.join(special_patterns), na=False)]

special_counts = special_data['배송처명'].value_counts()
print(f"  ✅ 특판 업체 발견: {len(special_counts)}개")
for name, count in special_counts.head(5).items():
    print(f"     - {name}: {count}건")

section4_data = []
for name, count in special_counts.items():
    section4_data.append({
        "name": name,
        "count": int(count)
    })

# ========================================
# 3. 섹션6: 미출/부분출고 내역
# ========================================
print("\n[3단계] 섹션6 - 미출/부분출고 내역 추출...")

# 공통 키로 병합 (배송군, 배송처, 상품)
df1_key = df1.copy()
df2_key = df2.copy()

df1_key['key'] = df1_key['배송군'].astype(str) + '|' + df1_key['배송처명'] + '|' + df1_key['상품명']
df2_key['key'] = df2_key['배송군'].astype(str) + '|' + df2_key['배송처명'] + '|' + df2_key['상품명']

# 오더수량 비교
df1_orders = df1_key[['key', '배송군', '배송처명', '상품명', '오더수량*']].copy()
df2_orders = df2_key[['key', '배송군', '배송처명', '상품명', '오더수량*']].copy()

df1_orders.columns = ['key', '배송군', '배송처명', '상품명', 'order_qty_old']
df2_orders.columns = ['key', '배송군', '배송처명', '상품명', 'order_qty_new']

# 병합
merged = pd.merge(df1_orders, df2_orders[['key', 'order_qty_new']], on='key', how='inner')

# 변동 발견 (감소만)
merged['order_qty_old'] = pd.to_numeric(merged['order_qty_old'], errors='coerce').fillna(0)
merged['order_qty_new'] = pd.to_numeric(merged['order_qty_new'], errors='coerce').fillna(0)

changes = merged[merged['order_qty_new'] < merged['order_qty_old']].copy()
print(f"  ✅ 오더수량 변동: {len(changes)}건")

section6_data = []
for idx, row in changes.head(10).iterrows():
    section6_data.append({
        "delivery_group": str(row['배송군']),
        "delivery_name": row['배송처명'],
        "product_name": row['상품명'],
        "qty_before": int(row['order_qty_old']),
        "qty_after": int(row['order_qty_new'])
    })
    print(f"     - {row['배송군']} | {row['배송처명'][:15]:15s} | {row['상품명'][:20]:20s} | {int(row['order_qty_old'])} → {int(row['order_qty_new'])}")

# ========================================
# 4. 임시 샘플 데이터 (나머지 섹션)
# ========================================
print("\n[4단계] 임시 샘플 데이터 생성...")

# 섹션1: 선입선출 위반 (임시)
section1_data = [
    {"location": "A-01-01-01", "product": "닭가슴살채", "expiry": "2025-12-05"},
    {"location": "B-02-03-02", "product": "보쌈수소스", "expiry": "2025-12-03"},
    {"location": "C-03-02-01", "product": "간장소스우불고기", "expiry": "2025-12-08"}
]

# 섹션2: 총 재고 (임시)
section2_data = {
    "total_value": 17680000
}

# 섹션3: 상단 파레트 적치율 (임시)
section3_data = {
    "rate": 45.2
}

# 섹션5: 금일 삭제 현황 (임시)
section5_data = {
    "ansan": [
        {"name": "닭가슴살채", "unit": "EA", "count": 2},
        {"name": "보쌈수소스", "unit": "PK", "count": 3},
        {"name": "간장소스우불고기", "unit": "EA", "count": 1}
    ],
    "eumseong": [
        {"name": "프레시쿠팡용", "unit": "BOX", "count": 5},
        {"name": "이랜드용", "unit": "EA", "count": 2}
    ]
}

# ========================================
# 5. JSON 저장
# ========================================
print("\n[5단계] JSON 파일 저장...")

card6_sample = {
    "generated_at": datetime.now().isoformat(),
    "source_files": [
        "outbound_all_20251116.csv",
        "outbound_all_20251119.csv"
    ],
    "sections": {
        "section1_fifo_violation": section1_data,
        "section2_total_inventory": section2_data,
        "section3_storage_rate": section3_data,
        "section4_special_delivery": section4_data,
        "section5_delete_status": section5_data,
        "section6_partial_shipment": section6_data
    }
}

output_path = 'C:/Projects/WMS-DashBoard/Layout/card6_sample_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(card6_sample, f, ensure_ascii=False, indent=2)

print(f"  ✅ 저장 완료: {output_path}")

# ========================================
# 6. 요약
# ========================================
print("\n" + "=" * 60)
print("샘플 데이터 추출 완료!")
print("=" * 60)
print(f"섹션1 (선입선출): {len(section1_data)}건")
print(f"섹션2 (총재고): {section2_data['total_value']:,}원")
print(f"섹션3 (적치율): {section3_data['rate']}%")
print(f"섹션4 (특판): {len(section4_data)}개 업체")
print(f"섹션5 (삭제): 안산 {len(section5_data['ansan'])}건, 음성 {len(section5_data['eumseong'])}건")
print(f"섹션6 (미출): {len(section6_data)}건")
print("=" * 60)
