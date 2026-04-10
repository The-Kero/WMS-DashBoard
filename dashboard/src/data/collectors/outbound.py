"""
OutboundCollector - 출고 현황 데이터 수집기

역할: 출고 CSV 파일을 읽어 요약 통계 제공
"""
from .base_collector import BaseCollector


class OutboundCollector(BaseCollector):
    """출고 현황 Collector"""
    
    def get_summary(self) -> dict:
        """
        출고 현황 요약 통계
        
        Returns:
            dict: {
                'total_count': 총 출고 건수,
                'total_amount': 총 출하금액,
                'unique_destinations': 고유 배송처 수
            }
        """
        if self._data is None:
            self._data = self._read_csv()
        
        return {
            'total_count': len(self._data),
            'total_amount': int(self._data['출하금액'].sum()) if '출하금액' in self._data.columns else 0,
            'unique_destinations': self._data['배송처명'].nunique() if '배송처명' in self._data.columns else 0
        }
