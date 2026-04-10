import sys
sys.path.insert(0, 'C:/Projects/WMS-DashBoard/flask_app')

try:
    from api.dashboard import bp
    print("Import OK!")
    print(f"Blueprint name: {bp.name}")
except Exception as e:
    print(f"Error: {e}")
