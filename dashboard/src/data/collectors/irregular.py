"""
IrregularCollector - 비정형 오더 데이터 수집기

역할: 비정형 오더 CSV 파일을 읽어 요약 통계 제공
"""
from .base_collector import BaseCollector


class IrregularCollector(BaseCollector):
    """비정형 오더 Collector"""
    
    def get_summary(self) -> dict:
        """
        비정형 오더 요약 통계
        
        Returns:
            dict: {
                'total_count': 총 비정형 오더 건수,
                'unlabeled_count': 라벨 미출력 건수
            }
        """
        if self._data is None:
            self._data = self._read_csv()
        
        unlabeled = 0
        if '라벨출력' in self._data.columns:
            unlabeled = len(self._data[self._data['라벨출력'] == 'N'])
        
        return {
            'total_count': len(self._data),
            'unlabeled_count': unlabeled
        }
