# TV 모니터 대시보드 UI/UX 개선 - 기술 상세 문서

## 📐 ourhome 레이아웃 구조 완전 분석

### HTML 구조

```html
<!-- 메인 컨테이너 -->
<div class="gaugeWrap" id="wrap1">
    
    <!-- 카드 1 -->
    <div class="gaugeItem">
        <h2>제목</h2>
        <div class="chartGauge">
            <!-- Toast UI Chart 도넛/게이지 -->
        </div>
        <div class="gaugeTem">
            <em>27</em><span>°C</span>
        </div>
        <div class="chartLine">
            <canvas><!-- Chart.js 라인 차트 --></canvas>
        </div>
    </div>
    
    <!-- 카드 2, 3... 반복 -->
    
</div>

<!-- 경고 팝업 -->
<div class="pageLayer type074">
    <div class="pageMask"></div>
    <div class="pageInner typeWarning">
        <div class="modalInner">
            <div class="topBox">
                <img> <h2>경고 제목</h2>
            </div>
            <div class="middleBox">
                경고 메시지
            </div>
        </div>
    </div>
</div>
```

### CSS 클래스 구조

```css
/* 메인 Wrap */
.gaugeWrap {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
}

/* 카드 (정상) */
.gaugeItem {
    background: #EEF0F5;
    border: 3px solid #E7E8EB;
    border-radius: 15px;
    padding: 30px;
}

/* 카드 (경고) */
.gaugeItem.ingWarning {
    background: #FAE3E4;
    border: 3px solid #F05E5E;
    animation: pulse 2s infinite;
}

/* 제목 */
.gaugeItem h2 {
    font-size: 32pt;
    color: #56667B;
}

/* 큰 숫자 */
.gaugeTem em {
    font-size: 72pt;
    color: #2C365C;
    font-weight: bold;
}

/* 팝업 */
.pageLayer {
    position: fixed;
    z-index: 9999;
}

.pageMask {
    background: rgba(0, 0, 0, 0.7);
}
```

### JavaScript 로직

```javascript
// Vue.js 데이터 바인딩
data() {
    return {
        temp1: {
            data: { fr_temp: 0 },
            limit: { ref_vl: 0, ref_vl2: 20 }
        },
        predictionMsg1: "",
        layerOpenFlag1: false
    }
}

// 조건부 클래스
:class="temp1.data.fr_temp > temp1.limit.ref_vl2 ? 
        ['gaugeItem', 'ingWarning'] : ['gaugeItem']"

// 데이터 표시
<em>{{temp1.data.fr_temp}}</em>

// 차트 생성 (Toast UI Chart)
gaugeCharts[chartId] = new toastui.Chart.gaugeChart({
    el: document.getElementById(chartId),
    data: { series: [{ data: [temp] }] },
    options: {
        circularAxis: { scale: { min: 0, max: 20 } },
        plot: { bands: [
            { range: [0, 5], color: '#F05E5E' },
            { range: [5, 15], color: '#60CB2E' },
            { range: [15, 20], color: '#F05E5E' }
        ]}
    }
});

// 라인 차트 (Chart.js)
new Chart(ctx, {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            data: temperatures,
            borderColor: '#1b59f8',
            fill: true,
            tension: 0.4
        }]
    }
});
```

---

## 🎨 색상 시스템

### 상태별 색상
```javascript
정상 (Normal):
  - 배경: #EEF0F5
  - 테두리: #E7E8EB
  - 텍스트: #2C365C
  - 강조: #60CB2E (초록)

진행중 (Progress):
  - 강조: #FAB03C (주황)

경고 (Warning):
  - 배경: #FAE3E4
  - 테두리: #F05E5E
  - 텍스트: #F05E5E
  - 강조: #F05E5E (빨강)
```

### 차트 색상
```javascript
성공: #60CB2E (초록)
주의: #FAB03C (주황)
위험: #F05E5E (빨강)
정보: #1b59f8 (파랑)
```

---

## 📊 차트 라이브러리

### Toast UI Chart (게이지/도넛)
```javascript
// CDN
https://uicdn.toast.com/chart/latest/toastui-chart.min.js
https://uicdn.toast.com/chart/latest/toastui-chart.min.css

// 사용법
const chart = new toastui.Chart.gaugeChart({
    el: element,
    data: { series: [{ data: [value] }] },
    options: { ... }
});
```

### Chart.js (라인 차트)
```javascript
// CDN
https://cdn.jsdelivr.net/npm/chart.js

// 사용법
new Chart(canvas, {
    type: 'line',
    data: { ... },
    options: { ... }
});
```

---

## 🔄 Streamlit 통합 방법

### Option 1: st.components.v1.html()
```python
import streamlit as st
import streamlit.components.v1 as components

# HTML 생성
def create_tv_dashboard(data):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            /* ourhome CSS */
            .gaugeWrap {{ display: grid; ... }}
            .gaugeItem {{ background: #EEF0F5; ... }}
        </style>
    </head>
    <body>
        <div class="gaugeWrap">
            <div class="gaugeItem">
                <h2>오늘 입고</h2>
                <div class="gaugeTem">
                    <em>{data['inbound_count']}</em><span>건</span>
                </div>
            </div>
        </div>
        <script>
            // 차트 생성 JavaScript
        </script>
    </body>
    </html>
    '''
    return html

# 표시
html_content = create_tv_dashboard(data)
components.html(html_content, height=1080, scrolling=False)

# 30초마다 자동 갱신
import time
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

if time.time() - st.session_state.last_update > 30:
    st.session_state.last_update = time.time()
    st.rerun()
```

### Option 2: st.markdown() with HTML
```python
# 간단한 방식
st.markdown(html_content, unsafe_allow_html=True)
```

---

## 🔄 자동 화면 전환

```javascript
let currentScreen = 0;
const screens = ['wrap1', 'wrap2', 'wrap3']; // 입고, 출고, 재고
const displayTime = 10000; // 10초

function rotateScreens() {
    // 모든 화면 숨김
    screens.forEach(id => {
        document.getElementById(id).style.display = 'none';
    });
    
    // 현재 화면 표시
    document.getElementById(screens[currentScreen]).style.display = 'block';
    
    // 다음 화면으로
    currentScreen = (currentScreen + 1) % screens.length;
}

// 시작
setInterval(rotateScreens, displayTime);
rotateScreens(); // 즉시 첫 화면 표시
```

---

## 📡 실시간 데이터 갱신

```python
# Streamlit에서
import time

def get_dashboard_data():
    """Collector에서 데이터 수집"""
    from dashboard.src.data.collectors.inbound import InboundCollector
    from dashboard.src.data.collectors.outbound import OutboundCollector
    from dashboard.src.data.collectors.inventory import InventoryCollector
    
    inbound = InboundCollector()
    outbound = OutboundCollector()
    inventory = InventoryCollector()
    
    return {
        'inbound': {
            'total': inbound.get_total_count(),
            'progress': inbound.get_progress_rate(),
            'waiting': inbound.get_waiting_count()
        },
        'outbound': {
            'total': outbound.get_total_count(),
            'progress': outbound.get_progress_rate(),
            'caution': outbound.get_caution_count()
        },
        'inventory': {
            'total': inventory.get_product_count(),
            'available': inventory.get_available_quantity(),
            'risky': inventory.get_risky_count()
        }
    }

# 자동 갱신
while True:
    data = get_dashboard_data()
    
    # 경고 체크
    warnings = []
    if data['inventory']['risky'] > 10:
        warnings.append({
            'title': '재고 부족 경고',
            'message': f'{data["inventory"]["risky"]}건 발생'
        })
    
    # 화면 갱신
    display_dashboard(data, warnings)
    
    time.sleep(30)  # 30초 대기
```

---

## 🚨 경고 시스템

```javascript
// 경고 조건 체크
function checkWarnings(data) {
    const warnings = [];
    
    if (data.inventory_risky > 10) {
        warnings.push({
            type: 'danger',
            title: '재고 부족 경고',
            message: `재고 부족 상품 ${data.inventory_risky}건 발생`
        });
    }
    
    if (data.inbound_waiting > 50) {
        warnings.push({
            type: 'warning',
            title: '입고 대기 주의',
            message: `대기 상품 ${data.inbound_waiting}건`
        });
    }
    
    return warnings;
}

// 경고 표시
function showWarning(warning) {
    const layer = document.getElementById('warningLayer');
    document.querySelector('.modalInner h2').textContent = warning.title;
    document.querySelector('.middleBox').textContent = warning.message;
    layer.classList.add('active');
    
    // 10초 후 자동 닫기
    setTimeout(() => {
        layer.classList.remove('active');
    }, 10000);
}
```

---

## 📁 파일 구조

```
C:\Projects\WMS-DashBoard\
├── ourhome.pcapng                  # 원본 pcap 파일
├── ourhome_page.html               # 추출한 HTML
├── PROJECT_DIARY.md                # 작업 일지
├── NEXT_CHAT_GUIDE_TVUI.md         # 다음 대화 가이드
├── TV_UI_TECHNICAL_DOC.md          # 이 문서
└── dashboard\
    └── app.py                      # Streamlit 앱 (수정 예정)
```

---

**이 문서는 기술 참고용입니다. 다음 대화 시 NEXT_CHAT_GUIDE_TVUI.md를 먼저 읽으세요!**
