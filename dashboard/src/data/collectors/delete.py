"""
DeleteCollector - 삭제현황 데이터 수집 모듈

주요 기능:
1. 삭제현황 CSV 파일 읽기
2. 18시(18:00) 이후 삭제 건수 카운팅
3. 긴급 삭제 알림 필터링 (18시 이후 + 알림Y)
4. 센터별, 시간대별 통계
"""

import pandas as pd
from datetime import datetime, time
from pathlib import Path
from typing import Optional
from .base import BaseCollector


class DeleteCollector(BaseCollector):
    """삭제현황 데이터를 수집하는 콜렉터"""
    
    REQUIRED_COLUMNS = [
        '삭제처리일',
        '삭제처리시간',
        '상품',
        '상품명',
        '단위 및 규격',
        '삭제수량',
        '주문일자',
        '배송군',
        '배송처',
        '배송처명',
        '라벨출력',
        '출하바코드',
        'To로케이션',
        '알림여부',
        '알림시각',
    ]
    
    def load_data(self) -> pd.DataFrame:
        """CSV 파일에서 삭제현황 데이터를 로드하고 타입 변환"""
        df = pd.read_csv(self.file_path, encoding='utf-8-sig')
        
        if df.empty:
            return df
        
        # 삭제처리시간을 time 객체로 변환 (HHMMSS → HH:MM:SS)
        df['삭제처리시간_time'] = df['삭제처리시간'].apply(
            lambda x: time(int(str(x)[:2]), int(str(x)[2:4]), int(str(x)[4:6]))
            if pd.notna(x) and len(str(x)) >= 6 else None
        )
        
        # 알림시각 datetime 변환 (있는 경우만)
        if df['알림시각'].notna().any():
            df['알림시각'] = pd.to_datetime(df['알림시각'], errors='coerce')
        
        # 삭제수량 numeric 변환
        df['삭제수량'] = pd.to_numeric(df['삭제수량'], errors='coerce')
        
        return df
    
    def validate(self, df: pd.DataFrame) -> bool:
        """데이터 유효성 검증"""
        # 필수 컬럼 확인
        missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            raise ValueError(f"필수 컬럼이 없습니다: {missing_columns}")
        
        # 빈 데이터 확인
        if df.empty:
            return False
        
        return True
    
    def count_after_18(self) -> int:
        """18시(18:00) 이후 삭제된 건수 반환"""
        df = self.get_data()
        if df.empty:
            return 0
        
        cutoff_time = time(18, 0, 0)
        after_18 = df[df['삭제처리시간_time'] >= cutoff_time]
        return len(after_18)
    
    def get_urgent_deletes(self) -> pd.DataFrame:
        """18시 이후 삭제 + 알림Y 건만 필터링"""
        df = self.get_data()
        if df.empty:
            return df
        
        cutoff_time = time(18, 0, 0)
        urgent = df[
            (df['삭제처리시간_time'] >= cutoff_time) &
            (df['알림여부'] == 'Y')
        ]
        return urgent
    
    def get_summary(self) -> dict:
        """삭제현황 요약 통계 반환"""
        df = self.get_data()
        
        if df.empty:
            return {
                '총삭제건수': 0,
                '18시이후건수': 0,
                '긴급알림건수': 0,
                '총삭제수량': 0,
                '라벨출력건수': 0,
                '라벨미출력건수': 0,
                '배송처수': 0,
                '배송군수': 0,
                '상품종류': 0,
                '평균삭제수량': 0.0,
                '알림건수': 0,
            }
        
        # 18시 기준 필터링
        cutoff_time = time(18, 0, 0)
        after_18 = df[df['삭제처리시간_time'] >= cutoff_time]
        urgent = df[
            (df['삭제처리시간_time'] >= cutoff_time) &
            (df['알림여부'] == 'Y')
        ]
        
        return {
            '총삭제건수': len(df),
            '18시이후건수': len(after_18),
            '긴급알림건수': len(urgent),
            '총삭제수량': int(df['삭제수량'].sum()),
            '라벨출력건수': len(df[df['라벨출력'] == 'Y']),
            '라벨미출력건수': len(df[df['라벨출력'] == 'N']),
            '배송처수': df['배송처명'].nunique(),
            '배송군수': df['배송군'].nunique(),
            '상품종류': df['상품명'].nunique(),
            '평균삭제수량': round(df['삭제수량'].mean(), 2),
            '알림건수': len(df[df['알림여부'] == 'Y']),
        }
    
    def get_deletes_by_time_range(
        self, 
        start_hour: int = 0, 
        end_hour: int = 23
    ) -> pd.DataFrame:
        """특정 시간대의 삭제 내역 조회
        
        Args:
            start_hour: 시작 시간 (0-23)
            end_hour: 종료 시간 (0-23)
            
        Returns:
            해당 시간대의 삭제 데이터
        """
        df = self.get_data()
        if df.empty:
            return df
        
        start_time = time(start_hour, 0, 0)
        end_time = time(end_hour, 59, 59)
        
        filtered = df[
            (df['삭제처리시간_time'] >= start_time) &
            (df['삭제처리시간_time'] <= end_time)
        ]
        return filtered
    
    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        """삭제 수량이 많은 상위 N개 상품
        
        Args:
            n: 상위 N개
            
        Returns:
            상품별 삭제수량 합계 (내림차순)
        """
        df = self.get_data()
        if df.empty:
            return pd.DataFrame()
        
        product_stats = df.groupby('상품명').agg({
            '삭제수량': 'sum',
            '삭제처리일': 'count'
        }).rename(columns={'삭제처리일': '삭제건수'})
        
        return product_stats.sort_values('삭제수량', ascending=False).head(n)
