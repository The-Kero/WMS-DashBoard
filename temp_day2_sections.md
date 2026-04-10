#### 2.2 5개 Collector 데이터 수집 (60분)
- [ ] 2.2.1 try 블록 시작
- [ ] 2.2.2 `today = datetime.now().strftime("%Y%m%d")` 추가
- [ ] 2.2.3 빈 줄 추가
- [ ] 2.2.4 `# 1. 입고 데이터` 주석
- [ ] 2.2.5 inbound_file 경로 작성 (`C:/OSIS_AUTO/Inbound Status/integrated_inbound_{today}.csv`)
- [ ] 2.2.6 `inbound_collector = InboundCollector(inbound_file, encoding='utf-8-sig')` 생성
- [ ] 2.2.7 `inbound_data = inbound_collector.get_data()` DataFrame 가져오기
- [ ] 2.2.8 빈 줄 추가
- [ ] 2.2.9 `# 2. 출고 데이터` 주석
- [ ] 2.2.10 outbound_file 경로 작성 (`C:/OSIS_AUTO/Outbound Status/outbound_merged_{today}.csv`)
- [ ] 2.2.11 `outbound_collector = OutboundCollector(outbound_file, encoding='utf-8-sig')` 생성
- [ ] 2.2.12 `outbound_data = outbound_collector.get_data()` DataFrame 가져오기
- [ ] 2.2.13 빈 줄 추가
- [ ] 2.2.14 `# 3. 재고 데이터` 주석
- [ ] 2.2.15 inventory_file 경로 작성 (`C:/OSIS_AUTO/inventory_status/inventory_status_{today}.csv`)
- [ ] 2.2.16 `inventory_collector = InventoryCollector(inventory_file, encoding='utf-8-sig')` 생성
- [ ] 2.2.17 `inventory_data = inventory_collector.get_data()` DataFrame 가져오기
- [ ] 2.2.18 빈 줄 추가
- [ ] 2.2.19 `# 4. 삭제 데이터 (현재 미사용)` 주석
- [ ] 2.2.20 빈 줄 추가
- [ ] 2.2.21 `# 5. 비정형 오더 데이터` 주석
- [ ] 2.2.22 irregular_file 경로 작성 (`C:/OSIS_AUTO/irregular_order/irregular_order_{today}.csv`)
- [ ] 2.2.23 `irregular_collector = IrregularCollector(irregular_file, encoding='utf-8-sig')` 생성
- [ ] 2.2.24 `irregular_data = irregular_collector.get_data()` DataFrame 가져오기
- [ ] 2.2.25 빈 줄 추가
- [ ] 2.2.26 `# DataFrame 수집 완료` 주석
- [ ] 2.2.27 console.log 또는 logger.info로 확인 (선택)
- [ ] 2.2.28 빈 줄 추가
- [ ] 2.2.29 다음 섹션(2.3) 준비

**완료 시간**: ___

---

#### 2.3 카드2 계산 - 입고유의상품 (30분)
- [ ] 2.3.1 `# ==========================================` 주석
- [ ] 2.3.2 `# 카드2: 입고 현황` 주석
- [ ] 2.3.3 `# ==========================================` 주석
- [ ] 2.3.4 빈 줄 추가
- [ ] 2.3.5 `card2_total = len(inbound_data)` 총 건수
- [ ] 2.3.6 `card2_progress = float(inbound_data['진척률'].mean())` 평균 진척률
- [ ] 2.3.7 빈 줄 추가
- [ ] 2.3.8 `# 입고유의상품 계산 (입고 소비기한 < 재고 소비기한)` 주석
- [ ] 2.3.9 `inbound_exp = inbound_data.groupby('상품')['소비기한'].min().reset_index()` 집계
- [ ] 2.3.10 `inbound_exp.columns = ['상품', '입고_소비기한']` 컬럼명 변경
- [ ] 2.3.11 `inv_exp = inventory_data.groupby('상품')['소비기한'].min().reset_index()` 재고 집계
- [ ] 2.3.12 `inv_exp.columns = ['상품', '재고_소비기한']` 컬럼명 변경
- [ ] 2.3.13 `merged = pd.merge(inbound_exp, inv_exp, on='상품', how='inner')` 병합
- [ ] 2.3.14 `risky_inbound = merged[merged['입고_소비기한'] < merged['재고_소비기한']]` 필터링
- [ ] 2.3.15 `card2_risky = len(risky_inbound)` 유의상품 개수

**완료 시간**: ___

---

#### 2.4 카드3 계산 - L07 제외 + 영문키 (45분)
- [ ] 2.4.1 `# ==========================================` 주석
- [ ] 2.4.2 `# 카드3: 피킹 유의 상품` 주석
- [ ] 2.4.3 `# ==========================================` 주석
- [ ] 2.4.4 빈 줄 추가
- [ ] 2.4.5 `# 유효유통비 20% 이하 필터링` 주석
- [ ] 2.4.6 `risky = inventory_data[inventory_data['유효유통비(%)'] <= 20].copy()` 필터링
- [ ] 2.4.7 빈 줄 추가
- [ ] 2.4.8 `# ⚠️ 중요: L07 로케이션 제외` 주석
- [ ] 2.4.9 `risky_filtered = risky[~risky['로케이션'].str.startswith('L07')].copy()` L07 제외
- [ ] 2.4.10 빈 줄 추가
- [ ] 2.4.11 `# 긴급/주의 구분` 주석
- [ ] 2.4.12 `card3_urgent = len(risky_filtered[risky_filtered['유효유통비(%)'] <= 10])` 긴급 (≤10%)
- [ ] 2.4.13 `card3_warning = len(risky_filtered[risky_filtered['유효유통비(%)'] > 10])` 주의 (10%~20%)
- [ ] 2.4.14 `card3_total = len(risky_filtered)` 총 개수
- [ ] 2.4.15 빈 줄 추가
- [ ] 2.4.16 `# 유효비 오름차순 정렬` 주석
- [ ] 2.4.17 `risky_filtered = risky_filtered.sort_values('유효유통비(%)')` 정렬
- [ ] 2.4.18 빈 줄 추가
- [ ] 2.4.19 `# JSON 변환 (영문 키!)` 주석
- [ ] 2.4.20 `card3_items = []` 빈 리스트 생성

**완료 시간**: ___

---

#### 2.5 카드5 계산 - 자사출고 + 라벨 + 비정형 (50분)
- [ ] 2.5.1 `# ==========================================` 주석
- [ ] 2.5.2 `# 카드5: 자사 출고` 주석
- [ ] 2.5.3 `# ==========================================` 주석
- [ ] 2.5.4 빈 줄 추가
- [ ] 2.5.5 `# 자사 출고 타입 (14, 15, 18)` 주석
- [ ] 2.5.6 `card5_types = [14, 15, 18]` 타입 리스트 (숫자형!)
- [ ] 2.5.7 `card5_data = outbound_data[outbound_data['출고유형'].isin(card5_types)].copy()` 필터링
- [ ] 2.5.8 빈 줄 추가
- [ ] 2.5.9 `# 총 출하금액` 주석
- [ ] 2.5.10 `card5_amount = int(card5_data['출하금액'].sum())` 금액 계산
- [ ] 2.5.11 빈 줄 추가
- [ ] 2.5.12 `# 라벨 건수` 주석
- [ ] 2.5.13 `card5_total_label = len(card5_data)` 총 라벨
- [ ] 2.5.14 `card5_unpublished_label = len(card5_data[card5_data['라벨출력'] == 'N'])` 미발행 라벨
- [ ] 2.5.15 빈 줄 추가
- [ ] 2.5.16 `# 비정형 오더` 주석
- [ ] 2.5.17 `card5_irregular_total = len(irregular_data)` 총 건수
- [ ] 2.5.18 `card5_irregular_unpublished = len(irregular_data[irregular_data['라벨출력'] == 'N'])` 미출력
- [ ] 2.5.19 빈 줄 추가
- [ ] 2.5.20 `# 전일 대비 계산 (D-1부터 탐색)` 주석
- [ ] 2.5.21 `card5_compare = 0.0` 기본값
- [ ] 2.5.22 전일 파일 찾기 로직 (for days_ago in range(1, 11))
- [ ] 2.5.23 파일 존재 시 compare 계산
- [ ] 2.5.24 compare = ((card5_amount - compare_amount) / compare_amount * 100)
- [ ] 2.5.25 빈 줄 추가

**완료 시간**: ___

---

#### 2.6 카드6 계산 - 배송처 분류 + destinations (70분)
- [ ] 2.6.1 `# ==========================================` 주석
- [ ] 2.6.2 `# 카드6: 지방 출고` 주석
- [ ] 2.6.3 `# ==========================================` 주석
- [ ] 2.6.4 빈 줄 추가
- [ ] 2.6.5 `# classify_destination_card6() 함수 정의` 주석
- [ ] 2.6.6 함수 시작: `def classify_destination_card6(row):`
- [ ] 2.6.7 `출고유형 = row['출고유형']` 추출
- [ ] 2.6.8 `배송군_str = str(row['배송군'])` 문자열 변환
- [ ] 2.6.9 `배송처명 = row['배송처명']` 추출
- [ ] 2.6.10 `배송군_4자리 = len(배송군_str) == 4` 4자리 체크
- [ ] 2.6.11 빈 줄 추가
- [ ] 2.6.12 `# 05 타입 특수 규칙` 주석
- [ ] 2.6.13 if 출고유형 == 5: 블록 시작
- [ ] 2.6.14 식재 → 한익스 규칙
- [ ] 2.6.15 배송군 3 → 키즈 규칙
- [ ] 2.6.16 배송군 4 → 용인3 규칙
- [ ] 2.6.17 배송군 2 → 용인2 규칙
- [ ] 2.6.18 빈 줄 추가
- [ ] 2.6.19 `# 08 타입 규칙` 주석
- [ ] 2.6.20 elif 출고유형 == 8: 블록
- [ ] 2.6.21 배송군 4 → 용인3
- [ ] 2.6.22 배송군 2 → 용인2
- [ ] 2.6.23 빈 줄 추가
- [ ] 2.6.24 `# 기타 타입 (04, 16, 17, 52, 53)` 주석
- [ ] 2.6.25 elif 출고유형 in [4,16,17,52,53]: 블록
- [ ] 2.6.26 용인 분기 처리
- [ ] 2.6.27 양산/양산2 처리
- [ ] 2.6.28 기타 배송처명 return
- [ ] 2.6.29 빈 줄 추가
- [ ] 2.6.30 `# 지방 출고 타입 필터링` 주석
- [ ] 2.6.31 `card6_types = [4, 5, 8, 16, 17, 52, 53]` 타입 리스트
- [ ] 2.6.32 `card6_data = outbound_data[outbound_data['출고유형'].isin(card6_types)].copy()` 필터링
- [ ] 2.6.33 빈 줄 추가
- [ ] 2.6.34 `# 배송처 분류 적용` 주석
- [ ] 2.6.35 `card6_data['배송처_분류'] = card6_data.apply(classify_destination_card6, axis=1)` 적용

**완료 시간**: ___

---
#### 2.7 JSON 응답 구조 작성 (20분)
- [ ] 2.7.1 `# ==========================================` 주석
- [ ] 2.7.2 `# JSON 응답 구조` 주석
- [ ] 2.7.3 `# ==========================================` 주석
- [ ] 2.7.4 빈 줄 추가
- [ ] 2.7.5 `response = {'success': True, 'data': {}}` 기본 구조
- [ ] 2.7.6 `response['data']['card2'] = {...}` 카드2 데이터
- [ ] 2.7.7 `response['data']['card3'] = {...}` 카드3 데이터
- [ ] 2.7.8 `response['data']['card5'] = {...}` 카드5 데이터
- [ ] 2.7.9 `response['data']['card6'] = {...}` 카드6 데이터
- [ ] 2.7.10 `return jsonify(response)` 반환

**완료 시간**: ___

---

### 🌆 오후 1부 (13:00-14:30) - 에러 처리

#### 2.8 고급 에러 처리 (40분)
- [ ] 2.8.1 `except FileNotFoundError as e:` 블록
- [ ] 2.8.2 파일명 포함 에러 메시지
- [ ] 2.8.3 `return jsonify({'success': False, 'error': ...}), 404`
- [ ] 2.8.4 빈 줄 추가
- [ ] 2.8.5 `except ValueError as e:` 블록
- [ ] 2.8.6 데이터 검증 실패 메시지
- [ ] 2.8.7 `return jsonify({'success': False, 'error': ...}), 400`
- [ ] 2.8.8 빈 줄 추가
- [ ] 2.8.9 `except KeyError as e:` 블록
- [ ] 2.8.10 컬럼 없음 메시지
- [ ] 2.8.11 `return jsonify({'success': False, 'error': ...}), 400`
- [ ] 2.8.12 빈 줄 추가
- [ ] 2.8.13 `except Exception as e:` 블록
- [ ] 2.8.14 `logger.error(f'Dashboard API 에러: {str(e)}')` 로깅
- [ ] 2.8.15 일반 에러 메시지
- [ ] 2.8.16 `return jsonify({'success': False, 'error': ...}), 500`

**완료 시간**: ___

---

### ☕ 휴식 (14:30-14:45)

---

### 🌆 오후 2부 (14:45-17:00) - 테스트

#### 2.9 통합 테스트 (60분)
- [ ] 2.9.1 Flask 서버 실행
- [ ] 2.9.2 `/api/dashboard` 호출
- [ ] 2.9.3 HTTP 200 OK 확인
- [ ] 2.9.4 JSON 구조 확인
- [ ] 2.9.5 card2 데이터 정확성 검증
- [ ] 2.9.6 card3 데이터 정확성 검증 (L07 제외 확인)
- [ ] 2.9.7 card5 데이터 정확성 검증 (타입 14,15,18 확인)
- [ ] 2.9.8 card6 데이터 정확성 검증 (배송처 13개 확인)
- [ ] 2.9.9 카드6 미발행 피킹리스트 (오더수량* > 0) 확인
- [ ] 2.9.10 서버 중지

**완료 시간**: ___

---

### 🌆 오후 3부 (17:00-18:00) - Git 커밋

#### 2.10 Git 커밋 (30분)
- [ ] 2.10.1 `git status` 확인
- [ ] 2.10.2 변경 파일 확인
- [ ] 2.10.3 `git add .` 실행
- [ ] 2.10.4 `git commit -m "Phase 2 Day 2: v9 규칙 완전 적용"` 실행
- [ ] 2.10.5 커밋 성공 확인
- [ ] 2.10.6 `git log --oneline -3` 확인

**완료 시간**: ___

---

## 📊 Day 2 완료 기준 체크

**필수 완료 항목:**
- [ ] ✅ /api/dashboard 엔드포인트 완성
- [ ] ✅ 카드2: 입고유의상품 계산 정확
- [ ] ✅ 카드3: L07 로케이션 제외 확인
- [ ] ✅ 카드5: 자사 출고 타입 (14,15,18) 정확
- [ ] ✅ 카드6: 배송처 분류 13개 정확
- [ ] ✅ 카드6: 미발행 피킹리스트 (오더수량* > 0) 정확
- [ ] ✅ JSON 영문 키 사용
- [ ] ✅ 고급 에러 처리 (FileNotFoundError, ValueError, KeyError, Exception)
- [ ] ✅ 통합 테스트 통과
- [ ] ✅ Git 커밋 완료

**Day 2 최종 완료율**: ___% (___/165개 완료) ⏳  
**실제 소요시간**: ___  
**완료 시각**: ___
