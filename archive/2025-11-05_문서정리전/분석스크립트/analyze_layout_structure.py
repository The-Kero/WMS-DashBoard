"""
pcapng에서 실제 화면 레이아웃 구조 심층 분석
- HTML 구조, 섹션 배치, 컴포넌트 위치
- 실제 화면 구성 패턴 파악
"""
import pyshark
import re
from collections import defaultdict
import json

def deep_analyze_layout(pcap_file):
    """화면 레이아웃 구조 심층 분석"""
    
    print("="*80)
    print("ourhome 시스템 화면 레이아웃 구조 분석")
    print("="*80)
    
    cap = pyshark.FileCapture(pcap_file, display_filter='http')
    
    layout_info = {
        'page_structure': [],
        'main_sections': [],
        'table_structures': [],
        'card_layouts': [],
        'navigation': [],
        'class_names': defaultdict(int),
        'id_names': [],
        'grid_patterns': [],
        'complete_html': []
    }
    
    packet_count = 0
    
    try:
        for packet in cap:
            packet_count += 1
            
            if hasattr(packet, 'http') and hasattr(packet.http, 'file_data'):
                try:
                    payload = bytes.fromhex(packet.http.file_data.replace(':', '')).decode('utf-8', errors='ignore')
                    
                    # HTML 문서 찾기
                    if '<html' in payload.lower() or '<!DOCTYPE' in payload.lower():
                        print("\n" + "="*80)
                        print("완전한 HTML 문서 발견!")
                        print("="*80)
                        
                        # HTML 저장
                        layout_info['complete_html'].append(payload)
                        
                        # 페이지 전체 구조 추출
                        print("\n[1단계: 페이지 전체 구조]")
                        
                        # DOCTYPE, html, head, body 구조
                        if '<!DOCTYPE' in payload:
                            print("✓ DOCTYPE 선언 있음")
                        if '<html' in payload.lower():
                            print("✓ HTML 태그 있음")
                        if '<head' in payload.lower():
                            print("✓ HEAD 섹션 있음")
                        if '<body' in payload.lower():
                            print("✓ BODY 섹션 있음")
                        
                        # Body 내부 메인 구조
                        print("\n[2단계: Body 내부 주요 섹션]")
                        
                        # Wrapper/Container
                        wrappers = re.findall(r'<div[^>]*(?:id|class)=["\']([^"\']*(?:wrap|container|main|content)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if wrappers:
                            print(f"\n컨테이너 구조:")
                            for w in set(wrappers):
                                print(f"  - {w}")
                        
                        # Header
                        headers = re.findall(r'<(?:header|div)[^>]*(?:id|class)=["\']([^"\']*(?:header|top|nav)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if headers:
                            print(f"\n헤더 영역:")
                            for h in set(headers):
                                print(f"  - {h}")
                        
                        # Main Content Area
                        contents = re.findall(r'<(?:div|main|section)[^>]*(?:id|class)=["\']([^"\']*(?:content|main|inner)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if contents:
                            print(f"\n메인 컨텐츠 영역:")
                            for c in set(contents):
                                print(f"  - {c}")
                        
                        # Sidebar
                        sidebars = re.findall(r'<(?:div|aside)[^>]*(?:id|class)=["\']([^"\']*(?:side|aside|left|right)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if sidebars:
                            print(f"\n사이드바 영역:")
                            for s in set(sidebars):
                                print(f"  - {s}")
                        
                        print("\n[3단계: 컨텐츠 컴포넌트 구조]")
                        
                        # 카드/패널 구조
                        cards = re.findall(r'<div[^>]*class=["\']([^"\']*(?:card|panel|box|item)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if cards:
                            print(f"\n카드/패널 컴포넌트:")
                            for card in set(cards):
                                print(f"  - {card}")
                        
                        # 테이블 구조
                        tables = re.findall(r'<table[^>]*(?:id|class)=["\']([^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if tables:
                            print(f"\n테이블 구조:")
                            for t in set(tables):
                                print(f"  - {t}")
                        
                        # 리스트 구조
                        lists = re.findall(r'<(?:ul|ol)[^>]*(?:class|id)=["\']([^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        if lists:
                            print(f"\n리스트 구조:")
                            for l in set(lists):
                                print(f"  - {l}")
                        
                        print("\n[4단계: 그리드/레이아웃 패턴]")
                        
                        # Row/Column 그리드
                        rows = re.findall(r'<div[^>]*class=["\']([^"\']*(?:row|grid)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        cols = re.findall(r'<div[^>]*class=["\']([^"\']*(?:col|column)[^"\']*)["\'][^>]*>', payload, re.IGNORECASE)
                        
                        if rows:
                            print(f"\nRow 클래스:")
                            for r in set(rows):
                                print(f"  - {r}")
                        
                        if cols:
                            print(f"\nColumn 클래스:")
                            for c in set(cols):
                                print(f"  - {c}")
                        
                        print("\n[5단계: 중요 ID/Class 목록]")
                        
                        # 모든 ID 추출
                        all_ids = re.findall(r'id=["\']([^"\']+)["\']', payload)
                        if all_ids:
                            print(f"\n주요 ID (상위 10개):")
                            unique_ids = list(set(all_ids))[:10]
                            for id_name in unique_ids:
                                print(f"  - #{id_name}")
                        
                        # 자주 사용되는 클래스
                        all_classes = re.findall(r'class=["\']([^"\']+)["\']', payload)
                        class_count = defaultdict(int)
                        for classes in all_classes:
                            for cls in classes.split():
                                class_count[cls] += 1
                        
                        if class_count:
                            print(f"\n자주 사용되는 Class (상위 15개):")
                            sorted_classes = sorted(class_count.items(), key=lambda x: x[1], reverse=True)[:15]
                            for cls, count in sorted_classes:
                                print(f"  - .{cls} ({count}회)")
                        
                        print("\n[6단계: JavaScript 데이터 구조]")
                        
                        # Vue/React 컴포넌트
                        vue_components = re.findall(r'(?:v-|:|@)[a-z-]+=["\']', payload)
                        if vue_components:
                            print(f"\nVue 디렉티브 발견: {len(set(vue_components))}개")
                        
                        # 데이터 바인딩
                        bindings = re.findall(r'\{\{[^}]+\}\}', payload)
                        if bindings:
                            print(f"데이터 바인딩 발견: {len(bindings)}개")
                            print(f"예시: {bindings[0] if bindings else 'N/A'}")
                        
                        # HTML 파일로 저장
                        with open('ourhome_layout_sample.html', 'w', encoding='utf-8') as f:
                            f.write(payload)
                        print(f"\n✅ HTML 파일 저장: ourhome_layout_sample.html")
                        
                        break  # 첫 번째 완전한 HTML만 분석
                        
                except Exception as e:
                    pass
            
            if packet_count >= 200:
                break
                
    except Exception as e:
        print(f"\n오류: {e}")
    
    finally:
        cap.close()
    
    return layout_info

if __name__ == '__main__':
    pcap_file = r'C:\Projects\WMS-DashBoard\ourhome.pcapng'
    layout_info = deep_analyze_layout(pcap_file)
    
    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)
