"""
InventoryCollector - 재고 현황 Collector

백엔드가 생성한 inventory_status_YYYYMMDD.csv 파일을 읽어서
Flask API에 제공합니다.

파일 위치: C:/OSIS_AUTO/inventory_status/inventory_status_YYYYMMDD.csv

Author: WMS 개발팀
Date: 2025-11-19
"""

from .base_collector import BaseCollector
import pandas as pd


class InventoryCollector(BaseCollector):
    """재고 현황 데이터 제공 Collector"""
    
    def get_summary(self) -> dict:
        """
        재고 현황 요약 정보
        
        Returns:
            dict: {
                'total_count': 총 재고 건수,
                'risky_count': 유효유통비 20% 이하 건수 (L07 제외),
                'urgent_count': 유효유통비 10% 이하 건수 (긴급)
            }
        """
        if not self.validate():
            return {
                'total_count': 0,
                'risky_count': 0,
                'urgent_count': 0
            }
        
        df = self._read_csv()
        
        # L07 로케이션 제외 후 유효유통비 계산
        if '로케이션' in df.columns and '유효유통비(%)' in df.columns:
            df_filtered = df[~df['로케이션'].str.startswith('L07', na=False)]
            risky = df_filtered[df_filtered['유효유통비(%)'] <= 20]
            urgent = risky[risky['유효유통비(%)'] <= 10]
            
            return {
                'total_count': len(df),
                'risky_count': len(risky),
                'urgent_count': len(urgent)
            }
        
        return {
            'total_count': len(df),
            'risky_count': 0,
            'urgent_count': 0
        }
    
    def get_risky_products(self, threshold: int = 20) -> pd.DataFrame:
        """
        유효유통비 임계값 이하 상품 목록 (L07 제외)
        
        Args:
            threshold: 유효유통비 임계값 (기본: 20%)
        
        Returns:
            pd.DataFrame: 위험 상품 목록 (유효유통비 오름차순 정렬)
        """
        if not self.validate():
            return pd.DataFrame()
        
        df = self._read_csv()
        
        if '로케이션' not in df.columns or '유효유통비(%)' not in df.columns:
            return pd.DataFrame()
        
        # L07 제외 + 임계값 필터링 + 정렬
        risky = df[~df['로케이션'].str.startswith('L07', na=False)]
        risky = risky[risky['유효유통비(%)'] <= threshold]
        risky = risky.sort_values('유효유통비(%)')
        
        return risky
    
    def get_data(self) -> pd.DataFrame:
        """
        전체 재고 데이터 반환
        
        Returns:
            pd.DataFrame: 재고 전체 데이터
        """
        return self._read_csv()
