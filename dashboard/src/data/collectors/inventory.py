"""
InventoryCollector: 재고정보 데이터 수집기

로케이션, 상품정보, 재고수량, 유효유통비, 단가 등을 수집
백엔드 실제 데이터 구조에 맞춤 (2025-10-20)
"""

import pandas as pd
from .base import BaseCollector


class InventoryCollector(BaseCollector):
    """재고정보 수집기"""
    
    # 백엔드 실제 컬럼 (12개)
    REQUIRED_COLUMNS = [
        '로케이션',        # 재고 위치
        '상품',            # 상품코드
        '상품명',          # 상품 이름
        '단위및규격',      # 단위 및 규격
        '소비기한',        # 유통기한
        '입수량',          # 박스당 개수
        '가용수량',        # 사용 가능한 수량
        '가용박스수량',    # 박스 단위 수량
        '가용잔량',        # 박스 외 낱개 수량
        '재고수량',        # 전체 재고
        '유효유통비(%)',   # 남은 유통기한 비율
        '단가'             # 상품 가격
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
        
        # CSV 읽기 (UTF-8 BOM 처리)
        df = pd.read_csv(self.file_path, encoding='utf-8-sig')
        
        # 데이터 검증
        if not self.validate(df):
            raise ValueError("재고 데이터 검증 실패")
        
        # 데이터 타입 변환
        df['소비기한'] = pd.to_datetime(df['소비기한'], format='%Y%m%d', errors='coerce')
        df['입수량'] = pd.to_numeric(df['입수량'], errors='coerce')
        df['가용수량'] = pd.to_numeric(df['가용수량'], errors='coerce')
        df['가용박스수량'] = pd.to_numeric(df['가용박스수량'], errors='coerce')
        df['가용잔량'] = pd.to_numeric(df['가용잔량'], errors='coerce')
        df['재고수량'] = pd.to_numeric(df['재고수량'], errors='coerce')
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
        재고 데이터 요약 정보 (4대 핵심 지표 포함)
        
        Returns:
            요약 정보 딕셔너리
        """
        df = self.get_data()
        
        # 총 재고 금액 계산 (재고수량 × 단가)
        df['재고금액'] = df['재고수량'] * df['단가']
        total_value = df['재고금액'].sum()
        
        # 위험 상품 수 (유효유통비 ≤ 20%)
        danger_count = len(df[df['유효유통비(%)'] <= 20])
        
        # 평균 유효유통비
        avg_effective_ratio = df['유효유통비(%)'].mean()
        
        summary = {
            # 4대 핵심 지표
            '총_상품_수': df['상품'].nunique(),           # 1. 총 상품 종류
            '총_재고_수량': int(df['재고수량'].sum()),    # 2. 총 재고 수량
            '총_재고_금액': int(total_value),             # 3. 총 재고 금액
            '위험_상품_수': int(danger_count),            # 4. 위험 상품 수 (유효비 ≤ 20%)
            
            # 보조 지표
            '평균_유효유통비': round(avg_effective_ratio, 1),
            '로케이션_수': df['로케이션'].nunique(),
            '가용_수량': int(df['가용수량'].sum()),
            '가용_박스수량': int(df['가용박스수량'].sum()),
        }
        
        return summary
    
    def get_expiring_soon(self, threshold: int = 20) -> pd.DataFrame:
        """
        유효기한 임박 상품 목록 (유효유통비 기준)
        
        Args:
            threshold: 유효유통비 기준값 (기본값: 20%)
            
        Returns:
            유효기한 임박 상품 DataFrame
        """
        df = self.get_data()
        
        # 유효유통비 기준 필터링
        expiring = df[df['유효유통비(%)'] <= threshold].copy()
        
        # 재고금액 계산
        expiring['재고금액'] = expiring['재고수량'] * expiring['단가']
        
        # 정렬 (유효유통비 낮은 순)
        expiring = expiring.sort_values('유효유통비(%)')
        
        # 필요한 컬럼만 선택
        result = expiring[[
            '로케이션', '상품', '상품명', '소비기한', 
            '재고수량', '유효유통비(%)', '단가', '재고금액'
        ]]
        
        return result
    
    def get_low_stock(self, threshold: int = 10) -> pd.DataFrame:
        """
        재고 부족 상품 목록 (가용수량 기준)
        
        Args:
            threshold: 가용수량 기준값 (기본값: 10개)
            
        Returns:
            재고 부족 상품 DataFrame
        """
        df = self.get_data()
        
        # 가용수량 기준 필터링
        low_stock = df[df['가용수량'] <= threshold].copy()
        
        # 재고금액 계산
        low_stock['재고금액'] = low_stock['재고수량'] * low_stock['단가']
        
        # 정렬 (가용수량 적은 순)
        low_stock = low_stock.sort_values('가용수량')
        
        # 필요한 컬럼만 선택
        result = low_stock[[
            '로케이션', '상품', '상품명', '가용수량', 
            '재고수량', '유효유통비(%)', '단가', '재고금액'
        ]]
        
        return result
    
    def get_by_location(self) -> pd.DataFrame:
        """
        로케이션별 재고 집계
        
        Returns:
            로케이션별 집계 DataFrame
        """
        df = self.get_data()
        
        # 재고금액 계산
        df['재고금액'] = df['재고수량'] * df['단가']
        
        result = (df.groupby('로케이션')
                  .agg({
                      '상품': 'nunique',
                      '재고수량': 'sum',
                      '가용수량': 'sum',
                      '재고금액': 'sum',
                      '유효유통비(%)': 'mean'
                  })
                  .sort_values('재고금액', ascending=False)
                  .reset_index())
        
        # 컬럼명 정리
        result.columns = [
            '로케이션', '상품_종류', '총_재고수량', 
            '총_가용수량', '총_재고금액', '평균_유효비'
        ]
        
        # 평균_유효비 반올림
        result['평균_유효비'] = result['평균_유효비'].round(1)
        
        return result
    
    def get_by_product(self, n: int = 10) -> pd.DataFrame:
        """
        상위 재고 상품 목록 (재고금액 기준)
        
        Args:
            n: 반환할 상품 수
            
        Returns:
            상품별 재고금액 DataFrame
        """
        df = self.get_data()
        
        # 재고금액 계산
        df['재고금액'] = df['재고수량'] * df['단가']
        
        result = (df.groupby(['상품', '상품명'])
                  .agg({
                      '재고수량': 'sum',
                      '가용수량': 'sum',
                      '재고금액': 'sum',
                      '유효유통비(%)': 'mean',
                      '로케이션': 'count'  # 보관 위치 수
                  })
                  .sort_values('재고금액', ascending=False)
                  .head(n)
                  .reset_index())
        
        # 컬럼명 정리
        result.columns = [
            '상품', '상품명', '총_재고수량', '총_가용수량', 
            '총_재고금액', '평균_유효비', '보관_위치_수'
        ]
        
        # 평균_유효비 반올림
        result['평균_유효비'] = result['평균_유효비'].round(1)
        
        return result
    
    def get_effective_ratio_distribution(self) -> pd.DataFrame:
        """
        유효유통비 구간별 분포
        
        Returns:
            유효비 구간별 상품 수 DataFrame
        """
        df = self.get_data()
        
        # 유효비 구간 정의
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['0-20% (위험)', '21-40% (주의)', '41-60% (보통)', '61-80% (양호)', '81-100% (우수)']
        
        df['유효비_구간'] = pd.cut(df['유효유통비(%)'], bins=bins, labels=labels, include_lowest=True)
        
        result = df.groupby('유효비_구간', observed=True).agg({
            '상품': 'nunique',
            '재고수량': 'sum'
        }).reset_index()
        
        result.columns = ['유효비_구간', '상품_수', '재고수량']
        
        return result
