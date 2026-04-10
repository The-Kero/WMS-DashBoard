# -*- coding: utf-8 -*-
"""
대시보드 통합 API
6개 카드 데이터를 통합하여 제공
"""

from flask import Blueprint, jsonify
from datetime import datetime
import sys
from pathlib import Path
import pandas as pd
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# Collector 직접 import
dashboard_path = Path(__file__).parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.inbound import InboundCollector
from src.data.collectors.outbound import OutboundCollector
from src.data.collectors.inventory import InventoryCollector
from src.data.collectors.irregular import IrregularCollector

# Blueprint 생성
bp = Blueprint('dashboard', __name__, url_prefix='/api')


@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    대시보드 6개 카드 데이터 반환
    
    Returns:
        JSON: {
            'success': bool,
            'cards': [...],
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
        # 4. 삭제 데이터 (현재 미사용)
        # ==========================================
        # delete_file = f"{base_path}/Delete Status/delete_status_{today}.csv"
        # delete_collector = DeleteCollector(file_path=delete_file, encoding='utf-8-sig')
        # delete_data = delete_collector.get_data()
        
        # ==========================================
        # 5. 비정형 오더 데이터
        # ==========================================
        irregular_file = f"{base_path}/IrregularOrder Status/irregular_order_{today}.csv"
        irregular_collector = IrregularCollector(file_path=irregular_file, encoding='utf-8-sig')
        irregular_data = irregular_collector.get_data()
        
        # DataFrame 수집 완료
        print(f"[DEBUG] 데이터 수집 완료 - 입고: {len(inbound_data)}, 출고: {len(outbound_data)}, 재고: {len(inventory_data)}, 비정형: {len(irregular_data)}")
        
        # ==========================================
        # 카드2: 입고 현황
        # ==========================================
        
        # 총 건수 및 평균 진척률
        card2_total = len(inbound_data)
        card2_progress = float(inbound_data['진척률'].mean()) if card2_total > 0 else 0.0
        
        # 입고유의상품 계산 (입고 소비기한 < 재고 소비기한)
        card2_risky = 0
        if card2_total > 0 and len(inventory_data) > 0:
            try:
                # 입고 데이터: 상품별 최소 소비기한
                inbound_exp = inbound_data.groupby('상품')['소비기한'].min().reset_index()
                inbound_exp.columns = ['상품', '입고_소비기한']
                
                # 재고 데이터: 상품별 최소 소비기한
                inv_exp = inventory_data.groupby('상품')['소비기한'].min().reset_index()
                inv_exp.columns = ['상품', '재고_소비기한']
                
                # 두 데이터 병합
                merged = pd.merge(inbound_exp, inv_exp, on='상품', how='inner')
                
                # 날짜 타입 변환 (안전 처리)
                merged['입고_소비기한'] = pd.to_datetime(merged['입고_소비기한'], errors='coerce')
                merged['재고_소비기한'] = pd.to_datetime(merged['재고_소비기한'], errors='coerce')
                
                # 입고 소비기한 < 재고 소비기한인 상품 필터링
                risky_inbound = merged[merged['입고_소비기한'] < merged['재고_소비기한']]
                card2_risky = len(risky_inbound)
            except Exception as e:
                print(f"[DEBUG] 카드2 - 입고유의상품 계산 에러: {str(e)}")
                card2_risky = 0
        
        print(f"[DEBUG] 카드2 - 총: {card2_total}, 진척률: {card2_progress:.1f}%, 유의상품: {card2_risky}")
        
        # ==========================================
        # 카드3: 피킹 유의 상품
        # ==========================================
        
        # 유효유통비 20% 이하 필터링
        risky = inventory_data[inventory_data['유효유통비(%)'] <= 20].copy()
        
        # ⚠️ 중요: L07 로케이션 제외
        risky_filtered = risky[~risky['로케이션'].str.startswith('L07', na=False)].copy()
        
        # 긴급/주의 구분
        card3_urgent = len(risky_filtered[risky_filtered['유효유통비(%)'] <= 10])  # 긴급 (≤10%)
        card3_warning = len(risky_filtered[risky_filtered['유효유통비(%)'] > 10])   # 주의 (10%~20%)
        card3_total = len(risky_filtered)
        
        # 유효비 오름차순 정렬
        risky_filtered = risky_filtered.sort_values('유효유통비(%)')
        
        # JSON 변환 (영문 키!)
        card3_items = []
        
        print(f"[DEBUG] 카드3 - 총: {card3_total}, 긴급: {card3_urgent}, 주의: {card3_warning}")
        
        # ==========================================
        # 카드6: 지방 출고 - 배송처 분류
        # ==========================================
        
        def classify_destination_card6(row):
            """
            출고유형, 배송군, 배송처명에 따라 배송처 분류
            
            Args:
                row: pandas Series (출고 데이터 한 행)
            
            Returns:
                str: 배송처 분류명 ('한익스', '키즈', '용인3', '용인2', '양산', '기타' 등)
            """
            출고유형 = row['출고유형']
            배송군 = row['배송군']
            배송처명 = row['배송처명']
            
            # NaN 처리
            if pd.isna(배송군):
                배송군_str = ''
            else:
                # 소수점 제거 후 문자열 변환 (예: 2.0 → '2')
                배송군_str = str(int(배송군))
            
            if pd.isna(배송처명):
                배송처명 = ''
            
            # ==========================================
            # 출고유형 05: 출고전표
            # ==========================================
            if 출고유형 == 5:
                if 배송처명 == '식재':
                    return '한익스'
                elif 배송군_str == '3':
                    return '키즈'
                elif 배송군_str == '4':
                    return '용인3'
                elif 배송군_str == '2':
                    return '용인2'
                else:
                    return '기타'
            
            # ==========================================
            # 출고유형 08: 발주출고
            # ==========================================
            elif 출고유형 == 8:
                if 배송군_str == '3':
                    return '키즈'
                elif 배송군_str == '4':
                    return '용인3'
                elif 배송군_str == '2':
                    return '용인2'
                else:
                    return '기타'
            
            # ==========================================
            # 출고유형 04, 16, 17, 52, 53: 기타 지방 출고
            # ==========================================
            elif 출고유형 in [4, 16, 17, 52, 53]:
                # 배송군 4자리 체크
                if len(배송군_str) == 4:
                    앞자리 = 배송군_str[:2]
                    
                    # 용인 분기 (01~50)
                    if 앞자리.isdigit() and 1 <= int(앞자리) <= 50:
                        뒷자리 = 배송군_str[2:]
                        
                        if 뒷자리 == '01':
                            return '용인1'
                        elif 뒷자리 == '02':
                            return '용인2'
                        elif 뒷자리 == '03':
                            return '용인3'
                        else:
                            return '기타'
                    
                    # 양산 분기 (51~99)
                    elif 앞자리.isdigit() and 51 <= int(앞자리) <= 99:
                        return '양산'
                    
                    else:
                        return '기타'
                else:
                    return '기타'
            
            # ==========================================
            # 그 외 출고유형
            # ==========================================
            else:
                return '기타'
        
        # 지방 출고 타입 필터링 (4, 5, 8, 16, 17, 52, 53)
        card6_types = [4, 5, 8, 16, 17, 52, 53]
        card6_data = outbound_data[outbound_data['출고유형'].isin(card6_types)].copy()
        
        # 배송처 분류 적용
        if len(card6_data) > 0:
            card6_data['배송처_분류'] = card6_data.apply(classify_destination_card6, axis=1)
        else:
            card6_data['배송처_분류'] = []
        
        print(f"[DEBUG] 카드6 - 지방출고 필터링: {len(card6_data)}건")
        
        # ==========================================
        # 카드5: 자사 출고
        # ==========================================
        
        # 자사 출고 타입 (14, 15, 18)
        card5_types = [14, 15, 18]
        card5_data = outbound_data[outbound_data['출고유형'].isin(card5_types)].copy()
        
        # 총 출하금액
        card5_amount = int(card5_data['출하금액'].sum()) if len(card5_data) > 0 else 0
        
        # 라벨 건수
        card5_total_label = len(card5_data)
        card5_unpublished_label = len(card5_data[card5_data['라벨출력'] == 'N']) if len(card5_data) > 0 else 0
        
        # 비정형 오더
        card5_irregular_total = len(irregular_data)
        card5_irregular_unpublished = len(irregular_data[irregular_data['라벨출력'] == 'N']) if len(irregular_data) > 0 else 0
        
        # 전일 대비 계산 (D-1부터 탐색)
        card5_compare = 0.0
        for days_ago in range(1, 11):  # D-1 ~ D-10
            compare_date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime("%Y%m%d")
            compare_file = f"C:/OSIS_AUTO/Outbound Status/outbound_all_{compare_date}.csv"
            
            try:
                # OutboundCollector 직접 사용 (파일 경로 전달)
                compare_collector = OutboundCollector(file_path=compare_file, encoding='utf-8-sig')
                compare_df = compare_collector.get_data()
                
                compare_data = compare_df[compare_df['출고유형'].isin(card5_types)]
                compare_amount = int(compare_data['출하금액'].sum()) if len(compare_data) > 0 else 0
                
                if compare_amount > 0:
                    card5_compare = ((card5_amount - compare_amount) / compare_amount * 100)
                    break  # 파일 찾으면 중단
            except FileNotFoundError:
                continue  # 파일 없으면 다음 날짜 시도
            except Exception:
                continue  # 기타 에러도 무시하고 다음 날짜
        
        print(f"[DEBUG] 카드5 - 금액: {card5_amount:,}원, 라벨: {card5_total_label}건({card5_unpublished_label}건 미발행), 비정형: {card5_irregular_total}건({card5_irregular_unpublished}건 미출력), 전일대비: {card5_compare:+.1f}%")
        
        # ==========================================
        # 카드6: 배송처별 집계
        # ==========================================
        
        # 배송처별 groupby 집계
        if len(card6_data) > 0:
            card6_grouped = card6_data.groupby('배송처_분류').agg({
                '출고유형': 'count',  # 건수
                '출하금액': 'sum'      # 금액
            }).reset_index()
            
            # 컬럼명 변경
            card6_grouped.columns = ['배송처', '건수', '금액']
            
            # 총계 계산
            card6_total_count = int(card6_grouped['건수'].sum())
            card6_total_amount = int(card6_grouped['금액'].sum())
            
            # destinations 배열 생성 (영문 키!)
            card6_destinations = [
                {
                    'name': row['배송처'],
                    'count': int(row['건수']),
                    'amount': int(row['금액'])
                }
                for _, row in card6_grouped.iterrows()
            ]
            
            print(f"[DEBUG] 카드6 - 총 {card6_total_count}건, 금액: {card6_total_amount:,}원, 배송처: {len(card6_destinations)}개")
            
        else:
            # 데이터 없을 때
            card6_total_count = 0
            card6_total_amount = 0
            card6_destinations = []
            
            print(f"[DEBUG] 카드6 - 데이터 없음")
        
        # 임시 응답 (다음 단계에서 카드6 추가)
        return jsonify({
            'success': True,
            'message': 'Dashboard API - 카드2, 카드3, 카드5, 카드6 계산 완료',
            'card2': {
                'totalCount': card2_total,
                'progressRate': round(card2_progress, 1),
                'inboundRiskyCount': card2_risky
            },
            'card3': {
                'totalCount': card3_total,
                'urgentCount': card3_urgent,
                'warningCount': card3_warning,
                'items': card3_items
            },
            'card5': {
                'totalAmount': card5_amount,
                'comparePercent': round(card5_compare, 1),
                'totalLabel': card5_total_label,
                'unpublishedLabel': card5_unpublished_label,
                'irregularTotal': card5_irregular_total,
                'irregularUnpublished': card5_irregular_unpublished
            },
            'card6': {
                'totalCount': card6_total_count,
                'totalAmount': card6_total_amount,
                'destinations': card6_destinations
            },
            'data_counts': {
                'inbound': len(inbound_data),
                'outbound': len(outbound_data),
                'inventory': len(inventory_data),
                'irregular': len(irregular_data)
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
