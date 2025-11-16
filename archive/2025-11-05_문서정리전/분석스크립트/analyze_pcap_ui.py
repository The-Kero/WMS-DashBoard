"""
pcapng 파일에서 UI/UX 관련 정보 추출
- HTTP 요청/응답에서 HTML/CSS/JavaScript 추출
- 화면 레이아웃, 색상, 스타일 정보 파악
"""
import pyshark
import json
import re
from collections import defaultdict

def analyze_pcap_for_ui(pcap_file):
    """pcapng 파일에서 UI 관련 정보 추출"""
    
    print("="*80)
    print("pcapng 파일 분석 시작...")
    print("="*80)
    
    # pyshark로 패킷 읽기
    cap = pyshark.FileCapture(pcap_file, display_filter='http')
    
    ui_data = {
        'html_files': [],
        'css_files': [],
        'js_files': [],
        'images': [],
        'colors': [],
        'layout_info': [],
        'http_requests': []
    }
    
    packet_count = 0
    
    try:
        for packet in cap:
            packet_count += 1
            
            # HTTP 레이어가 있는지 확인
            if hasattr(packet, 'http'):
                http = packet.http
                
                # HTTP 요청 정보 수집
                if hasattr(http, 'request_method'):
                    request_info = {
                        'method': str(http.request_method),
                        'uri': str(http.request_uri) if hasattr(http, 'request_uri') else '',
                        'host': str(http.host) if hasattr(http, 'host') else ''
                    }
                    ui_data['http_requests'].append(request_info)
                    
                    print(f"\n[HTTP Request]")
                    print(f"   Method: {request_info['method']}")
                    print(f"   Host: {request_info['host']}")
                    print(f"   URI: {request_info['uri']}")
                
                # HTTP 응답에서 컨텐츠 타입 확인
                if hasattr(http, 'content_type'):
                    content_type = str(http.content_type)
                    print(f"   Content-Type: {content_type}")
                    
                    # HTML 파일
                    if 'html' in content_type.lower():
                        ui_data['html_files'].append(content_type)
                    
                    # CSS 파일
                    elif 'css' in content_type.lower():
                        ui_data['css_files'].append(content_type)
                    
                    # JavaScript 파일
                    elif 'javascript' in content_type.lower() or 'json' in content_type.lower():
                        ui_data['js_files'].append(content_type)
                    
                    # 이미지 파일
                    elif 'image' in content_type.lower():
                        ui_data['images'].append(content_type)
                
                # HTTP 페이로드에서 HTML/CSS 추출 시도
                if hasattr(http, 'file_data'):
                    try:
                        payload = bytes.fromhex(http.file_data.replace(':', '')).decode('utf-8', errors='ignore')
                        
                        # 색상 코드 추출 (#xxxxxx 형식)
                        colors = re.findall(r'#[0-9A-Fa-f]{6}', payload)
                        if colors:
                            ui_data['colors'].extend(colors)
                            print(f"   [Colors Found]: {colors[:5]}")
                        
                        # CSS 클래스/레이아웃 정보 추출
                        css_classes = re.findall(r'class=["\']([^"\']+)["\']', payload)
                        if css_classes:
                            print(f"   [CSS Classes]: {css_classes[:3]}")
                        
                        # div/table 구조 찾기
                        layout_tags = re.findall(r'<(div|table|section|header|footer|nav)', payload, re.IGNORECASE)
                        if layout_tags:
                            print(f"   [Layout Tags]: {set(layout_tags)}")
                        
                    except Exception as e:
                        pass
            
            # 처음 100개 패킷만 분석 (빠른 미리보기)
            if packet_count >= 100:
                print(f"\n[Info] Analyzed first {packet_count} packets (quick preview)")
                break
                
    except Exception as e:
        print(f"\n[Error] {e}")
    
    finally:
        cap.close()
    
    # 결과 요약
    print("\n" + "="*80)
    print("분석 결과 요약")
    print("="*80)
    print(f"분석한 패킷 수: {packet_count}")
    print(f"HTTP 요청 수: {len(ui_data['http_requests'])}")
    print(f"HTML 파일: {len(ui_data['html_files'])}")
    print(f"CSS 파일: {len(ui_data['css_files'])}")
    print(f"JavaScript 파일: {len(ui_data['js_files'])}")
    print(f"이미지 파일: {len(ui_data['images'])}")
    print(f"발견된 색상 코드: {len(set(ui_data['colors']))}")
    
    if ui_data['colors']:
        print(f"\n[주요 색상]")
        for color in list(set(ui_data['colors']))[:10]:
            print(f"   {color}")
    
    if ui_data['http_requests']:
        print(f"\n[주요 HTTP 요청]")
        for req in ui_data['http_requests'][:5]:
            print(f"   {req['method']} {req['host']}{req['uri']}")
    
    # JSON 파일로 저장
    output_file = 'pcap_ui_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ui_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[Success] 상세 분석 결과가 '{output_file}'에 저장되었습니다!")
    
    return ui_data

if __name__ == '__main__':
    pcap_file = r'C:\Projects\WMS-DashBoard\ourhome.pcapng'
    analyze_pcap_for_ui(pcap_file)
