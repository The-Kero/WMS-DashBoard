"""
OutboundCollector 테스트
백엔드 실제 데이터로 수정된 Collector 테스트
"""

import sys
sys.path.append('C:/Projects/WMS-DashBoard/dashboard/src')

from data.collectors.outbound import OutboundCollector

# 테스트 1: 샘플 데이터로 테스트
print("="*80)
print("TEST 1: Sample Data Test")
print("="*80)

try:
    collector = OutboundCollector(
        file_path='C:/Projects/WMS-DashBoard/dashboard/tests/fixtures/sample_outbound.csv'
    )
    
    # 데이터 로드
    df = collector.get_data()
    print(f"[OK] Data loaded: {len(df)} records")
    print(f"[OK] Columns: {len(df.columns)}")
    
    # 요약 정보
    summary = collector.get_summary()
    print(f"\nSummary:")
    for key, value in summary.items():
        print(f"  - {key}: {value}")
    
    # 상위 배송처
    top_dest = collector.get_top_destinations(n=3)
    print(f"\nTop Destinations (Top 3):")
    print(top_dest.to_string(index=False))
    
    # 상위 상품
    top_prod = collector.get_top_products(n=3)
    print(f"\nTop Products (Top 3):")
    print(top_prod.to_string(index=False))
    
    print("\n[SUCCESS] Sample data test passed!")
    
except Exception as e:
    print(f"\n[FAIL] Sample data test failed: {e}")
    import traceback
    traceback.print_exc()

# 테스트 2: 실제 백엔드 데이터로 테스트
print("\n" + "="*80)
print("TEST 2: Real Backend Data Test")
print("="*80)

try:
    collector = OutboundCollector(
        file_path='C:/OSIS_AUTO/Outbound Status/outbound_all_20251020.csv'
    )
    
    # 데이터 로드
    df = collector.get_data()
    print(f"[OK] Data loaded: {len(df):,} records")
    print(f"[OK] Columns: {len(df.columns)}")
    
    # 요약 정보
    summary = collector.get_summary()
    print(f"\nSummary:")
    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"  - {key}:")
            for k, v in value.items():
                print(f"      {k}: {v} records")
        else:
            formatted_value = f"{value:,}" if isinstance(value, (int, float)) and not isinstance(value, bool) else value
            print(f"  - {key}: {formatted_value}")
    
    # 출고유형별 집계
    by_type = collector.get_by_type()
    if not by_type.empty:
        print(f"\nBy Type Summary:")
        print(by_type.to_string(index=False))
    
    # 상위 배송처
    top_dest = collector.get_top_destinations(n=5)
    print(f"\nTop Destinations (Top 5):")
    print(top_dest.to_string(index=False))
    
    # 상위 상품
    top_prod = collector.get_top_products(n=5)
    print(f"\nTop Products (Top 5):")
    print(top_prod.to_string(index=False))
    
    print("\n[SUCCESS] Real data test passed!")
    
except Exception as e:
    print(f"\n[FAIL] Real data test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("Test Completed")
print("="*80)
