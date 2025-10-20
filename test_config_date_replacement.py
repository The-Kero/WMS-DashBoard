"""
Config 날짜 치환 기능 테스트
"""

import sys
sys.path.append('C:/Projects/WMS-DashBoard/dashboard/src')

from utils.config_utils import (
    replace_date_placeholder,
    load_config_with_date,
    load_data_sources_with_date
)
from datetime import datetime

print("="*80)
print("Config Date Replacement Test")
print("="*80)

# 테스트 1: replace_date_placeholder 함수 테스트
print("\nTest 1: replace_date_placeholder()")
print("-"*80)

test_config = {
    'data_sources': {
        'inbound': 'C:/OSIS_AUTO/Inbound Status/inbound_merged_{date}.csv',
        'outbound': 'C:/OSIS_AUTO/Outbound Status/outbound_all_{date}.csv',
        'inventory': 'C:/OSIS_AUTO/inventory_status/inventory_status_{date}.csv'
    }
}

result = replace_date_placeholder(test_config)
today = datetime.now().strftime("%Y%m%d")

print(f"Today: {today}")
print(f"\nReplacement results:")
for key, value in result['data_sources'].items():
    original = test_config['data_sources'][key]
    print(f"  {key}:")
    print(f"    Before: {original}")
    print(f"    After:  {value}")
    
    # 검증
    if '{date}' in value:
        print(f"    Status: [FAIL] Still contains {{date}}")
    elif today in value:
        print(f"    Status: [OK] Date replaced successfully")
    else:
        print(f"    Status: [FAIL] Date not found")

# 테스트 2: config.example.yaml 로드 테스트
print("\n" + "="*80)
print("Test 2: load_config_with_date()")
print("-"*80)

try:
    config = load_config_with_date('C:/Projects/WMS-DashBoard/dashboard/config/config.example.yaml')
    
    print(f"Config loaded successfully!")
    print(f"\nData sources:")
    for key, value in config['data_sources'].items():
        print(f"  {key}: {value}")
        
        # 검증
        if '{date}' in value:
            print(f"    [FAIL] Still contains {{date}}")
        elif today in value:
            print(f"    [OK]")
        else:
            print(f"    [WARNING] No date pattern")
    
    print(f"\n[SUCCESS] Config file loaded and dates replaced!")
    
except Exception as e:
    print(f"\n[FAIL] Error loading config: {e}")
    import traceback
    traceback.print_exc()

# 테스트 3: data_sources.yaml 로드 테스트
print("\n" + "="*80)
print("Test 3: load_data_sources_with_date()")
print("-"*80)

try:
    sources = load_data_sources_with_date('C:/Projects/WMS-DashBoard/dashboard/config/data_sources.yaml')
    
    print(f"Data sources loaded: {len(sources)} modules")
    print(f"\nModules:")
    
    for source in sources:
        name = source.get('name', 'Unknown')
        path = source.get('path', 'Unknown')
        enabled = source.get('enabled', False)
        
        print(f"\n  {name}:")
        print(f"    Enabled: {enabled}")
        print(f"    Path: {path}")
        
        # 검증
        if '{date}' in path:
            print(f"    Status: [FAIL] Still contains {{date}}")
        elif today in path:
            print(f"    Status: [OK] Date replaced")
        else:
            print(f"    Status: [WARNING] No date pattern")
    
    print(f"\n[SUCCESS] Data sources loaded and dates replaced!")
    
except Exception as e:
    print(f"\n[FAIL] Error loading data sources: {e}")
    import traceback
    traceback.print_exc()

# 테스트 4: Collector와 통합 테스트
print("\n" + "="*80)
print("Test 4: Integration with OutboundCollector")
print("-"*80)

try:
    from data.collectors.outbound import OutboundCollector
    
    # config에서 경로 가져오기
    config = load_config_with_date('C:/Projects/WMS-DashBoard/dashboard/config/config.example.yaml')
    outbound_path = config['data_sources']['outbound']
    
    print(f"Outbound path from config: {outbound_path}")
    
    # Collector 생성
    collector = OutboundCollector(file_path=outbound_path)
    
    # 데이터 로드
    df = collector.get_data()
    
    print(f"\n[OK] Collector loaded data: {len(df)} records")
    print(f"[OK] Columns: {len(df.columns)}")
    
    # 요약 정보
    summary = collector.get_summary()
    print(f"\nSummary:")
    print(f"  Total records: {summary['총_출고건수']:,}")
    print(f"  Total order quantity: {summary['총_오더수량']:,}")
    print(f"  Total amount: {summary['총_출하금액']:,}")
    
    print(f"\n[SUCCESS] Integration test passed!")
    
except Exception as e:
    print(f"\n[FAIL] Integration test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("All Tests Completed")
print("="*80)
