"""
백엔드 CSV 파일명 방식 변경 확인 스크립트
"""

import os
from datetime import datetime

print("="*80)
print("Backend 5 Module Filename Check")
print("="*80)

modules = [
    {
        'name': 'Inbound Status',
        'path': 'C:/OSIS_AUTO/Inbound Status',
        'expected': 'inbound_merged_YYYYMMDD.csv',
    },
    {
        'name': 'Outbound Status',
        'path': 'C:/OSIS_AUTO/Outbound Status',
        'expected': 'outbound_all_YYYYMMDD.csv',
    },
    {
        'name': 'Inventory Status',
        'path': 'C:/OSIS_AUTO/inventory_status',
        'expected': 'inventory_status_YYYYMMDD.csv',
    },
    {
        'name': 'Delete Status',
        'path': 'C:/OSIS_AUTO/Delete Status',
        'expected': 'delete_status_YYYYMMDD.csv',
    },
    {
        'name': 'IrregularOrder Status',
        'path': 'C:/OSIS_AUTO/IrregularOrder Status',
        'expected': 'irregular_order_YYYYMMDD.csv',
    }
]

today = datetime.now().strftime("%Y%m%d")

for module in modules:
    print(f"\n{module['name']}")
    print("-"*80)
    
    if os.path.exists(module['path']):
        csv_files = [f for f in os.listdir(module['path']) if f.endswith('.csv')]
        
        # 오늘 날짜 파일 확인
        today_file = module['expected'].replace('YYYYMMDD', today)
        today_file_exists = today_file in csv_files
        
        # 타임스탬프 방식 파일 확인 (HHMMSS 포함)
        timestamp_files = []
        for f in csv_files:
            parts = f.replace('.csv', '').split('_')
            if len(parts) >= 2:
                last_part = parts[-1]
                # HHMMSS 형식 확인 (6자리 숫자)
                if last_part.isdigit() and len(last_part) == 6:
                    timestamp_files.append(f)
        
        print(f"Path: {module['path']}")
        print(f"Expected: {today_file}")
        print(f"Today file exists: {'YES' if today_file_exists else 'NO'}")
        print(f"Timestamp files: {len(timestamp_files)}")
        
        if today_file_exists:
            print(f"Status: Using DATE format [OK]")
        else:
            print(f"Status: NOT using date format OR not run today [WARNING]")
        
        # 백업 폴더 확인
        backup_path = os.path.join(module['path'], 'backup')
        if os.path.exists(backup_path):
            backup_files = [f for f in os.listdir(backup_path) if f.endswith('.csv')]
            print(f"Backup system: YES ({len(backup_files)} files) [OK]")
        else:
            print(f"Backup system: NO [WARNING]")
            
        # 타임스탬프 파일 목록 (최근 3개)
        if timestamp_files:
            print(f"\nTimestamp files (latest 3):")
            for f in sorted(timestamp_files, reverse=True)[:3]:
                print(f"  - {f}")
    else:
        print(f"Path not found [ERROR]")

print("\n" + "="*80)
print("Check Completed")
print("="*80)
