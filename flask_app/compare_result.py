# -*- coding: utf-8 -*-
"""생성된 파일과 샘플 파일 비교"""
import xlwings as xw

def rgb_from_color(color_int):
    if color_int is None or color_int == -4142:
        return "없음"
    r = int(color_int % 256)
    g = int((color_int // 256) % 256)
    b = int((color_int // 65536) % 256)
    return f"RGB({r},{g},{b})"

def compare_files():
    app = xw.apps.active
    
    sample = None
    generated = None
    
    for wb in app.books:
        if '251205' in wb.name and '신선식품' in wb.name:
            sample = wb.sheets['냉장']
            print(f"Sample: {wb.name}")
        elif '251207' in wb.name and '신선식품' in wb.name:
            generated = wb.sheets['냉장']
            print(f"Generated: {wb.name}")
    
    if not sample or not generated:
        print("Need both files open!")
        return
    
    print("\n" + "="*60)
    print("Column Width Comparison")
    print("="*60)
    diff_count = 0
    for col in ['A','B','C','D','E','F','G','H']:
        s_cw = sample.range(f'{col}1').api.ColumnWidth
        g_cw = generated.range(f'{col}1').api.ColumnWidth
        match = "[OK]" if abs(s_cw - g_cw) < 0.01 else "[DIFF]"
        if match == "[DIFF]":
            diff_count += 1
        print(f"{col}: Sample={s_cw:.2f}, Gen={g_cw:.2f} {match}")
    
    print("\n" + "="*60)
    print("Row Height Comparison")
    print("="*60)
    for row in [1,2,3]:
        s_rh = sample.range(f'A{row}').api.RowHeight
        g_rh = generated.range(f'A{row}').api.RowHeight
        match = "[OK]" if abs(s_rh - g_rh) < 0.01 else "[DIFF]"
        if match == "[DIFF]":
            diff_count += 1
        print(f"Row{row}: Sample={s_rh:.2f}pt, Gen={g_rh:.2f}pt {match}")
    
    print("\n" + "="*60)
    print("Header Background Color (A1)")
    print("="*60)
    s_bg = sample.range('A1').api.Interior.Color
    g_bg = generated.range('A1').api.Interior.Color
    match = "[OK]" if s_bg == g_bg else "[DIFF]"
    if match == "[DIFF]":
        diff_count += 1
    print(f"Sample: {rgb_from_color(s_bg)}")
    print(f"Gen:    {rgb_from_color(g_bg)} {match}")
    
    print("\n" + "="*60)
    print("F3 (Quantity) Background Color")
    print("="*60)
    s_f3 = sample.range('F3').api.Interior.Color
    g_f3 = generated.range('F3').api.Interior.Color
    match = "[OK]" if s_f3 == g_f3 else "[DIFF]"
    if match == "[DIFF]":
        diff_count += 1
    print(f"Sample: {rgb_from_color(s_f3)}")
    print(f"Gen:    {rgb_from_color(g_f3)} {match}")
    
    print("\n" + "="*60)
    print("Font Size Comparison")
    print("="*60)
    cells_to_check = ['A1','B2','G1','H2','A3','F3']
    for addr in cells_to_check:
        s_fs = sample.range(addr).api.Font.Size
        g_fs = generated.range(addr).api.Font.Size
        s_bold = sample.range(addr).api.Font.Bold
        g_bold = generated.range(addr).api.Font.Bold
        match = "[OK]" if s_fs == g_fs and s_bold == g_bold else "[DIFF]"
        if match == "[DIFF]":
            diff_count += 1
        print(f"{addr}: Sample={s_fs}pt/Bold={s_bold}, Gen={g_fs}pt/Bold={g_bold} {match}")
    
    print("\n" + "="*60)
    print("Number Format Comparison")
    print("="*60)
    format_cells = ['A3','B3','C3','D3','E3','F3','G3','H3']
    for addr in format_cells:
        s_nf = sample.range(addr).api.NumberFormat
        g_nf = generated.range(addr).api.NumberFormat
        match = "[OK]" if s_nf == g_nf else "[DIFF]"
        if match == "[DIFF]":
            diff_count += 1
        print(f"{addr}: Sample='{s_nf}', Gen='{g_nf}' {match}")
    
    print("\n" + "="*60)
    print(f"TOTAL DIFFERENCES: {diff_count}")
    print("="*60)

if __name__ == '__main__':
    compare_files()
