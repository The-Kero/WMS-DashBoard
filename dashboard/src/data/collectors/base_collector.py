"""
BaseCollector - 모든 Collector의 기본 클래스

역할: CSV 파일 읽기 및 검증 공통 기능 제공
"""
from pathlib import Path
from typing import Optional
import pandas as pd
from datetime import datetime


class BaseCollector:
    """모든 Collector의 추상 기본 클래스"""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8-sig'):
        """
        Args:
            file_path: CSV 파일 경로
            encoding: 파일 인코딩 (기본값: utf-8-sig, Excel 호환)
        """
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._data: Optional[pd.DataFrame] = None
    
    def validate(self) -> bool:
        """
        파일 존재 여부 및 데이터 유효성 검증
        
        Returns:
            bool: 검증 통과 여부
        """
        # 파일 존재 확인
        if not self.file_path.exists():
            return False
        
        # 파일 크기 확인 (0바이트면 False)
        if self.file_path.stat().st_size == 0:
            return False
        
        # DataFrame 로드 시도
        try:
            self._data = self._read_csv()
            return not self._data.empty
        except Exception:
            return False
    
    def _read_csv(self) -> pd.DataFrame:
        """
        CSV 파일을 읽어 DataFrame 반환 (Private 메서드)
        
        Returns:
            pd.DataFrame: 읽은 데이터
        """
        return pd.read_csv(
            self.file_path,
            encoding=self.encoding,
            low_memory=False
        )
    
    def get_data(self) -> pd.DataFrame:
        """
        전체 데이터 반환
        
        Returns:
            pd.DataFrame: 전체 데이터
        """
        if self._data is None:
            self._data = self._read_csv()
        return self._data.copy()
    
    def get_summary(self) -> dict:
        """
        요약 통계 반환 (서브클래스에서 구현)
        
        Returns:
            dict: 요약 정보
        """
        raise NotImplementedError("서브클래스에서 구현 필요")
