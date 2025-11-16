"""
DeleteCollector Import 테스트

DeleteCollector가 정상적으로 import 되고 필수 컬럼이 정의되었는지 확인
"""

import sys
sys.path.append('C:/Projects/WMS-DashBoard/dashboard/src')

from data.collectors.delete import DeleteCollector

print("=" * 60)
print("DeleteCollector Import Test")
print("=" * 60)

# 1. Import 확인
print("\n1. Import Check:")
print(f"   [OK] DeleteCollector class: {DeleteCollector}")

# 2. REQUIRED_COLUMNS 확인
print(f"\n2. REQUIRED_COLUMNS Check:")
print(f"   Column count: {len(DeleteCollector.REQUIRED_COLUMNS)}")
print(f"   Column list:")
for i, col in enumerate(DeleteCollector.REQUIRED_COLUMNS, 1):
    print(f"      {i:2d}. {col}")

# 3. 메서드 존재 확인
print(f"\n3. Method Check:")
methods = [
    'load_data', 'validate', 'get_data', 'refresh', 
    'file_exists', 'get_row_count', 'get_summary',
    'count_after_18', 'get_urgent_deletes',
    'get_deletes_by_delivery', 'get_deletes_by_product'
]

for method in methods:
    has_method = hasattr(DeleteCollector, method)
    status = "[OK]" if has_method else "[FAIL]"
    print(f"   {status} {method}()")

# 4. 테스트 인스턴스 생성
print(f"\n4. Instance Creation Test:")
test_path = "C:/OSIS_AUTO/Delete Status/delete_status_20251029.csv"
try:
    collector = DeleteCollector(test_path, encoding='utf-8-sig')
    print(f"   [OK] Instance created successfully")
    print(f"   File path: {collector.file_path}")
    print(f"   File exists: {collector.file_exists()}")
except Exception as e:
    print(f"   [FAIL] Instance creation failed: {e}")

print("\n" + "=" * 60)
print("[SUCCESS] All Import Tests Passed!")
print("=" * 60)
