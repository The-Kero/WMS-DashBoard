"""
v10.html 카드 번호 일괄 변경 스크립트 v3 (정규표현식 사용)

정규표현식으로 id="cardX" 형태만 변경
주석, 텍스트는 변경하지 않음
"""

import re

# 파일 읽기 (백업 파일 사용!)
file_path = r'C:\Projects\WMS-DashBoard\Layout\v10_backup_20251123.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== 변경 전 ===")
print('id="card1":', len(re.findall(r'id="card1"', content)))
print('id="card2":', len(re.findall(r'id="card2"', content)))
print('id="card3":', len(re.findall(r'id="card3"', content)))
print('id="card4":', len(re.findall(r'id="card4"', content)))
print('id="card5":', len(re.findall(r'id="card5"', content)))
print('id="card6":', len(re.findall(r'id="card6"', content)))
print()

# Phase 1: 모두 임시로 변경
print("=== Phase 1: 임시 변경 ===")

# card2 → TEMP1
content = re.sub(r'id="card2([^"]*)"', r'id="TEMP1\1"', content)
print('Step 1: id="card2*" -> id="TEMP1*"')
print('  TEMP1*:', len(re.findall(r'id="TEMP1[^"]*"', content)))

# card3 → TEMP3  
content = re.sub(r'id="card3([^"]*)"', r'id="TEMP3\1"', content)
print('Step 2: id="card3*" -> id="TEMP3*"')
print('  TEMP3*:', len(re.findall(r'id="TEMP3[^"]*"', content)))

# card5 → TEMP5
content = re.sub(r'id="card5([^"]*)"', r'id="TEMP5\1"', content)
print('Step 3: id="card5*" -> id="TEMP5*"')
print('  TEMP5*:', len(re.findall(r'id="TEMP5[^"]*"', content)))

# card6 → TEMP6
content = re.sub(r'id="card6([^"]*)"', r'id="TEMP6\1"', content)
print('Step 4: id="card6*" -> id="TEMP6*"')
print('  TEMP6*:', len(re.findall(r'id="TEMP6[^"]*"', content)))
print()

# Phase 2: 최종 변경
print("=== Phase 2: 최종 변경 ===")

# TEMP1 → card1 (입고)
content = re.sub(r'id="TEMP1([^"]*)"', r'id="card1\1"', content)
print('Step 1: id="TEMP1*" -> id="card1*" (입고)')
print('  card1*:', len(re.findall(r'id="card1[^"]*"', content)))

# TEMP5 → card2 (자사출고)
content = re.sub(r'id="TEMP5([^"]*)"', r'id="card2\1"', content)
print('Step 2: id="TEMP5*" -> id="card2*" (자사출고)')
print('  card2*:', len(re.findall(r'id="card2[^"]*"', content)))

# TEMP6 → card3 (지방출고)
content = re.sub(r'id="TEMP6([^"]*)"', r'id="card3\1"', content)
print('Step 3: id="TEMP6*" -> id="card3*" (지방출고)')
print('  card3*:', len(re.findall(r'id="card3[^"]*"', content)))

# TEMP3 → card5 (유의상품)
content = re.sub(r'id="TEMP3([^"]*)"', r'id="card5\1"', content)
print('Step 4: id="TEMP3*" -> id="card5*" (유의상품)')
print('  card5*:', len(re.findall(r'id="card5[^"]*"', content)))
print()

print("=== 변경 후 ===")
print('id="card1*":', len(re.findall(r'id="card1[^"]*"', content)), '(입고)')
print('id="card2*":', len(re.findall(r'id="card2[^"]*"', content)), '(자사출고)')
print('id="card3*":', len(re.findall(r'id="card3[^"]*"', content)), '(지방출고)')
print('id="card4*":', len(re.findall(r'id="card4[^"]*"', content)), '(스케줄)')
print('id="card5*":', len(re.findall(r'id="card5[^"]*"', content)), '(유의상품)')
print('id="card6*":', len(re.findall(r'id="card6[^"]*"', content)), '(삭제)')
print()

# 검증
temp_count = len(re.findall(r'id="TEMP[^"]*"', content))
if temp_count > 0:
    print(f"ERROR: 임시 이름 남음! count={temp_count}")
else:
    print("OK: 모든 임시 이름 제거됨!")
print()

# 파일 저장
output_path = r'C:\Projects\WMS-DashBoard\Layout\v10_renumbered.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"SUCCESS! Saved to: {output_path}")
print("Next: Check v10_renumbered.html")
