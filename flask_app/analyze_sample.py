# -*- coding: utf-8 -*-
"""샘플 파일 심층 분석 스크립트"""
import xlwings as xw

def rgb_from_color(color_int):
    """엑셀 색상값을 RGB로 변환"""
    if color_int is None or color_int == -4142:  # xlNone
        return "없음(투명)"
    r = color_int % 256
    g = (color_int // 256) % 256
    b = (color_int // 65536) % 256
    return f"RGB({r},{g},{b})"

def analyze_fresh():
    """신선식품 샘플 분석"""
    app = xw.apps.active
    for wb in app.books:
        if '신선식품' in wb.name:
            ws = wb.sheets['냉장']
            print('=' * 60)
            print('신선식품 샘플 완벽 분석')
            print('=' * 60)
            print(f'파일명: {wb.name}')
            print(f'시트명: {ws.name}')
            
            # 1. 열 너비
            print('\n[1] 열 너비')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H']:
                cw = ws.range(f'{col}1').api.ColumnWidth
                px = ws.range(f'{col}1').api.Width * 96 / 72
                print(f'  {col}열: ColumnWidth={cw:.2f}, 픽셀={px:.0f}px')
            
            # 2. 행 높이
            print('\n[2] 행 높이')
            print('-' * 40)
            for row in [1,2,3,4,5]:
                rh = ws.range(f'A{row}').api.RowHeight
                px = rh * 96 / 72
                print(f'  행{row}: RowHeight={rh:.2f}pt, 픽셀={px:.0f}px')
            
            # 3. 병합셀
            print('\n[3] 병합셀')
            print('-' * 40)
            checked = set()
            for row in range(1, 3):
                for col in range(1, 9):
                    cell = ws.range((row, col))
                    if cell.api.MergeCells:
                        addr = cell.api.MergeArea.Address.replace('$','')
                        if addr not in checked:
                            checked.add(addr)
                            val = ws.range(addr.split(':')[0]).value
                            print(f'  {addr}: "{val}"')
            
            # 4. 헤더 1행 스타일
            print('\n[4] 헤더 1행 스타일')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H']:
                cell = ws.range(f'{col}1')
                f = cell.api.Font
                i = cell.api.Interior
                fc = f.Color if hasattr(f, 'Color') else 0
                print(f'  {col}1: 폰트={f.Name}, 크기={f.Size}pt, Bold={f.Bold}')
                print(f'       배경={rgb_from_color(i.Color)}, 글자색={rgb_from_color(fc)}')
            
            # 5. 헤더 2행 스타일
            print('\n[5] 헤더 2행 스타일')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H']:
                cell = ws.range(f'{col}2')
                f = cell.api.Font
                i = cell.api.Interior
                print(f'  {col}2: 값="{cell.value}", 폰트크기={f.Size}pt, Bold={f.Bold}')
                print(f'       배경={rgb_from_color(i.Color)}')
            
            # 6. 데이터행 스타일 (3행)
            print('\n[6] 데이터 3행 스타일')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H']:
                cell = ws.range(f'{col}3')
                f = cell.api.Font
                i = cell.api.Interior
                nf = cell.api.NumberFormat
                print(f'  {col}3: 폰트크기={f.Size}pt, Bold={f.Bold}, 배경={rgb_from_color(i.Color)}, 서식={nf}')
            
            # 7. 정렬
            print('\n[7] 정렬 (3행 기준)')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H']:
                cell = ws.range(f'{col}3')
                ha = cell.api.HorizontalAlignment
                va = cell.api.VerticalAlignment
                # -4108=xlCenter, -4131=xlLeft, -4152=xlRight
                ha_str = {-4108:'가운데', -4131:'왼쪽', -4152:'오른쪽', -4160:'채우기'}.get(ha, ha)
                va_str = {-4108:'가운데', -4160:'위', -4107:'아래'}.get(va, va)
                print(f'  {col}3: 가로={ha_str}, 세로={va_str}')
            
            # 8. 테두리
            print('\n[8] 테두리 (A1 기준)')
            print('-' * 40)
            cell = ws.range('A1')
            borders = cell.api.Borders
            for idx, name in [(7,'왼쪽'), (8,'위'), (9,'아래'), (10,'오른쪽')]:
                b = borders(idx)
                style = b.LineStyle
                weight = b.Weight if style != -4142 else 'N/A'
                print(f'  {name}: LineStyle={style}, Weight={weight}')
            
            # 9. 인쇄 설정
            print('\n[9] 인쇄 설정')
            print('-' * 40)
            ps = ws.api.PageSetup
            print(f'  방향: {"가로" if ps.Orientation == 2 else "세로"}')
            print(f'  용지크기: {ps.PaperSize}')
            print(f'  여백(상): {ps.TopMargin / 72:.4f}인치')
            print(f'  여백(하): {ps.BottomMargin / 72:.4f}인치')
            print(f'  여백(좌): {ps.LeftMargin / 72:.4f}인치')
            print(f'  여백(우): {ps.RightMargin / 72:.4f}인치')
            print(f'  반복행: {ps.PrintTitleRows}')
            print(f'  머리글 오른쪽: {ps.RightHeader}')
            print(f'  바닥글 오른쪽: {ps.RightFooter}')
            
            return
    print('신선식품 파일을 찾을 수 없습니다.')

if __name__ == '__main__':
    analyze_fresh()
