"""
WMS 대시보드 - Phase 1 버전

입고/출고 정보 데이터를 수집하고 Streamlit으로 시각화
"""

import streamlit as st
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data.collectors import InboundCollector, OutboundCollector, InventoryCollector
from src.ui.components import (
    display_metrics,
    display_summary_cards,
    display_data_table,
    display_top_suppliers,
    display_outbound_metrics,
    display_outbound_summary_cards,
    display_top_destinations,
    display_top_outbound_products,
    display_inventory_metrics,
    display_inventory_summary,
    display_risky_products_table,
    display_inventory_table,
    display_low_stock_table,
    show_error,
    show_success
)


# 페이지 설정
st.set_page_config(
    page_title="WMS 대시보드",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_inbound_tab(sample_file: str):
    """입고 대시보드 탭 렌더링"""
    try:
        # 데이터 수집기 초기화
        collector = InboundCollector(sample_file, encoding='utf-8')
        
        # 데이터 로드
        with st.spinner("입고 데이터를 불러오는 중..."):
            df = collector.get_data()
            summary = collector.get_summary()
        
        show_success(f"입고 데이터를 성공적으로 불러왔습니다 ({len(df)}건)")
        
        # 핵심 지표 표시
        st.divider()
        display_metrics(summary)
        
        # 날짜 정보
        st.divider()
        display_summary_cards(summary)
        
        # 상위 공급사
        st.divider()
        top_suppliers = collector.get_top_suppliers(n=5)
        display_top_suppliers(top_suppliers)
        
        # 전체 데이터 테이블
        st.divider()
        display_data_table(df, title="📋 입고 데이터 전체 목록", height=400)
        
        # 추가 정보
        with st.expander("🔍 데이터 상세 정보"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**데이터 타입:**")
                st.dataframe(df.dtypes.to_frame(name='Type'), use_container_width=True)
            
            with col2:
                st.write("**기본 통계:**")
                st.dataframe(df.describe(), use_container_width=True)
        
    except FileNotFoundError as e:
        show_error(f"파일을 찾을 수 없습니다: {sample_file}")
        st.info("💡 사이드바에서 올바른 파일 경로를 입력해주세요.")
        
    except Exception as e:
        show_error(f"오류 발생: {str(e)}")
        with st.expander("상세 오류 정보"):
            st.exception(e)


def render_outbound_tab(sample_file: str):
    """출고 대시보드 탭 렌더링"""
    try:
        # 데이터 수집기 초기화
        collector = OutboundCollector(sample_file, encoding='utf-8')
        
        # 데이터 로드
        with st.spinner("출고 데이터를 불러오는 중..."):
            df = collector.get_data()
            summary = collector.get_summary()
        
        show_success(f"출고 데이터를 성공적으로 불러왔습니다 ({len(df)}건)")
        
        # 핵심 지표 표시
        st.divider()
        display_outbound_metrics(summary)
        
        # 날짜 정보 및 금액
        st.divider()
        display_outbound_summary_cards(summary)
        
        # 상위 배송처와 상위 상품을 나란히 표시
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            top_destinations = collector.get_top_destinations(n=5)
            display_top_destinations(top_destinations)
        
        with col2:
            top_products = collector.get_top_products(n=5)
            display_top_outbound_products(top_products)
        
        # 전체 데이터 테이블
        st.divider()
        display_data_table(df, title="📋 출고 데이터 전체 목록", height=400)
        
        # 추가 정보
        with st.expander("🔍 데이터 상세 정보"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**데이터 타입:**")
                st.dataframe(df.dtypes.to_frame(name='Type'), use_container_width=True)
            
            with col2:
                st.write("**기본 통계:**")
                st.dataframe(df.describe(), use_container_width=True)
        
    except FileNotFoundError as e:
        show_error(f"파일을 찾을 수 없습니다: {sample_file}")
        st.info("💡 사이드바에서 올바른 파일 경로를 입력해주세요.")
        
    except Exception as e:
        show_error(f"오류 발생: {str(e)}")
        with st.expander("상세 오류 정보"):
            st.exception(e)


def render_inventory_tab(sample_file: str):
    """재고 대시보드 탭 렌더링"""
    try:
        # 데이터 수집기 초기화
        collector = InventoryCollector(sample_file, encoding='utf-8-sig')
        
        # 데이터 로드
        with st.spinner("재고 데이터를 불러오는 중..."):
            df = collector.get_data()
            summary = collector.get_summary()
        
        show_success(f"재고 데이터를 성공적으로 불러왔습니다 ({len(df)}건)")
        
        # 4대 핵심 지표 표시
        st.divider()
        display_inventory_metrics(summary)
        
        # 추가 요약 정보 (평균 유효비, 유효비 구간별 분포)
        st.divider()
        display_inventory_summary(summary)
        
        # 유효비 위험 상품 (≤ 20%)
        st.divider()
        risky = collector.get_risky_products()
        display_risky_products_table(risky)
        
        # 가용수량 부족 상품 (선택 사항)
        if st.checkbox("📦 가용수량 부족 상품 보기 (≤10개)", value=False):
            st.divider()
            low_stock = collector.get_low_stock_products(threshold=10)
            display_low_stock_table(low_stock)
        
        # 재고금액 상위 상품
        st.divider()
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 💰 재고금액 TOP 10")
            top_value = collector.get_top_value_products(n=10)
            
            # 표시용 포맷
            display_top = top_value.copy()
            display_top['재고금액'] = display_top['재고금액'].apply(lambda x: f"{int(x):,}원")
            display_top['단가'] = display_top['단가'].apply(lambda x: f"{int(x):,}원")
            
            st.dataframe(display_top, use_container_width=True, height=400)
        
        with col2:
            st.markdown("#### 📊 총 재고 금액")
            total_value = collector.calculate_total_value()
            
            # 큰 숫자로 표시
            if total_value >= 100_000_000:  # 1억 이상
                value_str = f"{total_value/100_000_000:.2f}억원"
            elif total_value >= 10_000_000:  # 1천만 이상
                value_str = f"{total_value/10_000_000:.2f}천만원"
            else:
                value_str = f"{total_value:,}원"
            
            st.markdown(f"### {value_str}")
            st.caption(f"정확한 금액: {total_value:,}원")
            
            # 간단한 통계
            st.markdown("---")
            st.markdown("**재고 통계:**")
            st.write(f"- 총 상품 수: {summary.get('총_상품수', 0):,}개")
            st.write(f"- 총 가용수량: {summary.get('총_가용수량', 0):,}개")
            st.write(f"- 평균 유효비: {summary.get('평균_유효비', 0)}%")
        
        # 전체 재고 목록 (필터/정렬 가능)
        st.divider()
        
        # 재고금액 컬럼 추가
        df_with_value = df.copy()
        df_with_value['재고금액'] = df_with_value['가용수량'] * df_with_value['단가']
        
        display_inventory_table(df_with_value, show_filters=True)
        
        # 추가 정보
        with st.expander("🔍 데이터 상세 정보"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**데이터 타입:**")
                st.dataframe(df.dtypes.to_frame(name='Type'), use_container_width=True)
            
            with col2:
                st.write("**기본 통계:**")
                st.dataframe(df.describe(), use_container_width=True)
        
    except FileNotFoundError as e:
        show_error(f"파일을 찾을 수 없습니다: {sample_file}")
        st.info("💡 사이드바에서 올바른 파일 경로를 입력해주세요.")
        
    except Exception as e:
        show_error(f"오류 발생: {str(e)}")
        with st.expander("상세 오류 정보"):
            st.exception(e)


def main():
    """메인 앱 실행"""
    
    # 헤더
    st.title("📦 WMS 대시보드")
    st.caption("창고관리 시스템 실시간 현황판 (Phase 1 - MVP)")
    
    # 기본 파일 경로 (절대 경로)
    default_inbound = str(project_root / "tests" / "fixtures" / "sample_inbound.csv")
    default_outbound = str(project_root / "tests" / "fixtures" / "sample_outbound.csv")
    default_inventory = str(project_root / "tests" / "fixtures" / "sample_inventory.csv")
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 샘플 데이터 경로
        inbound_file = st.text_input(
            "입고 데이터 파일",
            value=default_inbound
        )
        
        outbound_file = st.text_input(
            "출고 데이터 파일",
            value=default_outbound
        )
        
        inventory_file = st.text_input(
            "재고 데이터 파일",
            value=default_inventory
        )
        
        # 새로고침 버튼
        if st.button("🔄 데이터 새로고침", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        # 정보
        st.info("""
        **Phase 1 기능:**
        - ✅ 입고 정보 대시보드
        - ✅ 출고 정보 대시보드
        - ✅ 재고 정보 대시보드 (NEW!)
        - ⏳ 삭제 정보 (예정)
        - ⏳ 비정형 오더 (예정)
        """)
        
        st.success("""
        **새로운 기능:**
        - 3개 탭 시스템 (입고/출고/재고)
        - 재고 4대 핵심 지표
        - 유효기한 임박 상품 경고
        - 로케이션/상품별 재고 분석
        - 유효비 구간별 분포
        """)
    
    # 메인 컨텐츠 - 탭으로 구분
    tab1, tab2, tab3 = st.tabs(["📦 입고 현황", "🚚 출고 현황", "📊 재고 현황"])
    
    with tab1:
        render_inbound_tab(inbound_file)
    
    with tab2:
        render_outbound_tab(outbound_file)
    
    with tab3:
        render_inventory_tab(inventory_file)


if __name__ == "__main__":
    main()
