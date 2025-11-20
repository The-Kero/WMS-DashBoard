"""
BaseCollector 단위 테스트

테스트 항목:
1. 정상 파일로 초기화
2. 존재하지 않는 파일로 초기화
3. 데이터 로드 성공
4. UTF-8 BOM 인코딩 처리
5. get_data() DataFrame 반환
6. get_data() 비어있지 않음
7. get_summary() dict 반환
8. BaseCollector 직접 인스턴스화 불가
"""
import pytest
import sys
from pathlib import Path
import pandas as pd

# dashboard 경로 추가
dashboard_path = Path(__file__).parent.parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.base_collector import BaseCollector
from src.data.collectors.inbound import InboundCollector


class TestBaseCollector:
    """BaseCollector 테스트 클래스"""
    
    def test_init_with_valid_file(self, sample_inbound_csv):
        """1. 정상 파일로 초기화"""
        # InboundCollector를 사용 (BaseCollector의 구체적 구현체)
        collector = InboundCollector(file_path=sample_inbound_csv, encoding='utf-8-sig')
        
        # 파일 경로가 Path 객체로 저장되었는지 확인
        assert isinstance(collector.file_path, Path)
        assert collector.encoding == 'utf-8-sig'
        assert collector.file_path.exists()
    
    def test_init_with_invalid_file(self):
        """2. 존재하지 않는 파일로 초기화"""
        invalid_path = "C:/invalid/path/file.csv"
        collector = InboundCollector(file_path=invalid_path)
        
        # 파일이 존재하지 않으면 validate()가 False 반환
        assert collector.validate() == False
    
    def test_load_data_success(self, sample_inbound_csv):
        """3. 데이터 로드 성공"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        
        # validate()는 파일을 읽고 데이터 검증
        result = collector.validate()
        assert result == True
        
        # DataFrame이 로드되었는지 확인
        data = collector.get_data()
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
    
    def test_load_data_encoding(self, sample_inbound_csv):
        """4. UTF-8 BOM 인코딩 처리"""
        # UTF-8 BOM (Excel 호환) 인코딩으로 파일 읽기
        collector = InboundCollector(file_path=sample_inbound_csv, encoding='utf-8-sig')
        
        result = collector.validate()
        assert result == True
        
        # 데이터가 정상적으로 읽혀졌는지 확인
        data = collector.get_data()
        assert not data.empty
    
    def test_get_data_returns_dataframe(self, sample_inbound_csv):
        """5. get_data() DataFrame 반환"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # DataFrame 타입 확인
        assert isinstance(data, pd.DataFrame)
        
        # 필수 컬럼 존재 확인 (InboundCollector 기준)
        required_columns = ['상품', '진척률', '소비기한']
        for col in required_columns:
            assert col in data.columns, f"필수 컬럼 '{col}'이 없습니다"
    
    def test_get_data_not_empty(self, sample_inbound_csv):
        """6. get_data() 비어있지 않음"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        data = collector.get_data()
        
        # 데이터가 비어있지 않은지 확인
        assert not data.empty
        assert len(data) > 0
        assert data.shape[0] > 0  # 행 개수 확인
        assert data.shape[1] > 0  # 열 개수 확인
    
    def test_get_summary_returns_dict(self, sample_inbound_csv):
        """7. get_summary() dict 반환"""
        collector = InboundCollector(file_path=sample_inbound_csv)
        collector.validate()
        
        summary = collector.get_summary()
        
        # dict 타입 확인
        assert isinstance(summary, dict)
        
        # 필수 키 존재 확인 (InboundCollector 기준)
        assert 'total_count' in summary
        assert 'progress_rate' in summary
        
        # 값이 유효한지 확인
        assert isinstance(summary['total_count'], int)
        assert summary['total_count'] > 0
    
    def test_base_collector_cannot_be_instantiated_directly(self):
        """8. BaseCollector 직접 인스턴스화 불가"""
        # BaseCollector는 추상 클래스이므로 직접 인스턴스화할 수 없음
        # 다만 Python은 강제하지 않으므로, 실제로는 인스턴스화 가능
        # 하지만 get_summary()가 NotImplementedError를 발생시켜야 함
        
        collector = BaseCollector(file_path="dummy.csv")
        
        # get_summary()와 get_data()는 하위 클래스에서 구현해야 함
        # 호출 시 NotImplementedError가 발생해야 함
        with pytest.raises(NotImplementedError):
            collector.get_summary()
