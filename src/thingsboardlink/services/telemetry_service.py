"""
thingsboardlink 遥测服务模块

本模块提供遥测数据相关的 API 调用功能。
包括遥测数据的上传、查询、历史数据获取等操作。
"""

import time
from typing import List, Optional, Dict, Any, Union

from ..models import TelemetryData, TimeseriesData
from ..exceptions import ValidationError, TelemetryError, NotFoundError


class TelemetryService:
    """
    遥测服务类

    提供遥测数据相关的所有操作。
    包括数据上传、最新数据获取、历史数据查询等功能。
    """

    def __init__(self, client):
        """
        初始化遥测服务

        Args:
            client: ThingsBoardClient 实例
        """
        self.client = client

    