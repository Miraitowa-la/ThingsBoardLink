# thingsboardlink 设备服务模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的设备服务模块 (`device_service.py`)，该模块封装了与 ThingsBoard 平台进行设备管理相关的所有 API 调用功能。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**设备服务类详解**](#设备服务类详解)
    - [**1. `DeviceService` (设备服务类)**](#1-deviceservice-设备服务类)
        - [**1.1. `__init__()` (初始化设备服务)**](#11-__init__-初始化设备服务)
        - [**1.2. `create_device()` (创建设备)**](#12-create_device-创建设备)
        - [**1.3. `get_device_by_id()` (根据 ID 获取设备)**](#13-get_device_by_id-根据-id-获取设备)
        - [**1.4. `update_device()` (更新设备信息)**](#14-update_device-更新设备信息)
        - [**1.5. `delete_device()` (删除设备)**](#15-delete_device-删除设备)
        - [**1.6. `get_tenant_devices()` (获取租户下的设备列表)**](#16-get_tenant_devices-获取租户下的设备列表)
        - [**1.7. `get_device_credentials()` (获取设备凭证)**](#17-get_device_credentials-获取设备凭证)
        - [**1.8. `get_devices_by_name()` (根据名称搜索设备)**](#18-get_devices_by_name-根据名称搜索设备)
        - [**1.9. `device_exists()` (检查设备是否存在)**](#19-device_exists-检查设备是否存在)

## 概述

`thingsboardlink.services.device_service` 模块提供了用于管理 ThingsBoard 平台上设备实体的功能。它封装了对 ThingsBoard REST API `/api/device` 和 `/api/tenant/devices` 等端点的调用，使得开发者能够通过类型安全的 Python 方法执行设备的创建、查询、更新、删除以及凭证管理等操作。该模块旨在简化设备生命周期的管理。

## 核心功能

* **设备 CRUD 操作**: 提供创建、按 ID 获取、更新和删除设备的基本功能。
* **设备凭证管理**: 允许获取指定设备的认证凭证。
* **批量设备查询**: 支持按租户查询设备列表，并提供分页、文本搜索和排序功能。
* **按名称搜索设备**: 提供根据设备名称进行搜索的功能，返回匹配的设备列表。
* **设备存在性检查**: 快速判断某个设备 ID 对应的设备是否存在。
* **错误处理**: 将 ThingsBoard API 返回的错误转换为 `thingsboardlink` 自定义的异常（如 `NotFoundError`, `DeviceError`, `ValidationError`），提供更清晰的错误信息。

## 设备服务类详解

### 1. `DeviceService` (设备服务类)

`DeviceService` 类是设备管理功能的入口点，通过它您可以执行所有与设备相关的操作。

#### 1.1. `__init__()` (初始化设备服务)

构造函数用于初始化 `DeviceService` 实例，它需要一个已配置的 `ThingsBoardClient` 实例来发送 HTTP 请求。

* **参数**:
    * `client`: `ThingsBoardClient` 实例，用于与 ThingsBoard 平台进行通信。

#### 1.2. `create_device()` (创建设备)

在 ThingsBoard 平台上创建一个新的设备。

* **参数**:
    * `name` (str): 设备的唯一名称。
    * `device_type` (str, default: "default"): 设备的类型标识。
    * `label` (Optional[str]): 设备的标签，用于标识或分类。
    * `additional_info` (Optional[Dict[str, Any]]): 设备的额外 JSON 格式信息。
* **返回**:
    * `Device` - 创建成功的设备对象。
* **抛出**:
    * `ValidationError`: 如果设备名称为空或无效。
    * `DeviceError`: 如果设备创建失败（通常是由于 API 调用错误）。

#### 1.3. `get_device_by_id()` (根据 ID 获取设备)

根据设备的唯一 ID 获取设备详情。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
* **返回**:
    * `Device` - 匹配的设备对象。
* **抛出**:
    * `ValidationError`: 如果设备 ID 为空或无效。
    * `NotFoundError`: 如果指定 ID 的设备不存在。
    * `DeviceError`: 如果获取设备失败。

#### 1.4. `update_device()` (更新设备信息)

更新现有设备的属性。此方法通过发送包含完整设备对象的 POST 请求来实现更新。

* **参数**:
    * `device` (`Device`): 包含要更新设备 ID 和新属性值的设备对象。
* **返回**:
    * `Device` - 更新后的设备对象。
* **抛出**:
    * `ValidationError`: 如果设备对象缺少 ID 或名称无效。
    * `DeviceError`: 如果设备更新失败。

#### 1.5. `delete_device()` (删除设备)

根据设备的 ID 删除 ThingsBoard 上的设备。

* **参数**:
    * `device_id` (str): 要删除设备的唯一标识符。
* **返回**:
    * `bool` - 如果删除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果设备 ID 为空或无效。
    * `DeviceError`: 如果设备删除失败。

#### 1.6. `get_tenant_devices()` (获取租户下的设备列表)

获取当前租户下的所有设备列表，支持分页、文本搜索和排序。

* **参数**:
    * `page_size` (int, default: 10): 每页返回的设备数量。
    * `page` (int, default: 0): 要获取的页码（从 0 开始）。
    * `text_search` (Optional[str]): 用于模糊匹配设备名称、类型或标签的搜索文本。
    * `sort_property` (Optional[str]): 用于排序的设备属性（例如 "name", "type", "createdTime"）。
    * `sort_order` (Optional[str]): 排序顺序，可以是 "ASC" (升序) 或 "DESC" (降序)。
* **返回**:
    * `PageData` - 包含设备列表和分页信息的对象。
* **抛出**:
    * `ValidationError`: 如果 `page_size` 或 `page` 参数无效。
    * `DeviceError`: 如果获取设备列表失败。

#### 1.7. `get_device_credentials()` (获取设备凭证)

获取指定设备的认证凭证，例如设备访问令牌。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
* **返回**:
    * `DeviceCredentials` - 设备的凭证对象。
* **抛出**:
    * `ValidationError`: 如果设备 ID 为空或无效。
    * `NotFoundError`: 如果指定设备的凭证不存在。
    * `DeviceError`: 如果获取设备凭证失败。

#### 1.8. `get_devices_by_name()` (根据名称搜索设备)

通过设备名称在当前租户下搜索匹配的设备。此方法会进行精确（不区分大小写）匹配。

* **参数**:
    * `device_name` (str): 要搜索的设备名称。
* **返回**:
    * `List[Device]` - 匹配的设备对象列表。
* **抛出**:
    * `ValidationError`: 如果设备名称为空或无效。
    * `DeviceError`: 如果搜索设备失败。

#### 1.9. `device_exists()` (检查设备是否存在)

检查具有给定 ID 的设备是否存在于 ThingsBoard 平台上。

* **参数**:
    * `device_id` (str): 要检查的设备 ID。
* **返回**:
    * `bool` - 如果设备存在则返回 `True`，否则返回 `False`。