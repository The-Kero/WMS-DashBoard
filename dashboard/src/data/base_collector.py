"""
기본 데이터 수집기 추상 클래스
모든 Collector는 이 클래스를 상속받아 구현
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
import glob
import os


class BaseCollector(ABC):
    """모든 데이터 수집기의 베이스 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: 수집기 설정
                - name: 수집기 이름
                - path: 데이터 파일 경로 패턴
                - enabled: 활성화 여부
        """
        self.config = config
        self.name = config.get('name', self.__class__.__name__)
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    def collect(self) -> pd.DataFrame:
        """
        데이터 수집 - 반드시 구현해야 함
        
        Returns:
            pd.DataFrame: 수집된 데이터
        """
        pass
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """
        데이터 검증 - 반드시 구현해야 함
        
        Args:
            df: 검증할 데이터프레임
            
        Returns:
            bool: 유효하면 True
        """
        pass
    
    def get_latest_file(self, pattern: str) -> str:
        """
        패턴에 맞는 최신 파일 찾기
        
        Args:
            pattern: 파일 경로 패턴 (예: "C:/data/*.csv")
            
        Returns:
            str: 최신 파일 경로, 없으면 None
        """
        files = glob.glob(pattern)
        if not files:
            return None
        return max(files, key=os.path.getctime)
    
    def is_enabled(self) -> bool:
        """수집기 활성화 여부"""
        return self.enabled
