# thingsboardlink 数据模型模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中定义的所有数据模型，旨在提供类型安全的数据结构和便捷的数据转换方法，以便与
ThingsBoard 平台进行高效交互。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**数据模型详解**](#数据模型详解)
    - [**1. EntityType (实体类型枚举)**](#1-entitytype-实体类型枚举)
    - [**2. AlarmSeverity (警报严重程度枚举)**](#2-alarmseverity-警报严重程度枚举)
    - [**3. AlarmStatus (警报状态枚举)**](#3-alarmstatus-警报状态枚举)
    - [**4. AttributeScope (属性范围枚举)**](#4-attributescope-属性范围枚举)
    - [**5. RpcPersistentStatus (RPC 持久化状态枚举)**](#5-rpcpersistentstatus-rpc-持久化状态枚举)
    - [**6. EntityId (实体 ID 模型)**](#6-entityid-实体-id-模型)
    - [**7. Device (设备模型)**](#7-device-设备模型)
    - [**8. DeviceCredentials (设备凭证模型)**](#8-devicecredentials-设备凭证模型)
    - [**9. TelemetryData (遥测数据模型)**](#9-telemetrydata-遥测数据模型)
    - [**10. Attribute (属性模型)**](#10-attribute-属性模型)
    - [**11. Alarm (警报模型)**](#11-alarm-警报模型)
    - [**12. RPCRequest (RPC 请求模型)**](#12-rpcrequest-rpc-请求模型)
    - [**13. RPCResponse (RPC 响应模型)**](#13-rpcresponse-rpc-响应模型)
    - [**14. PersistentRPCRequest (持久化 RPC 请求模型)**](#14-persistentrpcrequest-持久化-rpc-请求模型)
    - [**15. EntityRelation (实体关系模型)**](#15-entityrelation-实体关系模型)
    - [**16. PageData (分页数据模型)**](#16-pagedata-分页数据模型)
    - [**17. TimeseriesData (时间序列数据模型)**](#17-timeseriesdata-时间序列数据模型)

## 概述

`thingsboardlink` 数据模型模块 (`models.py`) 提供了与 ThingsBoard 平台各种实体、数据类型和操作相对应的数据结构。这些模型通过 Python 的 `dataclasses` 和 `Enum` 实现，确保了数据的类型安全、可读性和易用性。它们封装了 ThingsBoard API 的 JSON 结构，并提供了方便的转换方法，使得开发者可以以面向对象的方式处理 ThingsBoard 数据。

## 核心功能

* **类型安全**: 使用 `dataclasses` 定义结构，并利用 `typing` 模块进行类型提示，增强了代码的可读性和健壮性。
* **枚举类型**: 为 ThingsBoard 中常见的固定值（如实体类型、警报严重程度、属性范围等）提供了枚举类，避免了硬编码字符串。
* **数据转换**: 所有主要数据模型都提供了 `to_dict()` 和 `from_dict()` 方法，方便在 Python 对象和 ThingsBoard API 所需的 JSON (字典) 格式之间进行转换。
* **业务逻辑封装**: 部分模型包含了与业务逻辑相关的便利方法，例如 `TelemetryData.create_batch()`、`RPCResponse.is_success`等。
* **时间戳处理**: 自动处理时间戳的转换，通常在 ThingsBoard 中以毫秒为单位的 Unix 时间戳，在 Python 中转换为 `datetime`对象或反之。

## 数据模型详解

### 1. EntityType (实体类型枚举)

表示 ThingsBoard 平台中不同实体的类型。

* **成员**:
    * `DEVICE`: 设备
    * `ASSET`: 资产
    * `USER`: 用户
    * `CUSTOMER`: 客户
    * `TENANT`: 租户
    * `RULE_CHAIN`: 规则链
    * `RULE_NODE`: 规则节点
    * `DASHBOARD`: 仪表盘
    * `WIDGET_TYPE`: 部件类型
    * `WIDGET_BUNDLE`: 部件包
    * `ALARM`: 告警

### 2. AlarmSeverity (警报严重程度枚举)

定义了 ThingsBoard 警报的严重程度级别。

* **成员**:
    * `CRITICAL`: 关键级别
    * `MAJOR`: 主要级别
    * `MINOR`: 次要级别
    * `WARNING`: 警告级别
    * `INDETERMINATE`: 不确定级别

### 3. AlarmStatus (警报状态枚举)

定义了 ThingsBoard 警报的生命周期状态。

* **成员**:
    * `ACTIVE_UNACK`: 活动且未确认
    * `ACTIVE_ACK`: 活动且已确认
    * `CLEARED_UNACK`: 已清除但未确认
    * `CLEARED_ACK`: 已清除且已确认

### 4. AttributeScope (属性范围枚举)

定义了 ThingsBoard 实体属性的不同存储和访问范围。

* **成员**:
    * `CLIENT_SCOPE`: 客户端属性，由设备设置并推送到服务器。
    * `SERVER_SCOPE`: 服务端属性，由服务器设置并可推送到设备。
    * `SHARED_SCOPE`: 共享属性，由服务器设置，对所有客户端可见。

### 5. RpcPersistentStatus (RPC 持久化状态枚举)

定义了持久化 RPC 请求的当前状态。

* **成员**:
    * `QUEUED`: 已排队 - RPC 已创建并保存到数据库，尚未发送到设备。
    * `SENT`: 已发送 - ThingsBoard 已尝试将 RPC 发送到设备。
    * `DELIVERED`: 已送达 - 设备已确认 RPC（单向 RPC 的最终状态）。
    * `SUCCESSFUL`: 成功 - ThingsBoard 已收到双向 RPC 的回复。
    * `TIMEOUT`: 超时 - 传输层检测到 RPC 超时。
    * `EXPIRED`: 过期 - RPC 在配置的到期时间内未送达或未收到回复。
    * `FAILED`: 失败 - 在配置的重试次数内未能传递 RPC，或设备不支持此类命令。

### 6. EntityId (实体 ID 模型)

一个通用的模型，用于表示 ThingsBoard 中任何实体的唯一标识符，包括其 ID 字符串和实体类型。

* **属性**:
    * `id` (str): 实体的唯一 ID 字符串。
    * `entity_type` (EntityType): 实体的类型。
* **方法**:
    * `to_dict() -> Dict[str, Any]`: 将 `EntityId` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_dict(data: Dict[str, Any]) -> 'EntityId'`: 从字典数据创建 `EntityId` 对象。

### 7. Device (设备模型)

表示 ThingsBoard 平台中的一个设备实体，包含其基本信息和元数据。

* **属性**:
    * `name` (str): 设备名称。
    * `type` (str, default: "default"): 设备类型。
    * `id` (Optional[str]): 设备的唯一 ID。
    * `label` (Optional[str]): 设备标签。
    * `additional_info` (Optional[Dict[str, Any]]): 额外信息字典。
    * `created_time` (Optional[datetime]): 设备创建时间。
    * `customer_id` (Optional[EntityId]): 所属客户的 ID。
    * `tenant_id` (Optional[EntityId]): 所属租户的 ID。
* **方法**:
    * `__post_init__()`: 初始化后处理，确保 `additional_info` 字段为字典。
    * `to_dict() -> Dict[str, Any]`: 将 `Device` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_dict(data: Dict[str, Any]) -> 'Device'`: 从字典数据创建 `Device` 对象。

### 8. DeviceCredentials (设备凭证模型)

表示设备的认证凭证信息，通常用于设备连接到 ThingsBoard。

* **属性**:
    * `device_id` (str): 凭证所属设备的 ID。
    * `credentials_type` (str, default: "ACCESS_TOKEN"): 凭证类型（例如 "ACCESS_TOKEN"）。
    * `credentials_id` (Optional[str]): 凭证的 ID。
    * `credentials_value` (Optional[str]): 凭证的值（例如访问令牌）。
* **方法**:
    * `to_dict() -> Dict[str, Any]`: 将 `DeviceCredentials` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_dict(data: Dict[str, Any]) -> 'DeviceCredentials'`: 从字典数据创建 `DeviceCredentials` 对象，并特别处理`ACCESS_TOKEN` 类型的 `credentials_value`。

### 9. TelemetryData (遥测数据模型)

表示设备上传到 ThingsBoard 的单个遥测数据点，包含键值对和时间戳。

* **属性**:
    * `key` (str): 遥测数据的键名。
    * `value` (Union[str, int, float, bool]): 遥测数据的值。
    * `timestamp` (Optional[int]): 数据产生的时间戳，默认为当前时间（毫秒级 Unix 时间戳）。
* **方法**:
    * `__post_init__()`: 初始化后处理，如果 `timestamp` 未指定则自动设置为当前时间。
    * `to_dict() -> Dict[str, Any]`: 将 `TelemetryData` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_dict(key: str, data: Dict[str, Any]) -> 'TelemetryData'`: 从字典数据创建 `TelemetryData` 对象。
    * `create_batch(data: Dict[str, Union[str, int, float, bool]], timestamp: Optional[int] = None) -> List['TelemetryData']`: 静态方法，用于从一个键值对字典创建批量 `TelemetryData` 列表。

### 10. Attribute (属性模型)

表示 ThingsBoard 实体的一个属性，具有键、值和范围。

* **属性**:
    * `key` (str): 属性的键名。
    * `value` (Any): 属性的值。
    * `scope` (AttributeScope, default: `AttributeScope.SERVER_SCOPE`): 属性的范围（客户端、服务端、共享）。
    * `last_update_ts` (Optional[int]): 属性最后更新的时间戳。
* **方法**:
    * `to_dict() -> Dict[str, Any]`: 将 `Attribute` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_api_response(key: str, data: Dict[str, Any], scope: AttributeScope = AttributeScope.SERVER_SCOPE) -> 'Attribute'`: 从 ThingsBoard API 响应数据创建 `Attribute` 对象。
    * `create_batch(data: Dict[str, Any], scope: AttributeScope = AttributeScope.SERVER_SCOPE) -> List['Attribute']`: 静态方法，用于从一个键值对字典创建批量 `Attribute` 列表。

### 11. Alarm (警报模型)

表示 ThingsBoard 系统中的一个警报，包含其类型、来源、严重程度和状态等信息。

* **属性**:
    * `type` (str): 警报类型。
    * `originator_id` (str): 警报来源实体的 ID。
    * `severity` (AlarmSeverity, default: `AlarmSeverity.CRITICAL`): 警报严重程度。
    * `status` (AlarmStatus, default: `AlarmStatus.ACTIVE_UNACK`): 警报状态。
    * `id` (Optional[str]): 警报的唯一 ID。
    * `start_ts` (Optional[int]): 警报开始时间戳。
    * `end_ts` (Optional[int]): 警报结束时间戳。
    * `ack_ts` (Optional[int]): 警报确认时间戳。
    * `clear_ts` (Optional[int]): 警报清除时间戳。
    * `details` (Optional[Dict[str, Any]]): 警报的详细信息。
    * `propagate` (bool, default: `True`): 是否传播警报到相关实体。
* **方法**:
    * `__post_init__()`: 初始化后处理，确保 `details` 字段为字典，并自动设置 `start_ts`。
    * `to_dict() -> Dict[str, Any]`: 将 `Alarm` 对象转换为 ThingsBoard API 请求期望的字典格式。
    * `from_dict(data: Dict[str, Any]) -> 'Alarm'`: 从字典数据创建 `Alarm` 对象。

### 12. RPCRequest (RPC 请求模型)

表示一个向设备发送的远程过程调用 (RPC) 请求。

* **属性**:
    * `method` (str): RPC 方法名称。
    * `params` (Dict[str, Any], default: `dict()`): RPC 方法的参数。
    * `timeout` (Optional[int]): RPC 请求的超时时间（毫秒）。
    * `persistent` (bool, default: `False`): 是否为持久化 RPC 请求。
* **方法**:
    * `to_dict() -> Dict[str, Any]`: 将 `RPCRequest` 对象转换为 ThingsBoard API 期望的字典格式。

### 13. RPCResponse (RPC 响应模型)

表示设备对一个 RPC 请求的响应。

* **属性**:
    * `id` (str): 响应对应的 RPC 请求 ID。
    * `method` (str): 响应对应的 RPC 方法名称。
    * `response` (Optional[Dict[str, Any]]): RPC 调用的结果数据。
    * `error` (Optional[str]): RPC 调用发生的错误信息。
    * `timestamp` (Optional[int]): 响应时间戳。
* **方法**:
    * `__post_init__()`: 初始化后处理，如果 `timestamp` 未指定则自动设置为当前时间。
    * `from_dict(data: Dict[str, Any]) -> 'RPCResponse'`: 从字典数据创建 `RPCResponse` 对象。
* **属性**:
    * `is_success` (bool): 检查 RPC 调用是否成功（即 `error` 为 `None`）。

### 14. PersistentRPCRequest (持久化 RPC 请求模型)

表示一个存储在 ThingsBoard 中的持久化 RPC 请求，可以查询其状态和响应。

* **属性**:
    * `id` (Optional[str]): 持久化 RPC 请求的 ID。
    * `device_id` (Optional[str]): 目标设备的 ID。
    * `method` (str, default: `""`): RPC 方法名称。
    * `params` (Dict[str, Any], default: `dict()`): RPC 方法的参数。
    * `expiration_time` (Optional[int]): RPC 请求的过期时间戳。
    * `status` (str, default: `RpcPersistentStatus.QUEUED.value`): RPC 请求的当前状态。
    * `created_time` (Optional[int]): RPC 请求的创建时间戳。
    * `response` (Optional[Dict[str, Any]]): RPC 调用的响应数据。
* **方法**:
    * `__post_init__()`: 初始化后处理，如果 `created_time` 未指定则自动设置为当前时间。
    * `to_dict() -> Dict[str, Any]`: 将 `PersistentRPCRequest` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_dict(data: Dict[str, Any]) -> 'PersistentRPCRequest'`: 从字典数据创建 `PersistentRPCRequest` 对象。
* **属性**:
    * `is_completed` (bool): 检查 RPC 请求是否已完成（成功、失败或过期）。
    * `is_expired` (bool): 检查 RPC 请求是否已过期。

### 15. EntityRelation (实体关系模型)

表示 ThingsBoard 中两个实体之间的关系。

* **属性**:
    * `from_id` (EntityId): 关系发起方实体的 ID。
    * `to_id` (EntityId): 关系目标方实体的 ID。
    * `type` (str): 关系的类型（例如 "Contains"）。
    * `type_group` (str, default: "COMMON"): 关系类型组。
    * `additional_info` (Optional[Dict[str, Any]]): 关系的额外信息字典。
* **方法**:
    * `__post_init__()`: 初始化后处理，确保 `additional_info` 字段为字典。
    * `to_dict() -> Dict[str, Any]`: 将 `EntityRelation` 对象转换为 ThingsBoard API 期望的字典格式。
    * `from_dict(data: Dict[str, Any]) -> 'EntityRelation'`: 从字典数据创建 `EntityRelation` 对象。

### 16. PageData (分页数据模型)

一个通用的模型，用于封装 ThingsBoard API 返回的分页数据结果。

* **属性**:
    * `data` (List[Any]): 当前页的数据列表，可以是任何类型的对象。
    * `total_pages` (int): 总页数。
    * `total_elements` (int): 总元素数量。
    * `has_next` (bool): 是否有下一页。
* **方法**:
    * `from_dict(data: Dict[str, Any], item_class=None) -> 'PageData'`: 从字典数据创建 `PageData` 对象。如果提供了
      `item_class` 且其具有 `from_dict` 方法，则列表中的每个项目将被转换为该类的实例。

### 17. TimeseriesData (时间序列数据模型)

表示从 ThingsBoard 获取的某个键的时间序列数据。

* **属性**:
    * `key` (str): 时间序列数据的键名。
    * `values` (List[Dict[str, Any]]): 包含时间戳 (`ts`) 和值 (`value`) 的字典列表。
* **方法**:
    * `from_dict(key: str, data: List[Dict[str, Any]]) -> 'TimeseriesData'`: 从字典数据创建 `TimeseriesData` 对象。
    * `get_latest_value() -> Optional[Any]`: 获取时间序列数据中的最新值。
    * `get_values_in_range(start_ts: int, end_ts: int) -> List[Dict[str, Any]]`: 获取指定时间范围内的值。
* **特殊方法**:
    * `__len__() -> int`: 支持 `len()` 函数，返回 `values` 列表的长度。
    * `__getitem__(index: int) -> Dict[str, Any]`: 支持通过下标直接访问 `values` 列表中的元素。
