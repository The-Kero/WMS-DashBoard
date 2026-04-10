# -*- coding: utf-8 -*-
"""인쇄 설정 상세 비교"""
import xlwings as xw

def check_print_settings():
    app = xw.apps.active
    
    for wb in app.books:
        print(f"\n{'='*60}")
        print(f"File: {wb.name}")
        print('='*60)
        
        ws = wb.sheets[0]
        ps = ws.api.PageSetup
        
        # 인쇄영역
        print(f"\n[Print Area]")
        try:
            print_area = ps.PrintArea
            print(f"  PrintArea: '{print_area}'")
        except Exception as e:
            print(f"  PrintArea: Error - {e}")
        
        # 인쇄 설정 상세
        print(f"\n[Page Setup]")
        print(f"  Orientation: {'Landscape' if ps.Orientation == 2 else 'Portrait'}")
        print(f"  PaperSize: {ps.PaperSize}")
        print(f"  FitToPagesWide: {ps.FitToPagesWide}")
        print(f"  FitToPagesTall: {ps.FitToPagesTall}")
        print(f"  Zoom: {ps.Zoom}")
        print(f"  PrintTitleRows: {ps.PrintTitleRows}")
        print(f"  PrintTitleColumns: {ps.PrintTitleColumns}")
        
        # 사용 범위 확인
        used_range = ws.used_range.address
        print(f"\n[Used Range]")
        print(f"  Address: {used_range}")

if __name__ == '__main__':
    check_print_settings()
