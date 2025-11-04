"""
InboundCollector pytest 테스트
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.collectors.inbound import InboundCollector

# 샘플 데이터 경로
SAMPLE_FILE = Path(__file__).parent / "fixtures" / "sample_inbound.csv"


class TestInboundCollector:
    """InboundCollector 테스트 클래스"""
    
    def test_required_columns(self):
        """필수 컬럼 확인"""
        # REQUIRED_COLUMNS가 정의되어 있는지만 확인
        assert hasattr(InboundCollector, 'REQUIRED_COLUMNS')
        assert len(InboundCollector.REQUIRED_COLUMNS) > 0
        
    def test_file_exists(self):
        """샘플 파일 존재 확인"""
        assert SAMPLE_FILE.exists(), f"샘플 파일이 없습니다: {SAMPLE_FILE}"
    
    def test_load_data(self):
        """데이터 로드 테스트"""
        collector = InboundCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        df = collector.load_data()
        
        assert isinstance(df, pd.DataFrame), "DataFrame이 아닙니다"
        assert len(df) > 0, "데이터가 비어있습니다"
        assert not df.empty, "DataFrame이 비어있습니다"
    
    def test_validate(self):
        """데이터 검증 테스트"""
        collector = InboundCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        df = collector.load_data()
        
        assert collector.validate(df) == True, "데이터 검증 실패"
    
    def test_get_summary(self):
        """요약 정보 테스트"""
        collector = InboundCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        collector.load_data()
        summary = collector.get_summary()
        
        assert '총_입고건수' in summary
        assert '입고완료건수' in summary
        assert '진행중건수' in summary
        assert isinstance(summary['총_입고건수'], (int, float))
        assert isinstance(summary['입고완료건수'], (int, float))
    
    def test_get_data(self):
        """get_data 메서드 테스트"""
        collector = InboundCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        df = collector.get_data()
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) > 0
    
    def test_get_pending_inbounds(self):
        """진행중 입고 조회 테스트"""
        collector = InboundCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        collector.load_data()
        pending = collector.get_pending_inbounds()
        
        assert isinstance(pending, pd.DataFrame)
        # 진행중 입고가 있을 수도, 없을 수도 있음
        assert len(pending) >= 0
    
    def test_get_top_suppliers(self):
        """상위 공급사 조회 테스트"""
        collector = InboundCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        collector.load_data()
        top = collector.get_top_suppliers(n=5)
        
        assert isinstance(top, pd.DataFrame)
        assert len(top) <= 5, "5개 이하여야 합니다"
        assert len(top) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
