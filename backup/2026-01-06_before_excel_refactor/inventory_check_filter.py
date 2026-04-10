# -*- coding: utf-8 -*-
"""
재고조사 대상 상품코드 필터 모듈
- 초록불 판정 시 재고조사 대상 상품만 필터링
- 신선식품 + 부진재고(신선제외) 상품코드 추출
- 작성일: 2025-12-12
- 버전: v1.0
"""

import pandas as pd
from pathlib import Path
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# 필터 파일 경로
FILTER_DIR = Path(r"C:\Users\JWPark\Desktop\냉장 재고조사")
FRESH_FILTER_FILE = FILTER_DIR / "신선식품.csv"
SLOW_FILTER_FILE = FILTER_DIR / "부진재고.csv"


def get_target_product_codes(inventory_df):
    """
    재고조사 대상 상품코드 추출
    
    로직:
        1. 신선식품.csv → 상품코드 리스트
        2. 부진재고.csv → 로케이션 리스트
        3. inventory_df에서 해당 로케이션의 상품코드 추출
        4. 신선식품 제외한 상품코드 추가
        5. 최종: 신선식품 + 부진재고(신선제외) 상품코드 반환
    
    Args:
        inventory_df: 재고현황 DataFrame (로케이션, 상품 컬럼 필수)
    
    Returns:
        set: 재고조사 대상 상품코드 set
              실패 시 빈 set() 반환 (폴백 신호)
    """
    try:
        # 1. 필터 파일 존재 확인
        if not FRESH_FILTER_FILE.exists():
            logger.warning(f"신선식품 필터 파일 없음: {FRESH_FILTER_FILE}")
            return set()
        
        if not SLOW_FILTER_FILE.exists():
            logger.warning(f"부진재고 필터 파일 없음: {SLOW_FILTER_FILE}")
            return set()
        
        # 2. inventory_df 유효성 확인
        if inventory_df is None or len(inventory_df) == 0:
            logger.warning("재고 데이터가 비어있음")
            return set()
        
        if '상품' not in inventory_df.columns or '로케이션' not in inventory_df.columns:
            logger.warning("재고 데이터에 필수 컬럼(상품, 로케이션) 없음")
            return set()
        
        # 3. 신선식품.csv 로드 (헤더 없음)
        fresh_df = pd.read_csv(FRESH_FILTER_FILE, encoding='utf-8-sig', header=None, names=['상품'])
        fresh_codes = set(fresh_df['상품'].astype(str).tolist())
        logger.info(f"신선식품 필터 로드: {len(fresh_codes)}개 상품코드")
        
        # 4. 부진재고.csv 로드 (헤더 없음)
        slow_df = pd.read_csv(SLOW_FILTER_FILE, encoding='utf-8-sig', header=None, names=['로케이션'])
        slow_locations = set(slow_df['로케이션'].astype(str).tolist())
        logger.info(f"부진재고 필터 로드: {len(slow_locations)}개 로케이션")
        
        # 5. 부진재고 로케이션에 있는 상품코드 추출
        inventory_df_str = inventory_df.copy()
        inventory_df_str['상품'] = inventory_df_str['상품'].astype(str)
        inventory_df_str['로케이션'] = inventory_df_str['로케이션'].astype(str)
        
        slow_products = inventory_df_str[
            inventory_df_str['로케이션'].isin(slow_locations)
        ]['상품'].unique()
        slow_codes = set(slow_products)
        logger.info(f"부진재고 로케이션 내 상품: {len(slow_codes)}개")
        
        # 6. 부진재고에서 신선식품 제외
        slow_codes_filtered = slow_codes - fresh_codes
        logger.info(f"부진재고 (신선제외): {len(slow_codes_filtered)}개")
        
        # 7. 최종: 신선식품 + 부진재고(신선제외)
        target_codes = fresh_codes | slow_codes_filtered
        logger.info(f"재고조사 대상 총 상품코드: {len(target_codes)}개 (신선:{len(fresh_codes)} + 부진:{len(slow_codes_filtered)})")
        
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
