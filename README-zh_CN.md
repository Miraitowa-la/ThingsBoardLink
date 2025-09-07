# ThingsBoardLink

<div align="center">

[![PyPI Downloads](https://static.pepy.tech/badge/thingsboardlink)](https://pepy.tech/projects/thingsboardlink)
[![PyPI version](https://badge.fury.io/py/thingsboardlink.svg)](https://badge.fury.io/py/thingsboardlink)
[![Python Version](https://img.shields.io/pypi/pyversions/thingsboardlink.svg)](https://pypi.org/project/thingsboardlink/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**专为 Python 开发者设计的高级 IoT 平台交互工具包**

*物联网云平台 • 开发者友好 • 生产就绪*

[英文版](README.md)  | [文档]() | [示例](#examples)

</div>

---

## 🚀 为什么选择ThingsBoardLink?

ThingsBoardLink 是一个功能强大的 Python 软件包，专为简化与 ThingsBoard IoT 平台的集成而设计。它封装了 ThingsBoard 的 REST API，提供面向对象的接口，让开发者能够轻松管理设备、处理遥测数据、控制警报等核心功能。

### ✨ 核心特性

| 特性           | 描述                    | 优势                 |
|--------------|-----------------------|--------------------|
| 🔐 **认证管理**  | 自动处理 JWT 令牌和会话管理      | 提升安全性，实现无状态认证      |
| 📱 **设备管理**  | 完整的设备 CRUD 操作和凭证管理    | 便捷管理设备生命周期和接入      |
| 📊 **遥测数据**  | 数据上传、查询和历史数据获取        | 高效处理时序数据，支持实时监控与分析 |
| ⚙️ **属性管理**  | 客户端、服务端和共享属性操作        | 灵活管理设备元数据，支持动态配置   |
| 🚨 **警报管理**  | 警报创建、查询、确认和清除         | 及时响应异常事件，保障系统可靠性   |
| 🔄 **RPC调用** | 支持单向和双向远程过程调用         | 实现设备与云端间高效指令交互     |
| 🔗 **关系管理**  | 实体间关系的创建和管理           | 构建设备拓扑，实现复杂业务逻辑    |
| 🛡️ **错误处理** | 完善的异常处理和错误信息          | 快速定位问题，提升系统健壮性     |
| 📚 **类型安全**  | 完整的 TypeScript 风格类型提示 | 减少开发错误，提升代码质量和开发效率 |
| 🚀 **易于使用**  | 简洁的 API 设计和丰富的文档      | 降低学习成本，加速项目开发与集成   |

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装
pip install thingsboardlink

# 或安装包含开发依赖的版本
pip install thingsboardlink[dev]
```

### 30秒快速体验

```python
from thingsboardlink import ThingsBoardClient

# 连接对应云平台
with ThingsBoardClient(
    base_url="http://localhost:8080",
    username="tenant@thingsboard.org",
    password="tenant"
) as client:
    # 设备ID
    device_id = "MY_DEVICE_ID"
    
    # 获取对应设备的遥测数据
    value = client.telemetry_service.get_latest_telemetry(device_id)
    print(value)
```

## 📚 完整使用指南

### ...