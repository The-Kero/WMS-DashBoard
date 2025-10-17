"""
InboundCollector: 입고정보 데이터 수집기

입고예정번호, 공급사, 입고예정일, 상품정보 등을 수집
"""

import pandas as pd
from .base import BaseCollector


class InboundCollector(BaseCollector):
    """입고정보 수집기"""
    
    REQUIRED_COLUMNS = [
        '입고예정번호', '공급사', '공급사명', '입고유형',
        '입고예정일', '로케이션', '상품', '상품명',
        '단위및규격', '소비기한', '입고수량'
    ]
    
    def load_data(self) -> pd.DataFrame:
        """
        CSV 파일에서 입고 데이터 로드
        
        Returns:
            입고 데이터 DataFrame
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            ValueError: 데이터 검증 실패 시
        """
        if not self.file_exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
        
        # CSV 읽기
        df = pd.read_csv(self.file_path, encoding=self.encoding)
        
        # 데이터 검증
        if not self.validate(df):
            raise ValueError("입고 데이터 검증 실패")
        
        # 데이터 타입 변환
        df['입고예정일'] = pd.to_datetime(df['입고예정일'], format='%Y%m%d', errors='coerce')
        df['소비기한'] = pd.to_datetime(df['소비기한'], format='%Y%m%d', errors='coerce')
        df['입고수량'] = pd.to_numeric(df['입고수량'], errors='coerce')
        
        return df
    
    def validate(self, df: pd.DataFrame) -> bool:
        """
        입고 데이터 유효성 검증
        
        Args:
            df: 검증할 DataFrame
            
        Returns:
            유효성 여부
        """
        # 필수 컬럼 확인
        missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            print(f"❌ 누락된 컬럼: {missing_columns}")
            return False
        
        # 빈 데이터 확인
        if df.empty:
            print("❌ 데이터가 비어있습니다")
            return False
        
        return True
    
    def get_summary(self) -> dict:
        """
        입고 데이터 요약 정보
        
        Returns:
            요약 정보 딕셔너리
        """
        df = self.get_data()
        
        return {
            '총_입고건수': len(df),
            '총_입고수량': df['입고수량'].sum(),
            '공급사_수': df['공급사'].nunique(),
            '상품_종류': df['상품'].nunique(),
            '최근_입고예정일': df['입고예정일'].max(),
            '최초_입고예정일': df['입고예정일'].min(),
        }
    
    def get_top_suppliers(self, n: int = 5) -> pd.DataFrame:
        """
        상위 공급사 목록
        
        Args:
            n: 반환할 공급사 수
            
        Returns:
            공급사별 입고수량 DataFrame
        """
        df = self.get_data()
        return (df.groupby(['공급사', '공급사명'])['입고수량']
                .sum()
                .sort_values(ascending=False)
                .head(n)
                .reset_index())
