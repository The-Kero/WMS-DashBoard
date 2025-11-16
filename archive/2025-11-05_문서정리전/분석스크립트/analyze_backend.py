import pandas as pd
import os

print("="*80)
print("백엔드 5개 모듈 컬럼 구조 분석")
print("="*80)

# 1. Inbound Status
print("\n" + "="*80)
print("1. INBOUND STATUS")
print("="*80)
inbound_df = pd.read_csv('C:/OSIS_AUTO/Inbound Status/inbound_merged_20251020.csv')
print(f"파일명: inbound_merged_20251020.csv")
print(f"컬럼 수: {len(inbound_df.columns)}")
print(f"레코드 수: {len(inbound_df)}")
print(f"\n컬럼 목록:")
for i, col in enumerate(inbound_df.columns, 1):
    sample_value = inbound_df[col].iloc[0] if len(inbound_df) > 0 else "N/A"
    print(f"  {i:2}. {col:<25} (샘플: {sample_value})")

# 2. Outbound Status
print("\n" + "="*80)
print("2. OUTBOUND STATUS")
print("="*80)
outbound_df = pd.read_csv('C:/OSIS_AUTO/Outbound Status/outbound_all_20251020.csv')
print(f"파일명: outbound_all_20251020.csv")
print(f"컬럼 수: {len(outbound_df.columns)}")
print(f"레코드 수: {len(outbound_df)}")
print(f"\n컬럼 목록:")
for i, col in enumerate(outbound_df.columns, 1):
    sample_value = outbound_df[col].iloc[0] if len(outbound_df) > 0 else "N/A"
    print(f"  {i:2}. {col:<25} (샘플: {str(sample_value)[:30]})")

# 3. inventory_status
print("\n" + "="*80)
print("3. INVENTORY STATUS")
print("="*80)
inventory_df = pd.read_csv('C:/OSIS_AUTO/inventory_status/inventory_status_20251020.csv')
print(f"파일명: inventory_status_20251020.csv")
print(f"컬럼 수: {len(inventory_df.columns)}")
print(f"레코드 수: {len(inventory_df)}")
print(f"\n컬럼 목록:")
for i, col in enumerate(inventory_df.columns, 1):
    sample_value = inventory_df[col].iloc[0] if len(inventory_df) > 0 else "N/A"
    print(f"  {i:2}. {col:<25} (샘플: {sample_value})")

# 4. Delete Status
print("\n" + "="*80)
print("4. DELETE STATUS")
print("="*80)
delete_path = 'C:/OSIS_AUTO/Delete Status/delete_status_20251020.csv'
if os.path.exists(delete_path):
    delete_df = pd.read_csv(delete_path)
    print(f"파일명: delete_status_20251020.csv")
    print(f"컬럼 수: {len(delete_df.columns)}")
    print(f"레코드 수: {len(delete_df)}")
    print(f"\n컬럼 목록:")
    for i, col in enumerate(delete_df.columns, 1):
        sample_value = delete_df[col].iloc[0] if len(delete_df) > 0 else "N/A"
        print(f"  {i:2}. {col:<25} (샘플: {sample_value})")
else:
    print("❌ 파일 없음 (오늘 데이터 없음)")
    print("백업 폴더에서 최근 파일 확인...")
    backup_dir = 'C:/OSIS_AUTO/Delete Status/backup'
    if os.path.exists(backup_dir):
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.csv')]
        if backup_files:
            latest_backup = sorted(backup_files)[-1]
            print(f"최근 백업 파일: {latest_backup}")
            delete_df = pd.read_csv(os.path.join(backup_dir, latest_backup))
            print(f"컬럼 수: {len(delete_df.columns)}")
            print(f"레코드 수: {len(delete_df)}")
            print(f"\n컬럼 목록:")
            for i, col in enumerate(delete_df.columns, 1):
                sample_value = delete_df[col].iloc[0] if len(delete_df) > 0 else "N/A"
                print(f"  {i:2}. {col:<25} (샘플: {sample_value})")

# 5. IrregularOrder Status
print("\n" + "="*80)
print("5. IRREGULAR ORDER STATUS")
print("="*80)
irregular_df = pd.read_csv('C:/OSIS_AUTO/IrregularOrder Status/irregular_order_20251020.csv')
print(f"파일명: irregular_order_20251020.csv")
print(f"컬럼 수: {len(irregular_df.columns)}")
print(f"레코드 수: {len(irregular_df)}")
print(f"\n컬럼 목록:")
for i, col in enumerate(irregular_df.columns, 1):
    sample_value = irregular_df[col].iloc[0] if len(irregular_df) > 0 else "N/A"
    print(f"  {i:2}. {col:<25} (샘플: {sample_value})")

# Summary Table
print("\n" + "="*80)
print("백엔드 모듈 요약")
print("="*80)
print(f"{'모듈':<20} {'컬럼 수':<10} {'레코드 수':<15} {'상태'}")
print("-"*80)
print(f"{'Inbound':<20} {len(inbound_df.columns):<10} {len(inbound_df):<15} ✅")
print(f"{'Outbound':<20} {len(outbound_df.columns):<10} {len(outbound_df):<15} ✅")
print(f"{'Inventory':<20} {len(inventory_df.columns):<10} {len(inventory_df):<15} ✅")
print(f"{'Delete':<20} {'N/A':<10} {'N/A':<15} ⚠️ (파일 없음)")
print(f"{'Irregular':<20} {len(irregular_df.columns):<10} {len(irregular_df):<15} ✅")

print("\n" + "="*80)
print("분석 완료")
print("="*80)
