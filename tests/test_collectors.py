"""
단위 테스트: IrregularCollector 및 InboundCollector
pytest를 사용한 자동화된 테스트
"""
import pytest
import pandas as pd
from pathlib import Path
from dashboard.src.data.collectors.irregular import IrregularCollector
from dashboard.src.data.collectors.inbound import InboundCollector


class TestIrregularCollector:
    """IrregularCollector 테스트"""
    
    @pytest.fixture
    def irregular_csv_path(self):
        """테스트용 CSV 경로"""
        return r"C:\OSIS_AUTO\IrregularOrder Status\irregular_order_20251029.csv"
    
    @pytest.fixture
    def irregular_collector(self, irregular_csv_path):
        """IrregularCollector 인스턴스"""
        return IrregularCollector(irregular_csv_path, encoding='utf-8-sig')
    
    def test_required_columns(self):
        """필수 컬럼 7개 확인"""
        expected_columns = [
            '상세내용', '출고센터명', '입고센터명', '상품명',
            '입출수량', '라벨출력', '최초입력시각'
        ]
        assert IrregularCollector.REQUIRED_COLUMNS == expected_columns
        assert len(IrregularCollector.REQUIRED_COLUMNS) == 7
    
    def test_file_exists(self, irregular_collector):
        """파일 존재 확인"""
        assert irregular_collector.file_exists()
    
    def test_load_data(self, irregular_collector):
        """데이터 로드 테스트"""
        df = irregular_collector.load_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert '최초입력시각' in df.columns
        assert df['최초입력시각'].dtype == 'datetime64[ns]'
    
    def test_validate(self, irregular_collector):
        """데이터 검증 테스트"""
        df = irregular_collector.load_data()
        assert irregular_collector.validate(df) == True
    
    def test_get_summary(self, irregular_collector):
        """요약 정보 테스트"""
        summary = irregular_collector.get_summary()
        assert '총건수' in summary
        assert '라벨미출력' in summary
        assert '라벨출력완료' in summary
        assert summary['총건수'] > 0
        assert isinstance(summary['총건수'], int)
    
    def test_get_recent_orders(self, irregular_collector):
        """최근 오더 조회 테스트"""
        recent = irregular_collector.get_recent_orders(hours=24)
        assert isinstance(recent, pd.DataFrame)
    
    def test_get_unlabeled_orders(self, irregular_collector):
        """라벨 미출력 오더 테스트"""
        unlabeled = irregular_collector.get_unlabeled_orders()
        assert isinstance(unlabeled, pd.DataFrame)
        if len(unlabeled) > 0:
            assert all(unlabeled['라벨출력'] == 'N')
    
    def test_get_orders_by_center(self, irregular_collector):
        """센터별 통계 테스트"""
        outbound_stats = irregular_collector.get_orders_by_center('outbound')
        assert isinstance(outbound_stats, pd.DataFrame)
        assert '출고센터명' in outbound_stats.columns
        assert '오더건수' in outbound_stats.columns


class TestInboundCollector:
    """InboundCollector 테스트"""
    
    @pytest.fixture
    def inbound_csv_path(self):
        """테스트용 CSV 경로"""
        return r"C:\OSIS_AUTO\Inbound Status\integrated_inbound_20251027.csv"
    
    @pytest.fixture
    def inbound_collector(self, inbound_csv_path):
        """InboundCollector 인스턴스"""
        return InboundCollector(inbound_csv_path, encoding='utf-8-sig')
    
    def test_required_columns(self):
        """필수 컬럼 12개 확인"""
        expected_columns = [
            '입고예정일', '입고예정번호', '공급사명', '입고유형',
            '상품', '상품명', '단위및규격', '소비기한',
            '기본로케이션', '입고예정수량', '총입고수량', '진척률'
        ]
        assert InboundCollector.REQUIRED_COLUMNS == expected_columns
        assert len(InboundCollector.REQUIRED_COLUMNS) == 12
    
    def test_file_exists(self, inbound_collector):
        """파일 존재 확인"""
        assert inbound_collector.file_exists()
    
    def test_load_data(self, inbound_collector):
        """데이터 로드 테스트"""
        df = inbound_collector.load_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert '진척률' in df.columns
        assert df['진척률'].dtype in ['float64', 'int64']
    
    def test_validate(self, inbound_collector):
        """데이터 검증 테스트"""
        df = inbound_collector.load_data()
        assert inbound_collector.validate(df) == True
    
    def test_get_summary(self, inbound_collector):
        """요약 정보 테스트"""
        summary = inbound_collector.get_summary()
        assert '총_입고건수' in summary
        assert '입고완료건수' in summary
        assert '진행중건수' in summary
        assert '미입고건수' in summary
        assert '평균_진척률' in summary
        assert summary['총_입고건수'] > 0
    
    def test_get_pending_inbounds(self, inbound_collector):
        """미입고/진행중 목록 테스트"""
        pending = inbound_collector.get_pending_inbounds()
        assert isinstance(pending, pd.DataFrame)
        if len(pending) > 0:
            assert all(pending['진척률'] < 100.0)
    
    def test_get_completed_inbounds(self, inbound_collector):
        """입고완료 목록 테스트"""
        completed = inbound_collector.get_completed_inbounds()
        assert isinstance(completed, pd.DataFrame)
        if len(completed) > 0:
            assert all(completed['진척률'] >= 100.0)
    
    def test_get_top_suppliers(self, inbound_collector):
        """상위 공급사 테스트"""
        top_suppliers = inbound_collector.get_top_suppliers(3)
        assert isinstance(top_suppliers, pd.DataFrame)
        assert '공급사명' in top_suppliers.columns
        assert '총입고수량' in top_suppliers.columns
        assert len(top_suppliers) <= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
