# -*- coding: utf-8 -*-
"""기본 폰트 설정 비교"""
import xlwings as xw

def check_default_font():
    app = xw.apps.active
    
    for wb in app.books:
        print(f"\n{'='*50}")
        print(f"File: {wb.name}")
        print('='*50)
        
        # Normal 스타일 확인
        try:
            normal_style = wb.api.Styles("Normal")
            font = normal_style.Font
            print(f"Normal Style Font:")
            print(f"  Name: {font.Name}")
            print(f"  Size: {font.Size}")
        except Exception as e:
            print(f"Error: {e}")
        
        # 시트의 StandardWidth 확인
        ws = wb.sheets[0]
        try:
            std_width = ws.api.StandardWidth
            std_height = ws.api.StandardHeight
            print(f"\nSheet Standard:")
            print(f"  StandardWidth: {std_width}")
            print(f"  StandardHeight: {std_height}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    check_default_font()
