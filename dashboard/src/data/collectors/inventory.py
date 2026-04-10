"""
InventoryCollector - 재고 현황 데이터 수집기

역할: 재고 CSV 파일을 읽어 요약 통계 및 위험상품 제공
"""
import pandas as pd
from .base_collector import BaseCollector


class InventoryCollector(BaseCollector):
    """재고 현황 Collector"""
    
    def get_summary(self) -> dict:
        """
        재고 현황 요약 통계
        
        Returns:
            dict: {
                'total_count': 총 재고 건수,
                'unique_products': 고유 상품 수,
                'risky_count': 유효유통비 20% 이하 건수
            }
        """
        if self._data is None:
            self._data = self._read_csv()
        
        risky = 0
        if '유효유통비(%)' in self._data.columns:
            risky = len(self._data[self._data['유효유통비(%)'] <= 20])
        
        return {
            'total_count': len(self._data),
            'unique_products': self._data['상품'].nunique() if '상품' in self._data.columns else 0,
            'risky_count': risky
        }
    
    def get_risky_products(self, threshold: int = 20) -> pd.DataFrame:
        """
        유효유통비 기준 이하 위험 상품 반환
        
        Args:
            threshold: 유효유통비 임계값 (기본 20%)
        
        Returns:
            pd.DataFrame: 위험 상품 목록
        """
        if self._data is None:
            self._data = self._read_csv()
        
        if '유효유통비(%)' not in self._data.columns:
            return pd.DataFrame()
        
        return self._data[self._data['유효유통비(%)'] <= threshold].copy()
