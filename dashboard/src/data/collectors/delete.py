"""
DeleteCollector: 삭제현황 데이터 수집기

삭제처리일, 삭제처리시간, 상품, 상품명, 삭제수량, 알림여부, 알림시각 등을 수집
18시 이후 삭제 알림 기능 포함
"""

import pandas as pd
from datetime import datetime, time
from .base import BaseCollector


class DeleteCollector(BaseCollector):
    """삭제현황 수집기"""
    
    REQUIRED_COLUMNS = [
        '삭제처리일', '삭제처리시간', '상품', '상품명', '단위 및 규격',
        '삭제수량', '주문일자', '배송군', '배송처', '배송처명',
        '라벨출력', '출하바코드', 'To로케이션', '알림여부', '알림시각'
    ]
    
    def load_data(self) -> pd.DataFrame:
        """
        CSV 파일에서 삭제현황 데이터 로드
        
        Returns:
            삭제현황 데이터 DataFrame
            
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
            raise ValueError("삭제현황 데이터 검증 실패")
        
        # 데이터 타입 변환
        df['삭제처리일'] = pd.to_datetime(df['삭제처리일'], format='%Y%m%d', errors='coerce')
        df['주문일자'] = pd.to_datetime(df['주문일자'], format='%Y%m%d', errors='coerce')
        df['삭제수량'] = pd.to_numeric(df['삭제수량'], errors='coerce')
        
        # 삭제처리시간을 time 객체로 변환 (HHMMSS → HH:MM:SS)
        df['삭제시각'] = df['삭제처리시간'].apply(self._parse_time)
        
        # 알림시각 변환 (비어있을 수 있음)
        df['알림시각'] = pd.to_datetime(df['알림시각'], errors='coerce')
        
        # 알림여부 빈 값을 'N'으로 처리
        df['알림여부'] = df['알림여부'].fillna('N')
        
        return df
    
    def _parse_time(self, time_str) -> time:
        """
        시간 문자열을 time 객체로 변환
        
        Args:
            time_str: HHMMSS 형식 문자열 (예: '161117')
            
        Returns:
            time 객체
        """
        try:
            if pd.isna(time_str):
                return time(0, 0, 0)
            
            time_str = str(int(time_str)).zfill(6)  # 6자리로 패딩
            hour = int(time_str[0:2])
            minute = int(time_str[2:4])
            second = int(time_str[4:6])
            return time(hour, minute, second)
        except:
            return time(0, 0, 0)
    
    def validate(self, df: pd.DataFrame) -> bool:
        """
        삭제현황 데이터 유효성 검증
        
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
        삭제현황 데이터 요약 정보
        
        Returns:
            요약 정보 딕셔너리
        """
        df = self.get_data()
        
        # 18시 이후 삭제 건수
        after_18_count = self.count_after_18()
        
        # 알림 관련 통계
        alerted = df[df['알림여부'] == 'Y']
        not_alerted = df[df['알림여부'] == 'N']
        
        return {
            '총건수': len(df),
            '18시이후삭제': after_18_count,
            '알림완료': len(alerted),
            '알림미완료': len(not_alerted),
            '총삭제수량': df['삭제수량'].sum(),
            '배송처수': df['배송처명'].nunique(),
            '상품종류': df['상품명'].nunique(),
            '라벨출력완료': len(df[df['라벨출력'] == 'Y']),
            '라벨미출력': len(df[df['라벨출력'] == 'N']),
            '최근삭제일': df['삭제처리일'].max(),
            '최초삭제일': df['삭제처리일'].min(),
        }
    
    def count_after_18(self) -> int:
        """
        18시(18:00) 이후 삭제된 건수 계산
        
        Returns:
            18시 이후 삭제 건수
        """
        df = self.get_data()
        cutoff = time(18, 0, 0)  # 18:00:00
        
        # 18시 이후 데이터 필터링
        after_18 = df[df['삭제시각'] >= cutoff]
        return len(after_18)
    
    def get_urgent_deletes(self) -> pd.DataFrame:
        """
        긴급 삭제 알림 목록 (18시 이후 + 알림Y)
        
        Returns:
            긴급 삭제 알림 DataFrame
        """
        df = self.get_data()
        cutoff = time(18, 0, 0)
        
        # 18시 이후이면서 알림이 Y인 데이터
        urgent = df[(df['삭제시각'] >= cutoff) & (df['알림여부'] == 'Y')]
        return urgent
    
    def get_deletes_by_delivery(self) -> pd.DataFrame:
        """
        배송처별 삭제 통계
        
        Returns:
            배송처별 통계 DataFrame
        """
        df = self.get_data()
        
        return (df.groupby('배송처명')
                .agg({
                    '상품': 'count',
                    '삭제수량': 'sum'
                })
                .rename(columns={'상품': '삭제건수', '삭제수량': '총삭제수량'})
                .sort_values('삭제건수', ascending=False)
                .reset_index())
    
    def get_deletes_by_product(self) -> pd.DataFrame:
        """
        상품별 삭제 통계
        
        Returns:
            상품별 통계 DataFrame
        """
        df = self.get_data()
        
        return (df.groupby(['상품', '상품명'])
                .agg({
                    '삭제처리일': 'count',
                    '삭제수량': 'sum'
                })
                .rename(columns={'삭제처리일': '삭제건수', '삭제수량': '총삭제수량'})
                .sort_values('총삭제수량', ascending=False)
                .reset_index())
