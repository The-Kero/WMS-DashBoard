# -*- coding: utf-8 -*-
"""
대시보드 통합 API (v10 구조)
6개 카드 데이터를 통합하여 제공

카드 매핑 (v10 기준):
- card1: 입고현황
- card2: 자사출고
- card3: 지방출고
- card4: 스케줄 (정적)
- card5: 피킹유의
- card6: 재고현황 (5섹션)
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import sys
from pathlib import Path
import pandas as pd
import logging
import json
import glob
import os

# 로거 설정
logger = logging.getLogger(__name__)

# Collector 직접 import
dashboard_path = Path(__file__).parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.inbound import InboundCollector
from src.data.collectors.outbound import OutboundCollector
from src.data.collectors.inventory import InventoryCollector
from src.data.collectors.irregular import IrregularCollector
from src.data.collectors.delete import DeleteCollector

# 재고조사 엑셀 생성기 import
try:
    from services.inventory_excel_generator import generate_inventory_excel
    EXCEL_GENERATOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"재고조사 엑셀 생성기 import 실패: {e}")
    EXCEL_GENERATOR_AVAILABLE = False

# 재고조사 엑셀 출력 경로
INVENTORY_EXCEL_OUTPUT_DIR = r"C:\Users\JWPark\Desktop\냉장 재고조사"

# Blueprint 생성
bp = Blueprint('dashboard', __name__, url_prefix='/api')


def check_inventory_excel_exists(date_str):
    """
    당일 재고조사 엑셀 파일 존재 여부 확인 (중복 생성 방지)
    
    Args:
        date_str: YYYYMMDD 형식 날짜
    Returns:
        bool: 파일 존재 여부
    """
    file_date = date_str[2:]  # 20251207 → 251207
    fresh_file = Path(INVENTORY_EXCEL_OUTPUT_DIR) / f"{file_date} 냉장 재고조사(신선식품).xlsx"
    slow_file = Path(INVENTORY_EXCEL_OUTPUT_DIR) / f"{file_date} 냉장 재고조사(부진재고).xlsx"
    return fresh_file.exists() and slow_file.exists()


def get_baseline_unpicked_by_dest(base_path, target_hour, target_destinations, classify_func):
    """
    백업파일에서 특정 시간 이전의 배송처별 미발행 피킹 건수 추출
    
    Args:
        base_path: C:/OSIS_AUTO
        target_hour: 기준 시간 (13 또는 18)
        target_destinations: 대상 배송처 목록 ['yangsan', 'eumseong', ...]
        classify_func: 배송처 분류 함수
    
    Returns:
        dict: {'total': 총건수, 'by_dest': {배송처: 건수}}
    """
    try:
        backup_folder = f"{base_path}/Outbound Status/backup"
        today = datetime.now().strftime("%Y%m%d")
        pattern = f"{backup_folder}/outbound_all_{today}_{today}_*_backup.csv"
        
        backup_files = glob.glob(pattern)
        if not backup_files:
            logger.warning(f"백업파일 없음: {pattern}")
            return {'total': 0, 'by_dest': {d: 0 for d in target_destinations}}
        
        # 시간 기준 필터링 (target_hour 이전 파일 중 가장 최근)
        valid_files = []
        for f in backup_files:
            filename = os.path.basename(f)
            # outbound_all_YYYYMMDD_YYYYMMDD_HHMMSS_backup.csv
            parts = filename.replace('_backup.csv', '').split('_')
            if len(parts) >= 4:
                time_str = parts[-1]  # HHMMSS
                if len(time_str) == 6:
                    file_hour = int(time_str[:2])
                    if file_hour < target_hour:
                        valid_files.append((f, time_str))
        
        if not valid_files:
            logger.warning(f"{target_hour}시 이전 백업파일 없음")
            return {'total': 0, 'by_dest': {d: 0 for d in target_destinations}}
        
        # 가장 최근 파일 선택
        valid_files.sort(key=lambda x: x[1], reverse=True)
        baseline_file = valid_files[0][0]
        logger.info(f"기준 백업파일: {os.path.basename(baseline_file)}")
        
        # 백업파일 로드
        baseline_df = pd.read_csv(baseline_file, encoding='utf-8-sig')
        
        # 지방 출고 타입 필터링
        card3_types = [4, 5, 8, 16, 17, 52, 53]
        baseline_data = baseline_df[baseline_df['출고유형'].isin(card3_types)].copy()
        
        if len(baseline_data) == 0:
            return {'total': 0, 'by_dest': {d: 0 for d in target_destinations}}
        
        # 배송처 분류 적용
        baseline_data['dest_key'] = baseline_data.apply(classify_func, axis=1)
        
        # 대상 배송처별 미발행 건수 계산
        result = {'total': 0, 'by_dest': {d: 0 for d in target_destinations}}
        
        if '피킹 리스트' in baseline_data.columns and '오더수량*' in baseline_data.columns:
            unpicked = baseline_data[(baseline_data['피킹 리스트'] == 'N') & (baseline_data['오더수량*'] > 0)]
            for dest in target_destinations:
                count = len(unpicked[unpicked['dest_key'] == dest])
                result['by_dest'][dest] = count
                result['total'] += count
        
        return result
        
    except Exception as e:
        logger.error(f"백업파일 기준값 추출 오류: {str(e)}")
        return {'total': 0, 'by_dest': {d: 0 for d in target_destinations}}


# ==========================================
# 미할당 입고현황 스냅샷 헬퍼 함수들
# ==========================================

# 지방센터 9개 목록 (그대로 표시, 그 외는 "공급사"로 통일)
LOCAL_CENTERS = {'안산', '음성', '제주', '제천', '호남', '구미', '계룡', '용인', '양산'}

def normalize_supplier(supplier_raw):
    """공급사명 정규화 (용인2→용인, 지방센터 9개 외 '공급사')"""
    for center in LOCAL_CENTERS:
        if supplier_raw.startswith(center):
            return center
    return '공급사'


# ==========================================
# 미할당 입고현황 CSV 헬퍼 함수들 (v30 설계)
# ==========================================

def get_unallocated_csv_path(date_str):
    """미할당 입고현황 CSV 파일 경로 반환"""
    csv_dir = Path("C:/OSIS_AUTO/Inbound Status/unallocated")
    csv_dir.mkdir(parents=True, exist_ok=True)
    return csv_dir / f"unallocated_inbound_{date_str}.csv"


def load_unallocated_csv(date_str):
    """기존 CSV 파일 로드 (없으면 None)"""
    path = get_unallocated_csv_path(date_str)
    if path.exists():
        try:
            return pd.read_csv(path, encoding='utf-8-sig', dtype=str)
        except Exception as e:
            logger.warning(f"미할당 CSV 로드 실패: {e}")
    return None


def save_unallocated_csv(date_str, df):
    """CSV 파일 저장"""
    path = get_unallocated_csv_path(date_str)
    try:
        df.to_csv(path, index=False, encoding='utf-8-sig')
        logger.info(f"미할당 CSV 저장 완료: {path.name}")
    except Exception as e:
        logger.error(f"미할당 CSV 저장 실패: {e}")


def get_recorded_inbound_numbers(df):
    """CSV에서 이미 기록된 입고예정번호 목록 추출"""
    recorded = set()
    if df is None:
        return recorded
    
    # 입고예정번호N 패턴의 모든 컬럼에서 값 수집
    for col in df.columns:
        if col.startswith('입고예정번호'):
            for val in df[col].dropna():
                if val and str(val).strip():
                    recorded.add(str(val).strip())
    return recorded


def match_new_inbound_info(unallocated_df, inbound_df, recorded_numbers):
    """새 입고정보 매칭 (중복 제외, 미입고량 > 0 조건)"""
    result = {}
    
    if inbound_df is None or len(inbound_df) == 0:
        return result
    
    # 미입고량 > 0 필터
    inbound_df['미입고량_num'] = pd.to_numeric(inbound_df['미입고량'], errors='coerce').fillna(0)
    inbound_filtered = inbound_df[inbound_df['미입고량_num'] > 0].copy()
    
    if len(inbound_filtered) == 0:
        return result
    
    # 미할당 상품코드 목록
    unallocated_codes = set(unallocated_df['상품'].astype(str))
    
    for _, row in inbound_filtered.iterrows():
        product_code = str(row['상품'])
        inbound_number = str(row.get('입고예정번호', ''))
        
        # 미할당 목록에 있는 상품만
        if product_code not in unallocated_codes:
            continue
        
        # 이미 기록된 입고예정번호는 스킵
        if inbound_number in recorded_numbers:
            continue
        
        supplier_raw = str(row.get('공급사명', ''))
        undelivered_qty = int(row['미입고량_num'])
        current_time = datetime.now().strftime('%H:%M')
        
        if product_code not in result:
            result[product_code] = []
        
        result[product_code].append({
            'supplier': supplier_raw,
            'qty': undelivered_qty,
            'inbound_number': inbound_number,
            'time': current_time
        })
    
    return result


def add_inbound_columns(df, new_inbound_dict):
    """CSV DataFrame에 새 입고현황 컬럼 추가 (상품별 독립 번호)"""
    if not new_inbound_dict:
        return df, False
    
    added = False
    
    for product_code, infos in new_inbound_dict.items():
        # 해당 상품의 기존 입고현황 개수 파악
        mask = df['상품'].astype(str) == product_code
        product_rows = df[mask]
        
        if len(product_rows) == 0:
            continue
        
        # 해당 상품 행에서 값이 있는 입고현황 컬럼 개수
        existing_count = 0
        for col in df.columns:
            if col.startswith('입고현황') and not col.startswith('입고예정번호'):
                val = product_rows.iloc[0].get(col)
                if pd.notna(val) and str(val).strip():
                    try:
                        num = int(col.replace('입고현황', ''))
                        existing_count = max(existing_count, num)
                    except ValueError:
                        continue
        
        # 이 상품의 다음 번호부터 시작
        next_num = existing_count + 1
        
        for info in infos:
            col_name = f'입고현황{next_num}'
            num_col_name = f'입고예정번호{next_num}'
            
            # 컬럼이 없으면 생성 (빈 값으로)
            if col_name not in df.columns:
                df[col_name] = ''
            if num_col_name not in df.columns:
                df[num_col_name] = ''
            
            # 해당 상품 행에 값 설정
            value = f"{info['supplier']}({info['qty']})|{info['time']}"
            df.loc[mask, col_name] = value
            df.loc[mask, num_col_name] = info['inbound_number']
            
            next_num += 1
            added = True
    
    return df, added


def get_section5_display_data(df):
    """현황판 섹션5 표시용 데이터 생성 (정규화 + 합산)"""
    display_items = []
    
    if df is None or len(df) == 0:
        return display_items
    
    for _, row in df.iterrows():
        product_name = str(row.get('상품명', ''))
        unit = str(row.get('단위', ''))
        unallocated_qty = int(row.get('미할당수량', 0)) if row.get('미할당수량') else 0
        
        # 입고현황 컬럼들 파싱 (정규화 + 합산)
        supplier_qty = {}
        has_inbound = False
        
        for col in df.columns:
            if col.startswith('입고현황') and not col.startswith('입고예정번호'):
                val = row.get(col)
                if pd.notna(val) and str(val).strip():
                    has_inbound = True
                    # "공급사명(수량)|시간" 형식 파싱
                    try:
                        main_part = str(val).split('|')[0]  # 시간 부분 제거
                        supplier_raw = main_part.split('(')[0]
                        qty_str = main_part.split('(')[1].replace(')', '')
                        qty = int(qty_str)
                        
                        # 정규화 (용인2→용인)
                        supplier_normalized = normalize_supplier(supplier_raw)
                        supplier_qty[supplier_normalized] = supplier_qty.get(supplier_normalized, 0) + qty
                    except:
                        continue
        
        # 표시 문자열 생성
        if has_inbound:
            inbound_str = ', '.join([f"{s}({q})" for s, q in supplier_qty.items()])
        else:
            inbound_str = '⏳입고정보 대기중'
        
        display_items.append({
            'product_name': product_name,
            'unit': unit,
            'unallocated_qty': unallocated_qty,
            'inbound_info': inbound_str
        })
    
    # 상품명 가나다순 정렬
    display_items.sort(key=lambda x: x['product_name'])
    
    return display_items



def get_outbound_backup_before_1830(base_path, today):
    """18:30 이전 출고 백업 파일 찾기 (없으면 당일 마지막 백업)"""
    backup_folder = f"{base_path}/Outbound Status/backup"
    pattern = f"{backup_folder}/outbound_all_{today}_{today}_*_backup.csv"
    backup_files = glob.glob(pattern)
    
    if not backup_files:
        logger.warning(f"출고 백업파일 없음: {pattern}")
        return None
    
    # 18:30 이전 파일 필터링
    before_1830_files = []
    all_files_with_time = []
    
    for f in backup_files:
        filename = os.path.basename(f)
        parts = filename.replace('_backup.csv', '').split('_')
        if len(parts) >= 4:
            time_str = parts[-1]  # HHMMSS
            if len(time_str) == 6:
                file_hour = int(time_str[:2])
                file_minute = int(time_str[2:4])
                all_files_with_time.append((f, time_str))
                # 18:30 이전 체크
                if file_hour < 18 or (file_hour == 18 and file_minute < 30):
                    before_1830_files.append((f, time_str))
    
    # 1순위: 18:30 이전 중 가장 늦은 파일
    if before_1830_files:
        before_1830_files.sort(key=lambda x: x[1], reverse=True)
        return before_1830_files[0][0]
    
    # 2순위: 당일 마지막 백업 파일
    if all_files_with_time:
        all_files_with_time.sort(key=lambda x: x[1], reverse=True)
        logger.warning("18:30 이전 백업파일 없음, 당일 마지막 파일 사용")
        return all_files_with_time[0][0]
    
    return None

def extract_unallocated_from_outbound(outbound_df):
    """출고 데이터에서 미할당 상품 추출 (필터 5가지 적용)"""
    if outbound_df is None or len(outbound_df) == 0:
        return []
    
    # 필터 5가지 적용
    filtered = outbound_df[
        (outbound_df['문서상태명'].isin(['미할당', '미작업'])) &
        (outbound_df['출하타입구분'] == '재고') &
        (outbound_df['출고유형'].isin([14, 15, 18])) &
        (~outbound_df['배송군'].isin([6601, 6602])) &
        (pd.to_numeric(outbound_df['오더수량*'], errors='coerce').fillna(0) > 0)
    ].copy()
    
    if len(filtered) == 0:
        return []
    
    # 상품별 합산 (같은 상품 여러 행이면 합산)
    filtered['미할당수량'] = pd.to_numeric(filtered['오더수량*'], errors='coerce').fillna(0)
    grouped = filtered.groupby('상품').agg({
        '상품명': 'first',
        '단위및규격': 'first',
        '미할당수량': 'sum'
    }).reset_index()
    
    products = []
    for _, row in grouped.iterrows():
        products.append({
            'product_code': str(row['상품']),
            'product_name': str(row['상품명']),
            'unit': str(row['단위및규격']),
            'unallocated_qty': int(row['미할당수량']),
            'inbound_info': []  # 나중에 매칭
        })
    
    return products




@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    대시보드 6개 카드 데이터 반환 (v10 구조)
    
    Returns:
        JSON: {
            'success': bool,
            'card1': 입고현황,
            'card2': 자사출고,
            'card3': 지방출고,
            'card5': 피킹유의,
            'card6': 재고현황,
            'timestamp': str
        }
    """
    try:
        # 오늘 날짜
        today = datetime.now().strftime("%Y%m%d")
        base_path = "C:/OSIS_AUTO"
        
        # ==========================================
        # 1. 입고 데이터
        # ==========================================
        inbound_file = f"{base_path}/Inbound Status/integrated_inbound_{today}.csv"
        inbound_collector = InboundCollector(file_path=inbound_file, encoding='utf-8-sig')
        inbound_data = inbound_collector.get_data()
        
        # ==========================================
        # 2. 출고 데이터
        # ==========================================
        outbound_file = f"{base_path}/Outbound Status/outbound_all_{today}.csv"
        outbound_collector = OutboundCollector(file_path=outbound_file, encoding='utf-8-sig')
        outbound_data = outbound_collector.get_data()
        
        # ==========================================
        # 2-1. 재고조사 준비상태 신호등 계산 (출고 + 입고 AND 조합)
        # ==========================================
        inventory_check_count = 0
        inventory_check_status = 'green'  # 기본값: 완료
        outbound_status = 'green'
        inbound_status = 'green'
        inbound_avg_rate = 100.0
        
        # --- 출고 상태 계산 ---
        if len(outbound_data) > 0 and '문서상태명' in outbound_data.columns:
            unwork_count = len(outbound_data[outbound_data['문서상태명'] == '미작업'])
            unalloc_count = len(outbound_data[outbound_data['문서상태명'] == '미할당'])
            inventory_check_count = unalloc_count  # v47: 미할당만 체크 (미작업 제외)
            
            if inventory_check_count >= 11:
                outbound_status = 'red'
            elif inventory_check_count >= 1:
                outbound_status = 'orange'
            else:
                outbound_status = 'green'
            
            logger.info(f"출고 신호등 - 미작업: {unwork_count}(참고), 미할당: {unalloc_count}, 판정기준: {inventory_check_count}, 상태: {outbound_status}")
        
        # --- 입고 진척률 계산 (미입고 목록 제외) ---
        if len(inbound_data) > 0 and '진척률' in inbound_data.columns:
            exclude_file = f"{base_path}/Inbound Status/미입고_목록.csv"
            exclude_keys = set()
            
            try:
                exclude_df = pd.read_csv(exclude_file, encoding='utf-8-sig')
                exclude_df = exclude_df[exclude_df['입고예정일'] == int(today)]
                for _, row in exclude_df.iterrows():
                    key = (str(row['입고예정번호']), str(row['상품']))
                    exclude_keys.add(key)
                logger.info(f"미입고 제외 목록: {len(exclude_keys)}건")
            except FileNotFoundError:
                logger.info("미입고_목록.csv 없음 - 제외 없이 계산")
            except Exception as e:
                logger.warning(f"미입고 목록 로드 실패: {str(e)}")
            
            if len(exclude_keys) > 0:
                mask = inbound_data.apply(
                    lambda row: (str(row['입고예정번호']), str(row['상품'])) not in exclude_keys, 
                    axis=1
                )
                filtered_inbound = inbound_data[mask]
            else:
                filtered_inbound = inbound_data
            
            if len(filtered_inbound) > 0:
                inbound_avg_rate = filtered_inbound['진척률'].mean()
            else:
                inbound_avg_rate = 100.0
            
            if inbound_avg_rate >= 100.0:
                inbound_status = 'green'
            elif inbound_avg_rate >= 91.0:
                inbound_status = 'orange'
            else:
                inbound_status = 'red'
            
            logger.info(f"입고 신호등 - 진척률 평균: {inbound_avg_rate:.1f}%, 상태: {inbound_status}")
        
        # --- 최종 신호등 (AND 조합: 더 나쁜 쪽 적용) ---
        status_priority = {'red': 0, 'orange': 1, 'green': 2}
        if status_priority[outbound_status] <= status_priority[inbound_status]:
            inventory_check_status = outbound_status
        else:
            inventory_check_status = inbound_status
        
        logger.info(f"최종 신호등 - 출고: {outbound_status}, 입고: {inbound_status} → 최종: {inventory_check_status}")
        
        # ==========================================
        # 2-2. 초록불 시 재고조사 엑셀 자동 생성
        # ==========================================
        if inventory_check_status == 'green' and EXCEL_GENERATOR_AVAILABLE:
            try:
                if check_inventory_excel_exists(today):
                    logger.info(f"재고조사 엑셀 이미 존재 - 생성 스킵 ({today})")
                else:
                    logger.info(f"초록불! 재고조사 엑셀 생성 시작 ({today})")
                    result = generate_inventory_excel(today)
                    if result['success']:
                        logger.info(f"재고조사 엑셀 생성 완료: {result['files']}")
                    else:
                        logger.warning(f"재고조사 엑셀 생성 실패: {result['message']}")
            except Exception as e:
                logger.error(f"재고조사 엑셀 생성 중 오류: {str(e)}")
        
        # ==========================================
        # 3. 재고 데이터
        # ==========================================
        inventory_file = f"{base_path}/inventory_status/inventory_status_{today}.csv"
        inventory_collector = InventoryCollector(file_path=inventory_file, encoding='utf-8-sig')
        inventory_data = inventory_collector.get_data()
        
        # ==========================================
        # 4. 비정형 오더 데이터
        # ==========================================
        irregular_file = f"{base_path}/IrregularOrder Status/irregular_order_{today}.csv"
        try:
            irregular_collector = IrregularCollector(file_path=irregular_file, encoding='utf-8-sig')
            irregular_data = irregular_collector.get_data()
        except FileNotFoundError:
            logger.warning(f"비정형 오더 파일 없음: {irregular_file}")
            irregular_data = pd.DataFrame()
        except Exception as e:
            logger.warning(f"비정형 오더 로드 실패: {str(e)}")
            irregular_data = pd.DataFrame()
        
        # ==========================================
        # 5. 삭제 현황 데이터 (card6 섹션4용)
        # ==========================================
        delete_file = f"{base_path}/Delete Status/delete_status_{today}.csv"
        try:
            delete_collector = DeleteCollector(file_path=delete_file, encoding='utf-8-sig')
            delete_data = delete_collector.get_data()
        except FileNotFoundError:
            logger.warning(f"삭제 현황 파일 없음: {delete_file}")
            delete_data = pd.DataFrame()
        except Exception as e:
            logger.warning(f"삭제 현황 로드 실패: {str(e)}")
            delete_data = pd.DataFrame()
        
        # DataFrame 수집 완료
        logger.info(f"데이터 수집 완료 - 입고: {len(inbound_data)}, 출고: {len(outbound_data)}, 재고: {len(inventory_data)}, 비정형: {len(irregular_data)}, 삭제: {len(delete_data)}")
        
        # ==========================================
        # card1: 입고 현황 (구 card2)
        # ==========================================
        
        # 총 건수 및 평균 진척률
        card1_total = len(inbound_data)
        card1_progress = float(inbound_data['진척률'].mean()) if card1_total > 0 else 0.0
        
        # 입고유의상품 계산 (입고 소비기한 < 재고 소비기한)
        card1_risky_count = 0
        card1_risky_items = []
        
        if card1_total > 0 and len(inventory_data) > 0:
            try:
                # 입고 데이터: 상품별 최소 소비기한 + 상품명
                inbound_exp = inbound_data.groupby('상품').agg({
                    '소비기한': 'min',
                    '상품명': 'first'
                }).reset_index()
                inbound_exp.columns = ['상품', '입고_소비기한', '입고_상품명']
                
                # 재고 데이터: 상품별 최소 소비기한
                inv_exp = inventory_data.groupby('상품')['소비기한'].min().reset_index()
                inv_exp.columns = ['상품', '재고_소비기한']
                
                # 두 데이터 병합
                merged = pd.merge(inbound_exp, inv_exp, on='상품', how='inner')
                
                # 날짜 타입 변환 (format 명시)
                merged['입고_소비기한'] = pd.to_datetime(merged['입고_소비기한'], format='%Y%m%d', errors='coerce')
                merged['재고_소비기한'] = pd.to_datetime(merged['재고_소비기한'], format='%Y%m%d', errors='coerce')
                
                # 입고 소비기한 < 재고 소비기한인 상품 필터링
                risky_inbound = merged[merged['입고_소비기한'] < merged['재고_소비기한']]
                card1_risky_count = len(risky_inbound)
                
                # riskyItems 배열 생성
                for _, row in risky_inbound.iterrows():
                    card1_risky_items.append({
                        'productName': row['입고_상품명'],
                        'inboundExpiry': row['입고_소비기한'].strftime('%Y%m%d') if pd.notna(row['입고_소비기한']) else '',
                        'stockExpiry': row['재고_소비기한'].strftime('%Y%m%d') if pd.notna(row['재고_소비기한']) else ''
                    })
            except Exception as e:
                logger.warning(f"card1 - 입고유의상품 계산 에러: {str(e)}")
        
        logger.info(f"card1 - 총: {card1_total}, 진척률: {card1_progress:.1f}%, 유의상품: {card1_risky_count}")
        
        # ==========================================
        # card2: 자사 출고 (구 card5)
        # ==========================================
        
        # 자사 출고 타입 (14, 15, 18)
        card2_types = [14, 15, 18]
        card2_data = outbound_data[outbound_data['출고유형'].isin(card2_types)].copy()
        
        # 총 출하금액
        card2_amount = int(card2_data['출하금액'].sum()) if len(card2_data) > 0 else 0
        
        # 라벨 건수
        card2_total_label = len(card2_data)
        card2_unprinted_label = len(card2_data[card2_data['라벨출력'] == 'N']) if len(card2_data) > 0 else 0
        
        # 전일 대비 계산 (D-1부터 탐색)
        card2_compare = 0.0
        for days_ago in range(1, 11):
            compare_date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime("%Y%m%d")
            compare_file = f"{base_path}/Outbound Status/outbound_all_{compare_date}.csv"
            
            try:
                compare_collector = OutboundCollector(file_path=compare_file, encoding='utf-8-sig')
                compare_df = compare_collector.get_data()
                compare_data = compare_df[compare_df['출고유형'].isin(card2_types)]
                compare_amount = int(compare_data['출하금액'].sum()) if len(compare_data) > 0 else 0
                
                if compare_amount > 0:
                    card2_compare = ((card2_amount - compare_amount) / compare_amount * 100)
                    break
            except:
                continue
        
        logger.info(f"card2 - 금액: {card2_amount:,}원, 라벨: {card2_total_label}건, 전일대비: {card2_compare:+.1f}%")
        
        # ==========================================
        # card3: 지방 출고 (구 card6)
        # ==========================================
        
        def classify_destination(row):
            """배송처 분류 함수 (v9 가이드 기준)"""
            출고유형 = row['출고유형']
            배송군 = row['배송군']
            배송처명 = row['배송처명']
            
            if pd.isna(배송군):
                배송군_str = ''
            else:
                배송군_str = str(int(배송군))
            
            if pd.isna(배송처명):
                배송처명 = ''
            
            배송군_4자리 = len(배송군_str) == 4
            
            # 출고유형 05
            if 출고유형 == 5:
                if 배송처명 == '식재':
                    return 'hanex'
                elif 배송군_4자리 and 배송군_str[0] == '3':
                    return 'kids'
                elif 배송군_4자리 and 배송군_str[0] == '4':
                    return 'yongin3'
                elif 배송군_4자리 and 배송군_str[0] == '2':
                    return 'yongin2'
            
            # 출고유형 08
            elif 출고유형 == 8:
                if 배송군_4자리 and 배송군_str[0] == '4':
                    return 'yongin3'
                elif 배송군_4자리 and 배송군_str[0] == '2':
                    return 'yongin2'
            
            # 출고유형 04, 16, 17, 52, 53
            elif 출고유형 in [4, 16, 17, 52, 53]:
                if '용인' in 배송처명:
                    if 배송군_4자리 and 배송군_str[0] == '4':
                        return 'yongin3'
                    else:
                        return 'yongin2'
                elif 배송처명 == '양산':
                    return 'yangsan'
                elif 배송처명 == '양산2':
                    return 'yangsan2'
                else:
                    # 배송처명 → 영문키 매핑
                    dest_mapping = {
                        '제주': 'jeju', '제천': 'jecheon', '호남': 'honam',
                        '구미': 'gumi', '계룡': 'gyeryong', '음성': 'eumseong',
                        '안산': 'ansan'
                    }
                    return dest_mapping.get(배송처명, 'etc')
            
            return 'etc'
        
        # 지방 출고 타입 필터링
        card3_types = [4, 5, 8, 16, 17, 52, 53]
        card3_data = outbound_data[outbound_data['출고유형'].isin(card3_types)].copy()
        
        # 총 출하금액
        card3_amount = int(card3_data['출하금액'].sum()) if len(card3_data) > 0 else 0
        
        # 미발행 피킹리스트 (오더수량* > 0 조건 필수!)
        # ⚠️ 오더수량이 0이면 피킹할 물량 없음 → 리스트 안 뽑는게 정상
        card3_unprinted_picking = 0
        if len(card3_data) > 0 and '피킹 리스트' in card3_data.columns and '오더수량*' in card3_data.columns:
            card3_unprinted_picking = len(card3_data[(card3_data['피킹 리스트'] == 'N') & (card3_data['오더수량*'] > 0)])
        
        # 전일 대비 계산
        card3_compare = 0.0
        for days_ago in range(1, 11):
            compare_date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime("%Y%m%d")
            compare_file = f"{base_path}/Outbound Status/outbound_all_{compare_date}.csv"
            try:
                compare_collector = OutboundCollector(file_path=compare_file, encoding='utf-8-sig')
                compare_df = compare_collector.get_data()
                compare_data = compare_df[compare_df['출고유형'].isin(card3_types)]
                compare_amount = int(compare_data['출하금액'].sum()) if len(compare_data) > 0 else 0
                if compare_amount > 0:
                    card3_compare = ((card3_amount - compare_amount) / compare_amount * 100)
                    break
            except:
                continue
        
        # 배송처별 집계 (destinations 객체) - printedQty, unprintedQty, unprintedCount 포함
        card3_destinations = {
            'jeju': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'jecheon': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'honam': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'gumi': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'gyeryong': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'eumseong': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'yongin2': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'yongin3': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'ansan': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'yangsan': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'yangsan2': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'hanex': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0},
            'kids': {'printedQty': 0, 'unprintedQty': 0, 'unprintedCount': 0}
        }
        
        if len(card3_data) > 0:
            card3_data['dest_key'] = card3_data.apply(classify_destination, axis=1)
            
            if '오더수량*' in card3_data.columns and '피킹 리스트' in card3_data.columns:
                # 발행된 것 (피킹리스트=Y 또는 오더수량*=0)
                printed_data = card3_data[(card3_data['피킹 리스트'] == 'Y') | (card3_data['오더수량*'] == 0)]
                printed_qty_by_dest = printed_data.groupby('dest_key')['오더수량*'].sum().to_dict()
                
                # 미발행된 것 (피킹리스트=N AND 오더수량*>0)
                unprinted_data = card3_data[(card3_data['피킹 리스트'] == 'N') & (card3_data['오더수량*'] > 0)]
                unprinted_qty_by_dest = unprinted_data.groupby('dest_key')['오더수량*'].sum().to_dict()
                unprinted_count_by_dest = unprinted_data.groupby('dest_key').size().to_dict()
                
                # 각 배송처별로 값 설정
                for dest_key in card3_destinations.keys():
                    card3_destinations[dest_key]['printedQty'] = int(printed_qty_by_dest.get(dest_key, 0))
                    card3_destinations[dest_key]['unprintedQty'] = int(unprinted_qty_by_dest.get(dest_key, 0))
                    card3_destinations[dest_key]['unprintedCount'] = int(unprinted_count_by_dest.get(dest_key, 0))
        
        logger.info(f"card3 - 금액: {card3_amount:,}원, 미발행피킹: {card3_unprinted_picking}건")
        
        # ==========================================
        # card3 긴급알림 로직
        # ==========================================
        card3_urgent_alert = False
        card3_urgent_destinations = []
        card3_urgent_count = 0
        card3_baseline_count = 0
        card3_alert_time_slot = None
        
        # 시간대 체크 및 긴급알림 계산
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        current_total_minutes = current_hour * 60 + current_minute  # 총 분으로 변환
        test_alert = request.args.get('test_alert', 'false').lower() == 'true'
        test_unallocated_count = int(request.args.get('test_unallocated', '0'))  # 미할당 더미 데이터 개수
        
        # 시간대별 대상 배송처 정의
        slot1_dests = ['yangsan', 'yangsan2', 'eumseong']  # 13~16시: 3곳
        slot2_dests = ['jeju', 'jecheon', 'honam', 'gumi', 'gyeryong', 'eumseong', 
                       'yongin2', 'yongin3', 'ansan', 'yangsan', 'yangsan2', 'hanex', 'kids']  # 18:40~20시: 전체
        
        target_dests = None
        target_hour = None
        
        if test_alert:
            # 테스트 모드: 시간 무시, 18:40~20시 조건으로 테스트
            target_dests = slot2_dests
            target_hour = 18
            card3_alert_time_slot = "test"
            logger.info("card3 긴급알림 테스트 모드 활성화")
        elif 860 <= current_total_minutes < 960:  # 14:20 ~ 16:00
            target_dests = slot1_dests
            target_hour = 13
            card3_alert_time_slot = "14:20-16"
        elif 1160 <= current_total_minutes < 1220:  # 19:20 ~ 20:20
            target_dests = slot2_dests
            target_hour = 18  # 기준값은 18시 파일 사용
            card3_alert_time_slot = "19:20-20:20"
        
        if target_dests and target_hour:
            # 기준값 조회 (백업파일에서)
            baseline = get_baseline_unpicked_by_dest(base_path, target_hour, target_dests, classify_destination)
            card3_baseline_count = baseline['total']
            
            # 대상 배송처 미발행 건수 합계 (현재값) - 팝업 트리거용
            dest_name_map = {
                'jeju': '제주', 'jecheon': '제천', 'honam': '호남', 'gumi': '구미',
                'gyeryong': '계룡', 'eumseong': '음성', 'yongin2': '용인2', 'yongin3': '용인3',
                'ansan': '안산', 'yangsan': '양산', 'yangsan2': '양산2', 'hanex': '한익스', 'kids': '키즈'
            }
            
            for dest in target_dests:
                current_count = card3_destinations[dest]['unprintedCount']
                if current_count > 0:
                    card3_urgent_destinations.append(dest_name_map.get(dest, dest))
                card3_urgent_count += current_count
            
            # 긴급알림 표시 여부 (미발행 건수가 있으면)
            if card3_urgent_count > 0:
                card3_urgent_alert = True
                logger.info(f"card3 긴급알림 - 시간대: {card3_alert_time_slot}, "
                           f"기준: {card3_baseline_count}건, 현재: {card3_urgent_count}건, "
                           f"대상: {card3_urgent_destinations}")
        
        # ==========================================
        # card4: 스케줄 (JSON 파일에서 로드) - 날짜순 정렬
        # ==========================================
        card4_schedules = []
        
        try:
            schedule_file = Path(__file__).parent.parent / 'data' / 'schedule.json'
            if schedule_file.exists():
                with open(schedule_file, 'r', encoding='utf-8') as f:
                    all_schedules = json.load(f)
                
                today_date = datetime.now().date()
                
                # 오늘 이후 일정만 필터링
                future_schedules = []
                for schedule in all_schedules:
                    try:
                        sched_date = datetime.strptime(schedule['date'], '%Y-%m-%d').date()
                        
                        if sched_date >= today_date:
                            future_schedules.append({
                                'date': schedule['date'],
                                'content': schedule['content'],
                                'type': schedule.get('type', 'event')
                            })
                    except:
                        continue
                
                # 날짜순 정렬 후 최대 5개
                future_schedules.sort(key=lambda x: x['date'])
                card4_schedules = future_schedules[:5]
                
                logger.info(f"card4 - 스케줄 {len(card4_schedules)}건 (날짜순 정렬)")
        except Exception as e:
            logger.warning(f"card4 스케줄 로드 실패: {str(e)}")
        
        # ==========================================
        # card5: 피킹 유의 상품 (구 card3)
        # ==========================================
        
        # 유효유통비 20% 이하 필터링
        risky = inventory_data[inventory_data['유효유통비(%)'] <= 20].copy()
        
        # L07 로케이션 제외
        risky_filtered = risky[~risky['로케이션'].str.startswith('L07', na=False)].copy()
        
        # 가용수량 0 제외
        risky_filtered = risky_filtered[risky_filtered['가용수량'] != 0].copy()
        
        # 긴급/주의 구분
        card5_urgent = len(risky_filtered[risky_filtered['유효유통비(%)'] <= 10])
        card5_warning = len(risky_filtered[risky_filtered['유효유통비(%)'] > 10])
        card5_total = len(risky_filtered)
        
        # 유효비 오름차순 정렬
        risky_filtered = risky_filtered.sort_values('유효유통비(%)')
        
        # riskyItems 배열 생성 (v10 구조)
        card5_items = []
        for _, row in risky_filtered.iterrows():
            expiry_raw = row.get('소비기한', '')
            if pd.notna(expiry_raw):
                # YYYYMMDD → YY.MM.DD 형식 변환
                expiry_clean = str(expiry_raw).replace('-', '')[:8]
                if len(expiry_clean) == 8:
                    expiry_str = f"{expiry_clean[2:4]}.{expiry_clean[4:6]}.{expiry_clean[6:8]}"
                else:
                    expiry_str = expiry_clean
            else:
                expiry_str = ''
            
            card5_items.append({
                'location': str(row.get('로케이션', '')),
                'productCode': str(row.get('상품', '')),
                'productName': str(row.get('상품명', '')),
                'expiryDate': expiry_str,
                'validityRatio': float(row.get('유효유통비(%)', 0)),
                'availableQty': int(row.get('가용수량', 0))
            })
        
        logger.info(f"card5 - 총: {card5_total}, 긴급: {card5_urgent}, 주의: {card5_warning}")
        
        # ==========================================
        # card6: 재고 현황 (5섹션)
        # ==========================================
        # 섹션1: 총재고 + 적치율 (inventory_data)
        # 섹션2: 선입선출 위반 (inventory_data L/K 비교)
        # 섹션3: 미출/부분출고 (outbound_data, 18시 이후)
        # 섹션4: 삭제현황 (delete_data 안산/음성)
        # 섹션5: 미할당 (inbound_data 로케이션 없음)
        # ==========================================
        
        logger.info("card6 계산 시작...")
        
        # 섹션1: 총재고 + 적치율
        card6_total_value = 0
        card6_storage_rate = 0.0
        card6_product_count = 0
        card6_upper_used = 0
        card6_upper_total = 524
        
        if len(inventory_data) > 0:
            # 총 상품수
            if '상품' in inventory_data.columns:
                card6_product_count = inventory_data['상품'].nunique()
            
            # 총재고 = SUM(가용수량 * 단가)
            if '가용수량' in inventory_data.columns and '단가' in inventory_data.columns:
                card6_total_value = int((inventory_data['가용수량'] * inventory_data['단가']).sum())
            
            # 적치율 = (상단 로케이션 중 재고있는 것) / 524 * 100
            # 상단 로케이션 목록: 냉장 파레트 적재 로케이션.csv (524개)
            upper_loc_file = f"{base_path}/inventory_status/냉장 파레트 적재 로케이션.csv"
            try:
                upper_loc_df = pd.read_csv(upper_loc_file, header=None, encoding='utf-8-sig')
                upper_loc_set = set(upper_loc_df[0].str.strip())
                # 재고 중 상단 로케이션에 있는 것만 필터링
                upper_locations = inventory_data[inventory_data['로케이션'].isin(upper_loc_set)]
                if len(upper_locations) > 0:
                    unique_upper = upper_locations['로케이션'].nunique()
                    card6_upper_used = unique_upper
                    card6_upper_total = len(upper_loc_set)
                    card6_storage_rate = round(unique_upper / card6_upper_total * 100, 1)
            except Exception as e:
                logger.warning(f"상단 로케이션 파일 로드 실패: {str(e)}")
        
        # 섹션2~5: 기본값 (PART 2에서 구현)
        card6_fifo = []
        card6_partial = []
        card6_delete_ansan = []
        card6_delete_eumseong = []
        card6_unallocated = []
        
        # ==========================================
        # 섹션2: 선입선출 위반 계산
        # ==========================================
        # 위반 조건: 같은 상품에서 상단 소비기한 < 하단 소비기한
        # 상단 = CSV 파일에 있는 524개 로케이션, 하단 = CSV에 없는 로케이션
        if len(inventory_data) > 0 and '로케이션' in inventory_data.columns and '소비기한' in inventory_data.columns:
            try:
                # 상단 로케이션 목록 로드 (적치율에서 이미 로드했으면 재사용)
                if 'upper_loc_set' not in locals():
                    upper_loc_file = f"{base_path}/inventory_status/냉장 파레트 적재 로케이션.csv"
                    upper_loc_df = pd.read_csv(upper_loc_file, header=None, encoding='utf-8-sig')
                    upper_loc_set = set(upper_loc_df[0].str.strip())
                
                # 상단: CSV에 있는 로케이션 (가용수량 > 0만)
                upper_df = inventory_data[
                    (inventory_data['로케이션'].isin(upper_loc_set)) & 
                    (inventory_data['가용수량'] > 0)
                ].copy()
                
                # 하단: CSV에 없는 로케이션 (가용수량 > 0만)
                lower_df = inventory_data[
                    (~inventory_data['로케이션'].isin(upper_loc_set)) & 
                    (inventory_data['가용수량'] > 0)
                ].copy()
                
                if len(upper_df) > 0 and len(lower_df) > 0:
                    # 2.3.3 상품별 소비기한 비교
                    # 상단에서 상품별 최소 소비기한
                    upper_min = upper_df.groupby('상품')['소비기한'].min().reset_index()
                    upper_min.columns = ['상품', 'upper_expiry']
                    
                    # 하단에서 상품별 최소 소비기한
                    lower_min = lower_df.groupby('상품')['소비기한'].min().reset_index()
                    lower_min.columns = ['상품', 'lower_expiry']
                    
                    # 상품코드로 조인
                    merged = pd.merge(upper_min, lower_min, on='상품', how='inner')
                    
                    # 2.3.4 위반 항목 필터링 (상단 < 하단)
                    violations = merged[merged['upper_expiry'] < merged['lower_expiry']]
                    
                    # 2.3.5 fifo 배열 생성
                    for _, row in violations.iterrows():
                        product_code = str(row['상품'])
                        # 상품명 찾기
                        product_name_row = inventory_data[inventory_data['상품'] == row['상품']].iloc[0] if len(inventory_data[inventory_data['상품'] == row['상품']]) > 0 else None
                        product_name = str(product_name_row['상품명']) if product_name_row is not None and '상품명' in product_name_row else product_code
                        
                        # 상단 로케이션 찾기 (최소 소비기한 + 가용수량 최소)
                        upper_product_df = upper_df[upper_df['상품'] == row['상품']]
                        upper_loc_row = upper_product_df[upper_product_df['소비기한'] == row['upper_expiry']].sort_values('가용수량').iloc[0]
                        upper_location = str(upper_loc_row['로케이션'])
                        
                        # 하단 로케이션 찾기 (최소 소비기한 + 가용수량 최소)
                        lower_product_df = lower_df[lower_df['상품'] == row['상품']]
                        lower_loc_row = lower_product_df[lower_product_df['소비기한'] == row['lower_expiry']].sort_values('가용수량').iloc[0]
                        lower_location = str(lower_loc_row['로케이션'])
                        
                        # 날짜 포맷 변환 (YYYYMMDD → YY.MM.DD)
                        upper_exp = str(row['upper_expiry']).replace('-', '')[:8]
                        lower_exp = str(row['lower_expiry']).replace('-', '')[:8]
                        upper_exp_fmt = f"{upper_exp[2:4]}.{upper_exp[4:6]}.{upper_exp[6:8]}" if len(upper_exp) >= 8 else upper_exp
                        lower_exp_fmt = f"{lower_exp[2:4]}.{lower_exp[4:6]}.{lower_exp[6:8]}" if len(lower_exp) >= 8 else lower_exp
                        
                        card6_fifo.append({
                            'lower': {
                                'product': product_name,
                                'location': lower_location,
                                'expiry': lower_exp_fmt
                            },
                            'upper': {
                                'location': upper_location,
                                'expiry': upper_exp_fmt
                            }
                        })
                
                logger.info(f"card6 섹션2 - 선입선출 위반: {len(card6_fifo)}건")
            except Exception as e:
                logger.warning(f"선입선출 계산 오류: {str(e)}")
        
        # ==========================================
        # 섹션3: 미출/부분출고 계산
        # ==========================================
        # 18:30 이후에만 표시 (그 전에는 작업 진행 중)
        now = datetime.now()
        is_after_1830 = (now.hour > 18) or (now.hour == 18 and now.minute >= 30)
        
        if is_after_1830 and len(outbound_data) > 0:
            try:
                # 필요한 컬럼 확인 (출고유형 추가)
                required_cols = ['출고유형', '원주문수량', '오더수량*', '배송군', '배송처명', '상품명', '단위및규격']
                if all(col in outbound_data.columns for col in required_cols):
                    
                    # 자사출고 타입만 필터링 (14, 15, 18)
                    company_types = [14, 15, 18]
                    company_outbound = outbound_data[outbound_data['출고유형'].isin(company_types)].copy()
                    
                    # 숫자 변환
                    company_outbound['원주문수량_num'] = pd.to_numeric(company_outbound['원주문수량'], errors='coerce').fillna(0)
                    company_outbound['오더수량_num'] = pd.to_numeric(company_outbound['오더수량*'], errors='coerce').fillna(0)
                    
                    # 미출: 오더수량 = 0 AND 원주문수량 > 0
                    # 부분출고: 0 < 오더수량 < 원주문수량
                    partial_df = company_outbound[
                        (company_outbound['원주문수량_num'] > company_outbound['오더수량_num']) &
                        (company_outbound['원주문수량_num'] > 0)
                    ]
                    
                    for _, row in partial_df.iterrows():
                        original_qty = int(row['원주문수량_num'])
                        order_qty = int(row['오더수량_num'])
                        
                        card6_partial.append({
                            'delivery_group': str(row.get('배송군', '')),
                            'delivery_name': str(row.get('배송처명', '')),
                            'product_name': str(row.get('상품명', '')),
                            'unit': str(row.get('단위및규격', '')),
                            'original_qty': original_qty,
                            'order_qty': order_qty
                        })
                    
                    logger.info(f"card6 섹션3 - 미출/부분출고: {len(card6_partial)}건 (18:30 이후, 자사출고만)")
            except Exception as e:
                logger.warning(f"미출/부분출고 계산 오류: {str(e)}")
        else:
            if not is_after_1830:
                logger.info(f"card6 섹션3 - 18:30 이전({now.hour}:{now.minute:02d}), 미출/부분출고 미표시")
        
        # ==========================================
        # 섹션4: 삭제현황 계산 (안산/음성)
        # ==========================================
        # 삭제 상품코드.csv 기준으로 재고현황에서 가용수량 조회
        try:
            # 삭제 상품코드 매핑 파일 로드
            delete_code_file = f"{base_path}/inventory_status/삭제 상품코드.csv"
            delete_code_df = pd.read_csv(delete_code_file, header=None, encoding='utf-8-sig')
            delete_code_df.columns = ['상품코드', '센터', '상품명_참조']
            
            # 안산/음성 상품코드 Set 생성
            ansan_codes = set(delete_code_df[delete_code_df['센터'] == '안산']['상품코드'].astype(str))
            eumseong_codes = set(delete_code_df[delete_code_df['센터'] == '음성']['상품코드'].astype(str))
            
            # 재고현황에서 해당 상품코드 필터링
            if len(inventory_data) > 0 and '상품' in inventory_data.columns:
                inventory_data['상품_str'] = inventory_data['상품'].astype(str)
                
                # 안산 삭제 상품
                ansan_inventory = inventory_data[inventory_data['상품_str'].isin(ansan_codes)]
                for _, row in ansan_inventory.iterrows():
                    qty = int(row.get('가용수량', 0)) if pd.notna(row.get('가용수량')) else 0
                    if qty > 0:  # 가용수량이 있는 것만 표시
                        card6_delete_ansan.append({
                            'product_name': str(row.get('상품명', '')),
                            'unit': str(row.get('단위및규격', '')),
                            'qty': qty
                        })
                
                # 음성 삭제 상품
                eumseong_inventory = inventory_data[inventory_data['상품_str'].isin(eumseong_codes)]
                for _, row in eumseong_inventory.iterrows():
                    qty = int(row.get('가용수량', 0)) if pd.notna(row.get('가용수량')) else 0
                    if qty > 0:  # 가용수량이 있는 것만 표시
                        card6_delete_eumseong.append({
                            'product_name': str(row.get('상품명', '')),
                            'unit': str(row.get('단위및규격', '')),
                            'qty': qty
                        })
            
            logger.info(f"card6 섹션4 - 삭제현황: 안산 {len(card6_delete_ansan)}건, 음성 {len(card6_delete_eumseong)}건")
        except Exception as e:
            logger.warning(f"삭제현황 계산 오류: {str(e)}")
        
        # ==========================================
        # 섹션5: 미할당 상품 입고현황 (CSV 기반 v30)
        # ==========================================
        # 18:10 이후에만 표시, CSV로 미할당 목록 관리
        # 핵심 원칙: 기존 데이터 삭제/수정 금지, 추가만 허용
        try:
            if is_after_1830:
                unallocated_df = load_unallocated_csv(today)
                
                if unallocated_df is None:
                    # CSV 없음 → 새로 생성
                    logger.info("미할당 CSV 새로 생성 시작...")
                    backup_file = get_outbound_backup_before_1830(base_path, today)
                    
                    if backup_file:
                        backup_df = pd.read_csv(backup_file, encoding='utf-8-sig')
                        products = extract_unallocated_from_outbound(backup_df)
                        
                        if len(products) > 0:
                            # DataFrame 생성 (기본 컬럼)
                            unallocated_df = pd.DataFrame([{
                                '상품': p['product_code'],
                                '상품명': p['product_name'],
                                '단위': p['unit'],
                                '미할당수량': p['unallocated_qty']
                            } for p in products])
                            
                            # 입고정보 매칭 시도
                            recorded_numbers = set()
                            new_inbound = match_new_inbound_info(unallocated_df, inbound_data, recorded_numbers)
                            if new_inbound:
                                unallocated_df, _ = add_inbound_columns(unallocated_df, new_inbound)
                            
                            save_unallocated_csv(today, unallocated_df)
                            logger.info(f"미할당 CSV 생성 완료: {len(products)}개 상품")
                        else:
                            # 미할당 상품 없음 → 빈 CSV 생성
                            unallocated_df = pd.DataFrame(columns=['상품', '상품명', '단위', '미할당수량'])
                            save_unallocated_csv(today, unallocated_df)
                            logger.info("미할당 상품 없음 - 빈 CSV 생성")
                    else:
                        logger.warning("출고 백업파일 없음, 미할당 CSV 생성 불가")
                        unallocated_df = pd.DataFrame()
                else:
                    # 기존 CSV 있음 → 새 입고정보만 추가 (기존 유지)
                    recorded_numbers = get_recorded_inbound_numbers(unallocated_df)
                    new_inbound = match_new_inbound_info(unallocated_df, inbound_data, recorded_numbers)
                    
                    if new_inbound:
                        unallocated_df, added = add_inbound_columns(unallocated_df, new_inbound)
                        if added:
                            save_unallocated_csv(today, unallocated_df)
                            logger.info(f"미할당 CSV 갱신 완료 (새 입고정보 추가)")
                    else:
                        logger.info(f"미할당 CSV 변경 없음: {len(unallocated_df)}개 상품")
                
                # 현황판 표시용 데이터 생성 (정규화 + 합산)
                card6_unallocated = get_section5_display_data(unallocated_df)
                
                logger.info(f"card6 섹션5 - 미할당 입고현황: {len(card6_unallocated)}건 (18:30 이후)")
            else:
                logger.info(f"card6 섹션5 - 18:30 이전({now.hour}:{now.minute:02d}), 미할당 미표시")
        except Exception as e:
            logger.warning(f"미할당 입고현황 계산 오류: {str(e)}")
        
        logger.info(f"card6 - 총재고: {card6_total_value:,}원, 적치율: {card6_storage_rate}%")
        
        # ==========================================
        # JSON 응답 구조 (v10 규격)
        # ==========================================
        
        return jsonify({
            'success': True,
            'date': today,
            
            # card1: 입고현황
            'card1': {
                'totalCount': card1_total,
                'progressRate': round(card1_progress, 1),
                'inboundRiskyCount': card1_risky_count,
                'riskyItems': card1_risky_items
            },
            
            # card2: 자사출고
            'card2': {
                'amount': card2_amount,
                'compare': round(card2_compare, 1),
                'totalLabel': card2_total_label,
                'unprintedLabel': card2_unprinted_label
            },
            
            # card3: 지방출고
            'card3': {
                'amount': card3_amount,
                'compare': round(card3_compare, 1),
                'unprintedPicking': card3_unprinted_picking,
                'destinations': card3_destinations,
                'urgentAlert': card3_urgent_alert,
                'urgentDestinations': card3_urgent_destinations,
                'urgentCount': card3_urgent_count,
                'baselineCount': card3_baseline_count,
                'alertTimeSlot': card3_alert_time_slot
            },
            
            # card4: 스케줄 (날짜순 정렬, 최대 5개)
            'card4': {
                'schedules': card4_schedules
            },
            
            # card5: 피킹유의 / 미할당 입고현황 (18:30 기준 전환)
            # 테스트 파라미터: ?test_unallocated=N (N개 더미 데이터 생성)
            'card5': (lambda: {
                'isAfter1830': is_after_1830 or test_unallocated_count > 0,
                'totalCount': card5_total,
                'urgentCount': card5_urgent,
                'warningCount': card5_warning,
                'riskyItems': card5_items,
                'unallocatedItems': (
                    # 테스트 모드: 긴 상품명 위주 (레이아웃 테스트용) - 실제 재고 데이터 기반
                    (lambda n: [
                        {'product_name': '[Careplus] 청양풍매운간장맛소스 행복한맛남', 'unit': 'EA', 'unallocated_qty': 782, 'inbound_info': '제주(800)|18:15, 음성(200)|19:00, 안산(150)|19:30'},
                        {'product_name': '쿠킹크림(유지방 20%, 파스타 소스용) 나르만', 'unit': 'EA', 'unallocated_qty': 235, 'inbound_info': '음성(150)|18:22'},
                        {'product_name': '[Careplus] 토마토스파게티소스 행복한맛남', 'unit': 'EA', 'unallocated_qty': 25, 'inbound_info': '양산(30)|18:35, 제천(20)|19:10, 호남(40)|19:45, 구미(25)|20:00'},
                        {'product_name': '삼각유부 (배합초,후레이크없음) 자연촌(냉장)', 'unit': 'EA', 'unallocated_qty': 12, 'inbound_info': '제천(20)|18:42, 계룡(15)|19:20'},
                        {'product_name': '[Careplus] 미트스파게티소스 행복한맛남', 'unit': 'EA', 'unallocated_qty': 97, 'inbound_info': '호남(50)|18:50'},
                        {'product_name': '[재고]프레지덩 휘핑크림(유지방35%) 동서', 'unit': 'EA', 'unallocated_qty': 49, 'inbound_info': '구미(60)|19:05, 용인(40)|19:30, 양산(35)|20:00'},
                        {'product_name': '[Careplus]딸기요거트드레싱 행복한맛남', 'unit': 'EA', 'unallocated_qty': 83, 'inbound_info': '계룡(100)|19:12, 안산(80)|19:45'},
                        {'product_name': '[고쿠텐]커리토핑소스BOX(2kg*5pk)', 'unit': 'EA', 'unallocated_qty': 202, 'inbound_info': '용인(100)|19:20'},
                        {'product_name': '[미태리]유니그라 마티니 푸드 서비스 크림', 'unit': 'EA', 'unallocated_qty': 48, 'inbound_info': '안산(50)|19:28, 음성(30)|19:50, 제주(45)|20:15, 제천(25)|20:40'},
                        {'product_name': '[Careplus]블루베리드레싱 행복한맛남', 'unit': 'EA', 'unallocated_qty': 24, 'inbound_info': '음성(30)|19:35, 호남(20)|20:00'},
                        {'product_name': '[Careplus] 불고기양념장 행복한맛남', 'unit': 'EA', 'unallocated_qty': 105, 'inbound_info': '양산(120)|19:42, 구미(90)|20:10, 계룡(70)|20:35'},
                        {'product_name': '[특판_리치푸드]쫀득쫀득 쫄면사리(냉장)', 'unit': 'EA', 'unallocated_qty': 7, 'inbound_info': '제주(10)|19:50'},
                        {'product_name': '동치미물냉면소스(6배희석육수) 행복한맛남', 'unit': 'EA', 'unallocated_qty': 20, 'inbound_info': '제천(25)|20:05, 용인(30)|20:30'},
                        {'product_name': '[Careplus]발사믹드레싱 행복한맛남', 'unit': 'EA', 'unallocated_qty': 5, 'inbound_info': '호남(10)|20:12, 안산(15)|20:35, 양산(20)|21:00, 음성(25)|21:20'},
                        {'product_name': '[Careplus] 돈까스소스 행복한맛남', 'unit': 'EA', 'unallocated_qty': 154, 'inbound_info': '구미(200)|20:20'},
                        {'product_name': '아페띠블루베리맛젤리(35인분) 행복한맛남', 'unit': 'EA', 'unallocated_qty': 15, 'inbound_info': '계룡(20)|20:28, 제주(30)|20:50, 제천(15)|21:10'},
                        {'product_name': '(핏제리아오) 초리조 이베리코 슬라이스', 'unit': 'EA', 'unallocated_qty': 23, 'inbound_info': '용인(30)|20:35, 호남(25)|21:00'},
                        {'product_name': '멸균우유(3.2%,TWOJ) 믈레코비타', 'unit': 'EA', 'unallocated_qty': 109, 'inbound_info': '안산(120)|20:42'},
                        {'product_name': '[Careplus] 허니머스타드드레싱 행복한맛남', 'unit': 'EA', 'unallocated_qty': 49, 'inbound_info': '음성(30)|20:50, 계룡(25)|21:05, 구미(40)|21:25, 양산(35)|21:45'},
                        {'product_name': '[Careplus] 시저샐러드드레싱 행복한맛남', 'unit': 'EA', 'unallocated_qty': 75, 'inbound_info': '양산(80)|21:00, 제주(60)|21:20'},
                        {'product_name': '도토리묵(1kg) 행복한맛남(용기포장)', 'unit': 'EA', 'unallocated_qty': 32, 'inbound_info': '제주(40)|21:08, 제천(35)|21:30, 용인(45)|21:50'},
                        {'product_name': '아페띠 청포도젤리(35인분) 행복한맛남', 'unit': 'EA', 'unallocated_qty': 88, 'inbound_info': '음성(100)|21:15'},
                        {'product_name': '[미태리]앵커체다슬라이스치즈(80매)', 'unit': 'EA', 'unallocated_qty': 45, 'inbound_info': '양산(50)|21:22, 안산(40)|21:45, 호남(30)|22:05, 구미(25)|22:20'},
                        {'product_name': '(동대문매운김밥) 동대문간장닭강정소스', 'unit': 'EA', 'unallocated_qty': 67, 'inbound_info': '제천(80)|21:28, 계룡(60)|21:50'},
                        {'product_name': '(압구정샌드)더건강한브런치슬라이스햄①', 'unit': 'EA', 'unallocated_qty': 120, 'inbound_info': '호남(150)|21:35'},
                        {'product_name': '메추리알장조림(약270개) 행복한맛남', 'unit': 'EA', 'unallocated_qty': 18, 'inbound_info': '구미(25)|21:42, 용인(30)|22:00, 제주(20)|22:15'},
                        {'product_name': 'NB-아워홈 김치세끼 볶은김치 80g', 'unit': 'EA', 'unallocated_qty': 200, 'inbound_info': '계룡(250)|21:48, 안산(180)|22:10'},
                        {'product_name': '(면세)무&비트피클_5kg 행복한맛남', 'unit': 'EA', 'unallocated_qty': 35, 'inbound_info': '용인(40)|21:55, 음성(35)|22:15, 양산(45)|22:30, 제천(30)|22:45'},
                        {'product_name': '청포묵(3kg) 행복한맛남(용기포장)', 'unit': 'EA', 'unallocated_qty': 92, 'inbound_info': '안산(100)|22:02'},
                        {'product_name': '아페띠망고맛젤리(35인분) 행복한맛남', 'unit': 'EA', 'unallocated_qty': 55, 'inbound_info': '양산(60)|22:10, 호남(50)|22:30, 구미(40)|22:45'},
                    ][:n])(test_unallocated_count)
                    if test_unallocated_count > 0
                    else (card6_unallocated if is_after_1830 else [])
                )
            })(),
            
            # card6: 재고현황 (4섹션 - 섹션5는 card5로 이동)
            'card6': {
                'inventoryCheckStatus': inventory_check_status,
                'inventoryCheckCount': inventory_check_count,
                'inboundAvgRate': round(inbound_avg_rate, 1),
                'outboundStatus': outbound_status,
                'inboundStatus': inbound_status,
                'inventory': {
                    'total_value': card6_total_value,
                    'product_count': card6_product_count
                },
                'storageRate': {
                    'rate': card6_storage_rate,
                    'upper_used': card6_upper_used,
                    'upper_total': card6_upper_total
                },
                'fifo': card6_fifo,
                'partial': card6_partial,
                'deleteAnsan': card6_delete_ansan,
                'deleteEumseong': card6_delete_eumseong
            },
            
            'data_counts': {
                'inbound': len(inbound_data),
                'outbound': len(outbound_data),
                'inventory': len(inventory_data),
                'irregular': len(irregular_data),
                'delete': len(delete_data)
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except FileNotFoundError as e:
        logger.error(f'Dashboard API - 파일 없음: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'파일을 찾을 수 없습니다: {str(e)}'
        }), 404
    
    except ValueError as e:
        logger.error(f'Dashboard API - 데이터 검증 실패: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'데이터 검증 실패: {str(e)}'
        }), 400
    
    except KeyError as e:
        logger.error(f'Dashboard API - 필수 컬럼 없음: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'필수 컬럼이 없습니다: {str(e)}'
        }), 400
    
    except Exception as e:
        logger.error(f'Dashboard API - 서버 에러: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'error': f'서버 에러: {str(e)}'
        }), 500
