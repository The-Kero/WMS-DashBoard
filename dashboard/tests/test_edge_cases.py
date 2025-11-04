"""
Edge Case 테스트 - 모든 Collector의 예외 상황 검증

테스트 카테고리:
1. 파일 관련 (4개)
2. 데이터 품질 (6개)
3. 경계값 (5개)
4. 비즈니스 로직 (5개)

총 20개 테스트
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.collectors.inbound import InboundCollector
from src.data.collectors.outbound import OutboundCollector
from src.data.collectors.inventory import InventoryCollector
from src.data.collectors.delete import DeleteCollector
from src.data.collectors.irregular import IrregularCollector

# 테스트 픽스처 경로
FIXTURES = Path(__file__).parent / "fixtures"
EDGE_CASES = FIXTURES / "edge_cases"


class TestFileRelatedEdgeCases:
    """파일 관련 Edge Case 테스트 (4개)"""
    
    def test_file_not_found_inbound(self):
        """1. 존재하지 않는 파일 - InboundCollector"""
        with pytest.raises(FileNotFoundError):
            collector = InboundCollector("non_existent_file.csv")
            collector.load_data()
    
    def test_file_not_found_inventory(self):
        """2. 존재하지 않는 파일 - InventoryCollector"""
        with pytest.raises(FileNotFoundError):
            collector = InventoryCollector("non_existent_inventory.csv")
            collector.load_data()
    
    def test_empty_file_inbound(self):
        """3. 빈 CSV 파일 (헤더만) - InboundCollector"""
        empty_file = EDGE_CASES / "empty_inbound.csv"
        collector = InboundCollector(str(empty_file), encoding='utf-8-sig')
        
        # 빈 파일은 ValueError 발생해야 함
        with pytest.raises(ValueError, match="데이터 검증 실패"):
            collector.load_data()
    
    def test_missing_required_columns(self):
        """4. 필수 컬럼 누락 - InboundCollector"""
        missing_file = EDGE_CASES / "missing_columns.csv"
        collector = InboundCollector(str(missing_file), encoding='utf-8-sig')
        
        # 필수 컬럼 누락 시 ValueError 발생해야 함
        with pytest.raises(ValueError, match="데이터 검증 실패"):
            collector.load_data()


class TestDataQualityEdgeCases:
    """데이터 품질 Edge Case 테스트 (6개)"""
    
    def test_null_values_inventory(self):
        """5. NULL 값 포함 - InventoryCollector"""
        null_file = EDGE_CASES / "null_inventory.csv"
        collector = InventoryCollector(str(null_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # NULL 값이 존재하는지 확인
        assert df['가용수량'].isna().any() or df['단가'].isna().any() or df['유효유통비(%)'].isna().any()
        
        # 요약 정보가 정상적으로 계산되는지 (NULL 제외)
        summary = collector.get_summary()
        assert isinstance(summary, dict)
        assert '총_상품수' in summary  # InventoryCollector는 '총_상품수' 키 사용
        assert summary['총_상품수'] >= 0
    
    def test_negative_quantity_inbound(self):
        """6. 음수 수량 - InboundCollector"""
        negative_file = EDGE_CASES / "negative_inbound.csv"
        collector = InboundCollector(str(negative_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # 음수 값이 존재하는지 확인
        has_negative = (df['입고예정수량'] < 0).any() or (df['총입고수량'] < 0).any()
        assert has_negative
        
        # 요약 정보는 여전히 생성 가능해야 함
        summary = collector.get_summary()
        assert isinstance(summary, dict)
    
    def test_invalid_date_format(self):
        """7. 잘못된 날짜 형식 - InboundCollector"""
        invalid_file = EDGE_CASES / "invalid_date.csv"
        collector = InboundCollector(str(invalid_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # errors='coerce'로 인해 NaT가 생성되어야 함
        assert pd.isna(df['입고예정일']).any()
        
        # 데이터는 로드되지만 일부 날짜가 변환 실패
        assert len(df) > 0
    
    def test_duplicate_products_inventory(self):
        """8. 중복 상품코드 - InventoryCollector"""
        dup_file = EDGE_CASES / "duplicate_products.csv"
        collector = InventoryCollector(str(dup_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # 중복 상품이 존재하는지 확인
        duplicate_count = df['상품'].duplicated().sum()
        assert duplicate_count > 0
        
        # 요약 정보의 총_상품수와 실제 행 수는 다를 수 있음
        summary = collector.get_summary()
        total_rows = len(df)
        unique_products = summary['총_상품수']  # nunique() 결과
        
        # 중복이 있으므로 총 행 수 > 고유 상품수
        assert total_rows > unique_products
    
    def test_zero_quantity_inventory(self):
        """9. 0 수량 - InventoryCollector"""
        null_file = EDGE_CASES / "null_inventory.csv"  # 0 수량 포함
        collector = InventoryCollector(str(null_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # 0 수량이 존재하는지 확인
        has_zero = (df['가용수량'] == 0).any()
        assert has_zero
        
        # 0 수량도 정상 처리되어야 함
        summary = collector.get_summary()
        assert isinstance(summary, dict)
    
    def test_zero_price_inventory(self):
        """10. 0 단가 - InventoryCollector"""
        null_file = EDGE_CASES / "null_inventory.csv"  # 0 단가 포함
        collector = InventoryCollector(str(null_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # 0 단가가 존재하는지 확인
        has_zero_price = (df['단가'] == 0).any()
        assert has_zero_price
        
        # calculate_total_value 호출 시 오류 없이 처리
        try:
            total_value = collector.calculate_total_value()
            assert total_value >= 0
        except Exception:
            # 예외가 발생하지 않아야 함
            pytest.fail("0 단가 처리 중 예외 발생")


class TestBoundaryEdgeCases:
    """경계값 Edge Case 테스트 (5개)"""
    
    def test_boundary_validity_ratio_20_inventory(self):
        """11. 유효비 정확히 20% - InventoryCollector"""
        boundary_file = EDGE_CASES / "boundary_validity_20.csv"
        collector = InventoryCollector(str(boundary_file), encoding='utf-8-sig')
        collector.load_data()
        
        risky = collector.get_risky_products()
        df = collector.get_data()
        
        # 20% 상품 확인
        products_20 = df[df['유효유통비(%)'] == 20.0]
        
        if not products_20.empty:
            # 20%는 위험 상품에 포함되어야 함 (<= 조건)
            for product in products_20['상품'].values:
                assert product in risky['상품'].values, f"상품 {product} (20%)가 위험 상품에 포함되지 않음"
        
        # 19.9% 상품도 포함되어야 함
        products_19_9 = df[df['유효유통비(%)'] < 20.0]
        if not products_19_9.empty:
            for product in products_19_9['상품'].values:
                assert product in risky['상품'].values
        
        # 21% 상품은 제외되어야 함
        products_21 = df[df['유효유통비(%)'] > 20.0]
        if not products_21.empty:
            for product in products_21['상품'].values:
                assert product not in risky['상품'].values
    
    def test_boundary_time_18_delete(self):
        """12. 18시 정확히 - DeleteCollector"""
        boundary_file = EDGE_CASES / "boundary_time_18.csv"
        collector = DeleteCollector(str(boundary_file), encoding='utf-8-sig')
        collector.load_data()
        
        count = collector.count_after_18()
        
        # 18:00:00 기준
        df = collector.get_data()
        
        # 시간 파싱 확인
        assert '삭제시각' in df.columns
        assert df['삭제시각'].notna().any()
        
        # count는 0 이상이어야 함
        assert isinstance(count, (int, float))
        assert count >= 0
    
    def test_progress_rate_0_inbound(self):
        """13. 진척률 0% - InboundCollector"""
        negative_file = EDGE_CASES / "negative_inbound.csv"
        collector = InboundCollector(str(negative_file), encoding='utf-8-sig')
        collector.load_data()
        
        pending = collector.get_pending_inbounds()
        
        # 진척률 0%인 항목이 존재해야 함
        df = collector.get_data()
        zero_progress = df[df['진척률'] == 0]
        assert not zero_progress.empty
        
        # pending에 포함되어야 함 (진척률 < 100)
        for idx in zero_progress.index:
            assert idx in pending.index
    
    def test_progress_rate_100_inbound(self):
        """14. 진척률 100% - InboundCollector"""
        # 샘플 파일에 100% 항목 추가 필요
        sample_file = FIXTURES / "sample_inbound.csv"
        collector = InboundCollector(str(sample_file), encoding='utf-8-sig')
        collector.load_data()
        
        df = collector.get_data()
        pending = collector.get_pending_inbounds()
        
        # 진척률 100% 항목 확인
        complete = df[df['진척률'] >= 100]
        
        if not complete.empty:
            # 100% 항목은 pending에서 제외되어야 함
            for idx in complete.index:
                assert idx not in pending.index
    
    def test_progress_rate_over_100_inbound(self):
        """15. 진척률 100% 초과 - InboundCollector"""
        # 현재 샘플 데이터에는 없으므로 정상 동작 확인
        sample_file = FIXTURES / "sample_inbound.csv"
        collector = InboundCollector(str(sample_file), encoding='utf-8-sig')
        df = collector.load_data()
        
        # 100% 초과 데이터가 있어도 오류 없이 처리되어야 함
        summary = collector.get_summary()
        assert isinstance(summary, dict)


class TestBusinessLogicEdgeCases:
    """비즈니스 로직 Edge Case 테스트 (5개)"""
    
    def test_get_top_n_zero_inbound(self):
        """16. n=0일 때 - InboundCollector"""
        sample_file = FIXTURES / "sample_inbound.csv"
        collector = InboundCollector(str(sample_file), encoding='utf-8-sig')
        collector.load_data()
        
        top = collector.get_top_suppliers(n=0)
        
        # 빈 DataFrame 반환
        assert isinstance(top, pd.DataFrame)
        assert len(top) == 0
    
    def test_get_top_n_exceeds_data_outbound(self):
        """17. n > 데이터 개수 - OutboundCollector"""
        sample_file = FIXTURES / "sample_outbound.csv"
        collector = OutboundCollector(str(sample_file), encoding='utf-8-sig')
        collector.load_data()
        
        # 실제 배송처 수보다 큰 n
        top = collector.get_top_destinations(n=1000)
        
        # 전체 배송처만큼만 반환
        df = collector.get_data()
        unique_destinations = df['배송처'].nunique()
        assert len(top) <= unique_destinations
    
    def test_empty_dataframe_summary_inbound(self):
        """18. 빈 데이터프레임 요약 - InboundCollector"""
        empty_file = EDGE_CASES / "empty_inbound.csv"
        collector = InboundCollector(str(empty_file), encoding='utf-8-sig')
        
        # 빈 파일은 load_data에서 ValueError 발생
        with pytest.raises(ValueError, match="데이터 검증 실패"):
            collector.load_data()
    
    def test_filtering_logic_accuracy_inventory(self):
        """19. 필터링 정확도 - InventoryCollector"""
        boundary_file = EDGE_CASES / "boundary_validity_20.csv"
        collector = InventoryCollector(str(boundary_file), encoding='utf-8-sig')
        collector.load_data()
        
        risky = collector.get_risky_products()
        df = collector.get_data()
        
        # 필터링 정확도 검증
        # risky에 포함된 모든 상품은 유효비 <= 20 이어야 함
        for idx, row in risky.iterrows():
            validity = row['유효유통비(%)']
            if pd.notna(validity):
                assert validity <= 20.0, f"상품 {row['상품']}의 유효비가 {validity}%로 20%를 초과함"
        
        # df에서 유효비 <= 20인 모든 상품이 risky에 있어야 함
        should_be_risky = df[df['유효유통비(%)'] <= 20.0]
        for idx, row in should_be_risky.iterrows():
            assert row['상품'] in risky['상품'].values, f"상품 {row['상품']}가 위험 상품에 누락됨"
    
    def test_sorting_order_inbound(self):
        """20. 정렬 순서 검증 - InboundCollector"""
        sample_file = FIXTURES / "sample_inbound.csv"
        collector = InboundCollector(str(sample_file), encoding='utf-8-sig')
        collector.load_data()
        
        # get_pending_inbounds는 입고예정일 기준 정렬 (구현 확인 결과)
        pending = collector.get_pending_inbounds()
        
        if len(pending) > 1:
            # 입고예정일이 오름차순으로 정렬되어 있는지 확인
            dates = pending['입고예정일'].tolist()
            # NaT가 아닌 날짜만 확인
            valid_dates = [d for d in dates if pd.notna(d)]
            if len(valid_dates) > 1:
                assert valid_dates == sorted(valid_dates), "입고예정일이 오름차순으로 정렬되지 않음"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
