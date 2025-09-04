"""
thingsboardlink 属性服务模块

本模块提供属性管理相关的 API 调用功能。
包括客户端属性、服务端属性和共享属性的读写操作。
"""

from typing import List, Optional, Dict, Any, Union

from ..models import Attribute, AttributeScope
from ..exceptions import ValidationError, NotFoundError, APIError

class AttributeService:
    """
    属性服务类

    提供属性管理相关的所有操作。
    支持客户端属性、服务端属性和共享属性的完整管理。
    """

    def __init__(self,client):
        """
        初始化属性服务

        Args:
            client: ThingsBoardClient 实例
        """
        self.client = client