# -*- coding: utf-8 -*-
"""부진재고 픽셀 비교"""
import xlwings as xw

def compare_slow():
    app = xw.apps.active
    
    sample = None
    generated = None
    
    for wb in app.books:
        if '251205' in wb.name and '부진재고' in wb.name:
            sample = wb.sheets['냉장']
            print(f"Sample: {wb.name}")
        elif '251207' in wb.name and '부진재고' in wb.name:
            generated = wb.sheets['냉장']
            print(f"Generated: {wb.name}")
    
    if not sample or not generated:
        print("Need both files open!")
        return
    
    print("\n" + "="*70)
    print("SLOW MOVING - PIXEL WIDTH COMPARISON")
    print("="*70)
    print(f"{'Col':<4} {'Sample CW':<12} {'Sample PX':<12} {'Gen CW':<12} {'Gen PX':<12} {'PX Diff':<10}")
    print("-"*70)
    
    cols = ['A','B','C','D','E','F','G','H','I','J','K','L']
    all_match = True
    
    for col in cols:
        s_cw = sample.range(f'{col}1').api.ColumnWidth
        s_width = sample.range(f'{col}1').api.Width
        s_px = s_width * 96 / 72
        
        g_cw = generated.range(f'{col}1').api.ColumnWidth
        g_width = generated.range(f'{col}1').api.Width
        g_px = g_width * 96 / 72
        
        px_diff = g_px - s_px
        status = "[OK]" if abs(px_diff) < 1 else "[DIFF]"
        if abs(px_diff) >= 1:
            all_match = False
        
        print(f"{col:<4} {s_cw:<12.2f} {s_px:<12.0f} {g_cw:<12.2f} {g_px:<12.0f} {px_diff:<+10.0f} {status}")
    
    print("\n" + "="*70)
    if all_match:
        print("RESULT: ALL COLUMNS MATCH PERFECTLY!")
    else:
        print("RESULT: Some differences found")
    print("="*70)

if __name__ == '__main__':
    compare_slow()
