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


class TestDeleteCollector:
    """DeleteCollector 테스트"""
    
    @pytest.fixture
    def delete_csv_path(self):
        """테스트용 CSV 경로"""
        return r"C:\OSIS_AUTO\Delete Status\delete_status_20251029.csv"
    
    @pytest.fixture
    def delete_collector(self, delete_csv_path):
        """DeleteCollector 인스턴스"""
        from dashboard.src.data.collectors.delete import DeleteCollector
        return DeleteCollector(delete_csv_path, encoding='utf-8-sig')
    
    def test_required_columns(self):
        """필수 컬럼 15개 확인"""
        from dashboard.src.data.collectors.delete import DeleteCollector
        expected_columns = [
            '삭제처리일', '삭제처리시간', '상품', '상품명', '단위 및 규격',
            '삭제수량', '주문일자', '배송군', '배송처', '배송처명',
            '라벨출력', '출하바코드', 'To로케이션', '알림여부', '알림시각'
        ]
        assert DeleteCollector.REQUIRED_COLUMNS == expected_columns
        assert len(DeleteCollector.REQUIRED_COLUMNS) == 15
    
    def test_file_exists(self, delete_collector):
        """파일 존재 확인"""
        assert delete_collector.file_exists()
    
    def test_load_data(self, delete_collector):
        """데이터 로드 테스트"""
        df = delete_collector.load_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert '삭제처리시간_time' in df.columns
        assert '삭제수량' in df.columns
        assert df['삭제수량'].dtype in ['int64', 'float64']
    
    def test_validate(self, delete_collector):
        """데이터 검증 테스트"""
        df = delete_collector.load_data()
        assert delete_collector.validate(df) == True
    
    def test_count_after_18(self, delete_collector):
        """18시 이후 카운트 테스트"""
        count = delete_collector.count_after_18()
        assert isinstance(count, int)
        assert count >= 0
    
    def test_get_urgent_deletes(self, delete_collector):
        """긴급 삭제 조회 테스트"""
        urgent = delete_collector.get_urgent_deletes()
        assert isinstance(urgent, pd.DataFrame)
        # 18시 이후 + 알림Y 조건 확인
        if len(urgent) > 0:
            assert all(urgent['알림여부'] == 'Y')
    
    def test_get_summary(self, delete_collector):
        """요약 정보 테스트"""
        summary = delete_collector.get_summary()
        assert '총삭제건수' in summary
        assert '18시이후건수' in summary
        assert '긴급알림건수' in summary
        assert '총삭제수량' in summary
        assert '배송처수' in summary
        assert summary['총삭제건수'] > 0
        assert isinstance(summary['평균삭제수량'], float)
    
    def test_get_top_products(self, delete_collector):
        """상위 삭제 상품 테스트"""
        top_products = delete_collector.get_top_products(5)
        assert isinstance(top_products, pd.DataFrame)
        if len(top_products) > 0:
            assert '삭제수량' in top_products.columns
            assert '삭제건수' in top_products.columns
            assert len(top_products) <= 5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
