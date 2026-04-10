# -*- coding: utf-8 -*-
"""
재고조사 엑셀 자동 생성 모듈 (xlwings 안전 버전)
- 초록불 조건 충족 시 신선&임박상품 통합 엑셀 파일 생성
- xlwings로 샘플과 100% 동일한 결과물 생성
- SafeExcelApp 컨텍스트 매니저로 프로세스 안전 관리
- 작성일: 2025-12-07
- 버전: v5.0 (유효비 50%, 상단로케이션 조건 삭제)
- 수정일: 2026-01-13
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
COLOR_SEPARATOR_BG = 191 + 191*256 + 191*65536  # 회색 (구분 행)

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
        
        cleanup_zombie_excel_processes()
        
        try:
            self.app = xw.App(visible=False)
            self.pid = self.app.pid
            
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
                try:
                    for wb in self.app.books:
                        try:
                            wb.close()
                        except:
                            pass
                except:
                    pass
                
                try:
                    self.app.quit()
                    logger.info(f"[Excel] App 정상 종료 - PID: {self.pid}")
                except Exception as e:
                    logger.warning(f"[Excel] App 종료 중 오류: {e}")
                    force_kill_excel_pid(self.pid)
        finally:
            with _lock:
                _active_excel_app = None
                _active_excel_pid = None
            
            self.app = None
            self.pid = None
        
        return False


# ========================================
# 좀비 프로세스 정리 함수
# ========================================
def cleanup_zombie_excel_processes():
    """시작 전 기존 좀비 Excel 프로세스 탐지 및 정리"""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq EXCEL.EXE', '/FO', 'CSV', '/NH'],
            capture_output=True, text=True, timeout=10
        )
        if 'EXCEL.EXE' in result.stdout:
            lines = result.stdout.strip().split('\n')
            count = len([l for l in lines if 'EXCEL.EXE' in l])
            if count > 0:
                logger.warning(f"[Excel] 기존 Excel 프로세스 {count}개 발견 - 정리 권장")
    except Exception as e:
        logger.debug(f"[Excel] 프로세스 확인 중 오류: {e}")


def force_kill_excel_pid(pid):
    """특정 PID의 Excel 프로세스 강제 종료"""
    if pid is None:
        return
    try:
        subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True, timeout=10)
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


atexit.register(emergency_cleanup)


# ========================================
# 락 파일 메커니즘 (동시 실행 방지)
# ========================================
def acquire_lock():
    """락 파일 생성 (동시 실행 방지)"""
    try:
        if LOCK_FILE.exists():
            mtime = LOCK_FILE.stat().st_mtime
            age = datetime.now().timestamp() - mtime
            if age > 300:
                logger.warning(f"[Lock] 오래된 락 파일 제거 ({age:.0f}초)")
                LOCK_FILE.unlink()
            else:
                logger.warning(f"[Lock] 이미 생성 중 - 스킵")
                return False
        LOCK_FILE.write_text(datetime.now().isoformat())
        logger.info("[Lock] 락 파일 생성")
        return True
    except Exception as e:
        logger.error(f"[Lock] 락 처리 오류: {e}")
        return True


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


def load_fresh_codes():
    """신선식품.csv 로드 → 상품코드 set"""
    file_path = Path(FILTER_DIR) / "신선식품.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"신선식품 필터 파일 없음: {file_path}")
    df = pd.read_csv(file_path, encoding='utf-8-sig', header=None, names=['상품'])
    return set(df['상품'].astype(str).tolist())


# ========================================
# 필터 및 그룹핑 함수
# ========================================
def filter_fresh_products(inventory_df, fresh_codes):
    """신선식품 필터링: 상품코드 기준"""
    filtered = inventory_df[inventory_df['상품'].astype(str).isin(fresh_codes)].copy()
    return filtered


def filter_imminent_products(inventory_df, fresh_codes):
    """
    임박상품 필터링 (v3.0)
    조건:
      - 유효유통비(%) ≤ 50
      - 상품코드 ∉ 신선식품
      - 가용수량 > 0
    """
    df = inventory_df.copy()
    df['상품'] = df['상품'].astype(str)
    df['로케이션'] = df['로케이션'].astype(str).str.strip()
    df['유효유통비(%)'] = pd.to_numeric(df['유효유통비(%)'], errors='coerce').fillna(100)
    
    mask = (
        (df['유효유통비(%)'] <= 30) &
        (~df['상품'].isin(fresh_codes)) &
        (df['가용수량'] > 0)
    )
    return df[mask].copy()


def group_products(df):
    """상품 그룹핑 및 합산 (신선/임박 공통)"""
    grouped = df.groupby(
        ['로케이션', '상품', '상품명', '소비기한'],
        as_index=False
    ).agg({'가용수량': 'sum'})
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


def apply_separator_style(cell):
    """구분 행 스타일 적용"""
    cell.api.Font.Name = "맑은 고딕"
    cell.api.Font.Size = 10
    cell.api.Font.Bold = True
    cell.api.Interior.Color = COLOR_SEPARATOR_BG
    cell.api.HorizontalAlignment = XL_CENTER
    cell.api.VerticalAlignment = XL_CENTER
    apply_border(cell)


def setup_normal_style(wb):
    """워크북 기본 스타일을 샘플과 동일하게 설정 (굴림체 9pt)"""
    normal_style = wb.api.Styles("Normal")
    normal_style.Font.Name = "굴림체"
    normal_style.Font.Size = 9


def setup_print_settings(ws, last_row):
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
    ps.PrintArea = f"$A$1:$H${last_row}"


# ========================================
# 통합 워크북 생성 (신선 + 구분행 + 임박)
# ========================================
def create_combined_workbook(app, fresh_df, imminent_df, output_path):
    """
    신선&임박상품 통합 엑셀 워크북 생성
    구조: 헤더(2행) → 신선식품(No.1~N) → 구분행 → 임박상품(No.1~M)
    """
    wb = None
    try:
        wb = app.books.add()
        setup_normal_style(wb)
        
        ws = wb.sheets[0]
        ws.name = "냉장"
        
        # 열 너비 설정 (8열)
        col_widths = {
            'A': 5.67, 'B': 14.83, 'C': 18.00, 'D': 46.17,
            'E': 14.33, 'F': 12.00, 'G': 12.00, 'H': 63.33
        }
        for col, width in col_widths.items():
            ws.range(f'{col}1').api.ColumnWidth = width
        
        # 헤더 행 높이
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
        
        current_row = 3  # 데이터 시작 행
        
        # ---- 신선식품 데이터 입력 ----
        fresh_count = len(fresh_df)
        for idx, row_data in enumerate(fresh_df.itertuples(), start=1):
            row_num = current_row
            current_row += 1
            ws.range(f'{row_num}:{row_num}').api.RowHeight = 21.75
            
            # No. 열 (1부터 시작)
            cell_a = ws.range(f'A{row_num}')
            if idx == 1:
                cell_a.value = 1
            else:
                cell_a.formula = f'=A{row_num-1}+1'
            apply_data_style(cell_a, num_format='G/표준')
            
            # 로케이션
            cell_b = ws.range(f'B{row_num}')
            cell_b.value = row_data.로케이션
            apply_data_style(cell_b, num_format='0_);[빨강](0)')
            
            # 상품
            cell_c = ws.range(f'C{row_num}')
            cell_c.value = str(row_data.상품)
            apply_data_style(cell_c, num_format='G/표준')
            
            # 상품명
            cell_d = ws.range(f'D{row_num}')
            cell_d.value = row_data.상품명
            apply_data_style(cell_d, num_format='#,##0;-#,##0')
            
            # 소비기한
            cell_e = ws.range(f'E{row_num}')
            try:
                exp_str = str(int(row_data.소비기한))
                exp_date = datetime.strptime(exp_str, "%Y%m%d")
                cell_e.value = exp_date
            except:
                cell_e.value = str(row_data.소비기한)
            apply_data_style(cell_e, num_format='yyyy-mm-dd')
            
            # 가용수량
            cell_f = ws.range(f'F{row_num}')
            cell_f.value = row_data.가용수량
            apply_data_style(cell_f, is_bold=True, bg_color=COLOR_DATA_BLUE, num_format='#,##0;-#,##0')
            
            # 차이 (빈 칸)
            cell_g = ws.range(f'G{row_num}')
            cell_g.value = ''
            apply_data_style(cell_g, is_bold=True, num_format='@')
            
            # 비고 (빈 칸)
            cell_h = ws.range(f'H{row_num}')
            cell_h.value = ''
            apply_data_style(cell_h, num_format='@')
        
        # ---- 구분 행 입력 ----
        separator_row = current_row
        current_row += 1
        ws.range(f'{separator_row}:{separator_row}').api.RowHeight = 21.75
        
        # A~H 병합
        ws.range(f'A{separator_row}:H{separator_row}').api.Merge()
        
        # 스타일 및 텍스트
        cell_sep = ws.range(f'A{separator_row}')
        cell_sep.value = "유효비 30% 이하"
        apply_separator_style(cell_sep)
        
        # ---- 임박상품 데이터 입력 ----
        imminent_count = len(imminent_df)
        for idx, row_data in enumerate(imminent_df.itertuples(), start=1):
            row_num = current_row
            current_row += 1
            ws.range(f'{row_num}:{row_num}').api.RowHeight = 21.75
            
            # No. 열 (1부터 리셋)
            cell_a = ws.range(f'A{row_num}')
            if idx == 1:
                cell_a.value = 1
            else:
                cell_a.formula = f'=A{row_num-1}+1'
            apply_data_style(cell_a, num_format='G/표준')
            
            # 로케이션
            cell_b = ws.range(f'B{row_num}')
            cell_b.value = row_data.로케이션
            apply_data_style(cell_b, num_format='0_);[빨강](0)')
            
            # 상품
            cell_c = ws.range(f'C{row_num}')
            cell_c.value = str(row_data.상품)
            apply_data_style(cell_c, num_format='G/표준')
            
            # 상품명
            cell_d = ws.range(f'D{row_num}')
            cell_d.value = row_data.상품명
            apply_data_style(cell_d, num_format='#,##0;-#,##0')
            
            # 소비기한
            cell_e = ws.range(f'E{row_num}')
            try:
                exp_str = str(int(row_data.소비기한))
                exp_date = datetime.strptime(exp_str, "%Y%m%d")
                cell_e.value = exp_date
            except:
                cell_e.value = str(row_data.소비기한)
            apply_data_style(cell_e, num_format='yyyy-mm-dd')
            
            # 가용수량
            cell_f = ws.range(f'F{row_num}')
            cell_f.value = row_data.가용수량
            apply_data_style(cell_f, is_bold=True, bg_color=COLOR_DATA_BLUE, num_format='#,##0;-#,##0')
            
            # 차이 (빈 칸)
            cell_g = ws.range(f'G{row_num}')
            cell_g.value = ''
            apply_data_style(cell_g, is_bold=True, num_format='@')
            
            # 비고 (빈 칸)
            cell_h = ws.range(f'H{row_num}')
            cell_h.value = ''
            apply_data_style(cell_h, num_format='@')
        
        # 인쇄 설정
        last_row = current_row - 1
        setup_print_settings(ws, last_row)
        
        # 저장
        wb.save(output_path)
        logger.info(f"[Excel] 통합 파일 저장 완료: {output_path}")
        logger.info(f"        신선식품 {fresh_count}건 + 임박상품 {imminent_count}건")
        
        # 인쇄 (1부)
        try:
            ws.api.PrintOut(Copies=1)
            logger.info(f"[Excel] 인쇄 전송 완료")
        except Exception as e:
            logger.warning(f"[Excel] 인쇄 실패 (파일은 저장됨): {e}")
        
    finally:
        if wb is not None:
            try:
                wb.close()
            except:
                pass
    
    return output_path


# ========================================
# 메인 실행 함수 (v4.0 - 통합 버전)
# ========================================
def generate_inventory_excel(date_str=None):
    """
    재고조사 엑셀 파일 생성 메인 함수 (통합 버전)
    - 신선&임박상품 1개 파일 생성
    - SafeExcelApp으로 단일 App 관리
    - 락 파일로 동시 실행 방지
    
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
        logger.info(f"[1/4] 재고현황 CSV 로드 중... ({date_str})")
        inventory_df = load_inventory_csv(date_str)
        logger.info(f"      → {len(inventory_df)}행 로드 완료")
        
        # 3. 필터 파일 로드
        logger.info("[2/4] 필터 파일 로드 중...")
        fresh_codes = load_fresh_codes()
        logger.info(f"      → 신선식품 {len(fresh_codes)}개")
        
        # 4. 데이터 준비
        logger.info("[3/4] 데이터 필터링 및 그룹핑...")
        
        # 신선식품
        fresh_data = filter_fresh_products(inventory_df, fresh_codes)
        fresh_grouped = group_products(fresh_data)
        fresh_before = len(fresh_grouped)
        fresh_grouped = fresh_grouped[fresh_grouped['가용수량'] > 0]
        logger.info(f"      → 신선식품: {fresh_before}행 → {len(fresh_grouped)}행")
        fresh_sorted = fresh_grouped.sort_values(['로케이션', '상품', '소비기한'])
        
        # 임박상품
        imminent_data = filter_imminent_products(inventory_df, fresh_codes)
        imminent_grouped = group_products(imminent_data)
        imminent_before = len(imminent_grouped)
        imminent_grouped = imminent_grouped[imminent_grouped['가용수량'] > 0]
        logger.info(f"      → 임박상품: {imminent_before}행 → {len(imminent_grouped)}행")
        imminent_sorted = imminent_grouped.sort_values(['로케이션', '상품', '소비기한'])
        
        # 5. SafeExcelApp으로 엑셀 생성
        logger.info("[4/4] Excel 통합 파일 생성 중...")
        
        with SafeExcelApp() as app:
            combined_filename = f"{file_date} 냉장 재고조사(신선&임박상품).xlsx"
            combined_path = Path(OUTPUT_DIR) / combined_filename
            create_combined_workbook(app, fresh_sorted, imminent_sorted, str(combined_path))
            result['files'].append(str(combined_path))
        
        # 6. 완료
        logger.info("[완료] 재고조사 엑셀 통합 파일 생성 완료!")
        result['success'] = True
        result['message'] = f"재고조사 엑셀 생성 완료: 신선 {len(fresh_sorted)}건 + 임박 {len(imminent_sorted)}건"
        
    except FileNotFoundError as e:
        result['message'] = f"파일 없음: {e}"
        logger.error(f"[오류] {result['message']}")
    except Exception as e:
        result['message'] = f"생성 실패: {e}"
        logger.error(f"[오류] {result['message']}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        release_lock()
    
    return result


# ========================================
# 독립 실행
# ========================================
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 50)
    print("재고조사 엑셀 자동 생성 (v4.0 통합 버전)")
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
