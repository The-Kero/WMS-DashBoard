"""OutboundCollector Unit Test"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data.collectors import OutboundCollector

def test_outbound_collector():
    print("=" * 60)
    print("OutboundCollector Unit Test")
    print("=" * 60)
    
    print("\n[1] File load test...")
    collector = OutboundCollector('tests/fixtures/sample_outbound.csv')
    
    try:
        df = collector.load_data()
        print(f"[OK] Success: {len(df)} records loaded")
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False
    
    print("\n[2] Data validation test...")
    if collector.validate(df):
        print("[OK] Success: Data validation passed")
    else:
        print("[FAIL] Data validation failed")
        return False
    
    print("\n[3] Summary information test...")
    summary = collector.get_summary()
    print(f"   Total outbound: {summary['총_출고건수']} records")
    print(f"   Total quantity: {summary['총_출하수량']:,} items")
    print(f"   Total amount: {summary['총_출하금액']:,} KRW")
    print("[OK] Success: Summary generated")
    
    print("\n[4] Top destinations test...")
    top_dest = collector.get_top_destinations(n=3)
    print(f"[OK] Success: Top {len(top_dest)} destinations")
    print(top_dest.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_outbound_collector()
