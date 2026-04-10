"""
BaseCollector - Flask용 CSV 데이터 읽기 전용 Collector 기반 클래스

백엔드 프로그램(C:\OSIS_AUTO\)이 생성한 CSV 파일을 읽어서
Flask API에 제공하는 경량 래퍼 클래스입니다.

역할:
- CSV 파일 존재 확인
- CSV 파일 읽기 (pandas DataFrame)
- 데이터 검증
- 공통 기능 제공

Author: WMS 개발팀
Date: 2025-11-19
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional


class BaseCollector:
    """Flask용 기본 Collector 클래스"""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8-sig'):
        """
        Args:
            file_path: CSV 파일 경로
            encoding: 파일 인코딩 (기본: utf-8-sig, BOM 제거)
        """
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._data: Optional[pd.DataFrame] = None
    
    def validate(self) -> bool:
        """
        파일 존재 및 데이터 유효성 검증
        
        Returns:
            bool: 검증 성공 여부
        """
        if not self.file_path.exists():
            return False
        
        # 파일이 비어있는지 확인
        if self.file_path.stat().st_size == 0:
            return False
        
        return True
    
    def _read_csv(self) -> pd.DataFrame:
        """
        CSV 파일을 읽어서 DataFrame 반환
        
        Returns:
            pd.DataFrame: CSV 데이터
        """
        if self._data is None:
            self._data = pd.read_csv(
                self.file_path,
                encoding=self.encoding
            )
        return self._data
    
    def get_data(self) -> pd.DataFrame:
        """
        전체 데이터 반환 (자식 클래스에서 오버라이드 가능)
        
        Returns:
            pd.DataFrame: 전체 데이터
        """
        return self._read_csv()
