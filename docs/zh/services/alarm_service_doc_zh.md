# thingsboardlink 警报服务模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的警报服务模块 (`alarm_service.py`)，该模块封装了与 ThingsBoard 平台进行警报管理相关的所有 API 调用功能。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**警报服务类详解**](#警报服务类详解)
    - [**1. `AlarmService` (警报服务类)**](#1-alarmservice-警报服务类)
        - [**1.1. `__init__()` (初始化警报服务)**](#11-___init___-初始化警报服务)
        - [**1.2. `create_alarm()` (创建警报)**](#12-create_alarm-创建警报)
        - [**1.3. `get_alarm()` (根据 ID 获取警报)**](#13-get_alarm-根据-id-获取警报)
        - [**1.4. `get_alarms()` (获取警报列表)**](#14-get_alarms-获取警报列表)
        - [**1.5. `ack_alarm()` (确认警报)**](#15-ack_alarm-确认警报)
        - [**1.6. `clear_alarm()` (清除警报)**](#16-clear_alarm-清除警报)
        - [**1.7. `delete_alarm()` (删除警报)**](#17-delete_alarm-删除警报)
        - [**1.8. `alarm_exists()` (检查警报是否存在)**](#18-alarm_exists-检查警报是否存在)

## 概述

`thingsboardlink.services.alarm_service` 模块提供了用于管理 ThingsBoard 平台上警报实体的功能。它封装了对 ThingsBoard REST API 警报相关端点的调用，使得开发者能够通过类型安全的 Python 方法执行警报的创建、查询、确认、清除和删除等操作。该模块旨在简化警报生命周期的管理和监控。

## 核心功能

* **警报创建**: 允许创建具有指定类型、发起者、严重程度和详情的新警报。
* **警报查询**: 支持根据警报 ID 获取单个警报，或根据发起者 ID、时间范围、状态、严重程度和类型等多种条件查询警报列表，并提供分页和排序功能。
* **警报状态管理**: 提供确认 (ACK) 和清除 (CLEAR) 警报的功能，以管理警报的生命周期。
* **警报删除**: 允许彻底删除 ThingsBoard 上的警报。
* **警报存在性检查**: 快速判断某个警报 ID 对应的警报是否存在。
* **错误处理**: 将 ThingsBoard API 返回的错误转换为 `thingsboardlink` 自定义的异常（如 `ValidationError`, `AlarmError`, `NotFoundError`），提供更清晰的错误信息。

## 警报服务类详解

### 1. `AlarmService` (警报服务类)

`AlarmService` 类是警报管理功能的入口点，通过它您可以执行所有与警报相关的操作。

#### 1.1. `__init__()` (初始化警报服务)

构造函数用于初始化 `AlarmService` 实例，它需要一个已配置的 `ThingsBoardClient` 实例来发送 HTTP 请求。

* **参数**:
    * `client`: `ThingsBoardClient` 实例，用于与 ThingsBoard 平台进行通信。

#### 1.2. `create_alarm()` (创建警报)

在 ThingsBoard 平台上创建一个新的警报。

* **参数**:
    * `alarm_type` (str): 警报的类型（例如 "HIGH_TEMPERATURE"）。
    * `originator_id` (str): 警报发起者的 ID，通常是设备或资产的 ID。
    * `severity` (`AlarmSeverity`, default: `AlarmSeverity.CRITICAL`): 警报的严重程度。
    * `details` (Optional[Dict[str, Any]]): 警报的详细信息，JSON 格式。
    * `propagate` (bool, default: `True`): 是否将警报传播给相关实体。
* **返回**:
    * `Alarm` - 创建成功的警报对象。
* **抛出**:
    * `ValidationError`: 如果 `alarm_type` 或 `originator_id` 为空或无效。
    * `AlarmError`: 如果警报创建失败（通常是由于 API 调用错误）。

#### 1.3. `get_alarm()` (根据 ID 获取警报)

根据警报的唯一 ID 获取警报详情。

* **参数**:
    * `alarm_id` (str): 警报的唯一标识符。
* **返回**:
    * `Alarm` - 匹配的警报对象。
* **抛出**:
    * `ValidationError`: 如果 `alarm_id` 为空或无效。
    * `NotFoundError`: 如果指定 ID 的警报不存在。
    * `AlarmError`: 如果获取警报失败。

#### 1.4. `get_alarms()` (获取警报列表)

获取与指定发起者相关的警报列表，支持多种过滤、分页和排序选项。

* **参数**:
    * `originator_id` (str): 警报发起者的 ID。
    * `page_size` (int, default: 10): 每页返回的警报数量。
    * `page` (int, default: 0): 要获取的页码（从 0 开始）。
    * `text_search` (Optional[str]): 用于模糊匹配警报类型或详情的搜索文本。
    * `sort_property` (Optional[str]): 用于排序的警报属性（例如 "startTs", "severity", "type"）。
    * `sort_order` (Optional[str]): 排序顺序，可以是 "ASC" (升序) 或 "DESC" (降序)。
    * `start_time` (Optional[int]): 查询的开始时间戳（毫秒级 Unix 时间戳）。
    * `end_time` (Optional[int]): 查询的结束时间戳（毫秒级 Unix 时间戳）。
    * `fetch_originator` (bool, default: `False`): 是否在响应中包含发起者实体的信息。
    * `status_list` (Optional[List[AlarmStatus]]): 用于过滤警报状态的列表。
    * `severity_list` (Optional[List[AlarmSeverity]]): 用于过滤警报严重程度的列表。
    * `type_list` (Optional[List[str]]): 用于过滤警报类型的列表。
* **返回**:
    * `PageData` - 包含警报列表和分页信息的对象。
* **抛出**:
    * `ValidationError`: 如果 `originator_id`、`page_size` 或 `page` 参数无效。
    * `AlarmError`: 如果获取警报列表失败。

#### 1.5. `ack_alarm()` (确认警报)

确认指定 ID 的警报。此操作会将警报状态从 `ACTIVE_UNACK` 变为 `ACTIVE_ACK` 或 `CLEARED_UNACK` 变为 `CLEARED_ACK`。

* **参数**:
    * `alarm_id` (str): 要确认的警报 ID。
* **返回**:
    * `bool` - 如果确认成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `alarm_id` 为空或无效。
    * `AlarmError`: 如果警报确认失败。

#### 1.6. `clear_alarm()` (清除警报)

清除指定 ID 的警报。此操作会将警报状态从 `ACTIVE_UNACK` 或 `ACTIVE_ACK` 变为 `CLEARED_UNACK` 或 `CLEARED_ACK`。

* **参数**:
    * `alarm_id` (str): 要清除的警报 ID。
* **返回**:
    * `bool` - 如果清除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `alarm_id` 为空或无效。
    * `AlarmError`: 如果警报清除失败。

#### 1.7. `delete_alarm()` (删除警报)

根据警报的 ID 删除 ThingsBoard 上的警报。

* **参数**:
    * `alarm_id` (str): 要删除警报的唯一标识符。
* **返回**:
    * `bool` - 如果删除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `alarm_id` 为空或无效。
    * `AlarmError`: 如果警报删除失败。

#### 1.8. `alarm_exists()` (检查警报是否存在)

检查具有给定 ID 的警报是否存在于 ThingsBoard 平台上。

* **参数**:
    * `alarm_id` (str): 要检查的警报 ID。
* **返回**:
    * `bool` - 如果警报存在则返回 `True`，否则返回 `False`。