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

    def post_telemetry_with_device_token(self,
                                         device_token: str,
                                         telemetry_data: Union[Dict[str, Any], List[TelemetryData], TelemetryData],
                                         timestamp: Optional[int] = None) -> bool:
        """
        使用设备令牌上传遥测数据

        Args:
            device_token: 设备访问令牌
            telemetry_data: 遥测数据
            timestamp: 时间戳（毫秒），可选

        Returns:
            bool: 上传是否成功
        """
        if not device_token or not device_token.strip():
            raise ValidationError(
                field_name="device_token",
                expected_type="非空字符串",
                actual_value=device_token,
                message="设备令牌不能为空"
            )

        try:
            # 统一时间戳
            if timestamp is None:
                timestamp = int(time.time() * 1000)

            # 转换数据格式
            if isinstance(telemetry_data, dict):
                # 字典格式：{"key1": value1, "key2": value2}
                payload = {
                    "ts": timestamp,
                    "values": telemetry_data
                }
            elif isinstance(telemetry_data, TelemetryData):
                # 单个 TelemetryData 对象
                payload = telemetry_data.to_dict()
            elif isinstance(telemetry_data, list):
                # TelemetryData 对象列表
                if not telemetry_data:
                    raise ValidationError(
                        field_name="telemetry_data",
                        message="遥测数据列表不能为空 | Telemetry data list cannot be empty"
                    )

                # 按时间戳分组数据
                grouped_data = {}
                for item in telemetry_data:
                    if not isinstance(item, TelemetryData):
                        raise ValidationError(
                            field_name="telemetry_data",
                            expected_type="TelemetryData 对象列表 | List of TelemetryData objects",
                            actual_value=type(item).__name__
                        )

                    ts = item.timestamp or timestamp
                    if ts not in grouped_data:
                        grouped_data[ts] = {}
                    grouped_data[ts][item.key] = item.value

                # 转换为 API 格式
                if len(grouped_data) == 1:
                    # 单个时间戳
                    ts, values = next(iter(grouped_data.items()))
                    payload = {"ts": ts, "values": values}
                else:
                    # 多个时间戳
                    payload = [
                        {"ts": ts, "values": values}
                        for ts, values in grouped_data.items()
                    ]
            else:
                raise ValidationError(
                    field_name="telemetry_data",
                    expected_type="Dict, TelemetryData 或 List[TelemetryData] | Dict, TelemetryData or List[TelemetryData]",
                    actual_value=type(telemetry_data).__name__
                )

            # ThingsBoard 设备遥测数据上传端点
            response = self.client.post(f"/api/v1/{device_token}/telemetry", data=payload)

            if response.status_code == 200:
                return True
            else:
                raise TelemetryError(
                    f"遥测数据上传失败，状态码: {response.status_code}"
                )

        except Exception as e:
            if isinstance(e, (ValidationError, TelemetryError)):
                raise
            raise TelemetryError(
                f"上传遥测数据失败: {str(e)}"
            )
