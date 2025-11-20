"""
InboundCollector 단위 테스트

테스트 항목:
1. get_data() 데이터 구조
2. get_summary() 키 확인
3. get_summary() 계산 정확성
4. 진척률 범위 검증 (0~100%)
5. 빈 파일 처리
6. 데이터 타입 검증
"""
import pytest
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# dashboard 경로 추가
dashboard_path = Path(__file__).parent.parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.inbound import InboundCollector


class TestInboundCollector:
    """InboundCollector 테스트 클래스"""
    
    def test_get_data_structure(self, sample_inbound_csv):
        """1. get_data() 데이터 구조 - 필수 컬럼 존재"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 필수 컬럼 존재 확인
        required_columns = ['상품', '진척률', '소비기한']
        for col in required_columns:
            assert col in data.columns, f"필수 컬럼 '{col}'이 없습니다"
        
        # DataFrame 타입 확인
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
    
    def test_get_summary_keys(self, sample_inbound_csv):
        """2. get_summary() 키 확인"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        summary = collector.get_summary()
        
        # dict 타입 확인
        assert isinstance(summary, dict)
        
        # 필수 키 확인
        assert 'total_count' in summary
        assert 'progress_rate' in summary
        assert 'unique_products' in summary
    
    def test_get_summary_calculations(self, sample_inbound_csv):
        """3. get_summary() 계산 정확성"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        data = collector.get_data()
        summary = collector.get_summary()
        
        # 총 건수 계산 정확성
        assert summary['total_count'] == len(data)
        
        # 평균 진척률 계산 정확성
        expected_progress = float(data['진척률'].mean())
        assert abs(summary['progress_rate'] - expected_progress) < 0.01
        
        # 고유 상품 수
        expected_unique = data['상품'].nunique()
        assert summary['unique_products'] == expected_unique
    
    def test_progress_rate_range(self, sample_inbound_csv):
        """4. 진척률 0~100% 범위 검증"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 진척률 컬럼 존재 확인
        assert '진척률' in data.columns
        
        # 모든 진척률이 0~100 범위인지 확인
        assert data['진척률'].min() >= 0
        assert data['진척률'].max() <= 100
    
    def test_empty_file_handling(self):
        """5. 빈 파일 처리 - validate() False 반환"""
        # 존재하지 않는 파일
        collector = InboundCollector(file_path="C:/invalid/path.csv")
        
        # validate()가 False 반환해야 함
        assert collector.validate() == False
    
    def test_data_types(self, sample_inbound_csv):
        """6. 데이터 타입 검증"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        data = collector.get_data()
        summary = collector.get_summary()
        
        # 진척률은 숫자형
        assert pd.api.types.is_numeric_dtype(data['진척률'])
        
        # summary 값들의 타입 확인
        assert isinstance(summary['total_count'], int)
        assert isinstance(summary['progress_rate'], float)
        assert isinstance(summary['unique_products'], (int, np.int64))
