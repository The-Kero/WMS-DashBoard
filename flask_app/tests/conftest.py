"""
pytest configuration and fixtures for Flask WMS Dashboard tests
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add dashboard collector path to sys.path
dashboard_path = Path(__file__).parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

@pytest.fixture
def sample_inbound_csv():
    """실제 입고 현황 CSV 파일 경로 (오늘 또는 어제 날짜)"""
    today = datetime.now().strftime("%Y%m%d")
    base_path = "C:/OSIS_AUTO/Inbound Status"
    
    # 오늘 날짜 파일 우선
    today_file = f"{base_path}/integrated_inbound_{today}.csv"
    if Path(today_file).exists():
        return today_file
    
    # 어제 날짜 파일
    yesterday = datetime.now().replace(day=datetime.now().day-1).strftime("%Y%m%d")
    yesterday_file = f"{base_path}/integrated_inbound_{yesterday}.csv"
    return yesterday_file

@pytest.fixture
def sample_outbound_csv():
    """실제 출고 현황 CSV 파일 경로"""
    today = datetime.now().strftime("%Y%m%d")
    base_path = "C:/OSIS_AUTO/Outbound Status"
    
    today_file = f"{base_path}/outbound_merged_{today}.csv"
    if Path(today_file).exists():
        return today_file
    
    yesterday = datetime.now().replace(day=datetime.now().day-1).strftime("%Y%m%d")
    yesterday_file = f"{base_path}/outbound_merged_{yesterday}.csv"
    return yesterday_file

@pytest.fixture
def sample_inventory_csv():
    """실제 재고 현황 CSV 파일 경로"""
    today = datetime.now().strftime("%Y%m%d")
    base_path = "C:/OSIS_AUTO/inventory_status"
    
    today_file = f"{base_path}/inventory_status_{today}.csv"
    if Path(today_file).exists():
        return today_file
    
    yesterday = datetime.now().replace(day=datetime.now().day-1).strftime("%Y%m%d")
    yesterday_file = f"{base_path}/inventory_status_{yesterday}.csv"
    return yesterday_file

@pytest.fixture
def client():
    """Flask 테스트 클라이언트"""
    # Flask app import는 테스트 실행 시점에
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client
