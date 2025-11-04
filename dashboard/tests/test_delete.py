"""
DeleteCollector pytest 테스트
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.collectors.delete import DeleteCollector

# 샘플 데이터 경로
SAMPLE_FILE = Path(__file__).parent / "fixtures" / "sample_delete.csv"


class TestDeleteCollector:
    """DeleteCollector 테스트 클래스"""
    
    def test_required_columns(self):
        """필수 컬럼 확인"""
        # REQUIRED_COLUMNS가 정의되어 있는지만 확인
        assert hasattr(DeleteCollector, 'REQUIRED_COLUMNS')
        assert len(DeleteCollector.REQUIRED_COLUMNS) > 0
        
    def test_file_exists(self):
        """샘플 파일 존재 확인"""
        assert SAMPLE_FILE.exists(), f"샘플 파일이 없습니다: {SAMPLE_FILE}"
    
    def test_load_data(self):
        """데이터 로드 테스트"""
        collector = DeleteCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        df = collector.load_data()
        
        assert isinstance(df, pd.DataFrame), "DataFrame이 아닙니다"
        assert len(df) > 0, "데이터가 비어있습니다"
        assert not df.empty, "DataFrame이 비어있습니다"
    
    def test_validate(self):
        """데이터 검증 테스트"""
        collector = DeleteCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        df = collector.load_data()
        
        assert collector.validate(df) == True, "데이터 검증 실패"
    
    def test_get_summary(self):
        """요약 정보 테스트"""
        collector = DeleteCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        collector.load_data()
        summary = collector.get_summary()
        
        assert '총건수' in summary
        assert '총삭제수량' in summary
        assert isinstance(summary['총건수'], (int, float, np.integer))
        assert isinstance(summary['총삭제수량'], (int, float, np.integer))
    
    def test_get_data(self):
        """get_data 메서드 테스트"""
        collector = DeleteCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        df = collector.get_data()
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) > 0
    
    def test_count_after_18(self):
        """18시 이후 삭제 건수 조회 테스트"""
        collector = DeleteCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        collector.load_data()
        count = collector.count_after_18()
        
        assert isinstance(count, (int, float))
        assert count >= 0, "18시 이후 건수는 0 이상이어야 합니다"
    
    def test_get_deletes_by_delivery(self):
        """배송처별 삭제 현황 조회 테스트"""
        collector = DeleteCollector(str(SAMPLE_FILE), encoding='utf-8-sig')
        collector.load_data()
        deletes = collector.get_deletes_by_delivery()
        
        assert isinstance(deletes, pd.DataFrame)
        # 배송처가 있을 수도, 없을 수도 있음
        assert len(deletes) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
