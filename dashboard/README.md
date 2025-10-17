# WMS 대시보드 - 설치 및 실행 가이드

## 📦 설치

### 1. 저장소 복제
```bash
git clone https://github.com/The-Kero/WMS-DashBoard.git
cd WMS-DashBoard/dashboard
```

### 2. 가상환경 설정
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 설정 파일 생성
```bash
copy config\config.example.yaml config\config.yaml
# 또는
cp config/config.example.yaml config/config.yaml
```

### 5. 설정 파일 수정
`config/config.yaml` 파일을 열어 데이터 경로를 수정하세요:
```yaml
data_sources:
  inbound: "C:/OSIS_AUTO/입고정보/inbound_merged_*.csv"
  # ... 나머지 경로 수정
```

---

## 🚀 실행

### 개발 모드
```bash
streamlit run main_dashboard.py
```

### 테스트 실행
```bash
pytest tests/ -v
```

---

## 📁 프로젝트 구조

```
dashboard/
├── src/                  # 소스 코드
│   ├── data/            # 데이터 레이어
│   ├── business/        # 비즈니스 로직
│   ├── ui/              # UI 컴포넌트
│   └── utils/           # 유틸리티
│
├── config/              # 설정 파일
├── tests/               # 테스트
└── main_dashboard.py    # 메인 진입점
```

---

## ⚙️ 기능

- ✅ 4대 핵심 지표 표시
- ✅ 10종 긴급 알림
- ✅ 시간대별 레이아웃 전환
- ✅ 30초 자동 갱신

---

## 🐛 문제 해결

### 모듈을 찾을 수 없음
```bash
# PYTHONPATH 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 데이터 파일을 찾을 수 없음
- config/config.yaml의 경로 확인
- 5개 프로그램 정상 실행 확인

### 포트 충돌
```bash
streamlit run main_dashboard.py --server.port 8502
```

---

더 자세한 내용은 [프로젝트 문서](../docs/)를 참고하세요.