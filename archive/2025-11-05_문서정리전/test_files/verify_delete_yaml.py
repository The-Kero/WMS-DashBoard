"""
삭제현황 YAML 검증 스크립트
실제 CSV 파일과 data_sources.yaml의 delete 섹션 컬럼 비교
"""
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

def verify_delete_yaml():
    print("=" * 60)
    print("삭제현황 YAML 검증 시작")
    print("=" * 60)
    
    # YAML 파일 읽기
    yaml_path = Path("C:/Projects/WMS-DashBoard/dashboard/config/data_sources.yaml")
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # delete 섹션 찾기
    delete_config = None
    for source in config['sources']:
        if source['name'] == 'delete':
            delete_config = source
            break
    
    if not delete_config:
        print("[ERROR] delete 섹션을 찾을 수 없습니다!")
        return False
    
    yaml_columns = delete_config['required_columns']
    print(f"\n[YAML] 기대 컬럼 ({len(yaml_columns)}개):")
    for i, col in enumerate(yaml_columns, 1):
        print(f"  {i}. {col}")
    
    # 최신 CSV 파일 찾기
    csv_dir = Path("C:/OSIS_AUTO/Delete Status")
    csv_files = sorted(csv_dir.glob("delete_status_*.csv"), reverse=True)
    
    if not csv_files:
        print("\n[ERROR] CSV 파일을 찾을 수 없습니다!")
        return False
    
    latest_csv = csv_files[0]
    print(f"\n[CSV] 최신 파일: {latest_csv.name}")
    
    # CSV 컬럼 읽기 (BOM 처리)
    df = pd.read_csv(latest_csv, encoding='utf-8-sig', nrows=0)
    csv_columns = df.columns.tolist()
    
    print(f"\n[CSV] 실제 컬럼 ({len(csv_columns)}개):")
    for i, col in enumerate(csv_columns, 1):
        print(f"  {i}. {col}")
    
    # 컬럼 비교
    print("\n" + "=" * 60)
    print("컬럼 비교 결과")
    print("=" * 60)
    
    yaml_set = set(yaml_columns)
    csv_set = set(csv_columns)
    
    # 일치하는 컬럼
    matching = yaml_set & csv_set
    print(f"\n[OK] 일치하는 컬럼 ({len(matching)}개):")
    for col in sorted(matching):
        print(f"  - {col}")
    
    # YAML에만 있는 컬럼
    yaml_only = yaml_set - csv_set
    if yaml_only:
        print(f"\n[WARNING] YAML에만 있는 컬럼 ({len(yaml_only)}개):")
        for col in sorted(yaml_only):
            print(f"  - {col}")
    
    # CSV에만 있는 컬럼
    csv_only = csv_set - yaml_set
    if csv_only:
        print(f"\n[WARNING] CSV에만 있는 컬럼 ({len(csv_only)}개):")
        for col in sorted(csv_only):
            print(f"  - {col}")
    
    # 최종 결과
    print("\n" + "=" * 60)
    if len(yaml_columns) == len(csv_columns) and not yaml_only and not csv_only:
        print("[SUCCESS] 검증 통과! 모든 컬럼이 일치합니다")
        print(f"기대 컬럼 개수: {len(yaml_columns)}")
        print(f"실제 컬럼 개수: {len(csv_columns)}")
        print("=" * 60)
        return True
    else:
        print("[FAILED] 검증 실패! 컬럼이 일치하지 않습니다")
        print(f"기대 컬럼 개수: {len(yaml_columns)}")
        print(f"실제 컬럼 개수: {len(csv_columns)}")
        print(f"불일치 개수: {len(yaml_only) + len(csv_only)}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = verify_delete_yaml()
    exit(0 if success else 1)
