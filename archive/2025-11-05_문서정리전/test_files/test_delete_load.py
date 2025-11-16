"""
DeleteCollector 데이터 로드 및 기능 테스트
"""
import sys
from pathlib import Path
from datetime import time

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "dashboard" / "src"))

from data.collectors.delete import DeleteCollector

print("=" * 60)
print("DeleteCollector 데이터 로드 테스트")
print("=" * 60)

# CSV 파일 경로
csv_path = r"C:\OSIS_AUTO\Delete Status\delete_status_20251029.csv"

try:
    # DeleteCollector 인스턴스 생성
    collector = DeleteCollector(csv_path)
    
    # 데이터 로드
    df = collector.get_data()
    
    print(f"\n[SUCCESS] 데이터 로드 성공: {len(df)}건")
    print(f"컬럼 개수: {len(df.columns)}")
    
    # 데이터 샘플 출력
    print("\n" + "=" * 60)
    print("데이터 샘플 (처음 3건)")
    print("=" * 60)
    print(df[['삭제처리일', '삭제처리시간', '상품명', '삭제수량', '알림여부']].head(3))
    
    # 타입 확인
    print("\n" + "=" * 60)
    print("데이터 타입 확인")
    print("=" * 60)
    print(f"삭제처리시간_time 타입: {df['삭제처리시간_time'].dtype}")
    print(f"삭제수량 타입: {df['삭제수량'].dtype}")
    if df['알림시각'].notna().any():
        print(f"알림시각 타입: {df['알림시각'].dtype}")
    
    # 18시 이후 카운트 테스트
    print("\n" + "=" * 60)
    print("18시 이후 삭제 카운트 테스트")
    print("=" * 60)
    after_18_count = collector.count_after_18()
    print(f"18시 이후 삭제 건수: {after_18_count}건")
    
    # 긴급 삭제 조회
    print("\n" + "=" * 60)
    print("긴급 삭제(18시 이후 + 알림Y) 조회")
    print("=" * 60)
    urgent = collector.get_urgent_deletes()
    print(f"긴급 삭제 건수: {len(urgent)}건")
    if not urgent.empty:
        print(urgent[['삭제처리시간', '상품명', '삭제수량', '알림여부']])
    
    # get_summary() 테스트
    print("\n" + "=" * 60)
    print("요약 통계 (get_summary)")
    print("=" * 60)
    summary = collector.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # 상위 상품 테스트
    print("\n" + "=" * 60)
    print("상위 삭제 상품 (Top 5)")
    print("=" * 60)
    top_products = collector.get_top_products(5)
    if not top_products.empty:
        print(top_products)
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 모든 기능 테스트 통과!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] 테스트 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
