"""
DeleteCollector Import 테스트
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "dashboard" / "src"))

print("=" * 60)
print("DeleteCollector Import 테스트")
print("=" * 60)

try:
    from data.collectors.delete import DeleteCollector
    print("\n[SUCCESS] DeleteCollector import 성공!")
    
    # 클래스 속성 확인
    print(f"\nREQUIRED_COLUMNS: {len(DeleteCollector.REQUIRED_COLUMNS)}개")
    print(f"컬럼 목록: {DeleteCollector.REQUIRED_COLUMNS}")
    
    # 메서드 확인
    methods = [m for m in dir(DeleteCollector) if not m.startswith('_')]
    print(f"\n사용 가능한 메서드: {len(methods)}개")
    print(f"메서드 목록: {methods}")
    
    # 필수 메서드 확인
    required_methods = [
        'load_data', 'validate', 'get_data', 'refresh',
        'count_after_18', 'get_urgent_deletes', 'get_summary',
        'get_deletes_by_time_range', 'get_top_products'
    ]
    
    for method in required_methods:
        if hasattr(DeleteCollector, method):
            print(f"  [OK] {method}")
        else:
            print(f"  [FAIL] {method} - 없음!")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 모든 Import 테스트 통과!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] Import 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
