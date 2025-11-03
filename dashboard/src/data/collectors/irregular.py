"""
IrregularCollector: 비정형오더 데이터 수집기

상세내용, 출고센터명, 입고센터명, 상품명, 입출수량, 라벨출력, 최초입력시각 등을 수집
"""

import pandas as pd
from datetime import datetime, timedelta
from .base import BaseCollector


class IrregularCollector(BaseCollector):
    """비정형오더 수집기"""
    
    REQUIRED_COLUMNS = [
        '상세내용', '출고센터명', '입고센터명', '상품명',
        '입출수량', '라벨출력', '최초입력시각'
    ]
    
    def load_data(self) -> pd.DataFrame:
        """
        CSV 파일에서 비정형오더 데이터 로드
        
        Returns:
            비정형오더 데이터 DataFrame
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            ValueError: 데이터 검증 실패 시
        """
        if not self.file_exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
        
        # CSV 읽기 (BOM 처리)
        df = pd.read_csv(self.file_path, encoding=self.encoding)
        
        # 데이터 검증
        if not self.validate(df):
            raise ValueError("비정형오더 데이터 검증 실패")
        
        # 데이터 타입 변환
        df['최초입력시각'] = pd.to_datetime(df['최초입력시각'], errors='coerce')
        df['입출수량'] = pd.to_numeric(df['입출수량'], errors='coerce')
        
        return df
    
    def validate(self, df: pd.DataFrame) -> bool:
        """
        비정형오더 데이터 유효성 검증
        
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
        비정형오더 데이터 요약 정보
        
        Returns:
            요약 정보 딕셔너리
        """
        df = self.get_data()
        
        return {
            '총건수': len(df),
            '라벨미출력': len(df[df['라벨출력'] == 'N']),
            '라벨출력완료': len(df[df['라벨출력'] == 'Y']),
            '출고센터수': df['출고센터명'].nunique(),
            '입고센터수': df['입고센터명'].nunique(),
            '상품종류': df['상품명'].nunique(),
            '총입출수량': df['입출수량'].sum(),
            '최근입력시각': df['최초입력시각'].max(),
            '최초입력시각': df['최초입력시각'].min(),
        }
    
    def get_recent_orders(self, hours: int = 1) -> pd.DataFrame:
        """
        최근 N시간 이내 비정형오더 조회
        
        Args:
            hours: 조회할 시간 범위 (기본값: 1시간)
            
        Returns:
            최근 N시간 이내 오더 DataFrame
        """
        df = self.get_data()
        now = datetime.now()
        cutoff_time = now - timedelta(hours=hours)
        
        # 최근 N시간 이내 데이터 필터링
        recent_df = df[df['최초입력시각'] >= cutoff_time]
        return recent_df
    
    def get_unlabeled_orders(self) -> pd.DataFrame:
        """
        라벨 미출력 오더 목록 조회
        
        Returns:
            라벨 미출력(N) 오더 DataFrame
        """
        df = self.get_data()
        return df[df['라벨출력'] == 'N']
    
    def get_orders_by_center(self, center_type: str = 'outbound') -> pd.DataFrame:
        """
        센터별 오더 통계
        
        Args:
            center_type: 센터 유형 ('outbound': 출고센터, 'inbound': 입고센터)
            
        Returns:
            센터별 통계 DataFrame
        """
        df = self.get_data()
        
        if center_type == 'outbound':
            column = '출고센터명'
        else:
            column = '입고센터명'
        
        return (df.groupby(column)
                .agg({
                    '상세내용': 'count',
                    '입출수량': 'sum'
                })
                .rename(columns={'상세내용': '오더건수', '입출수량': '총수량'})
                .sort_values('오더건수', ascending=False)
                .reset_index())
