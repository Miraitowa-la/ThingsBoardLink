# thingsboardlink 核心客户端模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的核心客户端类 `ThingsBoardClient`。该客户端作为与 ThingsBoard 平台交互的中心枢纽，负责认证管理、HTTP 请求处理、统一的错误处理以及对各个服务模块的访问。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**ThingsBoardClient 详解**](#thingsboardclient-详解)
    - [**1. 客户端初始化 (`__init__`)**](#1-客户端初始化-__init__)
    - [**2. 服务模块属性**](#2-服务模块属性)
        - [**2.1. `device_service` (设备服务)**](#21-device_service-设备服务)
        - [**2.2. `telemetry_service` (遥测服务)**](#22-telemetry_service-遥测服务)
        - [**2.3. `attribute_service` (属性服务)**](#23-attribute_service-属性服务)
        - [**2.4. `alarm_service` (警报服务)**](#24-alarm_service-警报服务)
        - [**2.5. `rpc_service` (RPC 服务)**](#25-rpc_service-rpc-服务)
        - [**2.6. `relation_service` (关系服务)**](#26-relation_service-关系服务)
    - [**3. 认证管理方法**](#3-认证管理方法)
        - [**3.1. `login()` (用户登录)**](#31-login-用户登录)
        - [**3.2. `is_authenticated` (检查是否已认证)**](#32-is_authenticated-检查是否已认证)
        - [**3.3. `logout()` (用户登出)**](#33-logout-用户登出)
        - [**3.4. `refresh_token()` (刷新访问令牌)**](#34-refresh_token-刷新访问令牌)
        - [**3.5. `_ensure_authenticated()` (确保客户端已认证)**](#35-_ensure_authenticated-确保客户端已认证)
    - [**4. HTTP 请求方法**](#4-http-请求方法)
        - [**4.1. `request()` (发送 HTTP 请求)**](#41-request-发送-http-请求)
        - [**4.2. `get()` (发送 GET 请求)**](#42-get-发送-get-请求)
        - [**4.3. `post()` (发送 POST 请求)**](#43-post-发送-post-请求)
        - [**4.4. `put()` (发送 PUT 请求)**](#44-put-发送-put-请求)
        - [**4.5. `delete()` (发送 DELETE 请求)**](#45-delete-发送-delete-请求)
    - [**5. 资源管理方法**](#5-资源管理方法)
        - [**5.1. `close()` (关闭客户端连接)**](#51-close-关闭客户端连接)
        - [**5.2. `__enter__()` (上下文管理器入口)**](#52-__enter__-上下文管理器入口)
        - [**5.3. `__exit__()` (上下文管理器退出)**](#53-__exit__-上下文管理器退出)

## 概述

`ThingsBoardClient` 类是 `thingsboardlink` 库的核心，封装了与 ThingsBoard REST ful API 进行交互的所有底层细节。它负责建立和维护与 ThingsBoard 服务器的连接、处理用户认证（包括 JWT 令牌的获取、刷新和管理）、发送 HTTP 请求，并提供统一的错误处理机制。此外，它通过属性提供了对各种 ThingsBoard 服务（如设备、遥测、警报等）的便捷访问。

## 核心功能

* **集中式认证管理**: 自动处理用户登录、JWT 令牌存储、过期检查和刷新，确保 API 调用的连续性。
* **健壮的 HTTP 请求**: 基于 `requests` 库构建，支持请求超时、SSL 验证以及可配置的请求重试策略，以提高网络操作的可靠性。
* **统一的错误处理**: 将底层 `requests` 异常和 ThingsBoard API 错误转换为 `thingsboardlink` 自定义的异常类型，简化了开发者的错误捕获和处理逻辑。
* **服务模块集成**: 通过属性懒加载方式，提供对设备、遥测、属性、警报、RPC 和关系等高级服务模块的无缝访问。
* **上下文管理器支持**: 允许客户端在 `with` 语句中使用，确保在退出作用域时自动执行登出和连接关闭操作。
* **灵活的配置**: 支持配置 ThingsBoard 基础 URL、认证凭据、超时时间、重试策略和 SSL 验证。

## ThingsBoardClient 详解

### 1. 客户端初始化 (`__init__`)

构造函数用于初始化 `ThingsBoardClient` 实例，配置与 ThingsBoard 服务器通信所需的基本参数。

* **参数**:
    * `base_url` (str): ThingsBoard 服务器的基础 URL (例如: `http://localhost:8080`)。
    * `username` (Optional[str]): 用于登录的 ThingsBoard 用户名。
    * `password` (Optional[str]): 用于登录的 ThingsBoard 密码。
    * `timeout` (float, default: 30.0): 所有 HTTP 请求的默认超时时间（秒）。
    * `max_retries` (int, default: 3): 对于可重试的 HTTP 状态码（如 429, 5xx），最大重试次数。
    * `retry_backoff_factor` (float, default: 0.3): 重试之间的退避因子。重试等待时间会随此因子指数增长。
    * `verify_ssl` (bool, default: `True`): 是否验证 ThingsBoard 服务器的 SSL 证书。设置为 `False` 会禁用 SSL 验证，但在生产环境中不推荐。
* **内部处理**:
    * 初始化 `_jwt_token`, `_refresh_token`, `_token_expires_at` 等认证相关内部状态。
    * 创建一个 `requests.Session` 对象，用于持久化连接和会话状态。
    * 配置 `HTTPAdapter` 以实现请求重试逻辑，针对特定的状态码和 HTTP 方法。
    * 设置默认的 `Content-Type` 和 `Accept` 请求头为 `application/json`。
    * 延迟导入并初始化各个服务模块的实例，以避免循环导入问题并提高性能。

### 2. 服务模块属性

这些属性提供了对不同 ThingsBoard 服务模块的访问。它们采用**懒加载**模式，即只有在首次访问时才会创建相应的服务实例。

#### 2.1. `device_service` (设备服务)

* **返回**: `DeviceService` 实例
* **说明**: 用于执行设备相关的操作，如创建、检索、更新和删除设备，以及管理设备的凭证。

#### 2.2. `telemetry_service` (遥测服务)

* **返回**: `TelemetryService` 实例
* **说明**: 用于上传、检索和管理设备的遥测数据。

#### 2.3. `attribute_service` (属性服务)

* **返回**: `AttributeService` 实例
* **说明**: 用于获取、设置和删除实体（如设备、资产）的客户端、服务端和共享属性。

#### 2.4. `alarm_service` (警报服务)

* **返回**: `AlarmService` 实例
* **说明**: 用于创建、查询、确认和清除 ThingsBoard 中的警报。

#### 2.5. `rpc_service` (RPC 服务)

* **返回**: `RpcService` 实例
* **说明**: 用于向设备发送同步或异步的远程过程调用 (RPC) 请求，并处理其响应。

#### 2.6. `relation_service` (关系服务)

* **返回**: `RelationService` 实例
* **说明**: 用于管理 ThingsBoard 实体之间的关系。

### 3. 认证管理方法

#### 3.1. `login()` (用户登录)

通过用户名和密码向 ThingsBoard 平台进行认证，获取并存储 JWT 访问令牌和刷新令牌。

* **参数**:
    * `username` (Optional[str]): 用于本次登录的用户名，如果未提供则使用客户端初始化时的用户名。
    * `password` (Optional[str]): 用于本次登录的密码，如果未提供则使用客户端初始化时的密码。
* **返回**:
    * `bool` - 如果登录成功则返回 `True`，否则返回 `False`。
* **抛出**:
    * `ConfigurationError`: 如果未提供用户名或密码。
    * `AuthenticationError`: 如果认证失败（例如，用户名或密码错误，或服务器返回非 200 状态码）。
    * `ConnectionError`: 如果无法连接到 ThingsBoard 服务器。
    * `TimeoutError`: 如果登录请求超时。
* **副作用**: 成功登录后，会在内部设置 `_jwt_token` 和 `_refresh_token`，并更新 `requests.Session` 的 `X-Authorization` 请求头。

#### 3.2. `is_authenticated` (检查是否已认证)

一个属性，用于检查客户端当前是否处于认证状态且访问令牌未过期。

* **返回**: `bool` - 如果已认证且令牌有效则返回 `True`，否则返回 `False`。

#### 3.3. `logout()` (用户登出)

使当前的 JWT 访问令牌失效，并清除客户端内部存储的所有认证信息。

* **返回**: `bool` - 登出操作是否成功（即使因网络问题无法通知服务器，本地凭据也会被清除）。
* **副作用**: 清除 `_jwt_token`, `_refresh_token`, `_token_expires_at`，并从 `requests.Session` 移除 `X-Authorization` 请求头。

#### 3.4. `refresh_token()` (刷新访问令牌)

使用刷新令牌（`_refresh_token`）从 ThingsBoard 服务器获取新的 JWT 访问令牌。

* **返回**: `bool` - 如果令牌刷新成功则返回 `True`，否则返回 `False`。
* **副作用**: 如果刷新成功，会更新 `_jwt_token`, `_refresh_token`, `_token_expires_at`，并更新 `requests.Session` 的 `X-Authorization` 请求头。

#### 3.5. `_ensure_authenticated()` (确保客户端已认证)

一个内部方法，在发送需要认证的请求之前调用。它会检查当前认证状态，如果令牌过期，则尝试刷新；如果刷新失败，则尝试重新登录。

* **抛出**: `AuthenticationError`: 如果经过刷新和重试登录后仍然无法认证。

### 4. HTTP 请求方法

`ThingsBoardClient` 提供了用于发送各种 HTTP 请求的通用方法和便捷包装器。

#### 4.1. `request()` (发送 HTTP 请求)

底层通用的 HTTP 请求发送方法。所有 `get/post/put/delete` 方法最终都会调用此方法。

* **参数**:
    * `method` (str): HTTP 请求方法（如 "GET", "POST", "PUT", "DELETE"）。
    * `endpoint` (str): ThingsBoard API 的相对路径（例如: `"/api/device"`）。
    * `data` (Optional[Union[Dict[str, Any], str]]): 请求体数据，可以是字典（将被 JSON 序列化）或字符串。
    * `params` (Optional[Dict[str, Any]]): URL 查询参数字典。
    * `headers` (Optional[Dict[str, str]]): 额外的请求头部字典。
    * `require_auth` (bool, default: `True`): 是否需要认证。如果为 `True`，在发送请求前会调用 `_ensure_authenticated()`。
    * `timeout` (Optional[float]): 本次请求的超时时间（秒）。如果未提供，则使用客户端实例的默认 `timeout`。
* **返回**:
    * `requests.Response` - 原始的 HTTP 响应对象。
* **抛出**:
    * `AuthenticationError`: 如果 `require_auth` 为 `True` 但客户端未认证。
    * `APIError`: 如果 ThingsBoard API 返回 4xx 或 5xx 状态码。
    * `ConnectionError`: 如果发生网络连接错误。
    * `TimeoutError`: 如果请求超时。

#### 4.2. `get()` (发送 GET 请求)

发送 HTTP GET 请求的便捷方法。

* **参数**: `**kwargs` - 传递给 `request()` 方法的所有额外参数（如 `endpoint`, `params`, `headers`, `require_auth`, `timeout`）。
* **返回**: `requests.Response`。

#### 4.3. `post()` (发送 POST 请求)

发送 HTTP POST 请求的便捷方法。

* **参数**: `**kwargs` - 传递给 `request()` 方法的所有额外参数（如 `endpoint`, `data`, `params`, `headers`, `require_auth`, `timeout`）。
* **返回**: `requests.Response`。

#### 4.4. `put()` (发送 PUT 请求)

发送 HTTP PUT 请求的便捷方法。

* **参数**: `**kwargs` - 传递给 `request()` 方法的所有额外参数（如 `endpoint`, `data`, `params`, `headers`, `require_auth`, `timeout`）。
* **返回**: `requests.Response`。

#### 4.5. `delete()` (发送 DELETE 请求)

发送 HTTP DELETE 请求的便捷方法。

* **参数**: `**kwargs` - 传递给 `request()` 方法的所有额外参数（如 `endpoint`, `params`, `headers`, `require_auth`, `timeout`）。
* **返回**: `requests.Response`。

### 5. 资源管理方法

#### 5.1. `close()` (关闭客户端连接)

关闭内部 `requests.Session` 对象，释放相关的网络资源。

#### 5.2. `__enter__()` (上下文管理器入口)

实现上下文管理器协议的入口点。当 `ThingsBoardClient` 对象进入 `with` 语句块时被调用。

* **返回**: `self` - 客户端实例本身。

#### 5.3. `__exit__()` (上下文管理器退出)

实现上下文管理器协议的出口点。当 `ThingsBoardClient` 对象退出 `with` 语句块时被调用，它会自动执行 `logout()` 和 `close()`
操作，确保资源的正确释放和认证状态的清除。

* **参数**: `exc_type`, `exc_val`, `exc_tb` - 异常信息（如果 `with` 块中发生异常）。
