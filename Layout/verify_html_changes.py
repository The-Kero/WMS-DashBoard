"""
v10.html HTML ID Change Verification Script (English Version)
"""

import re

# Read files
backup_path = r'C:\Projects\WMS-DashBoard\Layout\v10_backup_20251123.html'
new_path = r'C:\Projects\WMS-DashBoard\Layout\v10.html'

with open(backup_path, 'r', encoding='utf-8') as f:
    backup_content = f.read()

with open(new_path, 'r', encoding='utf-8') as f:
    new_content = f.read()

# Save report to file
report_path = r'C:\Projects\WMS-DashBoard\Layout\verify_report.txt'
report = []

def log(msg):
    report.append(msg)
    print(msg)

log("=" * 80)
log("HTML ID Change Verification Report")
log("=" * 80)
log("")

# 1. File size comparison
log("[ 1. File Size Verification ]")
log(f"Backup file: {len(backup_content):,} bytes")
log(f"New file: {len(new_content):,} bytes")
log(f"Difference: {len(new_content) - len(backup_content):+,} bytes")
if len(backup_content) == len(new_content):
    log("PASS: File size identical (only string length changed)")
else:
    log("WARNING: File size changed")
log("")

# 2. Card container ID counts
log("[ 2. Card Container ID Verification ]")
log("-" * 80)
log(f"{'Card':<10} {'Backup':<15} {'New':<15} {'Status':<20}")
log("-" * 80)

results = {}
for card_num in range(1, 7):
    pattern = f'id="card{card_num}"'
    backup_count = len(re.findall(pattern, backup_content))
    new_count = len(re.findall(pattern, new_content))
    results[f'card{card_num}'] = new_count
    
    if card_num == 1:
        expected = 1
        status = "PASS" if new_count == expected else f"FAIL (expected {expected})"
    elif card_num == 2:
        expected = 1
        status = "PASS" if new_count == expected else f"FAIL (expected {expected})"
    elif card_num == 3:
        expected = 1
        status = "PASS" if new_count == expected else f"FAIL (expected {expected})"
    elif card_num == 4:
        expected = 1
        status = "PASS" if new_count == expected else f"FAIL (expected {expected})"
    elif card_num == 5:
        expected = 1
        status = "PASS" if new_count == expected else f"FAIL (expected {expected})"
    elif card_num == 6:
        expected = 0
        status = "PASS" if new_count == expected else f"FAIL (expected {expected})"
    
    log(f"card{card_num:<5} {backup_count:<15} {new_count:<15} {status}")

log("")

# 3. Element ID verification
log("[ 3. Element ID Change Verification ]")
log("")

# card1
log("3-1. card1 (Inbound) - originally card2")
card1_ids = re.findall(r'id="(card1[^"]*)"', new_content)
log(f"  Found IDs: {len(card1_ids)}")
for id_name in sorted(set(card1_ids)):
    log(f"    - {id_name}")
log("")

# card2
log("3-2. card2 (Company Outbound) - originally card5")
card2_ids = re.findall(r'id="(card2[^"]*)"', new_content)
log(f"  Found IDs: {len(card2_ids)}")
for id_name in sorted(set(card2_ids)):
    log(f"    - {id_name}")
log("")

# card3
log("3-3. card3 (Regional Outbound) - originally card6")
card3_ids = re.findall(r'id="(card3[^"]*)"', new_content)
log(f"  Found IDs: {len(card3_ids)}")
for id_name in sorted(set(card3_ids)):
    log(f"    - {id_name}")
log("")

# card4
log("3-4. card4 (Schedule) - kept")
card4_ids = re.findall(r'id="(card4[^"]*)"', new_content)
log(f"  Found IDs: {len(card4_ids)}")
for id_name in sorted(set(card4_ids)):
    log(f"    - {id_name}")
log("")

# card5
log("3-5. card5 (Caution Items) - originally card3")
card5_ids = re.findall(r'id="(card5[^"]*)"', new_content)
log(f"  Found IDs: {len(card5_ids)}")
for id_name in sorted(set(card5_ids)):
    log(f"    - {id_name}")
log("")

# card6
log("3-6. card6 (Deleted)")
card6_ids = re.findall(r'id="(card6[^"]*)"', new_content)
if len(card6_ids) == 0:
    log("  PASS: card6 completely removed")
else:
    log(f"  FAIL: card6 still has {len(card6_ids)} IDs!")
    for id_name in card6_ids:
        log(f"    - {id_name}")
log("")

# 4. CSS class verification
log("[ 4. CSS Class Verification ]")
card3_wide_backup = backup_content.count('card3-wide')
card3_wide_new = new_content.count('card3-wide')
card5_wide_new = new_content.count('card5-wide')

log(f"Backup: card3-wide = {card3_wide_backup}")
log(f"New: card3-wide = {card3_wide_new}")
log(f"New: card5-wide = {card5_wide_new}")

if card3_wide_new == 0 and card5_wide_new == card3_wide_backup:
    log("PASS: card3-wide -> card5-wide changed")
else:
    log("FAIL: CSS class change failed")
log("")

# 5. Temp name verification
log("[ 5. Temporary Name Removal Verification ]")
temp_patterns = ['TEMP', 'CARDTEMP', 'card2_NEW', 'card3_TEMP']
temp_found = False
for pattern in temp_patterns:
    count = new_content.count(pattern)
    if count > 0:
        log(f"FAIL: '{pattern}' found ({count})")
        temp_found = True
    else:
        log(f"PASS: '{pattern}' not found")
log("")

# 6. Final verdict
log("=" * 80)
log("[ Final Verdict ]")
log("=" * 80)

all_pass = True
checks = [
    (len(card1_ids) == 1, "card1 container: 1"),
    (len(card2_ids) == 9, "card2 IDs: 9 (container + 8 elements)"),
    (len(card3_ids) == 7, "card3 IDs: 7 (container + 6 elements)"),
    (len(card4_ids) == 1, "card4 container: 1"),
    (len(card5_ids) == 1, "card5 container: 1"),
    (len(card6_ids) == 0, "card6 completely removed"),
    (card5_wide_new > 0 and card3_wide_new == 0, "CSS class changed"),
    (not temp_found, "Temp names removed")
]

for passed, description in checks:
    status = "PASS" if passed else "FAIL"
    log(f"{status}: {description}")
    if not passed:
        all_pass = False

log("")
if all_pass:
    log("SUCCESS! All verifications passed! HTML ID change complete!")
else:
    log("WARNING! Some verifications failed! Fix required!")
log("=" * 80)

# Save report
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved to: {report_path}")
