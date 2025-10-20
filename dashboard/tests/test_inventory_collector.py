"""
InventoryCollector 테스트 스크립트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.collectors.inventory import InventoryCollector

def test_inventory_collector():
    """InventoryCollector 기본 테스트"""
    
    print("=" * 60)
    print("[테스트] InventoryCollector 테스트 시작")
    print("=" * 60)
    
    # 샘플 데이터 경로
    sample_file = project_root / "tests" / "fixtures" / "sample_inventory.csv"
    
    # Collector 생성
    print(f"\n[파일] {sample_file}")
    collector = InventoryCollector(str(sample_file), encoding='utf-8-sig')
    
    # 데이터 로드
    print("\n[로딩] 데이터 로딩...")
    df = collector.load_data()
    print(f"[성공] 총 {len(df)}개 레코드 로드 완료")
    
    # 요약 정보
    print("\n[요약] 요약 정보:")
    summary = collector.get_summary()
    for key, value in summary.items():
        if key == '유효비_구간별_분포':
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    - {k}: {v}개")
        elif key == '총_재고금액':
            print(f"  {key}: {value:,}원")
        else:
            print(f"  {key}: {value}")
    
    # 위험 상품
    print("\n[위험] 유효비 위험 상품 (<= 20%):")
    risky = collector.get_risky_products()
    if not risky.empty:
        print(f"  총 {len(risky)}개 상품")
        for idx, row in risky.iterrows():
            print(f"  - {row['상품명']} (유효비: {row['유효유통비(%)']}%, 가용수량: {row['가용수량']}개)")
    else:
        print("  없음")
    
    # 가용수량 부족 상품
    print("\n[부족] 가용수량 부족 상품 (<= 10개):")
    low_stock = collector.get_low_stock_products(threshold=10)
    if not low_stock.empty:
        print(f"  총 {len(low_stock)}개 상품")
        for idx, row in low_stock.iterrows():
            print(f"  - {row['상품명']} (가용수량: {row['가용수량']}개)")
    else:
        print("  없음")
    
    # 재고금액 상위 상품
    print("\n[TOP5] 재고금액 TOP 5:")
    top_value = collector.get_top_value_products(n=5)
    for idx, row in top_value.iterrows():
        print(f"  {idx+1}. {row['상품명']}")
        print(f"     재고금액: {int(row['재고금액']):,}원 (가용수량: {int(row['가용수량'])}개)")
    
    # 총 재고 금액
    print("\n[총금액] 총 재고 금액:")
    total_value = collector.calculate_total_value()
    print(f"  {total_value:,}원")
    
    print("\n" + "=" * 60)
    print("[완료] 테스트 완료!")
    print("=" * 60)

if __name__ == "__main__":
    test_inventory_collector()
