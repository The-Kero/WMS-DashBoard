"""
OutboundCollector: 출고정보 데이터 수집기

출고번호, 출고일자, 상품정보, 배송처 등을 수집
"""

import pandas as pd
from .base import BaseCollector


class OutboundCollector(BaseCollector):
    """출고정보 수집기"""
    
    REQUIRED_COLUMNS = [
        '출고번호', '출고일자', '상품코드', '상품명',
        '출하수량', '출하금액', '배송처'
    ]
    
    def load_data(self) -> pd.DataFrame:
        """
        CSV 파일에서 출고 데이터 로드
        
        Returns:
            출고 데이터 DataFrame
            
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
            raise ValueError("출고 데이터 검증 실패")
        
        # 데이터 타입 변환
        df['출고일자'] = pd.to_datetime(df['출고일자'], format='%Y%m%d', errors='coerce')
        df['출하수량'] = pd.to_numeric(df['출하수량'], errors='coerce')
        df['출하금액'] = pd.to_numeric(df['출하금액'], errors='coerce')
        
        return df
    
    def validate(self, df: pd.DataFrame) -> bool:
        """
        출고 데이터 유효성 검증
        
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
        출고 데이터 요약 정보
        
        Returns:
            요약 정보 딕셔너리
        """
        df = self.get_data()
        
        return {
            '총_출고건수': len(df),
            '총_출하수량': df['출하수량'].sum(),
            '총_출하금액': df['출하금액'].sum(),
            '배송처_수': df['배송처'].nunique(),
            '상품_종류': df['상품코드'].nunique(),
            '최근_출고일자': df['출고일자'].max(),
            '최초_출고일자': df['출고일자'].min(),
        }
    
    def get_top_destinations(self, n: int = 5) -> pd.DataFrame:
        """
        상위 배송처 목록
        
        Args:
            n: 반환할 배송처 수
            
        Returns:
            배송처별 출하수량 DataFrame
        """
        df = self.get_data()
        return (df.groupby('배송처')['출하수량']
                .sum()
                .sort_values(ascending=False)
                .head(n)
                .reset_index())
    
    def get_top_products(self, n: int = 5) -> pd.DataFrame:
        """
        상위 출고 상품 목록
        
        Args:
            n: 반환할 상품 수
            
        Returns:
            상품별 출하수량 DataFrame
        """
        df = self.get_data()
        return (df.groupby(['상품코드', '상품명'])['출하수량']
                .sum()
                .sort_values(ascending=False)
                .head(n)
                .reset_index())
