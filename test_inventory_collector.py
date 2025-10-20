# -*- coding: utf-8 -*-
"""
InventoryCollector 테스트 스크립트 (이모지 제거 버전)
백엔드 실제 데이터로 기능 검증
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'dashboard' / 'src'))

from data.collectors.inventory import InventoryCollector

def test_inventory_collector():
    """InventoryCollector 전체 기능 테스트"""
    
    print("="*70)
    print("[InventoryCollector 테스트 시작]")
    print("="*70)
    
    # 백엔드 실제 데이터 경로
    file_path = r"C:\OSIS_AUTO\inventory_status\inventory_status_20251020.csv"
    
    # Collector 생성
    print(f"\n[1] Collector 생성 중...")
    print(f"    파일: {file_path}")
    
    try:
        collector = InventoryCollector(file_path, encoding='utf-8-sig')
        print("    [OK] Collector 생성 완료")
    except Exception as e:
        print(f"    [ERROR] {e}")
        return
    
    # 데이터 로드
    print(f"\n[2] 데이터 로드 중...")
    
    try:
        df = collector.load_data()
        print(f"    [OK] 데이터 로드 완료")
        print(f"    - 총 레코드 수: {len(df):,}개")
        print(f"    - 컬럼 수: {len(df.columns)}개")
    except Exception as e:
        print(f"    [ERROR] {e}")
        return
    
    # 요약 정보 테스트
    print(f"\n[3] 요약 정보 테스트")
    
    try:
        summary = collector.get_summary()
        print(f"    [OK] 요약 정보 생성 완료")
        print(f"\n    [4대 핵심 지표]")
        print(f"    1. 총 상품 수: {summary['총_상품_수']:,}개")
        print(f"    2. 총 재고 수량: {summary['총_재고_수량']:,}개")
        print(f"    3. 총 재고 금액: {summary['총_재고_금액']:,}원")
        print(f"    4. 위험 상품 수: {summary['위험_상품_수']:,}개 (유효비 <= 20%)")
        
        print(f"\n    [보조 지표]")
        print(f"    - 평균 유효유통비: {summary['평균_유효유통비']}%")
        print(f"    - 로케이션 수: {summary['로케이션_수']:,}개")
        print(f"    - 가용 수량: {summary['가용_수량']:,}개")
    except Exception as e:
        print(f"    [ERROR] {e}")
    
    # 유효기한 임박 상품 테스트
    print(f"\n[4] 유효기한 임박 상품 테스트 (유효비 <= 20%)")
    
    try:
        expiring = collector.get_expiring_soon(threshold=20)
        print(f"    [OK] 유효기한 임박 상품: {len(expiring)}개")
        
        if len(expiring) > 0:
            print(f"\n    [위험 상품 Top 3]")
            for i, (idx, row) in enumerate(expiring.head(3).iterrows(), 1):
                print(f"    {i}. {row['상품명']}")
                print(f"       유효비: {row['유효유통비(%)']}%, 재고: {int(row['재고수량'])}개")
    except Exception as e:
        print(f"    [ERROR] {e}")
    
    # 로케이션별 집계 테스트
    print(f"\n[5] 로케이션별 집계 테스트")
    
    try:
        by_location = collector.get_by_location()
        print(f"    [OK] 로케이션별 집계 완료: {len(by_location)}개")
        
        print(f"\n    [상위 로케이션 Top 3 (재고금액 기준)]")
        for i, (idx, row) in enumerate(by_location.head(3).iterrows(), 1):
            print(f"    {i}. {row['로케이션']}")
            print(f"       상품 종류: {int(row['상품_종류'])}개, 재고금액: {int(row['총_재고금액']):,}원")
    except Exception as e:
        print(f"    [ERROR] {e}")
    
    # 상품별 집계 테스트
    print(f"\n[6] 상품별 집계 테스트")
    
    try:
        by_product = collector.get_by_product(n=3)
        print(f"    [OK] 상품별 집계 완료")
        
        print(f"\n    [상위 상품 Top 3 (재고금액 기준)]")
        for i, (idx, row) in enumerate(by_product.iterrows(), 1):
            print(f"    {i}. {row['상품명']}")
            print(f"       재고금액: {int(row['총_재고금액']):,}원, 재고: {int(row['총_재고수량'])}개")
    except Exception as e:
        print(f"    [ERROR] {e}")
    
    # 유효비 구간별 분포 테스트
    print(f"\n[7] 유효비 구간별 분포 테스트")
    
    try:
        distribution = collector.get_effective_ratio_distribution()
        print(f"    [OK] 유효비 분포 집계 완료")
        
        print(f"\n    [유효유통비 구간별 분포]")
        for idx, row in distribution.iterrows():
            print(f"    - {row['유효비_구간']}: {int(row['상품_수'])}개 상품")
    except Exception as e:
        print(f"    [ERROR] {e}")
    
    # 테스트 완료
    print(f"\n{'='*70}")
    print(f"[InventoryCollector 테스트 완료!]")
    print(f"{'='*70}")


if __name__ == "__main__":
    test_inventory_collector()
