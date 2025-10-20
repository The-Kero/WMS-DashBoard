"""
InventoryCollector: 재고정보 데이터 수집기

상품코드, 상품명, 가용수량, 유효유통비, 단가 등을 수집
재고 현황 모니터링 및 위험 상품 파악
"""

import pandas as pd
from .base import BaseCollector


class InventoryCollector(BaseCollector):
    """재고정보 수집기"""
    
    # 필수 컬럼
    REQUIRED_COLUMNS = [
        '상품',           # 상품코드
        '상품명',         # 상품명
        '가용수량',       # 가용수량 (실제 사용 가능한 재고)
        '유효유통비(%)',  # 유효유통비 (백엔드에서 계산됨)
        '단가'           # 단가 (금액 계산용)
    ]
    
    def load_data(self) -> pd.DataFrame:
        """
        CSV 파일에서 재고 데이터 로드
        
        Returns:
            재고 데이터 DataFrame
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            ValueError: 데이터 검증 실패 시
        """
        if not self.file_exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
        
        # CSV 읽기 (UTF-8 BOM 지원)
        df = pd.read_csv(self.file_path, encoding=self.encoding)
        
        # 데이터 검증
        if not self.validate(df):
            raise ValueError("재고 데이터 검증 실패")
        
        # 데이터 타입 변환
        df['가용수량'] = pd.to_numeric(df['가용수량'], errors='coerce')
        df['유효유통비(%)'] = pd.to_numeric(df['유효유통비(%)'], errors='coerce')
        df['단가'] = pd.to_numeric(df['단가'], errors='coerce')
        
        return df
    
    def validate(self, df: pd.DataFrame) -> bool:
        """
        재고 데이터 유효성 검증
        
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
        재고 데이터 요약 정보
        
        Returns:
            요약 정보 딕셔너리
            - 총_상품수: 고유 상품코드 개수
            - 총_가용수량: 가용수량 합계
            - 총_재고금액: (가용수량 × 단가) 합계
            - 위험_상품수: 유효비 ≤ 20% 상품 개수
            - 평균_유효비: 평균 유효유통비
            - 유효비_구간별_분포: 구간별 상품 개수
        """
        df = self.get_data()
        
        # 총 재고 금액 계산 (가용수량 × 단가)
        df['재고금액'] = df['가용수량'] * df['단가']
        total_value = df['재고금액'].sum()
        
        # 유효비 위험 상품 (≤ 20%)
        risky_count = len(df[df['유효유통비(%)'] <= 20])
        
        # 유효비 구간별 분포
        bins = [0, 20, 50, 100]
        labels = ['위험(≤20%)', '주의(21-50%)', '정상(51-100%)']
        df['유효비구간'] = pd.cut(df['유효유통비(%)'], bins=bins, labels=labels, include_lowest=True)
        distribution = df['유효비구간'].value_counts().to_dict()
        
        summary = {
            '총_상품수': df['상품'].nunique(),
            '총_가용수량': int(df['가용수량'].sum()),
            '총_재고금액': int(total_value),
            '위험_상품수': risky_count,
            '평균_유효비': round(df['유효유통비(%)'].mean(), 2),
            '유효비_구간별_분포': distribution
        }
        
        return summary
    
    def get_risky_products(self) -> pd.DataFrame:
        """
        유효비 위험 상품 목록 (≤ 20%)
        
        Returns:
            유효비 20% 이하 상품 DataFrame
            컬럼: 상품, 상품명, 가용수량, 유효유통비(%), 단가, 재고금액
        """
        df = self.get_data()
        
        # 유효비 20% 이하 필터링
        risky = df[df['유효유통비(%)'] <= 20].copy()
        
        # 재고금액 계산
        risky['재고금액'] = risky['가용수량'] * risky['단가']
        
        # 필요한 컬럼만 선택 및 정렬
        result = risky[['상품', '상품명', '가용수량', '유효유통비(%)', '단가', '재고금액']]
        result = result.sort_values('유효유통비(%)', ascending=True)
        
        return result
    
    def get_low_stock_products(self, threshold: int = 10) -> pd.DataFrame:
        """
        가용수량 부족 상품 목록
        
        Args:
            threshold: 가용수량 기준값 (기본값: 10)
            
        Returns:
            가용수량이 기준값 이하인 상품 DataFrame
        """
        df = self.get_data()
        
        # 가용수량 부족 필터링
        low_stock = df[df['가용수량'] <= threshold].copy()
        
        # 재고금액 계산
        low_stock['재고금액'] = low_stock['가용수량'] * low_stock['단가']
        
        # 필요한 컬럼만 선택 및 정렬
        result = low_stock[['상품', '상품명', '가용수량', '유효유통비(%)', '단가', '재고금액']]
        result = result.sort_values('가용수량', ascending=True)
        
        return result
    
    def get_top_value_products(self, n: int = 10) -> pd.DataFrame:
        """
        재고금액 상위 상품 목록
        
        Args:
            n: 반환할 상품 수
            
        Returns:
            재고금액 상위 N개 상품 DataFrame
        """
        df = self.get_data()
        
        # 재고금액 계산
        df['재고금액'] = df['가용수량'] * df['단가']
        
        # 상품별 집계 (같은 상품이 여러 로케이션에 있을 수 있음)
        result = (df.groupby(['상품', '상품명'])
                  .agg({
                      '가용수량': 'sum',
                      '재고금액': 'sum',
                      '유효유통비(%)': 'mean',  # 평균 유효비
                      '단가': 'first'  # 첫 번째 단가
                  })
                  .sort_values('재고금액', ascending=False)
                  .head(n)
                  .reset_index())
        
        # 유효비 반올림
        result['유효유통비(%)'] = result['유효유통비(%)'].round(2)
        
        return result
    
    def calculate_total_value(self) -> int:
        """
        총 재고 금액 계산
        
        Returns:
            총 재고 금액 (정수)
        """
        df = self.get_data()
        total = (df['가용수량'] * df['단가']).sum()
        return int(total)
