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


# ============================================================================
# 출고 관련 UI 컴포넌트
# ============================================================================

def display_outbound_metrics(summary: Dict[str, Any]):
    """
    출고 핵심 지표를 카드 형태로 표시
    
    Args:
        summary: 출고 요약 정보 딕셔너리
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚚 총 출고건수",
            value=f"{summary.get('총_출고건수', 0):,}건"
        )
    
    with col2:
        st.metric(
            label="📊 총 출하수량",
            value=f"{summary.get('총_출하수량', 0):,}개"
        )
    
    with col3:
        st.metric(
            label="🏪 배송처 수",
            value=f"{summary.get('배송처_수', 0):,}개"
        )
    
    with col4:
        st.metric(
            label="🎁 상품 종류",
            value=f"{summary.get('상품_종류', 0):,}개"
        )


def display_outbound_summary_cards(summary: Dict[str, Any]):
    """
    출고 날짜 관련 요약 정보 표시
    
    Args:
        summary: 출고 요약 정보 딕셔너리
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"📅 **최초 출고일자**: {summary.get('최초_출고일자', 'N/A')}")
    
    with col2:
        st.info(f"📅 **최근 출고일자**: {summary.get('최근_출고일자', 'N/A')}")
    
    with col3:
        st.info(f"💰 **총 출하금액**: {summary.get('총_출하금액', 0):,.0f}원")


def display_top_destinations(df: pd.DataFrame):
    """
    상위 배송처 차트 표시
    
    Args:
        df: 배송처별 출하수량 DataFrame
    """
    st.subheader("🏆 상위 배송처")
    
    if df.empty:
        st.warning("데이터가 없습니다")
        return
    
    # 막대 차트
    st.bar_chart(
        df.set_index('배송처')['출하수량'],
        use_container_width=True,
        color="#FF8C00"  # 주황색
    )
    
    # 데이터 테이블
    with st.expander("상세 데이터 보기"):
        st.dataframe(df, use_container_width=True)


def display_top_outbound_products(df: pd.DataFrame):
    """
    상위 출고 상품 차트 표시
    
    Args:
        df: 상품별 출하수량 DataFrame
    """
    st.subheader("📦 상위 출고 상품")
    
    if df.empty:
        st.warning("데이터가 없습니다")
        return
    
    # 상품명 표시를 위한 처리
    df_display = df.copy()
    df_display['상품'] = df_display['상품코드'] + ' - ' + df_display['상품명']
    
    # 막대 차트
    st.bar_chart(
        df_display.set_index('상품')['출하수량'],
        use_container_width=True,
        color="#FF6347"  # 토마토색
    )
    
    # 데이터 테이블
    with st.expander("상세 데이터 보기"):
        st.dataframe(df, use_container_width=True)



# ============================================================================
# 재고 관련 UI 컴포넌트
# ============================================================================

def display_inventory_metrics(summary: Dict[str, Any]):
    """
    재고 4대 핵심 지표를 카드 형태로 표시
    
    Args:
        summary: 재고 요약 정보 딕셔너리
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔢 총 상품 수",
            value=f"{summary.get('총_상품_수', 0):,}개",
            help="관리 중인 전체 상품 종류"
        )
    
    with col2:
        st.metric(
            label="📦 총 재고 수량",
            value=f"{summary.get('총_재고_수량', 0):,}개",
            help="창고 내 전체 재고 수량"
        )
    
    with col3:
        total_value = summary.get('총_재고_금액', 0)
        if total_value >= 100_000_000:  # 1억 이상
            display_value = f"{total_value / 100_000_000:.1f}억원"
        else:
            display_value = f"{total_value / 10_000:.0f}만원"
        
        st.metric(
            label="💰 총 재고 금액",
            value=display_value,
            help="재고수량 × 단가"
        )
    
    with col4:
        danger_count = summary.get('위험_상품_수', 0)
        st.metric(
            label="⚠️ 위험 상품",
            value=f"{danger_count}개",
            delta=f"유효비 ≤ 20%",
            delta_color="inverse",  # 빨간색으로 표시
            help="유효유통비 20% 이하 긴급 조치 필요"
        )


def display_inventory_summary_cards(summary: Dict[str, Any]):
    """
    재고 보조 지표 표시
    
    Args:
        summary: 재고 요약 정보 딕셔너리
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_ratio = summary.get('평균_유효유통비', 0)
        st.info(f"📊 **평균 유효유통비**: {avg_ratio}%")
    
    with col2:
        location_count = summary.get('로케이션_수', 0)
        st.info(f"📍 **로케이션 수**: {location_count:,}개")
    
    with col3:
        available = summary.get('가용_수량', 0)
        st.info(f"✅ **가용 수량**: {available:,}개")


def display_expiring_items_table(df: pd.DataFrame):
    """
    유효기한 임박 상품 테이블 표시 (빨간색 강조)
    
    Args:
        df: 유효기한 임박 상품 DataFrame
    """
    st.subheader("🚨 유효기한 임박 상품 (유효비 ≤ 20%)")
    
    if df.empty:
        st.success("✅ 위험 상품 없음 (모든 상품 유효비 > 20%)")
        return
    
    # 경고 메시지
    st.warning(f"⚠️ 총 {len(df)}개 상품이 유효기한 임박 상태입니다. 즉시 조치가 필요합니다!")
    
    # 컬럼 선택 및 이름 변경
    display_df = df.copy()
    display_df['소비기한'] = pd.to_datetime(display_df['소비기한']).dt.strftime('%Y-%m-%d')
    
    # 재고금액 포맷팅
    display_df['재고금액_표시'] = display_df['재고금액'].apply(lambda x: f"₩{int(x):,}")
    
    # 표시할 컬럼 선택
    display_columns = {
        '로케이션': '로케이션',
        '상품': '상품코드',
        '상품명': '상품명',
        '소비기한': '소비기한',
        '재고수량': '재고수량',
        '유효유통비(%)': '유효비(%)',
        '재고금액_표시': '재고금액'
    }
    
    final_df = display_df[list(display_columns.keys())].rename(columns=display_columns)
    
    # 테이블 표시 (높이 조정)
    st.dataframe(
        final_df,
        use_container_width=True,
        height=min(400, len(final_df) * 35 + 38)  # 동적 높이
    )


def display_low_stock_items_table(df: pd.DataFrame):
    """
    재고 부족 상품 테이블 표시
    
    Args:
        df: 재고 부족 상품 DataFrame
    """
    st.subheader("📉 재고 부족 상품 (가용수량 ≤ 10개)")
    
    if df.empty:
        st.success("✅ 재고 부족 상품 없음")
        return
    
    # 주의 메시지
    st.info(f"ℹ️ 총 {len(df)}개 상품이 재고 부족 상태입니다.")
    
    # 컬럼 선택 및 이름 변경
    display_df = df.copy()
    
    # 재고금액 포맷팅
    display_df['재고금액_표시'] = display_df['재고금액'].apply(lambda x: f"₩{int(x):,}")
    
    # 표시할 컬럼 선택
    display_columns = {
        '로케이션': '로케이션',
        '상품': '상품코드',
        '상품명': '상품명',
        '가용수량': '가용수량',
        '재고수량': '재고수량',
        '유효유통비(%)': '유효비(%)',
        '재고금액_표시': '재고금액'
    }
    
    final_df = display_df[list(display_columns.keys())].rename(columns=display_columns)
    
    # 테이블 표시
    st.dataframe(
        final_df,
        use_container_width=True,
        height=min(400, len(final_df) * 35 + 38)
    )


def display_top_inventory_by_location(df: pd.DataFrame):
    """
    상위 로케이션별 재고 차트 표시
    
    Args:
        df: 로케이션별 재고 집계 DataFrame
    """
    st.subheader("📍 상위 로케이션 (재고금액 기준)")
    
    if df.empty:
        st.warning("데이터가 없습니다")
        return
    
    # 상위 10개만 표시
    top_10 = df.head(10).copy()
    
    # 재고금액을 만원 단위로 변환
    top_10['재고금액_만원'] = (top_10['총_재고금액'] / 10_000).round(0)
    
    # 막대 차트
    st.bar_chart(
        top_10.set_index('로케이션')['재고금액_만원'],
        use_container_width=True,
        color="#4CAF50"  # 초록색
    )
    
    st.caption("단위: 만원")
    
    # 데이터 테이블
    with st.expander("상세 데이터 보기"):
        # 재고금액 포맷팅
        display_df = df.copy()
        display_df['총_재고금액'] = display_df['총_재고금액'].apply(lambda x: f"₩{int(x):,}")
        st.dataframe(display_df, use_container_width=True)


def display_top_inventory_by_product(df: pd.DataFrame):
    """
    상위 재고 상품 차트 표시
    
    Args:
        df: 상품별 재고 집계 DataFrame
    """
    st.subheader("🏆 상위 재고 상품 (재고금액 기준)")
    
    if df.empty:
        st.warning("데이터가 없습니다")
        return
    
    # 상품명 표시를 위한 처리 (상위 10개)
    top_10 = df.head(10).copy()
    top_10['상품_표시'] = top_10['상품명'].str[:20]  # 20자로 제한
    
    # 재고금액을 만원 단위로 변환
    top_10['재고금액_만원'] = (top_10['총_재고금액'] / 10_000).round(0)
    
    # 막대 차트
    st.bar_chart(
        top_10.set_index('상품_표시')['재고금액_만원'],
        use_container_width=True,
        color="#2196F3"  # 파란색
    )
    
    st.caption("단위: 만원")
    
    # 데이터 테이블
    with st.expander("상세 데이터 보기"):
        # 재고금액 포맷팅
        display_df = df.copy()
        display_df['총_재고금액'] = display_df['총_재고금액'].apply(lambda x: f"₩{int(x):,}")
        st.dataframe(display_df, use_container_width=True)


def display_effective_ratio_distribution(df: pd.DataFrame):
    """
    유효유통비 구간별 분포 차트 표시
    
    Args:
        df: 유효비 구간별 분포 DataFrame
    """
    st.subheader("📊 유효유통비 구간별 분포")
    
    if df.empty:
        st.warning("데이터가 없습니다")
        return
    
    # 파이 차트용 데이터 준비
    chart_data = df.set_index('유효비_구간')['상품_수']
    
    # 색상 정의 (위험 -> 우수)
    colors = ['#FF4444', '#FF9800', '#FFC107', '#8BC34A', '#4CAF50']
    
    # 차트 표시
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.bar_chart(
            chart_data,
            use_container_width=True,
            color=colors[0]  # Streamlit 기본 차트는 단색
        )
    
    with col2:
        st.write("**구간별 상품 수**")
        for idx, row in df.iterrows():
            st.write(f"• {row['유효비_구간']}: **{int(row['상품_수'])}개**")
    
    # 총 상품 수 표시
    total = df['상품_수'].sum()
    st.caption(f"총 {int(total)}개 상품")


# ============================================================================
# 재고(Inventory) 탭 컴포넌트
# ============================================================================

def display_inventory_metrics(summary: Dict[str, Any]):
    """
    재고 핵심 지표를 카드 형태로 표시
    
    Args:
        summary: 재고 요약 정보 딕셔너리
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 총 상품 수",
            value=f"{summary.get('총_상품수', 0):,}개"
        )
    
    with col2:
        st.metric(
            label="📊 총 가용수량",
            value=f"{summary.get('총_가용수량', 0):,}개"
        )
    
    with col3:
        total_value = summary.get('총_재고금액', 0)
        if total_value >= 100_000_000:  # 1억 이상
            value_str = f"{total_value/100_000_000:.1f}억원"
        elif total_value >= 10_000_000:  # 1천만 이상
            value_str = f"{total_value/10_000_000:.1f}천만원"
        else:
            value_str = f"{total_value:,}원"
        
        st.metric(
            label="💰 총 재고 금액",
            value=value_str
        )
    
    with col4:
        risky_count = summary.get('위험_상품수', 0)
        st.metric(
            label="⚠️ 위험 상품",
            value=f"{risky_count}개",
            delta=None,
            delta_color="inverse" if risky_count > 0 else "normal"
        )


def display_inventory_summary(summary: Dict[str, Any]):
    """
    재고 추가 요약 정보 표시
    
    Args:
        summary: 재고 요약 정보 딕셔너리
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 평균 유효유통비")
        avg_ratio = summary.get('평균_유효비', 0)
        
        # 유효비에 따른 색상
        if avg_ratio >= 70:
            color = "green"
            status = "양호"
        elif avg_ratio >= 40:
            color = "orange"
            status = "보통"
        else:
            color = "red"
            status = "주의"
        
        st.markdown(f"### :{color}[{avg_ratio}%] ({status})")
    
    with col2:
        st.markdown("#### 📊 유효비 구간별 분포")
        distribution = summary.get('유효비_구간별_분포', {})
        
        if distribution:
            # 데이터프레임으로 변환
            df_dist = pd.DataFrame([
                {"구간": k, "상품수": v}
                for k, v in distribution.items()
            ])
            
            # 구간 순서 정렬
            order = ['위험(≤20%)', '주의(21-50%)', '정상(51-100%)']
            df_dist['구간'] = pd.Categorical(df_dist['구간'], categories=order, ordered=True)
            df_dist = df_dist.sort_values('구간')
            
            # 바 차트
            st.bar_chart(df_dist.set_index('구간'))


def display_risky_products_table(df: pd.DataFrame):
    """
    유효비 위험 상품 테이블 표시 (빨간색 강조)
    
    Args:
        df: 위험 상품 DataFrame
    """
    if df.empty:
        st.success("✅ 위험 상품이 없습니다!")
        return
    
    st.markdown(f"#### ⚠️ 유효비 위험 상품 ({len(df)}개)")
    st.warning("유효유통비가 20% 이하인 상품들입니다. 빠른 조치가 필요합니다.")
    
    # 테이블 표시용 데이터 준비
    display_df = df.copy()
    
    # 재고금액 포맷
    display_df['재고금액'] = display_df['재고금액'].apply(lambda x: f"{int(x):,}원")
    display_df['단가'] = display_df['단가'].apply(lambda x: f"{int(x):,}원")
    
    # 유효비에 따라 스타일 적용
    def highlight_risky(row):
        ratio = row['유효유통비(%)']
        if ratio <= 10:
            return ['background-color: #ffcccc'] * len(row)  # 진한 빨강
        elif ratio <= 20:
            return ['background-color: #ffe6e6'] * len(row)  # 연한 빨강
        return [''] * len(row)
    
    styled_df = display_df.style.apply(highlight_risky, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=300)


def display_inventory_table(df: pd.DataFrame, show_filters: bool = True):
    """
    전체 재고 목록 테이블 표시
    
    Args:
        df: 재고 DataFrame
        show_filters: 필터 옵션 표시 여부
    """
    st.markdown("#### 📋 전체 재고 목록")
    
    if show_filters:
        # 필터 옵션
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 유효비 필터
            ratio_filter = st.selectbox(
                "유효비 필터",
                ["전체", "위험(≤20%)", "주의(21-50%)", "정상(51-100%)"]
            )
        
        with col2:
            # 정렬 기준
            sort_by = st.selectbox(
                "정렬 기준",
                ["유효유통비(%)", "가용수량", "재고금액"]
            )
        
        with col3:
            # 정렬 순서
            sort_order = st.radio(
                "정렬 순서",
                ["오름차순", "내림차순"],
                horizontal=True
            )
        
        # 필터 적용
        filtered_df = df.copy()
        
        if ratio_filter == "위험(≤20%)":
            filtered_df = filtered_df[filtered_df['유효유통비(%)'] <= 20]
        elif ratio_filter == "주의(21-50%)":
            filtered_df = filtered_df[(filtered_df['유효유통비(%)'] > 20) & 
                                     (filtered_df['유효유통비(%)'] <= 50)]
        elif ratio_filter == "정상(51-100%)":
            filtered_df = filtered_df[filtered_df['유효유통비(%)'] > 50]
        
        # 재고금액 계산 (정렬용)
        if '재고금액' not in filtered_df.columns:
            filtered_df['재고금액'] = filtered_df['가용수량'] * filtered_df['단가']
        
        # 정렬 적용
        ascending = (sort_order == "오름차순")
        filtered_df = filtered_df.sort_values(sort_by, ascending=ascending)
        
        st.caption(f"총 {len(filtered_df)}개 상품")
    else:
        filtered_df = df
    
    # 테이블 표시용 데이터 준비
    display_df = filtered_df.copy()
    
    # 금액 포맷
    if '재고금액' in display_df.columns:
        display_df['재고금액'] = display_df['재고금액'].apply(lambda x: f"{int(x):,}원")
    display_df['단가'] = display_df['단가'].apply(lambda x: f"{int(x):,}원")
    
    # 테이블 표시
    st.dataframe(display_df, use_container_width=True, height=400)


def display_low_stock_table(df: pd.DataFrame):
    """
    가용수량 부족 상품 테이블 표시
    
    Args:
        df: 가용수량 부족 상품 DataFrame
    """
    if df.empty:
        st.info("가용수량 부족 상품이 없습니다.")
        return
    
    st.markdown(f"#### 📦 가용수량 부족 상품 ({len(df)}개)")
    st.info("가용수량이 10개 이하인 상품들입니다.")
    
    # 테이블 표시용 데이터 준비
    display_df = df.copy()
    
    # 재고금액 포맷
    display_df['재고금액'] = display_df['재고금액'].apply(lambda x: f"{int(x):,}원")
    display_df['단가'] = display_df['단가'].apply(lambda x: f"{int(x):,}원")
    
    st.dataframe(display_df, use_container_width=True, height=300)
