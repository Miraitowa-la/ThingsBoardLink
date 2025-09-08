# ThingsBoardLink

<div align="center">

[![PyPI Downloads](https://static.pepy.tech/badge/thingsboardlink)](https://pepy.tech/projects/thingsboardlink)
[![PyPI version](https://badge.fury.io/py/thingsboardlink.svg)](https://badge.fury.io/py/thingsboardlink)
[![Python Version](https://img.shields.io/pypi/pyversions/thingsboardlink.svg)](https://pypi.org/project/thingsboardlink/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.txt)

**专为 Python 开发者设计的高级 IoT 平台交互工具包**

*物联网云平台 • 开发者友好 • 生产就绪*

[英文版](README.md)  | [文档]() | [示例](examples)

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
    # 对应设备ID
    device_id = "MY_DEVICE_ID"

    # 获取对应设备的遥测数据
    value = client.telemetry_service.get_latest_telemetry(device_id)
    print(value)
```

## 📁 项目架构

```
ThingsBoardLink/
├── src/thingsboardlink/
│   ├── services/                   # 🛠️ 服务模块包
│   │   ├── device_service.py       # 设备服务模块
│   │   ├── telemetry_service.py    # 遥测服务模块
│   │   ├── attribute_service.py    # 属性服务模块
│   │   ├── alarm_service.py        # 警报服务模块
│   │   ├── rpc_service.py          # RPC 服务模块
│   │   └── relation_service.py     # 关系服务模块
│   │
│   ├── client.py                   # 🖥️ 核心客户端模块
│   ├── exceptions.py               # 🔧 异常处理模块
│   └── models.py                   # 🚚 数据模型模块
│
├── examples/                       # 📚 使用示例
│   ├── 01_connect_and_auth.py      # 连接和认证示例
│   ├── 02_device_management.py     # 设备管理示例
│   ├── 03_telemetry_data.py        # 遥测数据示例
│   ├── 04_attribute_management.py  # 属性管理示例
│   ├── 05_alarm_management.py      # 警报管理示例
│   ├── 06_rpc_calls.py             # RPC 调用示例
│   └── 07_entity_relations.py      #  关系管理示例
│
└── docs/                           # 📜 说明文档
    ├── zh                          # 中文-说明文档
    │   ├── client_doc.md           # 核心客户端模块-说明文档
    │
    └── en                          # 英文-说明文档
```

## 🎃 功能说明

### 🔐 认证管理

#### 基础实例连接

```python
from thingsboardlink import ThingsBoardClient

# 创建连接实例
client = ThingsBoardClient(
    base_url="http://localhost:8080",  # 服务器URL
    username="tenant@thingsboard.org",  # 用户名(邮箱)
    password="tenant",  # 密码
)

try:
    # 登录
    client.login()

    # 相关运行逻辑...

finally:
    # 登出
    client.logout()
```

#### 高级实例连接

```python
from thingsboardlink import ThingsBoardClient

# 创建连接实例
client = ThingsBoardClient(
    base_url="http://localhost:8080",  # 服务器URL
    username="tenant@thingsboard.org",  # 用户名(邮箱)
    password="tenant",  # 密码
    timeout=60.0,  # 请求超时时间
    max_retries=5,  # 最大重试次数
    retry_backoff_factor=0.5,  # 重试退避因子
    verify_ssl=True  # SSL 验证
)

try:
    # 登录
    client.login()

    # 相关运行逻辑...

finally:
    # 登出
    client.logout()
```

#### 上下文管理器

```python
from thingsboardlink import ThingsBoardClient

# 创建连接实例
with ThingsBoardClient(
        base_url="http://localhost:8080",
        username="tenant@thingsboard.org",
        password="tenant"
) as client:
    # 相关运行逻辑...
    pass
```

### 📱 设备管理

### 📊 遥测数据

### ⚙️ 属性管理

### 🚨 警报管理

### 🔄 RPC调用

### 🔗 关系管理

### 🛡️ 错误处理

### 📚 类型安全

### 🚀 易于使用

## 📚 功能示例

在[examples](examples)目录中探索**真实的场景**：

### 🔐 认证管理 [01_connect_and_auth.py](examples/01_connect_and_auth.py)

- 本示例演示如何使用 ThingsBoardLink 连接到 ThingsBoard 服务器并进行用户认证。
- 包括客户端创建、登录、会话管理和安全退出等基本操作。

### 📱 设备管理 [02_device_management.py](examples/02_device_management.py)

- 本示例演示如何使用 ThingsBoardLink 进行设备管理操作。
- 包括设备的创建、查询、更新、删除以及设备凭证管理等功能。

### 📊 遥测数据 [03_telemetry_data.py](examples/03_telemetry_data.py)

- 本示例演示如何使用 ThingsBoardLink 进行遥测数据操作。 
- 包括遥测数据的上传、查询、删除以及时间序列数据处理等功能。

### ⚙️ 属性管理 [04_attribute_management.py](examples/04_attribute_management.py)

- 本示例演示如何使用 ThingsBoardLink 进行属性管理操作。 
- 包括客户端属性、服务端属性和共享属性的读取、设置、删除等功能。

### 🚨 警报管理 [05_alarm_management.py](examples/05_alarm_management.py)

- 本示例演示如何使用 ThingsBoardLink 进行警报管理操作。 
- 包括警报的创建、查询、确认、清除、删除等功能。

### 🔄 RPC调用 [06_rpc_calls.py](examples/06_rpc_calls.py)

- 本示例演示如何使用 ThingsBoardLink 进行 RPC（远程过程调用）操作。 
- 包括单向 RPC、双向 RPC、持久化 RPC 以及带重试机制的 RPC 调用等功能。

### 🔗 关系管理 [07_entity_relations.py](examples/07_entity_relations.py)

- 本示例演示如何使用 ThingsBoardLink 进行实体关系管理操作。
- 包括关系的创建、查询、删除以及复杂的关系查找等功能。

### 🛡️ 错误处理

### 📚 类型安全

### 🚀 易于使用
