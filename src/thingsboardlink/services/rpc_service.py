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
