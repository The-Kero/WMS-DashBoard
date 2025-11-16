# WMS Dashboard V6 - Docker 배포 가이드

## 📋 필요 파일
- `Dockerfile`: nginx 이미지 설정
- `docker-compose.yml`: 컨테이너 실행 설정
- `ourhome_layout_v6.html`: 대시보드 HTML
- `ourhome_ci.png`: 로고 이미지

## 🚀 실행 방법

### 1. Docker 컨테이너 빌드 및 실행
```bash
cd C:\Projects\WMS-DashBoard\Layout
docker-compose up -d --build
```

### 2. 접속 확인
- **로컬**: http://localhost:8080
- **네트워크**: http://10.60.27.130:8080

### 3. 로그 확인
```bash
docker-compose logs -f
```

### 4. 컨테이너 상태 확인
```bash
docker ps | grep wms-dashboard
```

## 🔄 업데이트 방법

### HTML 파일만 수정한 경우
```bash
docker-compose down
docker-compose up -d --build
```

### 완전 재시작
```bash
docker-compose down
docker system prune -f
docker-compose up -d --build
```

## 🛑 중지 및 제거

### 컨테이너 중지
```bash
docker-compose stop
```

### 컨테이너 중지 및 제거
```bash
docker-compose down
```

### 이미지까지 완전 삭제
```bash
docker-compose down --rmi all --volumes
```

## 🔍 트러블슈팅

### 포트 8080이 이미 사용중일 때
```bash
# 기존 컨테이너 확인
docker ps -a | grep 8080

# 해당 컨테이너 중지
docker stop <container_id>
```

### 방화벽 설정 (Windows)
```powershell
# PowerShell 관리자 권한으로 실행
New-NetFirewallRule -DisplayName "WMS Dashboard" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

## 📊 접속 정보
- **서버 IP**: 10.60.27.130
- **포트**: 8080
- **URL**: http://10.60.27.130:8080
- **해상도**: 1920x1080 (100인치 최적화)

## 🎯 100인치 모니터 설정 팁
1. 브라우저 전체화면: F11 키
2. 자동 새로고침: 필요시 브라우저 확장 프로그램 사용
3. 화면 보호기 비활성화
4. 전원 절약 모드 비활성화