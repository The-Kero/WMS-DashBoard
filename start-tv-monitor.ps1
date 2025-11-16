# WMS Dashboard TV Monitor - Docker 실행 스크립트
# 2025-11-09 작성

Write-Host "================================" -ForegroundColor Cyan
Write-Host "WMS Dashboard TV Monitor 시작" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. 기존 컨테이너 정리
Write-Host "[1/4] 기존 컨테이너 정리 중..." -ForegroundColor Yellow
docker stop wms-tv-monitor 2>$null
docker rm wms-tv-monitor 2>$null

# 2. Docker 이미지 빌드
Write-Host "[2/4] Docker 이미지 빌드 중..." -ForegroundColor Yellow
docker build -f Dockerfile.nginx -t wms-tv-monitor:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 이미지 빌드 실패!" -ForegroundColor Red
    exit 1
}

# 3. 컨테이너 실행
Write-Host "[3/4] 컨테이너 실행 중..." -ForegroundColor Yellow
docker run -d `
    --name wms-tv-monitor `
    -p 8080:80 `
    wms-tv-monitor:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 컨테이너 실행 실패!" -ForegroundColor Red
    exit 1
}

# 4. 로컬 IP 주소 확인
Write-Host "[4/4] 네트워크 정보 확인 중..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✅ WMS TV Monitor 실행 성공!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# 로컬 IP 주소 가져오기
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress

Write-Host "📺 접속 URL:" -ForegroundColor Cyan
Write-Host "   - 로컬: http://localhost:8080" -ForegroundColor White
Write-Host "   - 네트워크: http://${localIP}:8080" -ForegroundColor White
Write-Host ""
Write-Host "🔧 컨테이너 관리:" -ForegroundColor Cyan
Write-Host "   - 중지: docker stop wms-tv-monitor" -ForegroundColor White
Write-Host "   - 시작: docker start wms-tv-monitor" -ForegroundColor White
Write-Host "   - 삭제: docker rm -f wms-tv-monitor" -ForegroundColor White
Write-Host "   - 로그: docker logs wms-tv-monitor" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: 100인치 TV 브라우저에서 위 네트워크 URL로 접속하세요!" -ForegroundColor Yellow
Write-Host ""
