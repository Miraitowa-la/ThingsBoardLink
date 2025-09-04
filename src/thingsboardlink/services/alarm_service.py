"""
thingsboardlink 警报服务模块

本模块提供警报管理相关的 API 调用功能。
包括警报的创建、查询、确认、清除等操作。
"""

from typing import List, Optional, Dict, Any

from ..models import Alarm, AlarmSeverity, AlarmStatus, PageData
from ..exceptions import ValidationError, AlarmError, NotFoundError


class AlarmService:
    """
    警报服务类

    提供警报管理相关的所有操作。
    包括警报的创建、查询、状态管理等功能。
    """

    def __init__(self, client):
        """
        初始化警报服务

        Args:
            client: ThingsBoardClient 实例
        """
        self.client = client