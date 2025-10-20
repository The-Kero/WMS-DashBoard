"""
Config 유틸리티 함수
날짜 플레이스홀더 자동 치환 등
"""

from datetime import datetime
from pathlib import Path
import yaml


def replace_date_placeholder(config_dict: dict, date_format: str = "%Y%m%d") -> dict:
    """
    Config 딕셔너리의 {date} 플레이스홀더를 오늘 날짜로 치환
    
    Args:
        config_dict: 설정 딕셔너리
        date_format: 날짜 포맷 (기본값: YYYYMMDD)
        
    Returns:
        날짜가 치환된 설정 딕셔너리
    """
    today = datetime.now().strftime(date_format)
    
    def replace_in_value(value):
        """재귀적으로 값 치환"""
        if isinstance(value, str):
            return value.replace('{date}', today)
        elif isinstance(value, dict):
            return {k: replace_in_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_in_value(item) for item in value]
        else:
            return value
    
    return replace_in_value(config_dict)


def load_config_with_date(config_path: str) -> dict:
    """
    YAML 설정 파일을 로드하고 날짜 플레이스홀더 치환
    
    Args:
        config_path: 설정 파일 경로
        
    Returns:
        날짜가 치환된 설정 딕셔너리
        
    Example:
        >>> config = load_config_with_date('config/config.yaml')
        >>> print(config['data_sources']['inbound'])
        'C:/OSIS_AUTO/Inbound Status/inbound_merged_20251020.csv'
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 날짜 플레이스홀더 치환
    config = replace_date_placeholder(config)
    
    return config


def load_data_sources_with_date(data_sources_path: str) -> list:
    """
    data_sources.yaml 파일을 로드하고 날짜 플레이스홀더 치환
    
    Args:
        data_sources_path: data_sources.yaml 파일 경로
        
    Returns:
        날짜가 치환된 데이터 소스 리스트
        
    Example:
        >>> sources = load_data_sources_with_date('config/data_sources.yaml')
        >>> print(sources[0]['path'])
        'C:/OSIS_AUTO/Inbound Status/inbound_merged_20251020.csv'
    """
    sources_file = Path(data_sources_path)
    
    if not sources_file.exists():
        raise FileNotFoundError(f"데이터 소스 파일을 찾을 수 없습니다: {data_sources_path}")
    
    with open(sources_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 날짜 플레이스홀더 치환
    data = replace_date_placeholder(data)
    
    return data.get('sources', [])


# 사용 예시
if __name__ == "__main__":
    # 테스트
    test_config = {
        'data_sources': {
            'inbound': 'C:/OSIS_AUTO/Inbound Status/inbound_merged_{date}.csv',
            'outbound': 'C:/OSIS_AUTO/Outbound Status/outbound_all_{date}.csv'
        }
    }
    
    result = replace_date_placeholder(test_config)
    print("치환 결과:")
    for key, value in result['data_sources'].items():
        print(f"  {key}: {value}")
