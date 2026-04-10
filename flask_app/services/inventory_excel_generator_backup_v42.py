# -*- coding: utf-8 -*-
"""
재고조사 엑셀 자동 생성 모듈 (xlwings 버전)
- 초록불 조건 충족 시 부진재고/신선식품 엑셀 파일 생성
- xlwings로 샘플과 100% 동일한 결과물 생성
- 작성일: 2025-12-07
- 버전: v2.0 (xlwings 재작성)
"""

import pandas as pd
import xlwings as xw
from datetime import datetime
from pathlib import Path
import os

# ========================================
# 설정값
# ========================================
INVENTORY_CSV_DIR = r"C:\OSIS_AUTO\inventory_status"
FILTER_DIR = r"C:\Users\JWPark\Desktop\냉장 재고조사"
OUTPUT_DIR = r"C:\Users\JWPark\Desktop\냉장 재고조사"

# ========================================
# 색상 상수 (RGB → 엑셀 색상값)
# 계산식: r + g*256 + b*65536
# ========================================
COLOR_HEADER_BG = 51 + 63*256 + 79*65536      # RGB(51,63,79) = 5193523 어두운 올리브
COLOR_DATA_BLUE = 221 + 235*256 + 247*65536   # RGB(221,235,247) = 16247261 연한 파랑
COLOR_WHITE = 255 + 255*256 + 255*65536       # RGB(255,255,255) = 16777215 흰색

# ========================================
# 정렬 상수
# ========================================
XL_CENTER = -4108
XL_LEFT = -4131

# ========================================
# 데이터 로드 함수 (변경 없음)
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
# 필터 및 그룹핑 함수 (변경 없음)
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
    for i in range(7, 11):  # 7=왼쪽, 8=위, 9=아래, 10=오른쪽
        rng.api.Borders(i).LineStyle = 1  # xlContinuous
        rng.api.Borders(i).Weight = 2     # xlThin

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
    ps.Orientation = 2  # xlLandscape (가로)
    ps.PaperSize = 9    # A4
    ps.TopMargin = 0.5905511811023623 * 72  # 인치 → 포인트
    ps.BottomMargin = 0.5905511811023623 * 72
    ps.LeftMargin = 0.7874015748031497 * 72
    ps.RightMargin = 0.3937007874015748 * 72
    ps.PrintTitleRows = "$1:$2"
    ps.RightHeader = '&"HY견고딕,표준"&16재고조사일 : &D, &T'
    ps.RightFooter = '&"HY견고딕,표준"&16&P  /  &N'
    # [추가] 샘플과 동일한 설정
    ps.FitToPagesWide = 1      # 너비 1페이지에 맞춤
    ps.FitToPagesTall = False  # 높이는 자동 (여러 페이지 가능)
    ps.Zoom = False            # 배율 자동


# ========================================
# 신선식품 엑셀 생성 (8열) - xlwings
# ========================================
def create_fresh_products_excel(df, output_path):
    """신선식품 엑셀 파일 생성 - xlwings 버전"""
    app = xw.App(visible=False)
    try:
        wb = app.books.add()
        
        # [핵심] Normal 스타일을 샘플과 동일하게 설정 (굴림체 9pt)
        setup_normal_style(wb)
        
        ws = wb.sheets[0]
        ws.name = "냉장"
        
        # 1. 열 너비 설정 (샘플에서 측정한 정확한 ColumnWidth 값)
        col_widths = {
            'A': 5.67, 'B': 14.83, 'C': 18.00, 'D': 46.17,
            'E': 14.33, 'F': 12.00, 'G': 12.00, 'H': 63.33
        }
        for col, width in col_widths.items():
            ws.range(f'{col}1').api.ColumnWidth = width
        
        # 2. 행 높이 설정
        ws.range('1:1').api.RowHeight = 20.25  # 헤더 1행
        ws.range('2:2').api.RowHeight = 20.25  # 헤더 2행
        
        # 3. 헤더 1행, 2행 전체 스타일 적용
        for row in [1, 2]:
            for col_idx, col in enumerate(['A','B','C','D','E','F','G','H'], 1):
                cell = ws.range(f'{col}{row}')
                font_size = 10 if row == 1 else 9
                apply_header_style(cell, font_size=font_size)
        
        # 4. 특수 폰트 크기 조정
        ws.range('G1').api.Font.Size = 9   # 차이 헤더 9pt
        ws.range('H2').api.Font.Size = 10  # 비고 부제목 10pt
        
        # 5. 헤더 값 입력
        ws.range('A1').value = 'No.'
        ws.range('B1').value = '제품정보'
        ws.range('E1').value = '전산재고'
        ws.range('G1').value = '차이'
        ws.range('H1').value = '비고'
        
        # 6. 헤더 2행 값
        ws.range('B2').value = '로케이션'
        ws.range('C2').value = '상품'
        ws.range('D2').value = '상품명'
        ws.range('E2').value = '소비기한'
        ws.range('F2').value = '가용수량'
        ws.range('H2').value = '(특이사항 기재)'
        
        # 7. 셀 병합 (스타일 적용 후)
        ws.range('A1:A2').api.Merge()
        ws.range('B1:D1').api.Merge()
        ws.range('E1:F1').api.Merge()
        ws.range('G1:G2').api.Merge()
        
        # 8. 데이터 입력 (3행부터)
        for idx, row_data in enumerate(df.itertuples(), start=1):
            row_num = idx + 2
            
            # 행 높이
            ws.range(f'{row_num}:{row_num}').api.RowHeight = 21.75
            
            # A열: No. (첫 행은 1, 나머지는 수식)
            cell_a = ws.range(f'A{row_num}')
            if idx == 1:
                cell_a.value = 1
            else:
                cell_a.formula = f'=A{row_num-1}+1'
            apply_data_style(cell_a, num_format='G/표준')
            
            # B열: 로케이션
            cell_b = ws.range(f'B{row_num}')
            cell_b.value = row_data.로케이션
            apply_data_style(cell_b, num_format='0_);[빨강](0)')
            
            # C열: 상품 (문자열)
            cell_c = ws.range(f'C{row_num}')
            cell_c.value = str(row_data.상품)
            apply_data_style(cell_c, num_format='G/표준')
            
            # D열: 상품명
            cell_d = ws.range(f'D{row_num}')
            cell_d.value = row_data.상품명
            apply_data_style(cell_d, num_format='#,##0;-#,##0')
            
            # E열: 소비기한 (datetime 변환)
            cell_e = ws.range(f'E{row_num}')
            try:
                exp_str = str(int(row_data.소비기한))
                exp_date = datetime.strptime(exp_str, "%Y%m%d")
                cell_e.value = exp_date
            except:
                cell_e.value = str(row_data.소비기한)
            apply_data_style(cell_e, num_format='yyyy-mm-dd')
            
            # F열: 가용수량 (bold + 연한 파랑 배경)
            cell_f = ws.range(f'F{row_num}')
            cell_f.value = row_data.가용수량
            apply_data_style(cell_f, is_bold=True, bg_color=COLOR_DATA_BLUE, num_format='#,##0;-#,##0')
            
            # G열: 차이 (bold)
            cell_g = ws.range(f'G{row_num}')
            cell_g.value = ''
            apply_data_style(cell_g, is_bold=True, num_format='@')
            
            # H열: 비고
            cell_h = ws.range(f'H{row_num}')
            cell_h.value = ''
            apply_data_style(cell_h, num_format='@')
        
        # 9. 인쇄 설정
        setup_print_settings(ws)
        
        # 10. 인쇄영역 설정 (신선식품: A~H열)
        last_row = len(df) + 2  # 헤더 2행 + 데이터 행
        ws.api.PageSetup.PrintArea = f"$A$1:$H${last_row}"
        
        # 11. 저장 및 종료
        wb.save(output_path)
        wb.close()
        
    finally:
        app.quit()
    
    return output_path


# ========================================
# 부진재고 엑셀 생성 (12열) - xlwings
# ========================================
def create_slow_moving_excel(df, output_path):
    """부진재고 엑셀 파일 생성 - xlwings 버전"""
    app = xw.App(visible=False)
    try:
        wb = app.books.add()
        
        # [핵심] Normal 스타일을 샘플과 동일하게 설정 (굴림체 9pt)
        setup_normal_style(wb)
        
        ws = wb.sheets[0]
        ws.name = "냉장"
        
        # 1. 열 너비 설정 (샘플에서 측정한 정확한 ColumnWidth 값)
        col_widths = {
            'A': 5.67, 'B': 14.83, 'C': 18.00, 'D': 46.17, 'E': 17.50,
            'F': 14.33, 'G': 7.67, 'H': 12.00, 'I': 12.00, 'J': 12.00,
            'K': 12.00, 'L': 25.83
        }
        for col, width in col_widths.items():
            ws.range(f'{col}1').api.ColumnWidth = width
        
        # 2. 행 높이 설정
        ws.range('1:1').api.RowHeight = 20.25
        ws.range('2:2').api.RowHeight = 20.25
        
        # 3. 헤더 스타일 적용
        cols = ['A','B','C','D','E','F','G','H','I','J','K','L']
        for row in [1, 2]:
            for col in cols:
                cell = ws.range(f'{col}{row}')
                font_size = 10 if row == 1 else 9
                apply_header_style(cell, font_size=font_size)
        
        # 4. 특수 폰트 크기
        ws.range('K1').api.Font.Size = 9   # 차이 헤더 9pt
        ws.range('L2').api.Font.Size = 10  # 비고 부제목 10pt
        
        # 5. 헤더 값 입력
        ws.range('A1').value = 'No.'
        ws.range('B1').value = '제품정보'
        ws.range('F1').value = '전산재고'
        ws.range('K1').value = '차이'
        ws.range('L1').value = '비고'
        
        # 6. 헤더 2행 값
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
        
        # 7. 셀 병합
        ws.range('A1:A2').api.Merge()
        ws.range('B1:E1').api.Merge()
        ws.range('F1:J1').api.Merge()
        ws.range('K1:K2').api.Merge()
        
        # 8. 데이터 입력 (3행부터)
        for idx, row_data in enumerate(df.itertuples(), start=1):
            row_num = idx + 2
            
            # 행 높이 (부진재고는 22.50pt)
            ws.range(f'{row_num}:{row_num}').api.RowHeight = 22.50
            
            # A열: No.
            cell_a = ws.range(f'A{row_num}')
            if idx == 1:
                cell_a.value = 1
            else:
                cell_a.formula = f'=A{row_num-1}+1'
            apply_data_style(cell_a, num_format='G/표준')
            
            # B열: 로케이션
            cell_b = ws.range(f'B{row_num}')
            cell_b.value = row_data.로케이션
            apply_data_style(cell_b, num_format='0_);[빨강](0)')
            
            # C열: 상품
            cell_c = ws.range(f'C{row_num}')
            cell_c.value = str(row_data.상품)
            apply_data_style(cell_c, num_format='G/표준')
            
            # D열: 상품명
            cell_d = ws.range(f'D{row_num}')
            cell_d.value = row_data.상품명
            apply_data_style(cell_d, num_format='#,##0;-#,##0')
            
            # E열: 단위및규격
            cell_e = ws.range(f'E{row_num}')
            cell_e.value = row_data.단위및규격
            apply_data_style(cell_e, num_format='G/표준')
            
            # F열: 소비기한
            cell_f = ws.range(f'F{row_num}')
            try:
                exp_str = str(int(row_data.소비기한))
                exp_date = datetime.strptime(exp_str, "%Y%m%d")
                cell_f.value = exp_date
            except:
                cell_f.value = str(row_data.소비기한)
            apply_data_style(cell_f, num_format='yyyy-mm-dd')
            
            # G열: 입수량
            cell_g = ws.range(f'G{row_num}')
            cell_g.value = row_data.입수량
            apply_data_style(cell_g, num_format='#,##0;-#,##0')
            
            # H열: 가용수량 (bold + 연한 파랑)
            cell_h = ws.range(f'H{row_num}')
            cell_h.value = row_data.가용수량
            apply_data_style(cell_h, is_bold=True, bg_color=COLOR_DATA_BLUE, num_format='#,##0;-#,##0')
            
            # I열: BOX (bold)
            cell_i = ws.range(f'I{row_num}')
            cell_i.value = row_data.가용박스수량
            apply_data_style(cell_i, is_bold=True, num_format='G/표준')
            
            # J열: 낱개 (bold)
            cell_j = ws.range(f'J{row_num}')
            cell_j.value = row_data.가용잔량
            apply_data_style(cell_j, is_bold=True, num_format='G/표준')
            
            # K열: 차이 (bold)
            cell_k = ws.range(f'K{row_num}')
            cell_k.value = ''
            apply_data_style(cell_k, is_bold=True, num_format='@')
            
            # L열: 비고
            cell_l = ws.range(f'L{row_num}')
            cell_l.value = ''
            apply_data_style(cell_l, num_format='@')
        
        # 9. 인쇄 설정
        setup_print_settings(ws)
        
        # 10. 인쇄영역 설정 (부진재고: A~L열)
        last_row = len(df) + 2  # 헤더 2행 + 데이터 행
        ws.api.PageSetup.PrintArea = f"$A$1:$L${last_row}"
        
        # 11. 저장 및 종료
        wb.save(output_path)
        wb.close()
        
    finally:
        app.quit()
    
    return output_path


# ========================================
# 메인 실행 함수
# ========================================
def generate_inventory_excel(date_str=None):
    """
    재고조사 엑셀 파일 생성 메인 함수
    - 부진재고, 신선식품 2개 파일 생성
    - 반환: {'success': bool, 'files': list, 'message': str}
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
    
    # 파일명 형식: YYMMDD
    file_date = date_str[2:]  # 20251207 → 251207
    
    result = {
        'success': False,
        'files': [],
        'message': ''
    }
    
    try:
        # 1. 데이터 로드
        print(f"[1/5] 재고현황 CSV 로드 중... ({date_str})")
        inventory_df = load_inventory_csv(date_str)
        print(f"      → {len(inventory_df)}행 로드 완료")
        
        # 2. 필터 파일 로드
        print("[2/5] 필터 파일 로드 중...")
        fresh_filter = load_filter_csv("fresh")
        slow_filter = load_filter_csv("slow")
        print(f"      → 신선식품 {len(fresh_filter)}개, 부진재고 {len(slow_filter)}개")
        
        # 3. 신선식품 처리
        print("[3/5] 신선식품 엑셀 생성 중... (xlwings)")
        fresh_data = filter_fresh_products(inventory_df, fresh_filter)
        fresh_grouped = group_fresh_products(fresh_data)
        fresh_sorted = fresh_grouped.sort_values(['로케이션', '상품', '소비기한'])
        
        fresh_filename = f"{file_date} 냉장 재고조사(신선식품).xlsx"
        fresh_path = Path(OUTPUT_DIR) / fresh_filename
        create_fresh_products_excel(fresh_sorted, str(fresh_path))
        result['files'].append(str(fresh_path))
        print(f"      → {fresh_filename} 생성 완료 ({len(fresh_sorted)}행)")
        
        # 4. 부진재고 처리
        print("[4/5] 부진재고 엑셀 생성 중... (xlwings)")
        slow_data = filter_slow_moving(inventory_df, slow_filter, fresh_filter)
        slow_grouped = group_slow_moving(slow_data)
        slow_sorted = slow_grouped.sort_values(['로케이션', '상품', '소비기한'])
        
        slow_filename = f"{file_date} 냉장 재고조사(부진재고).xlsx"
        slow_path = Path(OUTPUT_DIR) / slow_filename
        create_slow_moving_excel(slow_sorted, str(slow_path))
        result['files'].append(str(slow_path))
        print(f"      → {slow_filename} 생성 완료 ({len(slow_sorted)}행)")
        
        # 5. 완료
        print("[5/5] 완료!")
        result['success'] = True
        result['message'] = f"재고조사 엑셀 2개 파일 생성 완료 (xlwings)"
        
    except FileNotFoundError as e:
        result['message'] = f"파일 없음: {e}"
        print(f"[오류] {result['message']}")
    except Exception as e:
        result['message'] = f"생성 실패: {e}"
        print(f"[오류] {result['message']}")
        import traceback
        traceback.print_exc()
    
    return result


# ========================================
# 독립 실행
# ========================================
if __name__ == '__main__':
    print("=" * 50)
    print("재고조사 엑셀 자동 생성 (xlwings 버전)")
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
