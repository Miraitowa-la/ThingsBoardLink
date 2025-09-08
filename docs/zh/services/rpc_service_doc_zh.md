# thingsboardlink RPC 服务模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的 RPC 服务模块 (`rpc_service.py`)，该模块封装了与 ThingsBoard
平台进行远程过程调用 (RPC) 相关的所有 API 调用功能。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**RPC 服务类详解**](#rpc-服务类详解)
    - [**1. `RpcService` (RPC 服务类)**](#1-rpcservice-rpc-服务类)
        - [**1.1. `__init__()` (初始化 RPC 服务)**](#11-___init___-初始化-rpc-服务)
        - [**1.2. `send_one_way_rpc()` (发送单向 RPC 请求)**](#12-send_one_way_rpc-发送单向-rpc-请求)
        - [**1.3. `send_two_way_rpc()` (发送双向 RPC 请求)**](#13-send_two_way_rpc-发送双向-rpc-请求)
        - [**1.4. `send_rpc_with_retry()` (发送带重试的双向 RPC 请求)**](#14-send_rpc_with_retry-发送带重试的双向-rpc-请求)
        - [**1.5. `send_persistent_rpc()` (发送持久化 RPC 请求)**](#15-send_persistent_rpc-发送持久化-rpc-请求)
        - [**1.6. `get_persistent_rpc_response()` (获取持久化 RPC 响应)**](#16-get_persistent_rpc_response-获取持久化-rpc-响应)
        - [**1.7. `delete_persistent_rpc()` (删除持久化 RPC 请求)**](#17-delete_persistent_rpc-删除持久化-rpc-请求)
        - [**1.8. `wait_for_persistent_rpc_response()` (等待持久化 RPC 响应)**](#18-wait_for_persistent_rpc_response-等待持久化-rpc-响应)

## 概述

`thingsboardlink.services.rpc_service` 模块提供了用于与 ThingsBoard 平台上设备进行远程过程调用 (RPC) 的功能。它封装了对 ThingsBoard REST API RPC 相关端点的调用，使得开发者能够通过类型安全的 Python 方法执行单向、双向、带重试和持久化 RPC 请求。该模块旨在实现对设备的实时控制和数据查询。

## 核心功能

* **单向 RPC**: 发送不等待设备响应的控制命令。
* **双向 RPC**: 发送并等待设备响应的请求，适用于需要获取设备状态或数据的场景。
* **带重试的双向 RPC**: 增强了双向 RPC 的可靠性，在设备短暂离线或网络抖动时自动重试。
* **持久化 RPC**: 允许发送即使设备离线也能被 ThingsBoard 存储和稍后传递给设备的请求。
* **持久化 RPC 状态查询**: 查询持久化 RPC 请求的当前状态和响应。
* **持久化 RPC 删除**: 清理已完成或不再需要的持久化 RPC 请求。
* **等待持久化 RPC 响应**: 提供轮询机制，等待持久化 RPC 请求完成并返回响应。
* **错误处理**: 将 ThingsBoard API 返回的错误转换为 `thingsboardlink` 自定义的异常（如 `ValidationError`, `RPCError`, `TimeoutError`），提供更清晰的错误信息。

## RPC 服务类详解

### 1. `RpcService` (RPC 服务类)

`RpcService` 类是 RPC 调用功能的入口点，通过它您可以执行所有与 RPC 相关的操作。

#### 1.1. `__init__()` (初始化 RPC 服务)

构造函数用于初始化 `RpcService` 实例，它需要一个已配置的 `ThingsBoardClient` 实例来发送 HTTP 请求。

* **参数**:
    * `client`: `ThingsBoardClient` 实例，用于与 ThingsBoard 平台进行通信。

#### 1.2. `send_one_way_rpc()` (发送单向 RPC 请求)

向指定设备发送一个单向 RPC 请求。此方法不等待设备的响应，适用于“即发即忘”的控制命令。

* **参数**:
    * `device_id` (str): 目标设备的 ID。
    * `method` (str): 要调用的 RPC 方法名。
    * `params` (Optional[Dict[str, Any]]): RPC 方法的参数，一个键值对字典。
* **返回**:
    * `bool` - 如果请求发送成功（ThingsBoard 接受了请求）则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 或 `method` 为空或无效。
    * `RPCError`: 如果 RPC 请求发送失败。

#### 1.3. `send_two_way_rpc()` (发送双向 RPC 请求)

向指定设备发送一个双向 RPC 请求，并等待设备响应。此方法适用于需要获取设备返回结果的场景。

* **参数**:
    * `device_id` (str): 目标设备的 ID。
    * `method` (str): 要调用的 RPC 方法名。
    * `params` (Optional[Dict[str, Any]]): RPC 方法的参数。
    * `timeout_seconds` (float, default: 30.0): 等待设备响应的超时时间（秒）。
* **返回**:
    * `RPCResponse` - 包含设备响应或错误信息的 RPC 响应对象。
* **抛出**:
    * `ValidationError`: 如果 `device_id`、`method` 或 `timeout_seconds` 参数无效。
    * `RPCError`: 如果 RPC 调用失败。
    * `TimeoutError`: 如果在 `timeout_seconds` 内未收到设备响应。

#### 1.4. `send_rpc_with_retry()` (发送带重试的双向 RPC 请求)

发送一个双向 RPC 请求，并支持在失败时自动重试。提高了 RPC 调用的健壮性。

* **参数**:
    * `device_id` (str): 目标设备的 ID。
    * `method` (str): 要调用的 RPC 方法名。
    * `params` (Optional[Dict[str, Any]]): RPC 方法的参数。
    * `max_retries` (int, default: 3): 最大重试次数。
    * `timeout_seconds` (float, default: 30.0): 每次尝试等待设备响应的超时时间（秒）。
    * `retry_delay` (float, default: 1.0): 每次重试之间的延迟时间（秒）。
* **返回**:
    * `RPCResponse` - 成功的 RPC 响应对象。
* **抛出**:
    * `ValidationError`: 如果参数无效。
    * `RPCError`: 如果所有重试都失败，会抛出最后一次尝试的错误。
    * `TimeoutError`: 如果在重试过程中发生超时。

#### 1.5. `send_persistent_rpc()` (发送持久化 RPC 请求)

向指定设备发送一个持久化 RPC 请求。即使设备当前离线，ThingsBoard 也会存储此请求，并在设备上线后将其传递。

* **参数**:
    * `device_id` (str): 目标设备的 ID。
    * `method` (str): 要调用的 RPC 方法名。
    * `params` (Optional[Dict[str, Any]]): RPC 方法的参数。
    * `expiration_time` (Optional[int]): 请求的过期时间（毫秒级 Unix 时间戳）。如果在此时间之前设备未上线或未响应，请求将过期。
* **返回**:
    * `str` - 创建的持久化 RPC 请求的 ID。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 或 `method` 为空或无效。
    * `RPCError`: 如果 RPC 调用失败。

#### 1.6. `get_persistent_rpc_response()` (获取持久化 RPC 响应)

查询指定持久化 RPC 请求的当前状态和设备响应。

* **参数**:
    * `rpc_id` (str): 持久化 RPC 请求的 ID。
* **返回**:
    * `Optional[PersistentRPCRequest]` - 持久化 RPC 请求对象。如果请求不存在，则返回 `None`。
* **抛出**:
    * `ValidationError`: 如果 `rpc_id` 为空或无效。
    * `RPCError`: 如果获取持久化 RPC 响应失败。

#### 1.7. `delete_persistent_rpc()` (删除持久化 RPC 请求)

删除指定 ID 的持久化 RPC 请求。这通常用于清理已完成、过期或不再需要的持久化请求。

* **参数**:
    * `rpc_id` (str): 要删除的持久化 RPC 请求的 ID。
* **返回**:
    * `bool` - 如果删除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `rpc_id` 为空或无效。
    * `RPCError`: 如果 RPC 调用失败。

#### 1.8. `wait_for_persistent_rpc_response()` (等待持久化 RPC 响应)

轮询指定 ID 的持久化 RPC 请求，直到它完成、过期或达到指定的超时时间。此方法提供了一种同步等待异步 RPC 结果的机制。

* **参数**:
    * `rpc_id` (str): 持久化 RPC 请求的 ID。
    * `timeout_seconds` (float, default: 60.0): 最大等待时间（秒）。
    * `poll_interval` (float, default: 2.0): 轮询检查状态的间隔时间（秒）。
* **返回**:
    * `Optional[PersistentRPCRequest]` - 如果在超时前完成或过期，则返回相应的 `PersistentRPCRequest` 对象。如果超时且未完成，则抛出 `TimeoutError`。
* **抛出**:
    * `ValidationError`: 如果 `rpc_id`、`timeout_seconds` 或 `poll_interval` 参数无效。
    * `RPCError`: 如果在等待过程中发生其他 RPC 错误，或指定 `rpc_id` 不存在。
    * `TimeoutError`: 如果在指定时间内未收到完成或过期的响应。