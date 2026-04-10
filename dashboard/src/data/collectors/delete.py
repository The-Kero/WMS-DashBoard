"""
DeleteCollector - 삭제 현황 데이터 수집기

역할: 삭제 CSV 파일을 읽어 요약 통계 제공
"""
from .base_collector import BaseCollector


class DeleteCollector(BaseCollector):
    """삭제 현황 Collector"""
    
    def get_summary(self) -> dict:
        """
        삭제 현황 요약 통계
        
        Returns:
            dict: {
                'total_count': 총 삭제 건수,
                'unique_products': 고유 상품 수
            }
        """
        if self._data is None:
            self._data = self._read_csv()
        
        return {
            'total_count': len(self._data),
            'unique_products': self._data['상품'].nunique() if '상품' in self._data.columns else 0
        }
