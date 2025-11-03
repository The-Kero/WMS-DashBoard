"""
InboundCollector 수정 검증 테스트
실제 CSV 파일로 데이터 로딩 및 새로운 기능 확인
"""
import sys
from pathlib import Path

def test_inbound_updated():
    print("="*60)
    print("InboundCollector 수정 검증 테스트")
    print("="*60)
    
    try:
        from dashboard.src.data.collectors.inbound import InboundCollector
        
        # 실제 CSV 파일 경로
        csv_path = r"C:\OSIS_AUTO\Inbound Status\integrated_inbound_20251027.csv"
        
        # 파일 존재 확인
        if not Path(csv_path).exists():
            print(f"[ERROR] 파일이 존재하지 않습니다: {csv_path}")
            return False
        
        print(f"[OK] 파일 확인: {csv_path}")
        
        # Collector 생성
        collector = InboundCollector(csv_path, encoding='utf-8-sig')
        print("[OK] InboundCollector 인스턴스 생성")
        
        # 필수 컬럼 확인
        print(f"\n[OK] REQUIRED_COLUMNS: {len(InboundCollector.REQUIRED_COLUMNS)}개")
        for i, col in enumerate(InboundCollector.REQUIRED_COLUMNS, 1):
            print(f"  {i}. {col}")
        
        # 데이터 로드
        df = collector.load_data()
        print(f"\n[OK] 데이터 로드 성공: {len(df)}건")
        
        # 데이터 타입 확인
        print("\n[OK] 데이터 타입 변환 확인:")
        print(f"  - 입고예정일: {df['입고예정일'].dtype}")
        print(f"  - 소비기한: {df['소비기한'].dtype}")
        print(f"  - 입고예정수량: {df['입고예정수량'].dtype}")
        print(f"  - 총입고수량: {df['총입고수량'].dtype}")
        print(f"  - 진척률: {df['진척률'].dtype}")
        
        # get_summary() 테스트
        print("\n" + "-"*60)
        print("get_summary() 테스트")
        print("-"*60)
        summary = collector.get_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # get_pending_inbounds() 테스트
        print("\n" + "-"*60)
        print("get_pending_inbounds() 테스트")
        print("-"*60)
        pending = collector.get_pending_inbounds()
        print(f"  미입고/진행중: {len(pending)}건")
        
        # get_completed_inbounds() 테스트
        print("\n" + "-"*60)
        print("get_completed_inbounds() 테스트")
        print("-"*60)
        completed = collector.get_completed_inbounds()
        print(f"  입고완료: {len(completed)}건")
        
        # get_top_suppliers() 테스트
        print("\n" + "-"*60)
        print("get_top_suppliers() 테스트")
        print("-"*60)
        top_suppliers = collector.get_top_suppliers(3)
        print(top_suppliers.to_string(index=False))
        
        print("\n" + "="*60)
        print("[SUCCESS] 모든 테스트 통과!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_inbound_updated()
    sys.exit(0 if result else 1)
