"""
DeleteCollector - 삭제 현황 Collector

백엔드가 생성한 delete_status_YYYYMMDD.csv 파일을 읽어서
Flask API에 제공합니다.

파일 위치: C:/OSIS_AUTO/Delete Status/delete_status_YYYYMMDD.csv

Author: WMS 개발팀
Date: 2025-11-19
"""

from .base_collector import BaseCollector
import pandas as pd


class DeleteCollector(BaseCollector):
    """삭제 현황 데이터 제공 Collector"""
    
    def get_summary(self) -> dict:
        """
        삭제 현황 요약 정보
        
        Returns:
            dict: {
                'total_count': 총 삭제 건수,
                'after_18_count': 18시 이후 삭제 건수
            }
        """
        if not self.validate():
            return {
                'total_count': 0,
                'after_18_count': 0
            }
        
        df = self._read_csv()
        
        # 18시 이후 삭제 건수 계산
        after_18_count = 0
        if '삭제시간' in df.columns:
            df['삭제시간_str'] = df['삭제시간'].astype(str)
            after_18 = df[df['삭제시간_str'].str[:2].astype(int) >= 18]
            after_18_count = len(after_18)
        
        return {
            'total_count': len(df),
            'after_18_count': after_18_count
        }
    
    def get_data(self) -> pd.DataFrame:
        """
        전체 삭제 데이터 반환
        
        Returns:
            pd.DataFrame: 삭제 전체 데이터
        """
        return self._read_csv()
