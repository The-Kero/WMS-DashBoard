"""
InboundCollector - 입고 현황 Collector

백엔드가 생성한 integrated_inbound_YYYYMMDD.csv 파일을 읽어서
Flask API에 제공합니다.

파일 위치: C:/OSIS_AUTO/Inbound Status/integrated_inbound_YYYYMMDD.csv

Author: WMS 개발팀
Date: 2025-11-19
"""

from .base_collector import BaseCollector
import pandas as pd


class InboundCollector(BaseCollector):
    """입고 현황 데이터 제공 Collector"""
    
    def get_summary(self) -> dict:
        """
        입고 현황 요약 정보
        
        Returns:
            dict: {
                'total_count': 총 입고 건수,
                'progress_rate': 평균 진척률,
                'risky_count': 입고 유의 상품 개수 (재고와 비교 필요)
            }
        """
        if not self.validate():
            return {
                'total_count': 0,
                'progress_rate': 0.0,
                'risky_count': 0
            }
        
        df = self._read_csv()
        
        return {
            'total_count': len(df),
            'progress_rate': float(df['진척률'].mean()) if '진척률' in df.columns else 0.0,
            'risky_count': 0  # CollectorService에서 재고와 비교 후 계산
        }
    
    def get_data(self) -> pd.DataFrame:
        """
        전체 입고 데이터 반환
        
        Returns:
            pd.DataFrame: 입고 전체 데이터
        """
        return self._read_csv()
