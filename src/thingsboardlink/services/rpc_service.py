"""
thingsboardlink RPC 服务模块

本模块提供 RPC（远程过程调用）相关的 API 调用功能。
包括单向和双向 RPC 调用，支持设备控制和通信。
"""

import time
from typing import Optional, Dict, Any, Union

from ..models import RPCRequest, RPCResponse
from ..exceptions import ValidationError, RPCError, TimeoutError, NotFoundError


class RpcService:
    """
    RPC 服务类

    提供 RPC 调用相关的所有操作。
    支持单向和双向 RPC 调用，以及超时处理。
    """

    def __init__(self, client):
        """
        初始化 RPC 服务

        Args:
            client: ThingsBoardClient 实例
        """
        self.client = client

    def send_one_way_rpc(self,
                         device_id: str,
                         method: str,
                         params: Optional[Dict[str, Any]] = None) -> bool:
        """
        发送单向 RPC 请求

        单向 RPC 不等待设备响应，适用于设备控制命令。

        Args:
            device_id: 设备 ID
            method: RPC 方法名
            params: RPC 参数

        Returns:
            bool: 发送是否成功

        Raises:
            ValidationError: 参数验证失败时抛出
            RPCError: RPC 调用失败时抛出
        """
        if not device_id or not device_id.strip():
            raise ValidationError(
                field_name="device_id",
                expected_type="非空字符串",
                actual_value=device_id,
                message="设备 ID 不能为空"
            )

        if not method or not method.strip():
            raise ValidationError(
                field_name="method",
                expected_type="非空字符串",
                actual_value=method,
                message="RPC 方法名不能为空"
            )

        rpc_request = RPCRequest(
            method=method.strip(),
            params=params or {},
            persistent=False
        )

        try:
            endpoint = f"/api/plugins/rpc/oneway/{device_id}"
            response = self.client.post(
                endpoint,
                data=rpc_request.to_dict()
            )

            return response.status_code == 200

        except Exception as e:
            raise RPCError(
                f"发送单向 RPC 请求失败: {str(e)}",
                method_name=method,
                device_id=device_id
            )
