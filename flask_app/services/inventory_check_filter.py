# -*- coding: utf-8 -*-
"""
재고조사 대상 상품코드 필터 모듈
- 초록불 판정 시 재고조사 대상 상품만 필터링
- 신선식품 + 임박상품(유효비≤50%, 신선제외) 상품코드 추출
- 작성일: 2025-12-12
- 수정일: 2026-01-13 (유효비 10%→50%, 상단로케이션 조건 삭제)
- 버전: v3.0
"""

import pandas as pd
from pathlib import Path
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# 필터 파일 경로
FILTER_DIR = Path(r"C:\Users\JWPark\Desktop\냉장 재고조사")
FRESH_FILTER_FILE = FILTER_DIR / "신선식품.csv"


def get_target_product_codes(inventory_df):
    """
    재고조사 대상 상품코드 추출
    
    로직 (v3.0):
        1. 신선식품.csv → fresh_codes (50개)
        2. inventory_df에서 임박상품 필터:
           - 유효유통비(%) ≤ 50
           - 상품코드 ∉ fresh_codes
           - 가용수량 > 0
           → imminent_codes 추출
        3. 반환: fresh_codes ∪ imminent_codes
    
    Args:
        inventory_df: 재고현황 DataFrame (로케이션, 상품, 유효유통비(%), 가용수량 컬럼 필수)
    
    Returns:
        set: 재고조사 대상 상품코드 set
              실패 시 빈 set() 반환 (폴백 신호)
    """
    try:
        # 1. 필터 파일 존재 확인
        if not FRESH_FILTER_FILE.exists():
            logger.warning(f"신선식품 필터 파일 없음: {FRESH_FILTER_FILE}")
            return set()
        
        # 2. inventory_df 유효성 확인
        if inventory_df is None or len(inventory_df) == 0:
            logger.warning("재고 데이터가 비어있음")
            return set()
        
        required_cols = ['상품', '로케이션', '유효유통비(%)', '가용수량']
        missing_cols = [col for col in required_cols if col not in inventory_df.columns]
        if missing_cols:
            logger.warning(f"재고 데이터에 필수 컬럼 없음: {missing_cols}")
            return set()
        
        # 3. 신선식품.csv 로드 (헤더 없음)
        fresh_df = pd.read_csv(FRESH_FILTER_FILE, encoding='utf-8-sig', header=None, names=['상품'])
        fresh_codes = set(fresh_df['상품'].astype(str).tolist())
        logger.info(f"신선식품 필터 로드: {len(fresh_codes)}개 상품코드")
        
        # 4. 임박상품 추출 (유효비 ≤ 50%, 신선 제외, 가용수량 > 0)
        inventory_df_copy = inventory_df.copy()
        inventory_df_copy['상품'] = inventory_df_copy['상품'].astype(str)
        inventory_df_copy['로케이션'] = inventory_df_copy['로케이션'].astype(str).str.strip()
        
        # 유효유통비(%) 숫자 변환
        inventory_df_copy['유효유통비(%)'] = pd.to_numeric(
            inventory_df_copy['유효유통비(%)'], errors='coerce'
        ).fillna(100)  # 변환 실패 시 100 (제외 대상)
        
        imminent_mask = (
            (inventory_df_copy['유효유통비(%)'] <= 30) &
            (~inventory_df_copy['상품'].isin(fresh_codes)) &
            (inventory_df_copy['가용수량'] > 0)
        )
        
        imminent_products = inventory_df_copy.loc[imminent_mask, '상품'].unique()
        imminent_codes = set(imminent_products)
        logger.info(f"임박상품 (유효비≤50%, 신선제외): {len(imminent_codes)}개")
        
        # 5. 최종: 신선식품 + 임박상품
        target_codes = fresh_codes | imminent_codes
        logger.info(f"재고조사 대상 총 상품코드: {len(target_codes)}개 (신선:{len(fresh_codes)} + 임박:{len(imminent_codes)})")
        
        return target_codes
        
    except Exception as e:
        logger.error(f"재고조사 대상 상품코드 추출 실패: {str(e)}")
        return set()


# 단독 테스트용
if __name__ == "__main__":
    import sys
    
    # 로깅 설정
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # 테스트용 재고 데이터 로드
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")
    inventory_file = Path(r"C:\OSIS_AUTO\inventory_status") / f"inventory_status_{today}.csv"
    
    if not inventory_file.exists():
        print(f"재고 파일 없음: {inventory_file}")
        sys.exit(1)
    
    inventory_df = pd.read_csv(inventory_file, encoding='utf-8-sig')
    print(f"재고 데이터 로드: {len(inventory_df)}건")
    
    # 함수 테스트
    target_codes = get_target_product_codes(inventory_df)
    print(f"\n결과: {len(target_codes)}개 상품코드")
    if len(target_codes) > 0:
        print(f"샘플 (처음 5개): {list(target_codes)[:5]}")
