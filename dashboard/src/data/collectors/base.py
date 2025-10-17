"""
BaseCollector: 모든 데이터 수집기의 추상 기본 클래스

확장 가능한 플러그인 아키텍처를 위한 베이스 클래스
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import pandas as pd


class BaseCollector(ABC):
    """데이터 수집기 추상 클래스"""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        """
        Args:
            file_path: CSV 파일 경로
            encoding: 파일 인코딩 (기본값: utf-8)
        """
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._data: Optional[pd.DataFrame] = None
        
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """
        데이터를 로드하고 반환
        
        Returns:
            pandas DataFrame
        """
        pass
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """
        데이터 유효성 검증
        
        Args:
            df: 검증할 DataFrame
            
        Returns:
            유효성 여부 (True/False)
        """
        pass
    
    def get_data(self) -> pd.DataFrame:
        """
        캐시된 데이터를 반환하거나 새로 로드
        
        Returns:
            pandas DataFrame
        """
        if self._data is None:
            self._data = self.load_data()
        return self._data
    
    def refresh(self) -> pd.DataFrame:
        """
        데이터 강제 새로고침
        
        Returns:
            pandas DataFrame
        """
        self._data = self.load_data()
        return self._data
    
    def file_exists(self) -> bool:
        """
        파일 존재 여부 확인
        
        Returns:
            파일 존재 여부
        """
        return self.file_path.exists()
    
    def get_row_count(self) -> int:
        """
        데이터 행 개수 반환
        
        Returns:
            행 개수
        """
        df = self.get_data()
        return len(df)
