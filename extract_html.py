# -*- coding: utf-8 -*-
import pyshark

print("Starting pcap analysis...")

cap = pyshark.FileCapture('C:/Projects/WMS-DashBoard/ourhome.pcapng', display_filter='http')

html_found = False
for i, packet in enumerate(cap):
    if i > 100:
        break
    
    try:
        if hasattr(packet, 'http') and hasattr(packet.http, 'file_data'):
            payload = bytes.fromhex(packet.http.file_data.replace(':', '')).decode('utf-8', errors='ignore')
            
            if '<html' in payload.lower() or '<!doctype' in payload.lower():
                with open('C:/Projects/WMS-DashBoard/ourhome_page.html', 'w', encoding='utf-8') as f:
                    f.write(payload)
                print(f"HTML saved! Length: {len(payload)} chars")
                html_found = True
                break
    except Exception as e:
        pass

if not html_found:
    print("HTML not found in first 100 packets")
else:
    print("Analysis complete! Check ourhome_page.html")

cap.close()
