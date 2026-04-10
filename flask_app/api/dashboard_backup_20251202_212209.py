# -*- coding: utf-8 -*-
"""
대시보드 통합 API (v10 구조)
6개 카드 데이터를 통합하여 제공

카드 매핑 (v10 기준):
- card1: 입고현황
- card2: 자사출고
- card3: 지방출고
- card4: 스케줄 (정적)
- card5: 피킹유의
- card6: 재고현황 (5섹션)
"""

from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import sys
from pathlib import Path
import pandas as pd
import logging
import json

# 로거 설정
logger = logging.getLogger(__name__)

# Collector 직접 import
dashboard_path = Path(__file__).parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.inbound import InboundCollector
from src.data.collectors.outbound import OutboundCollector
from src.data.collectors.inventory import InventoryCollector
from src.data.collectors.irregular import IrregularCollector
from src.data.collectors.delete import DeleteCollector

# Blueprint 생성
bp = Blueprint('dashboard', __name__, url_prefix='/api')


@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    대시보드 6개 카드 데이터 반환 (v10 구조)
    
    Returns:
        JSON: {
            'success': bool,
            'card1': 입고현황,
            'card2': 자사출고,
            'card3': 지방출고,
            'card5': 피킹유의,
            'card6': 재고현황,
            'timestamp': str
        }
    """
    try:
        # 오늘 날짜
        today = datetime.now().strftime("%Y%m%d")
        base_path = "C:/OSIS_AUTO"
        
        # ==========================================
        # 1. 입고 데이터
        # ==========================================
        inbound_file = f"{base_path}/Inbound Status/integrated_inbound_{today}.csv"
        inbound_collector = InboundCollector(file_path=inbound_file, encoding='utf-8-sig')
        inbound_data = inbound_collector.get_data()
        
        # ==========================================
        # 2. 출고 데이터
        # ==========================================
        outbound_file = f"{base_path}/Outbound Status/outbound_all_{today}.csv"
        outbound_collector = OutboundCollector(file_path=outbound_file, encoding='utf-8-sig')
        outbound_data = outbound_collector.get_data()
        
        # ==========================================
        # 3. 재고 데이터
        # ==========================================
        inventory_file = f"{base_path}/inventory_status/inventory_status_{today}.csv"
        inventory_collector = InventoryCollector(file_path=inventory_file, encoding='utf-8-sig')
        inventory_data = inventory_collector.get_data()
        
        # ==========================================
        # 4. 비정형 오더 데이터
        # ==========================================
        irregular_file = f"{base_path}/IrregularOrder Status/irregular_order_{today}.csv"
        try:
            irregular_collector = IrregularCollector(file_path=irregular_file, encoding='utf-8-sig')
            irregular_data = irregular_collector.get_data()
        except FileNotFoundError:
            logger.warning(f"비정형 오더 파일 없음: {irregular_file}")
            irregular_data = pd.DataFrame()
        except Exception as e:
            logger.warning(f"비정형 오더 로드 실패: {str(e)}")
            irregular_data = pd.DataFrame()
        
        # ==========================================
        # 5. 삭제 현황 데이터 (card6 섹션4용)
        # ==========================================
        delete_file = f"{base_path}/Delete Status/delete_status_{today}.csv"
        try:
            delete_collector = DeleteCollector(file_path=delete_file, encoding='utf-8-sig')
            delete_data = delete_collector.get_data()
        except FileNotFoundError:
            logger.warning(f"삭제 현황 파일 없음: {delete_file}")
            delete_data = pd.DataFrame()
        except Exception as e:
            logger.warning(f"삭제 현황 로드 실패: {str(e)}")
            delete_data = pd.DataFrame()
        
        # DataFrame 수집 완료
        logger.info(f"데이터 수집 완료 - 입고: {len(inbound_data)}, 출고: {len(outbound_data)}, 재고: {len(inventory_data)}, 비정형: {len(irregular_data)}, 삭제: {len(delete_data)}")
        
        # ==========================================
        # card1: 입고 현황 (구 card2)
        # ==========================================
        
        # 총 건수 및 평균 진척률
        card1_total = len(inbound_data)
        card1_progress = float(inbound_data['진척률'].mean()) if card1_total > 0 else 0.0
        
        # 입고유의상품 계산 (입고 소비기한 < 재고 소비기한)
        card1_risky_count = 0
        card1_risky_items = []
        
        if card1_total > 0 and len(inventory_data) > 0:
            try:
                # 입고 데이터: 상품별 최소 소비기한 + 상품명
                inbound_exp = inbound_data.groupby('상품').agg({
                    '소비기한': 'min',
                    '상품명': 'first'
                }).reset_index()
                inbound_exp.columns = ['상품', '입고_소비기한', '입고_상품명']
                
                # 재고 데이터: 상품별 최소 소비기한
                inv_exp = inventory_data.groupby('상품')['소비기한'].min().reset_index()
                inv_exp.columns = ['상품', '재고_소비기한']
                
                # 두 데이터 병합
                merged = pd.merge(inbound_exp, inv_exp, on='상품', how='inner')
                
                # 날짜 타입 변환 (format 명시)
                merged['입고_소비기한'] = pd.to_datetime(merged['입고_소비기한'], format='%Y%m%d', errors='coerce')
                merged['재고_소비기한'] = pd.to_datetime(merged['재고_소비기한'], format='%Y%m%d', errors='coerce')
                
                # 입고 소비기한 < 재고 소비기한인 상품 필터링
                risky_inbound = merged[merged['입고_소비기한'] < merged['재고_소비기한']]
                card1_risky_count = len(risky_inbound)
                
                # riskyItems 배열 생성
                for _, row in risky_inbound.iterrows():
                    card1_risky_items.append({
                        'productName': row['입고_상품명'],
                        'inboundExpiry': row['입고_소비기한'].strftime('%Y%m%d') if pd.notna(row['입고_소비기한']) else '',
                        'stockExpiry': row['재고_소비기한'].strftime('%Y%m%d') if pd.notna(row['재고_소비기한']) else ''
                    })
            except Exception as e:
                logger.warning(f"card1 - 입고유의상품 계산 에러: {str(e)}")
        
        logger.info(f"card1 - 총: {card1_total}, 진척률: {card1_progress:.1f}%, 유의상품: {card1_risky_count}")
        
        # ==========================================
        # card2: 자사 출고 (구 card5)
        # ==========================================
        
        # 자사 출고 타입 (14, 15, 18)
        card2_types = [14, 15, 18]
        card2_data = outbound_data[outbound_data['출고유형'].isin(card2_types)].copy()
        
        # 총 출하금액
        card2_amount = int(card2_data['출하금액'].sum()) if len(card2_data) > 0 else 0
        
        # 라벨 건수
        card2_total_label = len(card2_data)
        card2_unprinted_label = len(card2_data[card2_data['라벨출력'] == 'N']) if len(card2_data) > 0 else 0
        
        # 비정형 오더
        card2_irregular_total = len(irregular_data)
        card2_irregular_unprinted = len(irregular_data[irregular_data['라벨출력'] == 'N']) if len(irregular_data) > 0 else 0
        
        # 전일 대비 계산 (D-1부터 탐색)
        card2_compare = 0.0
        for days_ago in range(1, 11):
            compare_date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime("%Y%m%d")
            compare_file = f"{base_path}/Outbound Status/outbound_all_{compare_date}.csv"
            
            try:
                compare_collector = OutboundCollector(file_path=compare_file, encoding='utf-8-sig')
                compare_df = compare_collector.get_data()
                compare_data = compare_df[compare_df['출고유형'].isin(card2_types)]
                compare_amount = int(compare_data['출하금액'].sum()) if len(compare_data) > 0 else 0
                
                if compare_amount > 0:
                    card2_compare = ((card2_amount - compare_amount) / compare_amount * 100)
                    break
            except:
                continue
        
        logger.info(f"card2 - 금액: {card2_amount:,}원, 라벨: {card2_total_label}건, 전일대비: {card2_compare:+.1f}%")
        
        # ==========================================
        # card3: 지방 출고 (구 card6)
        # ==========================================
        
        def classify_destination(row):
            """배송처 분류 함수 (v9 가이드 기준)"""
            출고유형 = row['출고유형']
            배송군 = row['배송군']
            배송처명 = row['배송처명']
            
            if pd.isna(배송군):
                배송군_str = ''
            else:
                배송군_str = str(int(배송군))
            
            if pd.isna(배송처명):
                배송처명 = ''
            
            배송군_4자리 = len(배송군_str) == 4
            
            # 출고유형 05
            if 출고유형 == 5:
                if 배송처명 == '식재':
                    return 'hanex'
                elif 배송군_4자리 and 배송군_str[0] == '3':
                    return 'kids'
                elif 배송군_4자리 and 배송군_str[0] == '4':
                    return 'yongin3'
                elif 배송군_4자리 and 배송군_str[0] == '2':
                    return 'yongin2'
            
            # 출고유형 08
            elif 출고유형 == 8:
                if 배송군_4자리 and 배송군_str[0] == '4':
                    return 'yongin3'
                elif 배송군_4자리 and 배송군_str[0] == '2':
                    return 'yongin2'
            
            # 출고유형 04, 16, 17, 52, 53
            elif 출고유형 in [4, 16, 17, 52, 53]:
                if '용인' in 배송처명:
                    if 배송군_4자리 and 배송군_str[0] == '4':
                        return 'yongin3'
                    else:
                        return 'yongin2'
                elif 배송처명 == '양산':
                    return 'yangsan'
                elif 배송처명 == '양산2':
                    return 'yangsan2'
                else:
                    # 배송처명 → 영문키 매핑
                    dest_mapping = {
                        '제주': 'jeju', '제천': 'jecheon', '호남': 'honam',
                        '구미': 'gumi', '계룡': 'gyeryong', '음성': 'eumseong',
                        '안산': 'ansan'
                    }
                    return dest_mapping.get(배송처명, 'etc')
            
            return 'etc'
        
        # 지방 출고 타입 필터링
        card3_types = [4, 5, 8, 16, 17, 52, 53]
        card3_data = outbound_data[outbound_data['출고유형'].isin(card3_types)].copy()
        
        # 총 출하금액
        card3_amount = int(card3_data['출하금액'].sum()) if len(card3_data) > 0 else 0
        
        # 미발행 피킹리스트 (오더수량* > 0 조건 필수!)
        # ⚠️ 오더수량이 0이면 피킹할 물량 없음 → 리스트 안 뽑는게 정상
        card3_unprinted_picking = 0
        if len(card3_data) > 0 and '피킹 리스트' in card3_data.columns and '오더수량*' in card3_data.columns:
            card3_unprinted_picking = len(card3_data[(card3_data['피킹 리스트'] == 'N') & (card3_data['오더수량*'] > 0)])
        
        # 전일 대비 계산
        card3_compare = 0.0
        for days_ago in range(1, 11):
            compare_date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime("%Y%m%d")
            compare_file = f"{base_path}/Outbound Status/outbound_all_{compare_date}.csv"
            try:
                compare_collector = OutboundCollector(file_path=compare_file, encoding='utf-8-sig')
                compare_df = compare_collector.get_data()
                compare_data = compare_df[compare_df['출고유형'].isin(card3_types)]
                compare_amount = int(compare_data['출하금액'].sum()) if len(compare_data) > 0 else 0
                if compare_amount > 0:
                    card3_compare = ((card3_amount - compare_amount) / compare_amount * 100)
                    break
            except:
                continue
        
        # 배송처별 집계 (destinations 객체)
        card3_destinations = {
            'jeju': 0, 'jecheon': 0, 'honam': 0, 'gumi': 0,
            'gyeryong': 0, 'eumseong': 0, 'yongin2': 0, 'yongin3': 0,
            'ansan': 0, 'yangsan': 0, 'yangsan2': 0, 'hanex': 0, 'kids': 0
        }
        
        if len(card3_data) > 0:
            card3_data['dest_key'] = card3_data.apply(classify_destination, axis=1)
            # 배송처별 오더수량* 합계 (건수가 아님!)
            if '오더수량*' in card3_data.columns:
                dest_counts = card3_data.groupby('dest_key')['오더수량*'].sum().to_dict()
            else:
                dest_counts = card3_data.groupby('dest_key').size().to_dict()
            for key, count in dest_counts.items():
                if key in card3_destinations:
                    card3_destinations[key] = int(count)
        
        logger.info(f"card3 - 금액: {card3_amount:,}원, 미발행피킹: {card3_unprinted_picking}건")
        
        # ==========================================
        # card4: 스케줄 (JSON 파일에서 로드) - 날짜순 정렬
        # ==========================================
        card4_schedules = []
        
        try:
            schedule_file = Path(__file__).parent.parent / 'data' / 'schedule.json'
            if schedule_file.exists():
                with open(schedule_file, 'r', encoding='utf-8') as f:
                    all_schedules = json.load(f)
                
                today_date = datetime.now().date()
                
                # 오늘 이후 일정만 필터링
                future_schedules = []
                for schedule in all_schedules:
                    try:
                        sched_date = datetime.strptime(schedule['date'], '%Y-%m-%d').date()
                        
                        if sched_date >= today_date:
                            future_schedules.append({
                                'date': schedule['date'],
                                'content': schedule['content'],
                                'type': schedule.get('type', 'event')
                            })
                    except:
                        continue
                
                # 날짜순 정렬 후 최대 5개
                future_schedules.sort(key=lambda x: x['date'])
                card4_schedules = future_schedules[:5]
                
                logger.info(f"card4 - 스케줄 {len(card4_schedules)}건 (날짜순 정렬)")
        except Exception as e:
            logger.warning(f"card4 스케줄 로드 실패: {str(e)}")
        
        # ==========================================
        # card5: 피킹 유의 상품 (구 card3)
        # ==========================================
        
        # 유효유통비 20% 이하 필터링
        risky = inventory_data[inventory_data['유효유통비(%)'] <= 20].copy()
        
        # L07 로케이션 제외
        risky_filtered = risky[~risky['로케이션'].str.startswith('L07', na=False)].copy()
        
        # 긴급/주의 구분
        card5_urgent = len(risky_filtered[risky_filtered['유효유통비(%)'] <= 10])
        card5_warning = len(risky_filtered[risky_filtered['유효유통비(%)'] > 10])
        card5_total = len(risky_filtered)
        
        # 유효비 오름차순 정렬
        risky_filtered = risky_filtered.sort_values('유효유통비(%)')
        
        # riskyItems 배열 생성 (v10 구조)
        card5_items = []
        for _, row in risky_filtered.iterrows():
            expiry_raw = row.get('소비기한', '')
            if pd.notna(expiry_raw):
                # YYYYMMDD → YY.MM.DD 형식 변환
                expiry_clean = str(expiry_raw).replace('-', '')[:8]
                if len(expiry_clean) == 8:
                    expiry_str = f"{expiry_clean[2:4]}.{expiry_clean[4:6]}.{expiry_clean[6:8]}"
                else:
                    expiry_str = expiry_clean
            else:
                expiry_str = ''
            
            card5_items.append({
                'location': str(row.get('로케이션', '')),
                'productCode': str(row.get('상품', '')),
                'productName': str(row.get('상품명', '')),
                'expiryDate': expiry_str,
                'validityRatio': float(row.get('유효유통비(%)', 0))
            })
        
        logger.info(f"card5 - 총: {card5_total}, 긴급: {card5_urgent}, 주의: {card5_warning}")
        
        # ==========================================
        # card6: 재고 현황 (5섹션)
        # ==========================================
        # 섹션1: 총재고 + 적치율 (inventory_data)
        # 섹션2: 선입선출 위반 (inventory_data L/K 비교)
        # 섹션3: 미출/부분출고 (outbound_data, 18시 이후)
        # 섹션4: 삭제현황 (delete_data 안산/음성)
        # 섹션5: 미할당 (inbound_data 로케이션 없음)
        # ==========================================
        
        logger.info("card6 계산 시작...")
        
        # 섹션1: 총재고 + 적치율
        card6_total_value = 0
        card6_storage_rate = 0.0
        
        if len(inventory_data) > 0:
            # 총재고 = SUM(가용수량 * 단가)
            if '가용수량' in inventory_data.columns and '단가' in inventory_data.columns:
                card6_total_value = int((inventory_data['가용수량'] * inventory_data['단가']).sum())
            
            # 적치율 = (상단 로케이션 중 재고있는 것) / 524 * 100
            # 상단 로케이션 목록: 냉장 파레트 적재 로케이션.csv (524개)
            upper_loc_file = f"{base_path}/inventory_status/냉장 파레트 적재 로케이션.csv"
            try:
                upper_loc_df = pd.read_csv(upper_loc_file, header=None, encoding='utf-8-sig')
                upper_loc_set = set(upper_loc_df[0].str.strip())
                # 재고 중 상단 로케이션에 있는 것만 필터링
                upper_locations = inventory_data[inventory_data['로케이션'].isin(upper_loc_set)]
                if len(upper_locations) > 0:
                    unique_upper = upper_locations['로케이션'].nunique()
                    card6_storage_rate = round(unique_upper / 524 * 100, 1)
            except Exception as e:
                logger.warning(f"상단 로케이션 파일 로드 실패: {str(e)}")
        
        # 섹션2~5: 기본값 (PART 2에서 구현)
        card6_fifo = []
        card6_partial = []
        card6_delete_ansan = []
        card6_delete_eumseong = []
        card6_unallocated = []
        
        # ==========================================
        # 섹션2: 선입선출 위반 계산
        # ==========================================
        # 위반 조건: 같은 상품에서 상단 소비기한 < 하단 소비기한
        # 상단 = CSV 파일에 있는 524개 로케이션, 하단 = CSV에 없는 로케이션
        if len(inventory_data) > 0 and '로케이션' in inventory_data.columns and '소비기한' in inventory_data.columns:
            try:
                # 상단 로케이션 목록 로드 (적치율에서 이미 로드했으면 재사용)
                if 'upper_loc_set' not in locals():
                    upper_loc_file = f"{base_path}/inventory_status/냉장 파레트 적재 로케이션.csv"
                    upper_loc_df = pd.read_csv(upper_loc_file, header=None, encoding='utf-8-sig')
                    upper_loc_set = set(upper_loc_df[0].str.strip())
                
                # 상단: CSV에 있는 로케이션
                upper_df = inventory_data[inventory_data['로케이션'].isin(upper_loc_set)].copy()
                
                # 하단: CSV에 없는 로케이션
                lower_df = inventory_data[~inventory_data['로케이션'].isin(upper_loc_set)].copy()
                
                if len(upper_df) > 0 and len(lower_df) > 0:
                    # 2.3.3 상품별 소비기한 비교
                    # 상단에서 상품별 최소 소비기한
                    upper_min = upper_df.groupby('상품')['소비기한'].min().reset_index()
                    upper_min.columns = ['상품', 'upper_expiry']
                    
                    # 하단에서 상품별 최소 소비기한
                    lower_min = lower_df.groupby('상품')['소비기한'].min().reset_index()
                    lower_min.columns = ['상품', 'lower_expiry']
                    
                    # 상품코드로 조인
                    merged = pd.merge(upper_min, lower_min, on='상품', how='inner')
                    
                    # 2.3.4 위반 항목 필터링 (상단 < 하단)
                    violations = merged[merged['upper_expiry'] < merged['lower_expiry']]
                    
                    # 2.3.5 fifo 배열 생성
                    for _, row in violations.iterrows():
                        product_code = str(row['상품'])
                        # 상품명 찾기
                        product_name_row = inventory_data[inventory_data['상품'] == row['상품']].iloc[0] if len(inventory_data[inventory_data['상품'] == row['상품']]) > 0 else None
                        product_name = str(product_name_row['상품명']) if product_name_row is not None and '상품명' in product_name_row else product_code
                        
                        # 상단 로케이션 찾기
                        upper_loc_row = upper_df[upper_df['상품'] == row['상품']].iloc[0]
                        upper_location = str(upper_loc_row['로케이션'])
                        
                        # 하단 로케이션 찾기
                        lower_loc_row = lower_df[lower_df['상품'] == row['상품']].iloc[0]
                        lower_location = str(lower_loc_row['로케이션'])
                        
                        # 날짜 포맷 변환 (YYYYMMDD → YY.MM.DD)
                        upper_exp = str(row['upper_expiry']).replace('-', '')[:8]
                        lower_exp = str(row['lower_expiry']).replace('-', '')[:8]
                        upper_exp_fmt = f"{upper_exp[2:4]}.{upper_exp[4:6]}.{upper_exp[6:8]}" if len(upper_exp) >= 8 else upper_exp
                        lower_exp_fmt = f"{lower_exp[2:4]}.{lower_exp[4:6]}.{lower_exp[6:8]}" if len(lower_exp) >= 8 else lower_exp
                        
                        card6_fifo.append({
                            'lower': {
                                'product': product_name,
                                'location': lower_location,
                                'expiry': lower_exp_fmt
                            },
                            'upper': {
                                'location': upper_location,
                                'expiry': upper_exp_fmt
                            }
                        })
                
                logger.info(f"card6 섹션2 - 선입선출 위반: {len(card6_fifo)}건")
            except Exception as e:
                logger.warning(f"선입선출 계산 오류: {str(e)}")
        
        # ==========================================
        # 섹션3: 미출/부분출고 계산
        # ==========================================
        # 20시 이후에만 표시 (그 전에는 작업 진행 중)
        current_hour = datetime.now().hour
        
        if current_hour >= 20 and len(outbound_data) > 0:
            try:
                # 필요한 컬럼 확인 (출고유형 추가)
                required_cols = ['출고유형', '원주문수량', '오더수량*', '배송군', '배송처명', '상품명', '단위및규격']
                if all(col in outbound_data.columns for col in required_cols):
                    
                    # 자사출고 타입만 필터링 (14, 15, 18)
                    company_types = [14, 15, 18]
                    company_outbound = outbound_data[outbound_data['출고유형'].isin(company_types)].copy()
                    
                    # 숫자 변환
                    company_outbound['원주문수량_num'] = pd.to_numeric(company_outbound['원주문수량'], errors='coerce').fillna(0)
                    company_outbound['오더수량_num'] = pd.to_numeric(company_outbound['오더수량*'], errors='coerce').fillna(0)
                    
                    # 미출: 오더수량 = 0 AND 원주문수량 > 0
                    # 부분출고: 0 < 오더수량 < 원주문수량
                    partial_df = company_outbound[
                        (company_outbound['원주문수량_num'] > company_outbound['오더수량_num']) &
                        (company_outbound['원주문수량_num'] > 0)
                    ]
                    
                    for _, row in partial_df.iterrows():
                        original_qty = int(row['원주문수량_num'])
                        order_qty = int(row['오더수량_num'])
                        
                        card6_partial.append({
                            'delivery_group': str(row.get('배송군', '')),
                            'delivery_name': str(row.get('배송처명', '')),
                            'product_name': str(row.get('상품명', '')),
                            'unit': str(row.get('단위및규격', '')),
                            'original_qty': original_qty,
                            'order_qty': order_qty
                        })
                    
                    logger.info(f"card6 섹션3 - 미출/부분출고: {len(card6_partial)}건 (20시 이후, 자사출고만)")
            except Exception as e:
                logger.warning(f"미출/부분출고 계산 오류: {str(e)}")
        else:
            if current_hour < 20:
                logger.info(f"card6 섹션3 - 20시 이전({current_hour}시), 미출/부분출고 미표시")
        
        # ==========================================
        # 섹션4: 삭제현황 계산 (안산/음성)
        # ==========================================
        # 삭제 상품코드.csv 기준으로 재고현황에서 가용수량 조회
        try:
            # 삭제 상품코드 매핑 파일 로드
            delete_code_file = f"{base_path}/inventory_status/삭제 상품코드.csv"
            delete_code_df = pd.read_csv(delete_code_file, header=None, encoding='utf-8-sig')
            delete_code_df.columns = ['상품코드', '센터', '상품명_참조']
            
            # 안산/음성 상품코드 Set 생성
            ansan_codes = set(delete_code_df[delete_code_df['센터'] == '안산']['상품코드'].astype(str))
            eumseong_codes = set(delete_code_df[delete_code_df['센터'] == '음성']['상품코드'].astype(str))
            
            # 재고현황에서 해당 상품코드 필터링
            if len(inventory_data) > 0 and '상품' in inventory_data.columns:
                inventory_data['상품_str'] = inventory_data['상품'].astype(str)
                
                # 안산 삭제 상품
                ansan_inventory = inventory_data[inventory_data['상품_str'].isin(ansan_codes)]
                for _, row in ansan_inventory.iterrows():
                    qty = int(row.get('가용수량', 0)) if pd.notna(row.get('가용수량')) else 0
                    if qty > 0:  # 가용수량이 있는 것만 표시
                        card6_delete_ansan.append({
                            'product_name': str(row.get('상품명', '')),
                            'unit': str(row.get('단위및규격', '')),
                            'qty': qty
                        })
                
                # 음성 삭제 상품
                eumseong_inventory = inventory_data[inventory_data['상품_str'].isin(eumseong_codes)]
                for _, row in eumseong_inventory.iterrows():
                    qty = int(row.get('가용수량', 0)) if pd.notna(row.get('가용수량')) else 0
                    if qty > 0:  # 가용수량이 있는 것만 표시
                        card6_delete_eumseong.append({
                            'product_name': str(row.get('상품명', '')),
                            'unit': str(row.get('단위및규격', '')),
                            'qty': qty
                        })
            
            logger.info(f"card6 섹션4 - 삭제현황: 안산 {len(card6_delete_ansan)}건, 음성 {len(card6_delete_eumseong)}건")
        except Exception as e:
            logger.warning(f"삭제현황 계산 오류: {str(e)}")
        
        # ==========================================
        # 섹션5: 미할당 입고현황 계산
        # ==========================================
        if len(inbound_data) > 0:
            try:
                # 기본로케이션이 비어있는 항목 필터링
                if '기본로케이션' in inbound_data.columns:
                    unalloc_df = inbound_data[
                        (inbound_data['기본로케이션'].isna()) | 
                        (inbound_data['기본로케이션'] == '') |
                        (inbound_data['기본로케이션'].astype(str).str.strip() == '')
                    ]
                    
                    for _, row in unalloc_df.iterrows():
                        product_name = str(row.get('상품명', ''))
                        unit = str(row.get('단위및규격', ''))
                        qty = int(row.get('총입고수량', 0)) if pd.notna(row.get('총입고수량')) else 0
                        center = str(row.get('공급사명', ''))
                        
                        card6_unallocated.append({
                            'product_name': product_name,
                            'unit': unit,
                            'qty': qty,
                            'center': center
                        })
                    
                    logger.info(f"card6 섹션5 - 미할당: {len(card6_unallocated)}건")
            except Exception as e:
                logger.warning(f"미할당 계산 오류: {str(e)}")
        
        logger.info(f"card6 - 총재고: {card6_total_value:,}원, 적치율: {card6_storage_rate}%")
        
        # ==========================================
        # JSON 응답 구조 (v10 규격)
        # ==========================================
        
        return jsonify({
            'success': True,
            'date': today,
            
            # card1: 입고현황
            'card1': {
                'totalCount': card1_total,
                'progressRate': round(card1_progress, 1),
                'inboundRiskyCount': card1_risky_count,
                'riskyItems': card1_risky_items
            },
            
            # card2: 자사출고
            'card2': {
                'amount': card2_amount,
                'compare': round(card2_compare, 1),
                'totalLabel': card2_total_label,
                'unprintedLabel': card2_unprinted_label,
                'irregularTotal': card2_irregular_total,
                'irregularUnprinted': card2_irregular_unprinted
            },
            
            # card3: 지방출고
            'card3': {
                'amount': card3_amount,
                'compare': round(card3_compare, 1),
                'unprintedPicking': card3_unprinted_picking,
                'destinations': card3_destinations
            },
            
            # card4: 스케줄 (날짜순 정렬, 최대 5개)
            'card4': {
                'schedules': card4_schedules
            },
            
            # card5: 피킹유의
            'card5': {
                'totalCount': card5_total,
                'urgentCount': card5_urgent,
                'warningCount': card5_warning,
                'riskyItems': card5_items
            },
            
            # card6: 재고현황 (5섹션)
            'card6': {
                'inventory': {
                    'total_value': card6_total_value
                },
                'storageRate': {
                    'rate': card6_storage_rate
                },
                'fifo': card6_fifo,
                'partial': card6_partial,
                'deleteAnsan': card6_delete_ansan,
                'deleteEumseong': card6_delete_eumseong,
                'unallocated': card6_unallocated
            },
            
            'data_counts': {
                'inbound': len(inbound_data),
                'outbound': len(outbound_data),
                'inventory': len(inventory_data),
                'irregular': len(irregular_data),
                'delete': len(delete_data)
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except FileNotFoundError as e:
        logger.error(f'Dashboard API - 파일 없음: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'파일을 찾을 수 없습니다: {str(e)}'
        }), 404
    
    except ValueError as e:
        logger.error(f'Dashboard API - 데이터 검증 실패: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'데이터 검증 실패: {str(e)}'
        }), 400
    
    except KeyError as e:
        logger.error(f'Dashboard API - 필수 컬럼 없음: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'필수 컬럼이 없습니다: {str(e)}'
        }), 400
    
    except Exception as e:
        logger.error(f'Dashboard API - 서버 에러: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'error': f'서버 에러: {str(e)}'
        }), 500
