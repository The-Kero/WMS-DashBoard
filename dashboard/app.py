"""
WMS 대시보드 - POC 버전

입고정보 데이터를 수집하고 Streamlit으로 시각화
"""

import streamlit as st
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data.collectors import InboundCollector
from src.ui.components import (
    display_metrics,
    display_summary_cards,
    display_data_table,
    display_top_suppliers,
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


def main():
    """메인 앱 실행"""
    
    # 헤더
    st.title("📦 WMS 대시보드 - POC")
    st.caption("창고관리 시스템 실시간 현황판 (Phase 0)")
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 샘플 데이터 경로
        sample_file = st.text_input(
            "입고 데이터 파일",
            value="tests/fixtures/sample_inbound.csv"
        )
        
        # 새로고침 버튼
        if st.button("🔄 데이터 새로고침", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        # 정보
        st.info("""
        **POC 버전 기능:**
        - ✅ CSV 데이터 읽기
        - ✅ 입고 정보 표시
        - ✅ 핵심 지표 시각화
        - ✅ 상위 공급사 차트
        """)
    
    # 메인 컨텐츠
    try:
        # 데이터 수집기 초기화
        collector = InboundCollector(sample_file, encoding='utf-8')
        
        # 데이터 로드
        with st.spinner("데이터를 불러오는 중..."):
            df = collector.get_data()
            summary = collector.get_summary()
        
        show_success(f"데이터를 성공적으로 불러왔습니다 ({len(df)}건)")
        
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


if __name__ == "__main__":
    main()
