# -*- coding: utf-8 -*-
"""
샘플 재고 데이터 생성 스크립트
백엔드 실제 데이터에서 20개 샘플 추출
"""

import pandas as pd

# 백엔드 실제 데이터 로드
df = pd.read_csv(
    r"C:\OSIS_AUTO\inventory_status\inventory_status_20251020.csv",
    encoding='utf-8-sig'
)

print(f"[INFO] 원본 데이터: {len(df)}개 레코드")

# 다양한 유효비를 가진 샘플 선택
# - 유효비 20% 이하: 위험 상품
# - 유효비 20-80%: 보통 상품
# - 유효비 80% 이상: 우수 상품

samples = []

# 위험 상품 (유효비 <= 20%) - 5개
danger = df[df['유효유통비(%)'] <= 20].head(5)
samples.append(danger)

# 주의 상품 (유효비 21-40%) - 3개
warning = df[(df['유효유통비(%)'] > 20) & (df['유효유통비(%)'] <= 40)].head(3)
samples.append(warning)

# 보통 상품 (유효비 41-60%) - 3개
normal = df[(df['유효유통비(%)'] > 40) & (df['유효유통비(%)'] <= 60)].head(3)
samples.append(normal)

# 양호 상품 (유효비 61-80%) - 4개
good = df[(df['유효유통비(%)'] > 60) & (df['유효유통비(%)'] <= 80)].head(4)
samples.append(good)

# 우수 상품 (유효비 > 80%) - 5개
excellent = df[df['유효유통비(%)'] > 80].head(5)
samples.append(excellent)

# 샘플 합치기
sample_df = pd.concat(samples, ignore_index=True)

print(f"[INFO] 샘플 데이터: {len(sample_df)}개 레코드")
print(f"[INFO] 유효비 분포:")
print(f"  - 위험 (0-20%): {len(danger)}개")
print(f"  - 주의 (21-40%): {len(warning)}개")
print(f"  - 보통 (41-60%): {len(normal)}개")
print(f"  - 양호 (61-80%): {len(good)}개")
print(f"  - 우수 (81-100%): {len(excellent)}개")

# 샘플 저장
output_path = r"C:\Projects\WMS-DashBoard\dashboard\tests\fixtures\sample_inventory.csv"
sample_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"[SUCCESS] 샘플 데이터 저장 완료: {output_path}")
