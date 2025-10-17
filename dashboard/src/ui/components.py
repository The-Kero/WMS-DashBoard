"""
Streamlit UI 컴포넌트

대시보드에서 사용할 재사용 가능한 UI 요소들
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any


def display_metrics(summary: Dict[str, Any]):
    """
    핵심 지표를 카드 형태로 표시
    
    Args:
        summary: 요약 정보 딕셔너리
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 총 입고건수",
            value=f"{summary.get('총_입고건수', 0):,}건"
        )
    
    with col2:
        st.metric(
            label="📊 총 입고수량",
            value=f"{summary.get('총_입고수량', 0):,}개"
        )
    
    with col3:
        st.metric(
            label="🏢 공급사 수",
            value=f"{summary.get('공급사_수', 0):,}개"
        )
    
    with col4:
        st.metric(
            label="🎁 상품 종류",
            value=f"{summary.get('상품_종류', 0):,}개"
        )


def display_summary_cards(summary: Dict[str, Any]):
    """
    날짜 관련 요약 정보 표시
    
    Args:
        summary: 요약 정보 딕셔너리
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"📅 **최초 입고예정일**: {summary.get('최초_입고예정일', 'N/A')}")
    
    with col2:
        st.info(f"📅 **최근 입고예정일**: {summary.get('최근_입고예정일', 'N/A')}")


def display_data_table(df: pd.DataFrame, title: str = "데이터 테이블", height: int = 400):
    """
    데이터프레임을 테이블 형태로 표시
    
    Args:
        df: 표시할 DataFrame
        title: 테이블 제목
        height: 테이블 높이 (픽셀)
    """
    st.subheader(title)
    
    # 행 개수 표시
    st.caption(f"총 {len(df):,}개 행")
    
    # 테이블 표시
    st.dataframe(
        df,
        use_container_width=True,
        height=height
    )


def display_top_suppliers(df: pd.DataFrame):
    """
    상위 공급사 차트 표시
    
    Args:
        df: 공급사별 입고수량 DataFrame
    """
    st.subheader("🏆 상위 공급사")
    
    if df.empty:
        st.warning("데이터가 없습니다")
        return
    
    # 막대 차트
    st.bar_chart(
        df.set_index('공급사명')['입고수량'],
        use_container_width=True
    )
    
    # 데이터 테이블
    with st.expander("상세 데이터 보기"):
        st.dataframe(df, use_container_width=True)


def show_error(message: str):
    """
    에러 메시지 표시
    
    Args:
        message: 에러 메시지
    """
    st.error(f"❌ {message}")


def show_success(message: str):
    """
    성공 메시지 표시
    
    Args:
        message: 성공 메시지
    """
    st.success(f"✅ {message}")


def show_info(message: str):
    """
    정보 메시지 표시
    
    Args:
        message: 정보 메시지
    """
    st.info(f"ℹ️ {message}")
