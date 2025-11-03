"""
IrregularCollector Import 테스트
"""
import sys

def test_irregular_import():
    print("="*60)
    print("IrregularCollector Import 테스트")
    print("="*60)
    
    try:
        # Import 시도
        from dashboard.src.data.collectors.irregular import IrregularCollector
        print("[OK] IrregularCollector import 성공")
        
        # 클래스 속성 확인
        print(f"[OK] REQUIRED_COLUMNS: {len(IrregularCollector.REQUIRED_COLUMNS)}개")
        print("\n필수 컬럼 목록:")
        for i, col in enumerate(IrregularCollector.REQUIRED_COLUMNS, 1):
            print(f"  {i}. {col}")
        
        # 메서드 확인
        methods = ['load_data', 'validate', 'get_data', 'refresh', 'file_exists', 'get_row_count']
        print(f"\n[OK] 메서드 확인:")
        for method in methods:
            if hasattr(IrregularCollector, method):
                print(f"  - {method}: 존재")
            else:
                print(f"  - {method}: 없음 (상속 확인 필요)")
        
        print("\n" + "="*60)
        print("[SUCCESS] 모든 Import 테스트 통과!")
        print("="*60)
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import 실패: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    result = test_irregular_import()
    sys.exit(0 if result else 1)
