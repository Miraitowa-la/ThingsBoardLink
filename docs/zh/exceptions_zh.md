# thingsboardlink 异常处理模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中定义的各种自定义异常类，旨在帮助开发者理解和利用这些异常进行健壮的错误处理。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**异常类详解**](#异常类详解)
    - [**1. ThingsBoardError**](#1-thingsboarderror)
    - [**2. AuthenticationError**](#2-authenticationerror)
    - [**3. NotFoundError**](#3-notfounderror)
    - [**4. ValidationError**](#4-validationerror)
    - [**5. APIError**](#5-apierror)
    - [**6. ConnectionError**](#6-connectionerror)
    - [**7. TimeoutError**](#7-timeouterror)
    - [**8. ConfigurationError**](#8-configurationerror)
    - [**9. RateLimitError**](#9-ratelimiterror)
    - [**10. DeviceError**](#10-deviceerror)
    - [**11. TelemetryError**](#11-telemetryerror)
    - [**12. AlarmError**](#12-alarmerror)
    - [**13. RPCError**](#13-rpcerror)

## 概述

`thingsboardlink` 异常处理模块 (`exceptions.py`) 集中定义了 `thingsboardlink` 软件包在和 ThingsBoard 平台交互过程中可能遇到的所有自定义异常。这些异常类提供了一种结构化的方式来报告和处理错误，通过详细的错误信息和分层的继承关系，帮助开发者更准确地诊断问题并实现更健壮的应用程序。

## 核心功能

* **统一的异常基类**: 提供 `ThingsBoardError` 作为所有 `thingsboardlink` 相关异常的基类，方便进行统一的异常捕获和处理。
* **细粒度的错误分类**: 将潜在的错误场景划分为多个具体的异常子类，如认证、资源未找到、API 调用失败、连接问题、数据验证等，使得错误类型一目了然。
* **丰富的错误详情**: 每个异常类都支持存储 `message` (错误信息) 和 `details` (详细字典) 等属性，以便在捕获异常时获取更全面的上下文信息。
* **易于构造**: 异常构造函数通常接受特定于错误的参数，如资源类型、字段名称、状态码等，以便自动生成有意义的错误消息和详情。
* **HTTP 响应集成**: `APIError` 提供了 `from_response` 类方法，可以直接从 HTTP 响应对象构建异常，简化了 API 错误的处理。

## 异常类详解

### 1. ThingsBoardError

`ThingsBoardError` 是所有 `thingsboardlink` 异常的基类。它提供了统一的异常处理接口和基础功能，包括错误消息 (`message`)和可选的错误详情字典 (`details`)。

* **继承**: `Exception`
* **构造函数**:
    * `message` (str): 错误的主要信息。
    * `details` (Optional[Dict[str, Any]]): 包含额外错误上下文信息的字典。
* **属性**:
    * `message`: 存储传入的错误信息。
    * `details`: 存储传入的错误详情字典。

### 2. AuthenticationError

当用户认证失败时抛出此异常，例如登录失败、令牌过期或权限不足。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str, default: "认证失败"): 认证失败的描述。
    * `details` (Optional[Dict[str, Any]]): 认证失败的额外详情。

### 3. NotFoundError

当请求的 ThingsBoard 资源（如设备、用户、警报等）不存在时抛出此异常。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `resource_type` (str, default: "资源"): 未找到的资源类型。
    * `resource_id` (Optional[str]): 未找到资源的具体 ID。
    * `message` (Optional[str]): 错误信息，如果未提供则根据 `resource_type` 和 `resource_id` 自动生成。

### 4. ValidationError

当输入数据不符合预期格式或约束时抛出此异常，例如参数类型错误、值范围错误或必填字段缺失。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `field_name` (Optional[str]): 发生验证错误的字段名称。
    * `expected_type` (Optional[str]): 字段期望的数据类型。
    * `actual_value` (Any): 字段的实际值。
    * `message` (Optional[str]): 错误信息，如果未提供则根据 `field_name` 和 `expected_type` 自动生成。

### 5. APIError

当 API 调用返回错误状态码时（例如 HTTP 4xx, 5xx）抛出此异常。它包含详细的 HTTP 状态码、响应数据、请求 URL 和请求方法。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str): 错误信息。
    * `status_code` (Optional[int]): HTTP 状态码。
    * `response_data` (Optional[Dict[str, Any]]): 服务器响应的 JSON 数据。
    * `request_url` (Optional[str]): 发送请求的 URL。
    * `request_method` (Optional[str]): 请求使用的 HTTP 方法。
* **属性**:
    * `status_code`: HTTP 状态码。
    * `response_data`: 服务器响应数据。
    * `request_url`: 请求的 URL。
    * `request_method`: 请求的 HTTP 方法。
* **类方法**:
    * `from_response(cls, response, message: Optional[str] = None)`: 从 HTTP 响应对象（例如 `requests.Response`）创建`APIError` 实例。它会自动解析状态码、响应数据、URL 和方法。

### 6. ConnectionError

当无法连接到 ThingsBoard 服务器时抛出此异常，例如网络连接失败或服务器不可达。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str, default: "无法连接到 ThingsBoard 服务器"): 连接错误的描述。
    * `server_url` (Optional[str]): 尝试连接的服务器地址。
    * `details` (Optional[Dict[str, Any]]): 额外详情。

### 7. TimeoutError

当请求操作超时（例如连接超时或读取超时）时抛出此异常。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str, default: "请求超时"): 超时错误的描述。
    * `timeout_seconds` (Optional[float]): 设定的超时时间（秒）。
    * `operation` (Optional[str]): 发生超时的具体操作。

### 8. ConfigurationError

当配置参数无效或缺失时抛出此异常，例如服务器地址配置错误或认证信息缺失。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str, default: "配置错误"): 配置错误的描述。
    * `config_key` (Optional[str]): 发生错误的配置项键名。
    * `expected_value` (Optional[str]): 配置项的期望值或格式。

### 9. RateLimitError

当 API 调用超过 ThingsBoard 服务器设定的速率限制时抛出此异常。它是 `APIError` 的子类，通常伴随 HTTP 429 状态码。

* **继承**: `APIError`
* **构造函数**:
    * `message` (str, default: "API 调用速率超限"): 速率限制的描述。
    * `retry_after` (Optional[int]): 建议等待多少秒后重试。
    * `limit_type` (Optional[str]): 速率限制的类型（例如，按 IP、按用户等）。

### 10. DeviceError

处理设备相关的操作错误，例如设备创建失败、设备状态异常或设备属性操作失败。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str): 错误信息。
    * `device_id` (Optional[str]): 涉及设备的 ID。
    * `device_name` (Optional[str]): 涉及设备的名称。

### 11. TelemetryError

处理遥测数据相关的操作错误，例如数据格式不正确、遥测数据上传失败。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str): 错误信息。
    * `data_key` (Optional[str]): 遥测数据中的键。
    * `data_value` (Any): 遥测数据的值。

### 12. AlarmError

处理警报相关的操作错误，例如警报创建失败、警报状态更新失败。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str): 错误信息。
    * `alarm_id` (Optional[str]): 涉及警报的 ID。
    * `alarm_type` (Optional[str]): 涉及警报的类型。

### 13. RPCError

处理远程过程调用 (RPC) 相关的错误，例如 RPC 调用超时、设备未响应或 RPC 请求格式错误。

* **继承**: `ThingsBoardError`
* **构造函数**:
    * `message` (str): 错误信息。
    * `method_name` (Optional[str]): 调用的 RPC 方法名称。
    * `device_id` (Optional[str]): 目标设备的 ID。
    * `timeout_seconds` (Optional[float]): RPC 调用的超时时间（秒）。
