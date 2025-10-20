"""
OutboundCollector: 출고정보 데이터 수집기

출하바코드, 출고일자, 상품정보, 배송처 등을 수집
백엔드 실제 데이터 구조에 맞춰 수정됨 (2025-10-20)
"""

import pandas as pd
from .base import BaseCollector


class OutboundCollector(BaseCollector):
    """출고정보 수집기"""
    
    # 백엔드 실제 컬럼에 맞춤 (2025-10-20 수정)
    REQUIRED_COLUMNS = [
        '출하바코드',      # 출고번호 대체 (고유 식별자)
        '출고일자',        # 유지
        '상품',            # 상품코드 → 상품
        '상품명',          # 유지
        '오더수량*',       # 출하수량 → 오더수량*
        '출하금액',        # 신규 추가 (재고 단가 연동)
        '배송처'           # 유지
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
        df['오더수량*'] = pd.to_numeric(df['오더수량*'], errors='coerce')
        
        # 출하금액 처리 (N/A → NaN 변환)
        df['출하금액'] = df['출하금액'].replace('N/A', pd.NA)
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
        
        # 출하금액 유효 건수 계산 (N/A 제외)
        valid_amount = df['출하금액'].notna().sum()
        total_amount = df['출하금액'].sum()
        
        summary = {
            '총_출고건수': len(df),
            '총_오더수량': int(df['오더수량*'].sum()),
            '총_출하금액': int(total_amount) if pd.notna(total_amount) else 0,
            '출하금액_유효건수': int(valid_amount),
            '출하금액_N/A건수': len(df) - int(valid_amount),
            '배송처_수': df['배송처'].nunique(),
            '상품_종류': df['상품'].nunique(),
            '최근_출고일자': df['출고일자'].max(),
            '최초_출고일자': df['출고일자'].min(),
        }
        
        # 출고유형 분포 (백엔드에 출고유형 컬럼이 있으면 추가)
        if '출고유형' in df.columns:
            summary['출고유형_분포'] = df['출고유형'].value_counts().to_dict()
        
        return summary
    
    def get_top_destinations(self, n: int = 5) -> pd.DataFrame:
        """
        상위 배송처 목록
        
        Args:
            n: 반환할 배송처 수
            
        Returns:
            배송처별 오더수량 DataFrame
        """
        df = self.get_data()
        
        result = (df.groupby('배송처')
                  .agg({
                      '오더수량*': 'sum',
                      '출하금액': lambda x: x.sum() if x.notna().any() else 0
                  })
                  .sort_values('오더수량*', ascending=False)
                  .head(n)
                  .reset_index())
        
        # 컬럼명 정리
        result.columns = ['배송처', '총_오더수량', '총_출하금액']
        return result
    
    def get_top_products(self, n: int = 5) -> pd.DataFrame:
        """
        상위 출고 상품 목록
        
        Args:
            n: 반환할 상품 수
            
        Returns:
            상품별 오더수량 DataFrame
        """
        df = self.get_data()
        
        result = (df.groupby(['상품', '상품명'])
                  .agg({
                      '오더수량*': 'sum',
                      '출하금액': lambda x: x.sum() if x.notna().any() else 0
                  })
                  .sort_values('오더수량*', ascending=False)
                  .head(n)
                  .reset_index())
        
        # 컬럼명 정리
        result.columns = ['상품', '상품명', '총_오더수량', '총_출하금액']
        return result
    
    def get_by_type(self) -> pd.DataFrame:
        """
        출고유형별 집계 (백엔드에 출고유형 컬럼이 있을 때만 사용)
        
        Returns:
            출고유형별 집계 DataFrame
        """
        df = self.get_data()
        
        if '출고유형' not in df.columns or '출고유형명' not in df.columns:
            return pd.DataFrame()  # 컬럼 없으면 빈 DataFrame 반환
        
        result = (df.groupby(['출고유형', '출고유형명'])
                  .agg({
                      '오더수량*': 'sum',
                      '출하금액': lambda x: x.sum() if x.notna().any() else 0,
                      '출하바코드': 'count'  # 건수
                  })
                  .sort_values('오더수량*', ascending=False)
                  .reset_index())
        
        # 컬럼명 정리
        result.columns = ['출고유형', '출고유형명', '총_오더수량', '총_출하금액', '출고건수']
        return result
