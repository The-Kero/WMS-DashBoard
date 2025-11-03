"""
삭제현황 YAML 설정 검증 스크립트
- YAML의 required_columns와 실제 CSV 파일의 컬럼이 일치하는지 확인
"""
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

# 경로 설정
yaml_path = Path(r"C:\Projects\WMS-DashBoard\dashboard\config\data_sources.yaml")
csv_path = Path(r"C:\OSIS_AUTO\Delete Status\delete_status_20251029.csv")

def load_yaml():
    """YAML 파일에서 delete 섹션 읽기"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    for source in config['sources']:
        if source['name'] == 'delete':
            return source['required_columns']
    return None

def load_csv_columns():
    """CSV 파일의 컬럼명 읽기"""
    df = pd.read_csv(csv_path, encoding='utf-8-sig', nrows=0)
    return df.columns.tolist()

def verify():
    """검증 실행"""
    print("=" * 60)
    print("삭제현황 YAML 검증 시작")
    print("=" * 60)
    
    # YAML 컬럼 로드
    yaml_columns = load_yaml()
    if not yaml_columns:
        print("[ERROR] YAML에서 delete 섹션을 찾을 수 없습니다.")
        return False
    
    print(f"\n[OK] YAML 파일 로드 성공: {yaml_path}")
    print(f"  기대 컬럼 개수: {len(yaml_columns)}")
    print(f"  기대 컬럼: {yaml_columns}")
    
    # CSV 컬럼 로드
    csv_columns = load_csv_columns()
    print(f"\n[OK] CSV 파일 로드 성공: {csv_path}")
    print(f"  실제 컬럼 개수: {len(csv_columns)}")
    print(f"  실제 컬럼: {csv_columns}")
    
    # 컬럼 일치 확인
    print("\n" + "=" * 60)
    print("컬럼 비교 결과")
    print("=" * 60)
    
    all_match = True
    
    # YAML에는 있지만 CSV에 없는 컬럼
    missing_in_csv = set(yaml_columns) - set(csv_columns)
    if missing_in_csv:
        print(f"\n[ERROR] CSV에 없는 컬럼: {missing_in_csv}")
        all_match = False
    
    # CSV에는 있지만 YAML에 없는 컬럼
    extra_in_csv = set(csv_columns) - set(yaml_columns)
    if extra_in_csv:
        print(f"\n[WARNING] YAML에 없는 컬럼 (선택적): {extra_in_csv}")
    
    # 순서 비교
    if yaml_columns == csv_columns:
        print("\n[SUCCESS] 모든 컬럼이 순서까지 완벽하게 일치합니다!")
    elif set(yaml_columns) == set(csv_columns):
        print("\n[SUCCESS] 모든 컬럼이 존재합니다 (순서만 다름)")
    elif all_match:
        print("\n[SUCCESS] 필수 컬럼이 모두 존재합니다")
    else:
        print("\n[FAIL] 컬럼 불일치가 있습니다")
        return False
    
    print("\n" + "=" * 60)
    print("검증 완료!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = verify()
    exit(0 if success else 1)
