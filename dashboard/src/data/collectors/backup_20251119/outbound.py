"""
OutboundCollector - 출고 현황 Collector

백엔드가 생성한 outbound_merged_YYYYMMDD.csv 파일을 읽어서
Flask API에 제공합니다.

파일 위치: C:/OSIS_AUTO/Outbound Status/outbound_merged_YYYYMMDD.csv

Author: WMS 개발팀
Date: 2025-11-19
"""

from .base_collector import BaseCollector
import pandas as pd


class OutboundCollector(BaseCollector):
    """출고 현황 데이터 제공 Collector"""
    
    def get_summary(self) -> dict:
        """
        출고 현황 요약 정보
        
        Returns:
            dict: {
                'total_count': 총 출고 건수,
                'total_amount': 총 출하금액,
                'by_type': 출고 유형별 건수
            }
        """
        if not self.validate():
            return {
                'total_count': 0,
                'total_amount': 0,
                'by_type': {}
            }
        
        df = self._read_csv()
        
        by_type = df.groupby('출고유형').size().to_dict() if '출고유형' in df.columns else {}
        
        return {
            'total_count': len(df),
            'total_amount': int(df['출하금액'].sum()) if '출하금액' in df.columns else 0,
            'by_type': by_type
        }
    
    def get_data(self) -> pd.DataFrame:
        """
        전체 출고 데이터 반환
        
        Returns:
            pd.DataFrame: 출고 전체 데이터
        """
        return self._read_csv()
