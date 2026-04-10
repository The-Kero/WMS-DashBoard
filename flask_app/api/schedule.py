# -*- coding: utf-8 -*-
"""
스케줄 관리 API
카드4 냉장파트 스케줄 CRUD
"""

from flask import Blueprint, jsonify, request
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('schedule', __name__, url_prefix='/api')

# schedule.json 경로
SCHEDULE_FILE = Path(__file__).parent.parent / 'data' / 'schedule.json'


def load_schedule():
    """JSON 파일에서 스케줄 로드"""
    try:
        if SCHEDULE_FILE.exists():
            with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"스케줄 로드 실패: {e}")
        return []


def save_schedule(data):
    """스케줄을 JSON 파일에 저장"""
    try:
        # data 폴더 없으면 생성
        SCHEDULE_FILE.parent.mkdir(exist_ok=True)
        with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"스케줄 저장 실패: {e}")
        return False


@bp.route('/schedule', methods=['GET'])
def get_schedule():
    """전체 스케줄 조회"""
    try:
        schedules = load_schedule()
        # 날짜순 정렬
        schedules.sort(key=lambda x: x.get('date', ''))
        return jsonify({
            'success': True,
            'data': schedules,
            'count': len(schedules)
        })
    except Exception as e:
        logger.error(f"스케줄 조회 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/schedule', methods=['POST'])
def add_schedule():
    """스케줄 추가"""
    try:
        data = request.get_json()
        
        # 필수 필드 검증
        if not data or 'date' not in data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'date, content 필드 필수'
            }), 400
        
        # 타입 기본값
        schedule_type = data.get('type', 'event')
        valid_types = ['birthday', 'leave', 'education', 'event']
        if schedule_type not in valid_types:
            schedule_type = 'event'
        
        new_item = {
            'date': data['date'],
            'content': data['content'],
            'type': schedule_type
        }
        
        schedules = load_schedule()
        schedules.append(new_item)
        
        if save_schedule(schedules):
            logger.info(f"스케줄 추가: {new_item}")
            return jsonify({
                'success': True,
                'message': '일정이 추가되었습니다',
                'data': new_item
            })
        else:
            return jsonify({'success': False, 'error': '저장 실패'}), 500
            
    except Exception as e:
        logger.error(f"스케줄 추가 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/schedule', methods=['DELETE'])
def delete_schedule():
    """스케줄 삭제"""
    try:
        data = request.get_json()
        
        if not data or 'date' not in data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'date, content 필드 필수'
            }), 400
        
        schedules = load_schedule()
        original_count = len(schedules)
        
        # 일치하는 항목 삭제
        schedules = [
            s for s in schedules 
            if not (s['date'] == data['date'] and s['content'] == data['content'])
        ]
        
        if len(schedules) == original_count:
            return jsonify({
                'success': False,
                'error': '삭제할 일정을 찾을 수 없습니다'
            }), 404
        
        if save_schedule(schedules):
            logger.info(f"스케줄 삭제: {data['date']} - {data['content']}")
            return jsonify({
                'success': True,
                'message': '일정이 삭제되었습니다'
            })
        else:
            return jsonify({'success': False, 'error': '저장 실패'}), 500
            
    except Exception as e:
        logger.error(f"스케줄 삭제 실패: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
