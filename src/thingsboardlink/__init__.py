"""
thingsboardlink - 专为 Python 开发者设计的高级 IoT 平台交互工具包
"""

# 版本消息
__version__ = "1.0.0"
__author__ = "Miraitowa-la"
__email__ = "2056978412@qq.com"
__description__ = "一个专为 Python 开发者设计的高级 IoT 平台交互工具包"

# 导入核心类
from .exceptions import (
    ThingsBoardError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    APIError,
    ConnectionError,
    TimeoutError,
    ConfigurationError,
    RateLimitError,
    DeviceError,
    TelemetryError,
    AlarmError,
    RPCError
)

# 公开API
__all__ = [
    # 异常类
    "ThingsBoardError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "APIError",
    "ConnectionError",
    "TimeoutError",
    "ConfigurationError",
    "RateLimitError",
    "DeviceError",
    "TelemetryError",
    "AlarmError",
    "RPCError",
]
