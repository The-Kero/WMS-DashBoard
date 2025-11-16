"""
입고 YAML 검증 스크립트
inbound 섹션의 컬럼 구성이 올바른지 확인
"""
import yaml
import sys

def verify_inbound_yaml():
    yaml_path = r'C:\Projects\WMS-DashBoard\dashboard\config\data_sources.yaml'
    
    print("="*60)
    print("입고 YAML 검증 시작")
    print("="*60)
    
    try:
        # YAML 파일 로드
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("[OK] YAML 파일 로드 성공")
        
        # inbound 섹션 찾기
        inbound = None
        for source in config['sources']:
            if source['name'] == 'inbound':
                inbound = source
                break
        
        if not inbound:
            print("[ERROR] inbound 섹션을 찾을 수 없습니다")
            return False
        
        print("[OK] inbound 섹션 발견")
        
        # 파일명 확인
        print(f"[OK] 파일명: {inbound['path']}")
        if 'integrated_inbound' not in inbound['path']:
            print("[WARNING] 파일명이 integrated_inbound가 아닙니다")
        
        # 기대하는 컬럼 (실제 CSV와 일치)
        expected = [
            '입고예정일',
            '입고예정번호',
            '공급사명',
            '입고유형',
            '상품',
            '상품명',
            '단위및규격',
            '소비기한',
            '기본로케이션',
            '입고예정수량',
            '총입고수량',
            '진척률'
        ]
        
        # 실제 컬럼
        actual = inbound['required_columns']
        
        print(f"\n기대 컬럼 개수: {len(expected)}")
        print(f"실제 컬럼 개수: {len(actual)}")
        
        # 컬럼 비교
        if actual == expected:
            print("\n" + "="*60)
            print("[SUCCESS] 검증 통과! 모든 컬럼이 일치합니다")
            print("="*60)
            print("\n실제 컬럼 목록:")
            for i, col in enumerate(actual, 1):
                print(f"  {i}. {col}")
            return True
        else:
            print("\n[FAIL] 검증 실패! 컬럼이 일치하지 않습니다")
            print("\n기대 컬럼:")
            for i, col in enumerate(expected, 1):
                status = "[OK]" if col in actual else "[MISSING]"
                print(f"  {status} {i}. {col}")
            
            print("\n실제 컬럼:")
            for i, col in enumerate(actual, 1):
                status = "[OK]" if col in expected else "[EXTRA]"
                print(f"  {status} {i}. {col}")
            
            return False
            
    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        return False

if __name__ == "__main__":
    result = verify_inbound_yaml()
    sys.exit(0 if result else 1)
