"""
데이터 수집기 패키지
"""

from .base import BaseCollector
from .inbound import InboundCollector

__all__ = ['BaseCollector', 'InboundCollector']
