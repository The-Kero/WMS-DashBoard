import os

file_path = r'C:\OSIS_AUTO\Inbound Status\미입고_목록.csv'
with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
    f.write('입고예정일,입고예정번호,상품,상품명,메모\n')
print(f'파일 생성 완료: {file_path}')
