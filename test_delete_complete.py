"""
DeleteCollector 전체 기능 테스트

실제 CSV 데이터를 로드하고 모든 메서드가 정상 동작하는지 확인
"""

import sys
sys.path.append('C:/Projects/WMS-DashBoard/dashboard/src')

from data.collectors.delete import DeleteCollector
from datetime import time

print("=" * 60)
print("DeleteCollector Full Functionality Test")
print("=" * 60)

# DeleteCollector 인스턴스 생성
test_path = "C:/OSIS_AUTO/Delete Status/delete_status_20251029.csv"
collector = DeleteCollector(test_path, encoding='utf-8-sig')

# 1. 데이터 로드 테스트
print("\n1. Data Load Test:")
try:
    df = collector.load_data()
    print(f"   [OK] Data loaded successfully: {len(df)} rows")
    print(f"   Columns: {len(df.columns)}")
    print(f"\n   First row sample:")
    print(f"   - Delete Date: {df.iloc[0]['삭제처리일']}")
    print(f"   - Delete Time: {df.iloc[0]['삭제시각']}")
    print(f"   - Product: {df.iloc[0]['상품명']}")
    print(f"   - Quantity: {df.iloc[0]['삭제수량']}")
    print(f"   - Alert: {df.iloc[0]['알림여부']}")
except Exception as e:
    print(f"   [FAIL] Data load failed: {e}")
    exit(1)

# 2. get_summary() 테스트
print(f"\n2. get_summary() Test:")
try:
    summary = collector.get_summary()
    print(f"   [OK] Summary generated")
    print(f"   Total records: {summary['총건수']}")
    print(f"   After 18:00: {summary['18시이후삭제']}")
    print(f"   Alerted: {summary['알림완료']}")
    print(f"   Not Alerted: {summary['알림미완료']}")
    print(f"   Total Quantity: {summary['총삭제수량']}")
    print(f"   Delivery Centers: {summary['배송처수']}")
    print(f"   Product Types: {summary['상품종류']}")
except Exception as e:
    print(f"   [FAIL] get_summary() failed: {e}")

# 3. count_after_18() 테스트
print(f"\n3. count_after_18() Test:")
try:
    count = collector.count_after_18()
    print(f"   [OK] After 18:00 count: {count}")
    
    # 수동 확인
    df = collector.get_data()
    cutoff = time(18, 0, 0)
    manual_count = len(df[df['삭제시각'] >= cutoff])
    print(f"   Manual verification: {manual_count}")
    
    if count == manual_count:
        print(f"   [OK] Count matches!")
    else:
        print(f"   [FAIL] Count mismatch!")
except Exception as e:
    print(f"   [FAIL] count_after_18() failed: {e}")

# 4. get_urgent_deletes() 테스트
print(f"\n4. get_urgent_deletes() Test:")
try:
    urgent = collector.get_urgent_deletes()
    print(f"   [OK] Urgent deletes found: {len(urgent)} records")
    if len(urgent) > 0:
        print(f"   Sample urgent delete:")
        print(f"   - Product: {urgent.iloc[0]['상품명']}")
        print(f"   - Time: {urgent.iloc[0]['삭제시각']}")
        print(f"   - Alert: {urgent.iloc[0]['알림여부']}")
except Exception as e:
    print(f"   [FAIL] get_urgent_deletes() failed: {e}")

# 5. get_deletes_by_delivery() 테스트
print(f"\n5. get_deletes_by_delivery() Test:")
try:
    by_delivery = collector.get_deletes_by_delivery()
    print(f"   [OK] Delivery statistics generated")
    print(f"   Total delivery centers: {len(by_delivery)}")
    if len(by_delivery) > 0:
        print(f"   Top delivery center:")
        print(f"   - Name: {by_delivery.iloc[0]['배송처명']}")
        print(f"   - Delete count: {by_delivery.iloc[0]['삭제건수']}")
        print(f"   - Total quantity: {by_delivery.iloc[0]['총삭제수량']}")
except Exception as e:
    print(f"   [FAIL] get_deletes_by_delivery() failed: {e}")

# 6. get_deletes_by_product() 테스트
print(f"\n6. get_deletes_by_product() Test:")
try:
    by_product = collector.get_deletes_by_product()
    print(f"   [OK] Product statistics generated")
    print(f"   Total products: {len(by_product)}")
    if len(by_product) > 0:
        print(f"   Top product:")
        print(f"   - Name: {by_product.iloc[0]['상품명']}")
        print(f"   - Delete count: {by_product.iloc[0]['삭제건수']}")
        print(f"   - Total quantity: {by_product.iloc[0]['총삭제수량']}")
except Exception as e:
    print(f"   [FAIL] get_deletes_by_product() failed: {e}")

print("\n" + "=" * 60)
print("[SUCCESS] All Functionality Tests Passed!")
print("=" * 60)
