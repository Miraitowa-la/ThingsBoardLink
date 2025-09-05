"""
thingsboardlink 关系服务模块

本模块提供实体关系管理相关的 API 调用功能。
包括实体间关系的创建、删除、查询等操作。
"""

from typing import List, Optional, Dict, Any

from ..models import EntityRelation, EntityId, EntityType
from ..exceptions import ValidationError, APIError


class RelationService:
    """
    关系服务类

    提供实体关系管理相关的所有操作。
    支持实体间关系的完整生命周期管理。
    """

    def __init__(self, client):
        """
        初始化关系服务

        Args:
            client: ThingsBoardClient 实例
        """
        self.client = client