# -*- coding: utf-8 -*-
"""v30 미할당 입고현황 테스트"""
import sys
sys.path.insert(0, 'C:/Projects/WMS-DashBoard')

from flask_app.api.dashboard import (
    get_unallocated_csv_path,
    load_unallocated_csv,
    save_unallocated_csv,
    get_recorded_inbound_numbers,
    match_new_inbound_info,
    add_inbound_columns,
    get_section5_display_data,
    get_outbound_backup_before_1810,
    extract_unallocated_from_outbound,
    normalize_supplier
)
from datetime import datetime
import pandas as pd

print("="*60)
print("v30 미할당 입고현황 테스트")
print("="*60)

today = datetime.now().strftime("%Y%m%d")
base_path = "C:/OSIS_AUTO"

# 1. 함수 import 테스트
print("\n[1] 함수 import 테스트: OK")

# 2. CSV 경로 테스트
csv_path = get_unallocated_csv_path(today)
print(f"\n[2] CSV 경로: {csv_path}")

# 3. 18:10 이전 백업 파일 찾기
backup_file = get_outbound_backup_before_1810(base_path, today)
print(f"\n[3] 18:10 이전 백업파일: {backup_file if backup_file else '없음'}")

# 4. 현재 시간 확인
now = datetime.now()
is_after_1810 = (now.hour > 18) or (now.hour == 18 and now.minute >= 10)
print(f"\n[4] 현재 시간: {now.strftime('%H:%M:%S')}")
print(f"    18:10 이후 여부: {is_after_1810}")

# 5. 기존 CSV 확인
existing_csv = load_unallocated_csv(today)
if existing_csv is not None:
    print(f"\n[5] 기존 CSV 존재: {len(existing_csv)}행")
    print(f"    컬럼: {list(existing_csv.columns)}")
else:
    print(f"\n[5] 기존 CSV: 없음 (첫 실행)")

# 6. normalize_supplier 테스트
test_suppliers = ['용인2센터', '용인3', '안산', '제주', '(주)한진', '일반공급사']
print(f"\n[6] normalize_supplier 테스트:")
for s in test_suppliers:
    print(f"    {s} → {normalize_supplier(s)}")

print("\n" + "="*60)
print("테스트 완료!")
print("="*60)
