"""
IrregularCollector 데이터 로드 테스트
실제 CSV 파일로 데이터 로딩 및 타입 변환 확인
"""
import sys
from pathlib import Path

def test_irregular_load():
    print("="*60)
    print("IrregularCollector 데이터 로드 테스트")
    print("="*60)
    
    try:
        from dashboard.src.data.collectors.irregular import IrregularCollector
        
        # 실제 CSV 파일 경로
        csv_path = r"C:\OSIS_AUTO\IrregularOrder Status\irregular_order_20251029.csv"
        
        # 파일 존재 확인
        if not Path(csv_path).exists():
            print(f"[ERROR] 파일이 존재하지 않습니다: {csv_path}")
            return False
        
        print(f"[OK] 파일 확인: {csv_path}")
        
        # Collector 생성
        collector = IrregularCollector(csv_path, encoding='utf-8-sig')
        print("[OK] IrregularCollector 인스턴스 생성")
        
        # 데이터 로드
        df = collector.load_data()
        print(f"[OK] 데이터 로드 성공: {len(df)}건")
        
        # 컬럼 확인
        print(f"\n실제 컬럼 ({len(df.columns)}개):")
        for col in df.columns:
            print(f"  - {col}: {df[col].dtype}")
        
        # 데이터 타입 확인
        print("\n[OK] 데이터 타입 변환 확인:")
        print(f"  - 최초입력시각: {df['최초입력시각'].dtype} (datetime64 예상)")
        print(f"  - 입출수량: {df['입출수량'].dtype} (float64/int64 예상)")
        
        # 샘플 데이터 출력
        print(f"\n샘플 데이터 (첫 2건):")
        print(df.head(2).to_string())
        
        # 통계
        print(f"\n[OK] 데이터 통계:")
        print(f"  - 총 건수: {len(df)}")
        print(f"  - 라벨미출력(N): {len(df[df['라벨출력'] == 'N'])}")
        print(f"  - 라벨출력(Y): {len(df[df['라벨출력'] == 'Y'])}")
        print(f"  - 총 입출수량: {df['입출수량'].sum()}")
        
        print("\n" + "="*60)
        print("[SUCCESS] 데이터 로드 테스트 통과!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_irregular_load()
    sys.exit(0 if result else 1)
