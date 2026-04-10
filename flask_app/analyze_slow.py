# -*- coding: utf-8 -*-
"""부진재고 샘플 분석"""
import xlwings as xw

def rgb_from_color(color_int):
    if color_int is None or color_int == -4142:
        return "없음"
    r = color_int % 256
    g = (color_int // 256) % 256
    b = (color_int // 65536) % 256
    return f"RGB({r},{g},{b})"

def analyze_slow():
    app = xw.apps.active
    for wb in app.books:
        if '부진재고' in wb.name:
            ws = wb.sheets['냉장']
            print('=' * 60)
            print('부진재고 샘플 완벽 분석')
            print('=' * 60)
            print(f'파일명: {wb.name}')
            
            # 1. 열 너비 (A~L, 12열)
            print('\n[1] 열 너비')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H','I','J','K','L']:
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
                for col in range(1, 13):
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
            for col in ['A','B','C','D','E','F','G','H','I','J','K','L']:
                cell = ws.range(f'{col}1')
                f = cell.api.Font
                i = cell.api.Interior
                print(f'  {col}1: 크기={f.Size}pt, Bold={f.Bold}, 배경={rgb_from_color(i.Color)}')
            
            # 5. 헤더 2행 스타일
            print('\n[5] 헤더 2행 스타일')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H','I','J','K','L']:
                cell = ws.range(f'{col}2')
                f = cell.api.Font
                i = cell.api.Interior
                print(f'  {col}2: 값="{cell.value}", 크기={f.Size}pt, Bold={f.Bold}')
            
            # 6. 데이터 3행 스타일
            print('\n[6] 데이터 3행 스타일')
            print('-' * 40)
            for col in ['A','B','C','D','E','F','G','H','I','J','K','L']:
                cell = ws.range(f'{col}3')
                f = cell.api.Font
                i = cell.api.Interior
                nf = cell.api.NumberFormat
                print(f'  {col}3: Bold={f.Bold}, 배경={rgb_from_color(i.Color)}, 서식={nf}')
            
            # 7. 인쇄 설정
            print('\n[7] 인쇄 설정')
            print('-' * 40)
            ps = ws.api.PageSetup
            print(f'  방향: {"가로" if ps.Orientation == 2 else "세로"}')
            print(f'  용지크기: {ps.PaperSize}')
            print(f'  반복행: {ps.PrintTitleRows}')
            print(f'  머리글 오른쪽: {ps.RightHeader}')
            print(f'  바닥글 오른쪽: {ps.RightFooter}')
            
            return
    print('부진재고 파일을 찾을 수 없습니다.')

if __name__ == '__main__':
    analyze_slow()
