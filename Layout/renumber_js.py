#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JavaScript 함수명 및 데이터 키 일괄 변경 스크립트
- Phase 6: 함수명 변경 (4개) + 함수 내부 getElementById (13개)
- Phase 7: dashboardData 키 변경 (4개)
- Phase 8: 함수 호출 변경 (4개)
총 25개 변경
"""

import re

def renumber_javascript():
    input_file = r"C:\Projects\WMS-DashBoard\Layout\v10_backup_js_before.html"
    output_file = r"C:\Projects\WMS-DashBoard\Layout\v10_js_renumbered.html"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=" * 80)
    print("JavaScript 변경 시작")
    print("=" * 80)
    
    # ========================================
    # Phase 6-A-1: 함수 내부 getElementById('card6...') → getElementById('card3...')
    # ========================================
    print("\n[Phase 6-A-1] 함수 내부 getElementById('card6...') 변경 중...")
    
    before_count = len(re.findall(r"getElementById\('card6", content))
    content = re.sub(
        r"getElementById\('card6([^']+)'\)",
        r"getElementById('card3\1')",
        content
    )
    after_count = len(re.findall(r"getElementById\('card6", content))
    print(f"  card6 getElementById: {before_count} → {after_count} (변경: {before_count - after_count}개)")
    
    # ========================================
    # Phase 6-A-2: 함수 내부 getElementById('card5...') → getElementById('card2...')
    # ========================================
    print("\n[Phase 6-A-2] 함수 내부 getElementById('card5...') 변경 중...")
    
    before_count = len(re.findall(r"getElementById\('card5", content))
    content = re.sub(
        r"getElementById\('card5([^']+)'\)",
        r"getElementById('card2\1')",
        content
    )
    after_count = len(re.findall(r"getElementById\('card5", content))
    print(f"  card5 getElementById: {before_count} → {after_count} (변경: {before_count - after_count}개)")
    
    # ========================================
    # Phase 6-B: 함수명 변경 (역순, 임시 이름 사용)
    # ========================================
    print("\n[Phase 6-B] 함수명 변경 중 (임시 이름 사용)...")
    
    # Step 1: 모두 임시 이름으로
    content = re.sub(r'\bfunction updateCard2\b', 'function TEMP_updateCard1', content)
    content = re.sub(r'\bfunction updateCard3\b', 'function TEMP_updateCard5', content)
    content = re.sub(r'\bfunction updateCard5\b', 'function TEMP_updateCard2', content)
    content = re.sub(r'\bfunction updateCard6\b', 'function TEMP_updateCard3', content)
    
    # Step 2: 임시 이름을 최종 이름으로
    content = re.sub(r'\bfunction TEMP_updateCard1\b', 'function updateCard1', content)
    content = re.sub(r'\bfunction TEMP_updateCard2\b', 'function updateCard2', content)
    content = re.sub(r'\bfunction TEMP_updateCard3\b', 'function updateCard3', content)
    content = re.sub(r'\bfunction TEMP_updateCard5\b', 'function updateCard5', content)
    
    print("  ✓ updateCard2 → updateCard1")
    print("  ✓ updateCard5 → updateCard2")
    print("  ✓ updateCard6 → updateCard3")
    print("  ✓ updateCard3 → updateCard5")
    
    # ========================================
    # Phase 7: dashboardData 키 변경 (역순, 임시 이름)
    # ========================================
    print("\n[Phase 7] dashboardData 키 변경 중...")
    
    # Step 1: 모두 임시 이름으로
    content = re.sub(r'\bcard2:', 'TEMP_card1:', content)
    content = re.sub(r'\bcard3:', 'TEMP_card5:', content)
    content = re.sub(r'\bcard5:', 'TEMP_card2:', content)
    content = re.sub(r'\bcard6:', 'TEMP_card3:', content)
    
    # Step 2: 임시 이름을 최종 이름으로
    content = re.sub(r'\bTEMP_card1:', 'card1:', content)
    content = re.sub(r'\bTEMP_card2:', 'card2:', content)
    content = re.sub(r'\bTEMP_card3:', 'card3:', content)
    content = re.sub(r'\bTEMP_card5:', 'card5:', content)
    
    print("  ✓ card2: → card1:")
    print("  ✓ card5: → card2:")
    print("  ✓ card6: → card3:")
    print("  ✓ card3: → card5:")
    
    # ========================================
    # Phase 8: 함수 호출 변경 (역순, 임시 이름)
    # ========================================
    print("\n[Phase 8] 함수 호출 변경 중...")
    
    # Step 1: 모두 임시 이름으로
    content = re.sub(r'\bupdateCard2\(dashboardData\.card2\)', 'TEMP_updateCard1(dashboardData.card1)', content)
    content = re.sub(r'\bupdateCard3\(dashboardData\.card3\)', 'TEMP_updateCard5(dashboardData.card5)', content)
    content = re.sub(r'\bupdateCard5\(dashboardData\.card5\)', 'TEMP_updateCard2(dashboardData.card2)', content)
    content = re.sub(r'\bupdateCard6\(dashboardData\.card6\)', 'TEMP_updateCard3(dashboardData.card3)', content)
    
    # Step 2: 임시 이름을 최종 이름으로
    content = re.sub(r'\bTEMP_updateCard1\(dashboardData\.card1\)', 'updateCard1(dashboardData.card1)', content)
    content = re.sub(r'\bTEMP_updateCard2\(dashboardData\.card2\)', 'updateCard2(dashboardData.card2)', content)
    content = re.sub(r'\bTEMP_updateCard3\(dashboardData\.card3\)', 'updateCard3(dashboardData.card3)', content)
    content = re.sub(r'\bTEMP_updateCard5\(dashboardData\.card5\)', 'updateCard5(dashboardData.card5)', content)
    
    print("  ✓ updateCard2(dashboardData.card2) → updateCard1(dashboardData.card1)")
    print("  ✓ updateCard5(dashboardData.card5) → updateCard2(dashboardData.card2)")
    print("  ✓ updateCard6(dashboardData.card6) → updateCard3(dashboardData.card3)")
    print("  ✓ updateCard3(dashboardData.card3) → updateCard5(dashboardData.card5)")
    
    # ========================================
    # 파일 저장
    # ========================================
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 80)
    print(f"✅ JavaScript 변경 완료!")
    print(f"출력 파일: {output_file}")
    print("=" * 80)
    
    # ========================================
    # 최종 검증
    # ========================================
    print("\n[최종 검증]")
    print(f"  function updateCard1: {len(re.findall(r'function updateCard1\b', content))}개")
    print(f"  function updateCard2: {len(re.findall(r'function updateCard2\b', content))}개")
    print(f"  function updateCard3: {len(re.findall(r'function updateCard3\b', content))}개")
    print(f"  function updateCard5: {len(re.findall(r'function updateCard5\b', content))}개")
    print(f"  function updateCard6: {len(re.findall(r'function updateCard6\b', content))}개")
    print()
    print(f"  card1:: {len(re.findall(r'\bcard1:', content))}개")
    print(f"  card2:: {len(re.findall(r'\bcard2:', content))}개")
    print(f"  card3:: {len(re.findall(r'\bcard3:', content))}개")
    print(f"  card5:: {len(re.findall(r'\bcard5:', content))}개")
    print(f"  card6:: {len(re.findall(r'\bcard6:', content))}개")
    print()
    print(f"  TEMP: {len(re.findall(r'TEMP', content))}개 (0이어야 함!)")
    card6_count = content.count("getElementById('card6")
    card5_count = content.count("getElementById('card5")
    print(f"  card6 getElementById: {card6_count}개 (0이어야 함!)")
    print(f"  card5 getElementById: {card5_count}개 (0이어야 함!)")

if __name__ == "__main__":
    renumber_javascript()
