import pandas as pd

df = pd.read_csv('C:/OSIS_AUTO/Inbound Status/integrated_inbound_20251204.csv', encoding='utf-8-sig')

# 스냅샷에서 가져온 7개 상품 정보
products = [
    ('41040645', '런천미트(파우치,수입산) 행복한맛남'),
    ('41055038', '후레쉬햄(파우치,수입산) 행복한맛남'),
    ('41055700', '[아워키즈] 토마토스파게티소스'),
    ('41076156', '후레쉬햄 마일드(파우치,수입산)'),
    ('41120361', '(닥터로빈)스테비아시럽'),
    ('41126806', '[케어플러스]저당 오리엔탈드레싱'),
    ('41127612', '[케어플러스]라구소스'),
]

print("=== 7 products check ===\n")
for code, name in products:
    result = df[df['상품'].astype(str) == code]
    print(f"[{name}]")
    if len(result) > 0:
        for _, row in result.iterrows():
            status = "DONE(100%)" if row['진척률'] == 100 else f"progress={row['진척률']}%"
            print(f"  -> {status}, supplier={row['공급사명']}, qty={row.get('입고예정수량', 'N/A')}")
    else:
        print(f"  -> NOT FOUND in inbound CSV")
    print()
