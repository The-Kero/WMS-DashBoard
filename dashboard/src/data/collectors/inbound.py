"""
InboundCollector - 입고 현황 데이터 수집기

역할: 입고 CSV 파일을 읽어 요약 통계 제공
"""
from .base_collector import BaseCollector


class InboundCollector(BaseCollector):
    """입고 현황 Collector"""
    
    def get_summary(self) -> dict:
        """
        입고 현황 요약 통계
        
        Returns:
            dict: {
                'total_count': 총 입고 건수,
                'progress_rate': 평균 진척률 (%),
                'unique_products': 고유 상품 수
            }
        """
        if self._data is None:
            self._data = self._read_csv()
        
        return {
            'total_count': len(self._data),
            'progress_rate': float(self._data['진척률'].mean()) if '진척률' in self._data.columns else 0.0,
            'unique_products': self._data['상품'].nunique() if '상품' in self._data.columns else 0
        }
