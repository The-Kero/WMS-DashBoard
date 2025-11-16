"""
IrregularCollector 전체 기능 테스트
get_summary(), get_recent_orders(), get_unlabeled_orders() 등 모든 메서드 테스트
"""
import sys
from pathlib import Path

def test_irregular_complete():
    print("="*60)
    print("IrregularCollector 전체 기능 테스트")
    print("="*60)
    
    try:
        from dashboard.src.data.collectors.irregular import IrregularCollector
        
        # CSV 파일 경로
        csv_path = r"C:\OSIS_AUTO\IrregularOrder Status\irregular_order_20251029.csv"
        
        # Collector 생성
        collector = IrregularCollector(csv_path, encoding='utf-8-sig')
        print("[OK] Collector 생성 완료")
        
        # 1. get_summary() 테스트
        print("\n" + "-"*60)
        print("1. get_summary() 테스트")
        print("-"*60)
        summary = collector.get_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # 2. get_recent_orders() 테스트
        print("\n" + "-"*60)
        print("2. get_recent_orders(hours=24) 테스트")
        print("-"*60)
        recent = collector.get_recent_orders(hours=24)
        print(f"  최근 24시간 오더: {len(recent)}건")
        if len(recent) > 0:
            print(f"  샘플: {recent.iloc[0]['상세내용'][:50]}...")
        
        # 3. get_unlabeled_orders() 테스트
        print("\n" + "-"*60)
        print("3. get_unlabeled_orders() 테스트")
        print("-"*60)
        unlabeled = collector.get_unlabeled_orders()
        print(f"  라벨 미출력 오더: {len(unlabeled)}건")
        if len(unlabeled) > 0:
            print("  미출력 목록:")
            for idx, row in unlabeled.iterrows():
                print(f"    - {row['상세내용'][:40]}... ({row['입출수량']}개)")
        
        # 4. get_orders_by_center() 테스트
        print("\n" + "-"*60)
        print("4. get_orders_by_center() 테스트")
        print("-"*60)
        outbound_stats = collector.get_orders_by_center('outbound')
        print("  출고센터별 통계:")
        print(outbound_stats.to_string(index=False))
        
        inbound_stats = collector.get_orders_by_center('inbound')
        print("\n  입고센터별 통계:")
        print(inbound_stats.to_string(index=False))
        
        print("\n" + "="*60)
        print("[SUCCESS] 모든 기능 테스트 통과!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_irregular_complete()
    sys.exit(0 if result else 1)
