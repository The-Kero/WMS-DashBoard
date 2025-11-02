# -*- coding: utf-8 -*-
import re

# HTML 파일 읽기
with open('C:/Projects/WMS-DashBoard/ourhome_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*80)
print("ourhome 시스템 실제 화면 레이아웃 구조 분석")
print("="*80)

# 메인 레이아웃 DIV 찾기
print("\n[1] 메인 레이아웃 구조:")
main_layout = re.findall(r'<div[^>]*(?:id|class)=["\']([^"\']*(?:wrap|container|main|page)[^"\']*)["\']', content, re.I)
for layout in list(set(main_layout))[:15]:
    print(f"  - {layout}")

# 헤더 구조
print("\n[2] 헤더 영역:")
headers = re.findall(r'<(?:header|div)[^>]*(?:id|class)=["\']([^"\']*(?:header|top|gnb|nav)[^"\']*)["\']', content, re.I)
for h in list(set(headers))[:10]:
    print(f"  - {h}")

# 컨텐츠 영역
print("\n[3] 컨텐츠 영역:")
contents = re.findall(r'<div[^>]*(?:id|class)=["\']([^"\']*(?:content|inner|body|section)[^"\']*)["\']', content, re.I)
for c in list(set(contents))[:15]:
    print(f"  - {c}")

# 카드/패널 구조
print("\n[4] 카드/박스 컴포넌트:")
cards = re.findall(r'<div[^>]*class=["\']([^"\']*(?:card|panel|box|item|unit)[^"\']*)["\']', content, re.I)
for card in list(set(cards))[:15]:
    print(f"  - {card}")

# 테이블 구조
print("\n[5] 테이블 구조:")
tables = re.findall(r'<table[^>]*(?:id|class)=["\']([^"\']*)["\']', content, re.I)
for t in list(set(tables))[:10]:
    print(f"  - {t}")

# 그리드 시스템
print("\n[6] 그리드/Row/Col 시스템:")
grid_classes = re.findall(r'class=["\']([^"\']*(?:row|col|grid|flex)[^"\']*)["\']', content, re.I)
for g in list(set(grid_classes))[:15]:
    print(f"  - {g}")

# Vue 컴포넌트 찾기
print("\n[7] Vue 컴포넌트/데이터:")
vue_data = re.findall(r'(?:v-|:|@)([a-z-]+)=["\']', content)
if vue_data:
    print(f"  Vue 디렉티브: {len(set(vue_data))}개")
    for v in list(set(vue_data))[:10]:
        print(f"  - v-{v} / :{v} / @{v}")

# 실제 body 시작 부분 추출
body_start = content.find('<body')
body_section = content[body_start:body_start+5000]

# 메인 컨텐츠 시작 부분 찾기
main_content_match = re.search(r'(<div[^>]*(?:id|class)=["\'](?:wrap|container|main-wrap)[^>]*>.*?</div>)', body_section, re.S)
if main_content_match:
    print("\n[8] 메인 컨텐츠 구조 샘플:")
    print(main_content_match.group(1)[:500])

print("\n" + "="*80)
print("분석 완료!")
print("="*80)
