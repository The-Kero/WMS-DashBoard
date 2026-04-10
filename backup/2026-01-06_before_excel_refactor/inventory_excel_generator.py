# -*- coding: utf-8 -*-
"""
재고조사 엑셀 자동 생성 모듈 (xlwings 안전 버전)
- 초록불 조건 충족 시 부진재고/신선식품 엑셀 파일 생성
- xlwings로 샘플과 100% 동일한 결과물 생성
- SafeExcelApp 컨텍스트 매니저로 프로세스 안전 관리
- 작성일: 2025-12-07
- 버전: v3.0 (안전성 강화)
- 수정일: 2025-12-09
"""

import pandas as pd
import xlwings as xw
from datetime import datetime
from pathlib import Path
import os
import atexit
import logging
import threading
import subprocess

# ========================================
# 로깅 설정
# ========================================
logger = logging.getLogger(__name__)

# ========================================
# 설정값
# ========================================
INVENTORY_CSV_DIR = r"C:\OSIS_AUTO\inventory_status"
FILTER_DIR = r"C:\Users\JWPark\Desktop\냉장 재고조사"
OUTPUT_DIR = r"C:\Users\JWPark\Desktop\냉장 재고조사"
LOCK_FILE = Path(OUTPUT_DIR) / ".generating.lock"

# ========================================
# 색상 상수 (RGB → 엑셀 색상값)
# ========================================
COLOR_HEADER_BG = 51 + 63*256 + 79*65536
COLOR_DATA_BLUE = 221 + 235*256 + 247*65536
COLOR_WHITE = 255 + 255*256 + 255*65536

# ========================================
# 정렬 상수
# ========================================
XL_CENTER = -4108
XL_LEFT = -4131

# ========================================
# 전역 변수 (비상 정리용)
# ========================================
_active_excel_app = None
_active_excel_pid = None
_lock = threading.Lock()


# ========================================
# SafeExcelApp 컨텍스트 매니저
# ========================================
class SafeExcelApp:
    """
    안전한 Excel App 관리자
    - 단일 App으로 여러 워크북 처리
    - 3중 안전망: try/finally + atexit + 수동 정리
    - PID 추적 및 로깅
    """
    
    def __init__(self):
        self.app = None
        self.pid = None
    
    def __enter__(self):
        global _active_excel_app, _active_excel_pid
        
        # 1. 기존 좀비 프로세스 정리
        cleanup_zombie_excel_processes()
        
        # 2. Excel App 생성
        try:
            self.app = xw.App(visible=False)
            self.pid = self.app.pid
            
            # 전역 참조 저장 (비상 정리용)
            with _lock:
                _active_excel_app = self.app
                _active_excel_pid = self.pid
            
            logger.info(f"[Excel] App 생성 완료 - PID: {self.pid}")
            return self.app
            
        except Exception as e:
            logger.error(f"[Excel] App 생성 실패: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        global _active_excel_app, _active_excel_pid
        
        try:
            if self.app is not None:
                # 열린 워크북 모두 닫기 (저장 안 함)
                try:
                    for wb in self.app.books:
                        try:
                            wb.close()
                        except:
                            pass
                except:
                    pass
                
                # App 종료
                try:
                    self.app.quit()
                    logger.info(f"[Excel] App 정상 종료 - PID: {self.pid}")
                except Exception as e:
                    logger.warning(f"[Excel] App 종료 중 오류: {e}")
                    # 강제 종료 시도
                    force_kill_excel_pid(self.pid)
        finally:
            # 전역 참조 제거
            with _lock:
                _active_excel_app = None
                _active_excel_pid = None
            
            self.app = None
            self.pid = None
        
        # 예외 전파 (False 반환)
        return False


# ========================================
# 좀비 프로세스 정리 함수
# ========================================
def cleanup_zombie_excel_processes():
    """시작 전 기존 좀비 Excel 프로세스 탐지 및 정리"""
    try:
        # 현재 실행 중인 EXCEL.EXE 프로세스 확인
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq EXCEL.EXE', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if 'EXCEL.EXE' in result.stdout:
            lines = result.stdout.strip().split('\n')
            count = len([l for l in lines if 'EXCEL.EXE' in l])
            if count > 0:
                logger.warning(f"[Excel] 기존 Excel 프로세스 {count}개 발견 - 정리 권장")
                # 자동 정리는 위험할 수 있으므로 경고만 출력
    except Exception as e:
        logger.debug(f"[Excel] 프로세스 확인 중 오류: {e}")


def force_kill_excel_pid(pid):
    """특정 PID의 Excel 프로세스 강제 종료"""
    if pid is None:
        return
    
    try:
        subprocess.run(
            ['taskkill', '/F', '/PID', str(pid)],
            capture_output=True,
            timeout=10
        )
        logger.info(f"[Excel] PID {pid} 강제 종료 완료")
    except Exception as e:
        logger.warning(f"[Excel] PID {pid} 강제 종료 실패: {e}")


def emergency_cleanup():
    """비상 정리 함수 (atexit에서 호출)"""
    global _active_excel_app, _active_excel_pid
    
    with _lock:
        if _active_excel_pid is not None:
            logger.warning(f"[Excel] 비상 정리 실행 - PID: {_active_excel_pid}")
            force_kill_excel_pid(_active_excel_pid)
            _active_excel_app = None
            _active_excel_pid = None


# atexit 핸들러 등록
atexit.register(emergency_cleanup)


# ========================================
# 락 파일 메커니즘 (동시 실행 방지)
# ========================================
def acquire_lock():
    """락 파일 생성 (동시 실행 방지)"""
    try:
        if LOCK_FILE.exists():
            # 락 파일이 있으면 생성 시간 확인
            mtime = LOCK_FILE.stat().st_mtime
            age = datetime.now().timestamp() - mtime
            
            if age > 300:  # 5분 이상 된 락은 무효
                logger.warning(f"[Lock] 오래된 락 파일 제거 ({age:.0f}초)")
                LOCK_FILE.unlink()
            else:
                logger.warning(f"[Lock] 이미 생성 중 - 스킵")
                return False
        
        # 락 파일 생성
        LOCK_FILE.write_text(datetime.now().isoformat())
        logger.info("[Lock] 락 파일 생성")
        return True
        
    except Exception as e:
        logger.error(f"[Lock] 락 처리 오류: {e}")
        return True  # 오류 시에도 진행 허용


def release_lock():
    """락 파일 제거"""
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
            logger.info("[Lock] 락 파일 제거")
    except Exception as e:
        logger.warning(f"[Lock] 락 제거 오류: {e}")


# ========================================
# 데이터 로드 함수
# ========================================
def load_inventory_csv(date_str=None):
    """재고현황 CSV 로드"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
    
    file_path = Path(INVENTORY_CSV_DIR) / f"inventory_status_{date_str}.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"재고현황 파일 없음: {file_path}")
    
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    return df


def load_filter_csv(filter_type):
    """필터 CSV 로드 (신선식품 또는 부진재고) - 헤더 없음"""
    if filter_type == "fresh":
        file_path = Path(FILTER_DIR) / "신선식품.csv"
        col_name = "상품"
    elif filter_type == "slow":
        file_path = Path(FILTER_DIR) / "부진재고.csv"
        col_name = "로케이션"
    else:
        raise ValueError(f"알 수 없는 필터 타입: {filter_type}")
    
    if not file_path.exists():
        raise FileNotFoundError(f"필터 파일 없음: {file_path}")
    
    df = pd.read_csv(file_path, encoding='utf-8-sig', header=None, names=[col_name])
    return df


# ========================================
# 필터 및 그룹핑 함수
# ========================================
def filter_fresh_products(inventory_df, fresh_filter_df):
    """신선식품 필터링: 상품코드 기준"""
    fresh_codes = fresh_filter_df['상품'].astype(str).tolist()
    filtered = inventory_df[inventory_df['상품'].astype(str).isin(fresh_codes)].copy()
    return filtered


def filter_slow_moving(inventory_df, slow_filter_df, fresh_filter_df):
    """부진재고 필터링: 로케이션 기준 + 신선식품 제외"""
    slow_locations = slow_filter_df['로케이션'].astype(str).tolist()
    fresh_codes = fresh_filter_df['상품'].astype(str).tolist()
    
    filtered = inventory_df[inventory_df['로케이션'].astype(str).isin(slow_locations)].copy()
    filtered = filtered[~filtered['상품'].astype(str).isin(fresh_codes)]
    return filtered


def group_fresh_products(df):
    """신선식품 그룹핑 및 합산"""
    grouped = df.groupby(
        ['로케이션', '상품', '상품명', '소비기한'],
        as_index=False
    ).agg({'가용수량': 'sum'})
    return grouped


def group_slow_moving(df):
    """부진재고 그룹핑 및 합산"""
    grouped = df.groupby(
        ['로케이션', '상품', '상품명', '단위및규격', '소비기한', '입수량'],
        as_index=False
    ).agg({
        '가용수량': 'sum',
        '가용박스수량': 'sum',
        '가용잔량': 'sum'
    })
    return grouped


# ========================================
# xlwings 헬퍼 함수
# ========================================
def apply_border(rng):
    """테두리 적용 (얇은 실선)"""
    for i in range(7, 11):
        rng.api.Borders(i).LineStyle = 1
        rng.api.Borders(i).Weight = 2


def apply_header_style(cell, font_size=10, is_bold=True):
    """헤더 셀 스타일 적용"""
    cell.api.Font.Name = "맑은 고딕"
    cell.api.Font.Size = font_size
    cell.api.Font.Bold = is_bold
    cell.api.Font.Color = COLOR_WHITE
    cell.api.Interior.Color = COLOR_HEADER_BG
    cell.api.HorizontalAlignment = XL_CENTER
    cell.api.VerticalAlignment = XL_CENTER
    apply_border(cell)


def apply_data_style(cell, is_bold=False, bg_color=None, num_format=None):
    """데이터 셀 스타일 적용"""
    cell.api.Font.Name = "맑은 고딕"
    cell.api.Font.Size = 9
    cell.api.Font.Bold = is_bold
    cell.api.HorizontalAlignment = XL_CENTER
    cell.api.VerticalAlignment = XL_CENTER
    if bg_color:
        cell.api.Interior.Color = bg_color
    if num_format:
        cell.api.NumberFormat = num_format
    apply_border(cell)


def setup_normal_style(wb):
    """워크북 기본 스타일을 샘플과 동일하게 설정 (굴림체 9pt)"""
    normal_style = wb.api.Styles("Normal")
    normal_style.Font.Name = "굴림체"
    normal_style.Font.Size = 9


def setup_print_settings(ws):
    """인쇄 설정 적용"""
    ps = ws.api.PageSetup
    ps.Orientation = 2
    ps.PaperSize = 9
    ps.TopMargin = 0.5905511811023623 * 72
    ps.BottomMargin = 0.5905511811023623 * 72
    ps.LeftMargin = 0.7874015748031497 * 72
    ps.RightMargin = 0.3937007874015748 * 72
    ps.PrintTitleRows = "$1:$2"
    ps.RightHeader = '&"HY견고딕,표준"&16재고조사일 : &D, &T'
    ps.RightFooter = '&"HY견고딕,표준"&16&P  /  &N'
    ps.FitToPagesWide = 1
    ps.FitToPagesTall = False
    ps.Zoom = False



# ========================================
# 신선식품 워크북 생성 (App 외부에서 전달)
# ========================================
def create_fresh_workbook(app, df, output_path):
    """
    신선식품 엑셀 워크북 생성
    - App은 외부에서 전달받음 (단일 App 패턴)
    - 워크북 생성/저장/닫기만 담당
    """
    wb = None
    try:
        wb = app.books.add()
        setup_normal_style(wb)
        
        ws = wb.sheets[0]
        ws.name = "냉장"
        
        # 열 너비 설정
        col_widths = {
            'A': 5.67, 'B': 14.83, 'C': 18.00, 'D': 46.17,
            'E': 14.33, 'F': 12.00, 'G': 12.00, 'H': 63.33
        }
        for col, width in col_widths.items():
            ws.range(f'{col}1').api.ColumnWidth = width
        
        # 행 높이 설정
        ws.range('1:1').api.RowHeight = 20.25
        ws.range('2:2').api.RowHeight = 20.25
        
        # 헤더 스타일 적용
        for row in [1, 2]:
            for col in ['A','B','C','D','E','F','G','H']:
                cell = ws.range(f'{col}{row}')
                font_size = 10 if row == 1 else 9
                apply_header_style(cell, font_size=font_size)
        
        # 특수 폰트 크기
        ws.range('G1').api.Font.Size = 9
        ws.range('H2').api.Font.Size = 10
        
        # 헤더 값 입력
        ws.range('A1').value = 'No.'
        ws.range('B1').value = '제품정보'
        ws.range('E1').value = '전산재고'
        ws.range('G1').value = '차이'
        ws.range('H1').value = '비고'
        
        ws.range('B2').value = '로케이션'
        ws.range('C2').value = '상품'
        ws.range('D2').value = '상품명'
        ws.range('E2').value = '소비기한'
        ws.range('F2').value = '가용수량'
        ws.range('H2').value = '(특이사항 기재)'
        
        # 셀 병합
        ws.range('A1:A2').api.Merge()
        ws.range('B1:D1').api.Merge()
        ws.range('E1:F1').api.Merge()
        ws.range('G1:G2').api.Merge()
        
        # 데이터 입력
        for idx, row_data in enumerate(df.itertuples(), start=1):
            row_num = idx + 2
            ws.range(f'{row_num}:{row_num}').api.RowHeight = 21.75
            
            cell_a = ws.range(f'A{row_num}')
            if idx == 1:
                cell_a.value = 1
            else:
                cell_a.formula = f'=A{row_num-1}+1'
            apply_data_style(cell_a, num_format='G/표준')
            
            cell_b = ws.range(f'B{row_num}')
            cell_b.value = row_data.로케이션
            apply_data_style(cell_b, num_format='0_);[빨강](0)')
            
            cell_c = ws.range(f'C{row_num}')
            cell_c.value = str(row_data.상품)
            apply_data_style(cell_c, num_format='G/표준')
            
            cell_d = ws.range(f'D{row_num}')
            cell_d.value = row_data.상품명
            apply_data_style(cell_d, num_format='#,##0;-#,##0')
            
            cell_e = ws.range(f'E{row_num}')
            try:
                exp_str = str(int(row_data.소비기한))
                exp_date = datetime.strptime(exp_str, "%Y%m%d")
                cell_e.value = exp_date
            except:
                cell_e.value = str(row_data.소비기한)
            apply_data_style(cell_e, num_format='yyyy-mm-dd')
            
            cell_f = ws.range(f'F{row_num}')
            cell_f.value = row_data.가용수량
            apply_data_style(cell_f, is_bold=True, bg_color=COLOR_DATA_BLUE, num_format='#,##0;-#,##0')
            
            cell_g = ws.range(f'G{row_num}')
            cell_g.value = ''
            apply_data_style(cell_g, is_bold=True, num_format='@')
            
            cell_h = ws.range(f'H{row_num}')
            cell_h.value = ''
            apply_data_style(cell_h, num_format='@')
        
        # 인쇄 설정
        setup_print_settings(ws)
        last_row = len(df) + 2
        ws.api.PageSetup.PrintArea = f"$A$1:$H${last_row}"
        
        # 저장
        wb.save(output_path)
        logger.info(f"[Excel] 신선식품 저장 완료: {output_path}")
        
    finally:
        # 워크북만 닫기 (App은 외부에서 관리)
        if wb is not None:
            try:
                wb.close()
            except:
                pass
    
    return output_path


# ========================================
# 부진재고 워크북 생성 (App 외부에서 전달)
# ========================================
def create_slow_workbook(app, df, output_path):
    """
    부진재고 엑셀 워크북 생성
    - App은 외부에서 전달받음 (단일 App 패턴)
    - 워크북 생성/저장/닫기만 담당
    """
    wb = None
    try:
        wb = app.books.add()
        setup_normal_style(wb)
        
        ws = wb.sheets[0]
        ws.name = "냉장"
        
        # 열 너비 설정
        col_widths = {
            'A': 5.67, 'B': 14.83, 'C': 18.00, 'D': 46.17, 'E': 17.50,
            'F': 14.33, 'G': 7.67, 'H': 12.00, 'I': 12.00, 'J': 12.00,
            'K': 12.00, 'L': 25.83
        }
        for col, width in col_widths.items():
            ws.range(f'{col}1').api.ColumnWidth = width
        
        # 행 높이 설정
        ws.range('1:1').api.RowHeight = 20.25
        ws.range('2:2').api.RowHeight = 20.25
        
        # 헤더 스타일 적용
        cols = ['A','B','C','D','E','F','G','H','I','J','K','L']
        for row in [1, 2]:
            for col in cols:
                cell = ws.range(f'{col}{row}')
                font_size = 10 if row == 1 else 9
                apply_header_style(cell, font_size=font_size)
        
        # 특수 폰트 크기
        ws.range('K1').api.Font.Size = 9
        ws.range('L2').api.Font.Size = 10
        
        # 헤더 값 입력
        ws.range('A1').value = 'No.'
        ws.range('B1').value = '제품정보'
        ws.range('F1').value = '전산재고'
        ws.range('K1').value = '차이'
        ws.range('L1').value = '비고'
        
        ws.range('B2').value = '로케이션'
        ws.range('C2').value = '상품'
        ws.range('D2').value = '상품명'
        ws.range('E2').value = '단위및규격'
        ws.range('F2').value = '소비기한'
        ws.range('G2').value = '입수량'
        ws.range('H2').value = '가용수량'
        ws.range('I2').value = 'BOX'
        ws.range('J2').value = '낱개'
        ws.range('L2').value = '(특이사항 기재)'
        
        # 셀 병합
        ws.range('A1:A2').api.Merge()
        ws.range('B1:E1').api.Merge()
        ws.range('F1:J1').api.Merge()
        ws.range('K1:K2').api.Merge()
        
        # 데이터 입력
        for idx, row_data in enumerate(df.itertuples(), start=1):
            row_num = idx + 2
            ws.range(f'{row_num}:{row_num}').api.RowHeight = 22.50
            
            cell_a = ws.range(f'A{row_num}')
            if idx == 1:
                cell_a.value = 1
            else:
                cell_a.formula = f'=A{row_num-1}+1'
            apply_data_style(cell_a, num_format='G/표준')
            
            cell_b = ws.range(f'B{row_num}')
            cell_b.value = row_data.로케이션
            apply_data_style(cell_b, num_format='0_);[빨강](0)')
            
            cell_c = ws.range(f'C{row_num}')
            cell_c.value = str(row_data.상품)
            apply_data_style(cell_c, num_format='G/표준')
            
            cell_d = ws.range(f'D{row_num}')
            cell_d.value = row_data.상품명
            apply_data_style(cell_d, num_format='#,##0;-#,##0')
            
            cell_e = ws.range(f'E{row_num}')
            cell_e.value = row_data.단위및규격
            apply_data_style(cell_e, num_format='G/표준')
            
            cell_f = ws.range(f'F{row_num}')
            try:
                exp_str = str(int(row_data.소비기한))
                exp_date = datetime.strptime(exp_str, "%Y%m%d")
                cell_f.value = exp_date
            except:
                cell_f.value = str(row_data.소비기한)
            apply_data_style(cell_f, num_format='yyyy-mm-dd')
            
            cell_g = ws.range(f'G{row_num}')
            cell_g.value = row_data.입수량
            apply_data_style(cell_g, num_format='#,##0;-#,##0')
            
            cell_h = ws.range(f'H{row_num}')
            cell_h.value = row_data.가용수량
            apply_data_style(cell_h, is_bold=True, bg_color=COLOR_DATA_BLUE, num_format='#,##0;-#,##0')
            
            cell_i = ws.range(f'I{row_num}')
            cell_i.value = row_data.가용박스수량
            apply_data_style(cell_i, is_bold=True, num_format='G/표준')
            
            cell_j = ws.range(f'J{row_num}')
            cell_j.value = row_data.가용잔량
            apply_data_style(cell_j, is_bold=True, num_format='G/표준')
            
            cell_k = ws.range(f'K{row_num}')
            cell_k.value = ''
            apply_data_style(cell_k, is_bold=True, num_format='@')
            
            cell_l = ws.range(f'L{row_num}')
            cell_l.value = ''
            apply_data_style(cell_l, num_format='@')
        
        # 인쇄 설정
        setup_print_settings(ws)
        last_row = len(df) + 2
        ws.api.PageSetup.PrintArea = f"$A$1:$L${last_row}"
        
        # 저장
        wb.save(output_path)
        logger.info(f"[Excel] 부진재고 저장 완료: {output_path}")
        
    finally:
        # 워크북만 닫기 (App은 외부에서 관리)
        if wb is not None:
            try:
                wb.close()
            except:
                pass
    
    return output_path



# ========================================
# 메인 실행 함수 (안전 버전)
# ========================================
def generate_inventory_excel(date_str=None):
    """
    재고조사 엑셀 파일 생성 메인 함수 (안전 버전)
    - SafeExcelApp으로 단일 App 관리
    - 락 파일로 동시 실행 방지
    - 3중 안전망 적용
    
    Returns:
        dict: {'success': bool, 'files': list, 'message': str}
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
    
    file_date = date_str[2:]  # 20251207 → 251207
    
    result = {
        'success': False,
        'files': [],
        'message': ''
    }
    
    # 1. 락 획득
    if not acquire_lock():
        result['message'] = "이미 생성 중입니다. 잠시 후 다시 시도하세요."
        return result
    
    try:
        # 2. 데이터 로드
        logger.info(f"[1/5] 재고현황 CSV 로드 중... ({date_str})")
        inventory_df = load_inventory_csv(date_str)
        logger.info(f"      → {len(inventory_df)}행 로드 완료")
        
        # 3. 필터 파일 로드
        logger.info("[2/5] 필터 파일 로드 중...")
        fresh_filter = load_filter_csv("fresh")
        slow_filter = load_filter_csv("slow")
        logger.info(f"      → 신선식품 {len(fresh_filter)}개, 부진재고 {len(slow_filter)}개")
        
        # 4. 데이터 준비
        fresh_data = filter_fresh_products(inventory_df, fresh_filter)
        fresh_grouped = group_fresh_products(fresh_data)
        fresh_before = len(fresh_grouped)
        fresh_grouped = fresh_grouped[fresh_grouped['가용수량'] > 0]
        logger.info(f"      → 신선식품: {fresh_before}행 → {len(fresh_grouped)}행 (가용수량 0 제외: {fresh_before - len(fresh_grouped)}건)")
        fresh_sorted = fresh_grouped.sort_values(['로케이션', '상품', '소비기한'])
        
        slow_data = filter_slow_moving(inventory_df, slow_filter, fresh_filter)
        slow_grouped = group_slow_moving(slow_data)
        slow_before = len(slow_grouped)
        slow_grouped = slow_grouped[slow_grouped['가용수량'] > 0]
        logger.info(f"      → 부진재고: {slow_before}행 → {len(slow_grouped)}행 (가용수량 0 제외: {slow_before - len(slow_grouped)}건)")
        slow_sorted = slow_grouped.sort_values(['로케이션', '상품', '소비기한'])
        
        # 5. SafeExcelApp으로 엑셀 생성 (단일 App)
        logger.info("[3/5] Excel App 시작 (SafeExcelApp)...")
        
        with SafeExcelApp() as app:
            # 신선식품 생성
            logger.info("[4/5] 신선식품 엑셀 생성 중...")
            fresh_filename = f"{file_date} 냉장 재고조사(신선식품).xlsx"
            fresh_path = Path(OUTPUT_DIR) / fresh_filename
            create_fresh_workbook(app, fresh_sorted, str(fresh_path))
            result['files'].append(str(fresh_path))
            logger.info(f"      → {fresh_filename} 생성 완료 ({len(fresh_sorted)}행)")
            
            # 부진재고 생성
            logger.info("[5/5] 부진재고 엑셀 생성 중...")
            slow_filename = f"{file_date} 냉장 재고조사(부진재고).xlsx"
            slow_path = Path(OUTPUT_DIR) / slow_filename
            create_slow_workbook(app, slow_sorted, str(slow_path))
            result['files'].append(str(slow_path))
            logger.info(f"      → {slow_filename} 생성 완료 ({len(slow_sorted)}행)")
        
        # 6. 완료
        logger.info("[완료] 재고조사 엑셀 2개 파일 생성 완료!")
        result['success'] = True
        result['message'] = f"재고조사 엑셀 2개 파일 생성 완료 (SafeExcelApp)"
        
    except FileNotFoundError as e:
        result['message'] = f"파일 없음: {e}"
        logger.error(f"[오류] {result['message']}")
    except Exception as e:
        result['message'] = f"생성 실패: {e}"
        logger.error(f"[오류] {result['message']}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # 락 해제 (항상 실행)
        release_lock()
    
    return result


# ========================================
# 하위 호환성 함수 (기존 코드와 호환)
# ========================================
def create_fresh_products_excel(df, output_path):
    """하위 호환용 - 개별 App으로 신선식품 생성"""
    logger.warning("[경고] create_fresh_products_excel() 직접 호출 - SafeExcelApp 권장")
    with SafeExcelApp() as app:
        return create_fresh_workbook(app, df, output_path)


def create_slow_moving_excel(df, output_path):
    """하위 호환용 - 개별 App으로 부진재고 생성"""
    logger.warning("[경고] create_slow_moving_excel() 직접 호출 - SafeExcelApp 권장")
    with SafeExcelApp() as app:
        return create_slow_workbook(app, df, output_path)


# ========================================
# 독립 실행
# ========================================
if __name__ == '__main__':
    # 로깅 설정 (독립 실행 시)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 50)
    print("재고조사 엑셀 자동 생성 (SafeExcelApp 버전)")
    print("=" * 50)
    
    result = generate_inventory_excel()
    
    print()
    print("=" * 50)
    print("결과:")
    print(f"  성공 여부: {result['success']}")
    print(f"  메시지: {result['message']}")
    if result['files']:
        print("  생성된 파일:")
        for f in result['files']:
            print(f"    - {f}")
    print("=" * 50)
