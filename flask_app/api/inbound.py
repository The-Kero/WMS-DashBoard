# -*- coding: utf-8 -*-
"""입고 현황 API"""

from flask import Blueprint, jsonify
from datetime import datetime
import sys
from pathlib import Path
import logging

# Collector import
dashboard_path = Path(__file__).parent.parent.parent / "dashboard"
sys.path.insert(0, str(dashboard_path))

from src.data.collectors.inbound import InboundCollector

# Blueprint 생성
bp = Blueprint('inbound', __name__, url_prefix='/api')

# 로거 설정
logger = logging.getLogger(__name__)


@bp.route('/inbound', methods=['GET'])
def get_inbound():
    """
    입고 현황 데이터 조회 API
    
    Returns:
        JSON: {
            'success': True/False,
            'summary': {...},
            'data': [...],
            'timestamp': 'ISO 8601 형식'
        }
    """
    try:
        logger.info("입고 데이터 조회 시작")
        
        # 오늘 날짜로 파일 경로 설정
        today = datetime.now().strftime("%Y%m%d")
        file_path = f"C:/OSIS_AUTO/Inbound Status/integrated_inbound_{today}.csv"
        
        # Collector 직접 사용
        collector = InboundCollector(file_path=file_path, encoding='utf-8-sig')
        summary = collector.get_summary()
        data = collector.get_data()
        
        logger.info(f"입고 데이터 조회 성공: {len(data)}건")
        
        return jsonify({
            'success': True,
            'summary': summary,
            'data': data.to_dict('records'),
            'timestamp': datetime.now().isoformat()
        })
    
    except FileNotFoundError as e:
        logger.error(f"파일 없음: {str(e)}")
        today = datetime.now().strftime("%Y%m%d")
        return jsonify({
            'success': False,
            'error': '파일을 찾을 수 없습니다',
            'message': f'integrated_inbound_{today}.csv 파일이 없습니다'
        }), 404
    
    except ValueError as e:
        logger.warning(f"데이터 검증 실패: {str(e)}")
        return jsonify({
            'success': False,
            'error': '데이터 검증 실패',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"입고 API 오류: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': '서버 오류',
            'message': str(e)
        }), 500
