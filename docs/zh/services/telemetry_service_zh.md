# thingsboardlink 遥测服务模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的遥测服务模块 (`telemetry_service.py`)，该模块封装了与 ThingsBoard
平台进行遥测数据管理相关的所有 API 调用功能。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**遥测服务类详解**](#遥测服务类详解)
    - [**1. `TelemetryService` (遥测服务类)**](#1-telemetryservice-遥测服务类)
        - [**1.1. `__init__()` (初始化遥测服务)**](#11-___init___-初始化遥测服务)
        - [**1.2. `post_telemetry()` (上传遥测数据)**](#12-post_telemetry-上传遥测数据)
        - [**1.3. `post_telemetry_with_device_token()` (使用设备令牌上传遥测数据)**](#13-post_telemetry_with_device_token-使用设备令牌上传遥测数据)
        - [**1.4. `get_latest_telemetry()` (获取最新遥测数据)**](#14-get_latest_telemetry-获取最新遥测数据)
        - [**1.5. `get_timeseries_telemetry()` (获取时间序列遥测数据)**](#15-get_timeseries_telemetry-获取时间序列遥测数据)
        - [**1.6. `delete_telemetry()` (删除遥测数据)**](#16-delete_telemetry-删除遥测数据)
        - [**1.7. `get_telemetry_keys()` (获取设备的所有遥测数据键)**](#17-get_telemetry_keys-获取设备的所有遥测数据键)

## 概述

`thingsboardlink.services.telemetry_service` 模块提供了用于管理 ThingsBoard 平台上遥测数据的功能。它封装了对 ThingsBoard REST API 遥测数据相关端点的调用，使得开发者能够通过类型安全的 Python 方法执行遥测数据的上传、最新数据获取、历史数据查询和删除等操作。该模块旨在简化设备数据上报和分析的流程。

## 核心功能

* **遥测数据上传**: 支持多种数据格式（字典、单个 `TelemetryData` 对象、`TelemetryData` 对象列表）进行遥测数据的上传。
* **基于设备 ID 上传**: 提供通过设备 ID 自动获取凭证并上传数据的功能。
* **基于设备令牌上传**: 允许直接使用设备访问令牌上传数据，适用于设备端集成。
* **最新遥测数据获取**: 获取指定设备或指定键的最新遥测数据点。
* **历史时间序列数据查询**: 支持在指定时间范围内查询设备的遥测数据，并提供聚合功能（如 MIN, MAX, AVG 等）。
* **遥测数据删除**: 允许删除特定键或时间范围内的遥测数据。
* **遥测数据键列表获取**: 查询设备当前存在的所有遥测数据键。
* **错误处理**: 将 ThingsBoard API 返回的错误转换为 `thingsboardlink` 自定义的异常（如 `ValidationError`, `TelemetryError`, `NotFoundError`），提供更清晰的错误信息。

## 遥测服务类详解

### 1. `TelemetryService` (遥测服务类)

`TelemetryService` 类是遥测数据管理功能的入口点，通过它您可以执行所有与遥测数据相关的操作。

#### 1.1. `__init__()` (初始化遥测服务)

构造函数用于初始化 `TelemetryService` 实例，它需要一个已配置的 `ThingsBoardClient` 实例来发送 HTTP 请求。

* **参数**:
    * `client`: `ThingsBoardClient` 实例，用于与 ThingsBoard 平台进行通信。

#### 1.2. `post_telemetry()` (上传遥测数据)

通过设备 ID 上传遥测数据。此方法会自动调用 `client.device_service.get_device_credentials()` 获取设备访问令牌，然后使用该令牌进行数据上传。

* **参数**:
    * `device_id` (str): 要上传数据的设备 ID。
    * `telemetry_data` (Union[Dict[str, Any], List[TelemetryData], TelemetryData]): 要上传的遥测数据。可以是：
        * `Dict[str, Any]`: 键值对字典，例如 `{"temperature": 25.5, "humidity": 60}`。
        * `TelemetryData`: 单个 `TelemetryData` 对象。
        * `List[TelemetryData]`: `TelemetryData` 对象的列表。
    * `timestamp` (Optional[int]): 遥测数据的时间戳（毫秒级 Unix 时间戳）。如果未提供，将使用当前时间。
* **返回**:
    * `bool` - 如果上传成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 或 `telemetry_data` 参数无效。
    * `TelemetryError`: 如果无法获取设备访问令牌或遥测数据上传失败。
    * `NotFoundError`: 如果设备不存在。

#### 1.3. `post_telemetry_with_device_token()` (使用设备令牌上传遥测数据)

直接使用设备访问令牌上传遥测数据。此方法适用于已经拥有设备访问令牌的场景，例如在设备端或边缘网关应用中。

* **参数**:
    * `device_token` (str): 设备的访问令牌。
    * `telemetry_data` (Union[Dict[str, Any], List[TelemetryData], TelemetryData]): 要上传的遥测数据，格式与 `post_telemetry` 相同。
    * `timestamp` (Optional[int]): 遥测数据的时间戳（毫秒级 Unix 时间戳）。如果未提供，将使用当前时间。
* **返回**:
    * `bool` - 如果上传成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `device_token` 或 `telemetry_data` 参数无效。
    * `TelemetryError`: 如果遥测数据上传失败。

#### 1.4. `get_latest_telemetry()` (获取最新遥测数据)

获取指定设备的最新遥测数据。可以指定要获取的键，如果未指定则获取所有遥测键的最新值。

* **参数**:
    * `device_id` (str): 要获取数据的设备 ID。
    * `keys` (Optional[List[str]]): 要获取的遥测数据键列表。如果为 `None` 或空列表，则获取所有可用键的最新值。
* **返回**:
    * `Dict[str, Any]` - 一个字典，其中键是遥测数据键，值是包含 `value` 和 `timestamp` 的字典。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `NotFoundError`: 如果设备不存在。
    * `TelemetryError`: 如果获取最新遥测数据失败。

#### 1.5. `get_timeseries_telemetry()` (获取时间序列遥测数据)

获取指定设备在特定时间范围内的历史时间序列遥测数据。支持聚合功能。

* **参数**:
    * `device_id` (str): 要获取数据的设备 ID。
    * `keys` (List[str]): 要获取的时间序列数据键列表。
    * `start_ts` (int): 查询的开始时间戳（毫秒级 Unix 时间戳）。
    * `end_ts` (int): 查询的结束时间戳（毫秒级 Unix 时间戳）。
    * `interval` (Optional[int]): 聚合间隔（毫秒）。例如，设置为 3600000 (1小时) 可以获取每小时的聚合数据。
    * `limit` (Optional[int]): 返回数据点的最大数量。
    * `agg` (Optional[str]): 聚合方式。可选值包括 "MIN", "MAX", "AVG", "SUM", "COUNT"。
* **返回**:
    * `Dict[str, TimeseriesData]` - 一个字典，其中键是遥测数据键，值是 `TimeseriesData` 对象，包含该键的时间序列数据列表。
* **抛出**:
    * `ValidationError`: 如果 `device_id`、`keys`、`start_ts` 或 `end_ts` 参数无效。
    * `TelemetryError`: 如果获取时间序列遥测数据失败。

#### 1.6. `delete_telemetry()` (删除遥测数据)

删除指定设备的一个或多个遥测数据键的历史数据。可以删除特定时间范围的数据，或删除某个键的所有数据。

* **参数**:
    * `device_id` (str): 要删除数据的设备 ID。
    * `keys` (List[str]): 要删除的遥测数据键列表。
    * `delete_all_data_for_keys` (bool, default: `True`): 如果为 `True`，将删除指定键的所有数据。如果为 `False`，则必须提供 `start_ts` 和 `end_ts` 来指定删除范围。
    * `start_ts` (Optional[int]): 删除范围的开始时间戳（毫秒）。仅当 `delete_all_data_for_keys` 为 `False` 时有效。
    * `end_ts` (Optional[int]): 删除范围的结束时间戳（毫秒）。仅当 `delete_all_data_for_keys` 为 `False` 时有效。
* **返回**:
    * `bool` - 如果删除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 或 `keys` 参数无效，或者在 `delete_all_data_for_keys` 为 `False` 时未提供时间范围。
    * `TelemetryError`: 如果删除遥测数据失败。

#### 1.7. `get_telemetry_keys()` (获取设备的所有遥测数据键)

获取指定设备当前已存在的、具有时间序列数据的所有遥测数据键的列表。

* **参数**:
    * `device_id` (str): 要查询的设备 ID。
* **返回**:
    * `List[str]` - 遥测数据键的字符串列表。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `TelemetryError`: 如果获取遥测数据键失败。
