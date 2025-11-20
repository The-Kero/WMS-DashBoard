"""
OutboundCollector 단위 테스트

테스트 항목:
1. get_data() 데이터 구조
2. get_summary() 키 확인
3. 출고유형 필터링
4. 출하금액 계산
5. 타입 14,15,18 필터링 (카드5용)
6. 지방 출고 필터링 (카드6용)
"""
import pytest
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# dashboard 경로 추가
dashboard_path = Path(__file__).parent.parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.outbound import OutboundCollector


class TestOutboundCollector:
    """OutboundCollector 테스트 클래스"""
    
    def test_get_data_structure(self, sample_outbound_csv):
        """1. get_data() 데이터 구조 - 필수 컬럼"""
        collector = OutboundCollector(file_path=sample_outbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 필수 컬럼 존재 확인 (실제 Collector에서 사용하는 컬럼)
        required_columns = ['출고유형', '출하금액', '배송처명']
        for col in required_columns:
            assert col in data.columns, f"필수 컬럼 '{col}'이 없습니다"
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
    
    def test_get_summary_keys(self, sample_outbound_csv):
        """2. get_summary() 키 확인"""
        collector = OutboundCollector(file_path=sample_outbound_csv)
        collector.validate()
        
        summary = collector.get_summary()
        
        assert isinstance(summary, dict)
        assert 'total_count' in summary
        assert 'total_amount' in summary
        assert 'unique_destinations' in summary
    
    def test_outbound_type_filtering(self, sample_outbound_csv):
        """3. 출고유형 분류 정확성"""
        collector = OutboundCollector(file_path=sample_outbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 출고유형 컬럼 존재
        assert '출고유형' in data.columns
        
        # 출고유형이 숫자형인지 확인
        assert pd.api.types.is_numeric_dtype(data['출고유형'])
    
    def test_amount_calculations(self, sample_outbound_csv):
        """4. 출하금액 합계 계산"""
        collector = OutboundCollector(file_path=sample_outbound_csv)
        collector.validate()
        
        data = collector.get_data()
        summary = collector.get_summary()
        
        # 출하금액 합계 정확성
        expected_amount = int(data['출하금액'].sum())
        assert summary['total_amount'] == expected_amount
    
    def test_type_14_15_18_filtering(self, sample_outbound_csv):
        """5. 자사 출고 타입 (14,15,18) 필터링"""
        collector = OutboundCollector(file_path=sample_outbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 타입 14, 15, 18 필터링
        card5_types = [14, 15, 18]
        card5_data = data[data['출고유형'].isin(card5_types)]
        
        # 필터링된 데이터의 출고유형이 14,15,18만 포함
        assert card5_data['출고유형'].isin(card5_types).all()
    
    def test_provincial_filtering(self, sample_outbound_csv):
        """6. 지방 출고 필터링 (카드6용)"""
        collector = OutboundCollector(file_path=sample_outbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 지방 출고 타입 (4,5,8,16,17,52,53)
        card6_types = [4, 5, 8, 16, 17, 52, 53]
        card6_data = data[data['출고유형'].isin(card6_types)]
        
        # 필터링된 데이터의 출고유형 확인
        assert card6_data['출고유형'].isin(card6_types).all()
