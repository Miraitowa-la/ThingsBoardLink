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

    def post_telemetry(self,
                       device_id: str,
                       telemetry_data: Union[Dict[str, Any], List[TelemetryData], TelemetryData],
                       timestamp: Optional[int] = None) -> bool:
        """
        上传遥测数据

        Args:
            device_id: 设备 ID
            telemetry_data: 遥测数据
            timestamp: 时间戳（毫秒），可选

        Returns:
            bool: 上传是否成功

        Raises:
            ValidationError: 参数验证失败时抛出
            TelemetryError: 遥测数据上传失败时抛出
        """
        if not device_id or not device_id.strip():
            raise ValidationError(
                field_name="device_id",
                expected_type="非空字符串",
                actual_value=device_id,
                message="设备 ID 不能为空"
            )

        if not telemetry_data:
            raise ValidationError(
                field_name="telemetry_data",
                expected_type="非空数据",
                actual_value=telemetry_data,
                message="遥测数据不能为空"
            )

        try:
            # 获取设备凭证
            credentials = self.client.device_service.get_device_credentials(device_id)

            if not credentials or not credentials.credentials_value:
                raise TelemetryError(
                    "无法获取设备访问令牌"
                )

            # 使用设备令牌上传遥测数据
            return self.post_telemetry_with_device_token(
                device_token=credentials.credentials_value,
                telemetry_data=telemetry_data,
                timestamp=timestamp
            )

        except Exception as e:
            if isinstance(e, (ValidationError, TelemetryError)):
                raise
            raise TelemetryError(
                f"上传遥测数据失败: {str(e)}"
            )

