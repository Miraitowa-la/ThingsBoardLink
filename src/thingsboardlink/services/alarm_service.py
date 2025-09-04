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

    def create_alarm(self,
                     alarm_type: str,
                     originator_id: str,
                     severity: AlarmSeverity = AlarmSeverity.CRITICAL,
                     details: Optional[Dict[str, Any]] = None,
                     propagate: bool = True) -> Alarm:
        """
        创建警报

        Args:
            alarm_type: 警报类型
            originator_id: 发起者 ID（通常是设备 ID）
            severity: 警报严重程度
            details: 警报详情
            propagate: 是否传播警报

        Returns:
            Alarm: 创建的警报对象

        Raises:
            ValidationError: 参数验证失败时抛出
            AlarmError: 警报创建失败时抛出
        """
        if not alarm_type or not alarm_type.strip():
            raise ValidationError(
                field_name="alarm_type",
                expected_type="非空字符串",
                actual_value=alarm_type,
                message="警报类型不能为空"
            )

        if not originator_id or not originator_id.strip():
            raise ValidationError(
                field_name="originator_id",
                expected_type="非空字符串",
                actual_value=originator_id,
                message="发起者 ID 不能为空"
            )

        alarm = Alarm(
            type=alarm_type.strip(),
            originator_id=originator_id.strip(),
            severity=severity,
            status=AlarmStatus.ACTIVE_UNACK,
            details=details or {},
            propagate=propagate
        )

        try:
            response = self.client.post(
                "/api/alarm",
                data=alarm.to_dict()
            )

            alarm_data = response.json()
            return Alarm.from_dict(alarm_data)

        except Exception as e:
            raise AlarmError(
                message=f"创建警报失败: {str(e)}",
                alarm_type=alarm_type
            )
