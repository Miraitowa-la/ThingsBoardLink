"""
thingsboardlink 设备服务模块

本模块提供设备管理相关的 API 调用功能。
包括设备的创建、查询、更新、删除以及凭证管理等操作。
"""
from typing import List, Optional, Dict, Any

from ..models import Device, DeviceCredentials, PageData
from ..exceptions import NotFoundError, DeviceError, ValidationError


class DeviceService:
    """
    设备服务类

    提供设备管理相关的所有操作。
    包括 CRUD 操作、凭证管理和批量查询等功能。
    """

    def __init__(self, client):
        """
        初始化设备服务

        Args:
            client: ThingsBoardClient 实例
        """
        self.client = client

    def create_device(self,
                      name: str,
                      device_type: str = "default",
                      label: Optional[str] = None,
                      additional_info: Optional[Dict[str, Any]] = None) -> Device:
        """
        创建设备

        Args:
            name: 设备名称
            device_type: 设备类型
            label: 设备标签
            additional_info: 附加信息

        Returns:
            Device: 创建的设备对象

        Raises:
            ValidationError: 参数验证失败时抛出
            DeviceError: 设备创建失败时抛出
        """
        if not name or not name.strip():
            raise ValidationError(
                field_name="name",
                expected_type="非空字符串",
                actual_value=name,
                message="设备名称不能为空"
            )

        device = Device(
            name=name.strip(),
            type=device_type,
            label=label,
            additional_info=additional_info or {}
        )

        try:
            response = self.client.post(
                "/api/device",
                data=device.to_dict()
            )

            device_data = response.json()
            return Device.from_dict(device_data)

        except Exception as e:
            raise DeviceError(
                message=f"创建设备失败: {str(e)}",
                device_name=name
            )
