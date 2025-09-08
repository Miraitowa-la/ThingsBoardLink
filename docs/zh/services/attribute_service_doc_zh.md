# thingsboardlink 属性服务模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的属性服务模块 (`attribute_service.py`)，该模块封装了与 ThingsBoard 平台进行属性管理相关的所有 API 调用功能。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**属性服务类详解**](#属性服务类详解)
    - [**1. `AttributeService` (属性服务类)**](#1-attributeservice-属性服务类)
        - [**1.1. `__init__()` (初始化属性服务)**](#11-__init__-初始化属性服务)
        - [**1.2. `_get_attributes()` (获取指定范围的属性)**](#12-_get_attributes-获取指定范围的属性)
        - [**1.3. `_set_attributes()` (设置指定范围的属性)**](#13-_set_attributes-设置指定范围的属性)
        - [**1.4. `get_client_attributes()` (获取客户端属性)**](#14-get_client_attributes-获取客户端属性)
        - [**1.5. `get_server_attributes()` (获取服务端属性)**](#15-get_server_attributes-获取服务端属性)
        - [**1.6. `get_shared_attributes()` (获取共享属性)**](#16-get_shared_attributes-获取共享属性)
        - [**1.7. `set_server_attributes()` (设置服务端属性)**](#17-set_server_attributes-设置服务端属性)
        - [**1.8. `set_shared_attributes()` (设置共享属性)**](#18-set_shared_attributes-设置共享属性)
        - [**1.9. `delete_attributes()` (删除属性)**](#19-delete_attributes-删除属性)
        - [**1.10. `get_attribute_keys()` (获取属性键列表)**](#110-get_attribute_keys-获取属性键列表)
        - [**1.11. `get_all_attributes()` (获取设备的所有属性)**](#111-get_all_attributes-获取设备的所有属性)
        - [**1.12. `update_attribute()` (更新单个属性)**](#112-update_attribute-更新单个属性)
        - [**1.13. `attribute_exists()` (检查属性是否存在)**](#113-attribute_exists-检查属性是否存在)

## 概述

`thingsboardlink.services.attribute_service` 模块提供了用于管理 ThingsBoard 平台上实体（主要是设备）属性的功能。它封装了对 ThingsBoard REST API 属性相关端点的调用，使得开发者能够通过类型安全的 Python 方法执行客户端属性、服务端属性和共享属性的读取、设置、更新和删除操作。该模块旨在简化对设备或实体元数据和配置的管理。

## 核心功能

* **属性范围支持**: 全面支持 ThingsBoard 中的三种属性范围：客户端属性 (`CLIENT_SCOPE`)、服务端属性 (`SERVER_SCOPE`)和共享属性 (`SHARED_SCOPE`)。
* **属性 CRUD 操作**: 提供获取、设置（创建/更新）和删除属性的基本功能。
* **批量属性操作**: 支持一次性获取或设置多个属性。
* **属性键列表获取**: 获取指定范围内的所有属性键列表。
* **所有属性一次性获取**: 能够一次性获取设备在所有范围内的属性。
* **属性存在性检查**: 快速判断指定范围和键的属性是否存在。
* **错误处理**: 将 ThingsBoard API 返回的错误转换为 `thingsboardlink` 自定义的异常（如 `ValidationError`, `NotFoundError`, `APIError`），提供更清晰的错误信息。

## 属性服务类详解

### 1. `AttributeService` (属性服务类)

`AttributeService` 类是属性管理功能的入口点，通过它您可以执行所有与属性相关的操作。

#### 1.1. `__init__()` (初始化属性服务)

构造函数用于初始化 `AttributeService` 实例，它需要一个已配置的 `ThingsBoardClient` 实例来发送 HTTP 请求。

* **参数**:
    * `client`: `ThingsBoardClient` 实例，用于与 ThingsBoard 平台进行通信。

#### 1.2. `_get_attributes()` (获取指定范围的属性)

这是一个内部辅助方法，用于根据指定的设备 ID、属性范围和可选的键列表从 ThingsBoard 获取属性数据。它会处理 API 响应并将其转换为更友好的字典格式。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `scope` (`AttributeScope`): 要获取的属性范围。
    * `keys` (Optional[List[str]]): 要获取的属性键列表。如果为 `None`，则获取该范围内的所有属性。
* **返回**:
    * `Dict[str, Any]` - 一个字典，其中键是属性键，值是包含 `value` 和 `lastUpdateTs` 的字典。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `NotFoundError`: 如果设备不存在。
    * `APIError`: 如果获取属性失败。

#### 1.3. `_set_attributes()` (设置指定范围的属性)

这是一个内部辅助方法，用于根据指定的设备 ID、属性范围和属性数据设置（创建或更新）属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `scope` (`AttributeScope`): 要设置的属性范围。
    * `attributes` (Union[Dict[str, Any], List[Attribute]]): 要设置的属性数据。可以是：
        * `Dict[str, Any]`: 键值对字典，例如 `{"firmwareVersion": "1.0.1", "location": "Warehouse A"}`。
        * `List[Attribute]`: `Attribute` 对象的列表。
* **返回**:
    * `bool` - 如果设置成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 或 `attributes` 参数无效，或 `attributes` 列表中包含非 `Attribute` 对象。
    * `APIError`: 如果设置属性失败。

#### 1.4. `get_client_attributes()` (获取客户端属性)

获取指定设备的客户端属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `keys` (Optional[List[str]]): 要获取的属性键列表。如果为 `None`，则获取所有客户端属性。
* **返回**:
    * `Dict[str, Any]` - 客户端属性数据。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `NotFoundError`: 如果设备不存在。

#### 1.5. `get_server_attributes()` (获取服务端属性)

获取指定设备的服务端属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `keys` (Optional[List[str]]): 要获取的属性键列表。如果为 `None`，则获取所有服务端属性。
* **返回**:
    * `Dict[str, Any]` - 服务端属性数据。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `NotFoundError`: 如果设备不存在。

#### 1.6. `get_shared_attributes()` (获取共享属性)

获取指定设备的共享属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `keys` (Optional[List[str]]): 要获取的属性键列表。如果为 `None`，则获取所有共享属性。
* **返回**:
    * `Dict[str, Any]` - 共享属性数据。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `NotFoundError`: 如果设备不存在。

#### 1.7. `set_server_attributes()` (设置服务端属性)

设置指定设备的服务端属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `attributes` (Union[Dict[str, Any], List[Attribute]]): 要设置的服务端属性数据。
* **返回**:
    * `bool` - 如果设置成功则返回 `True`。
* **抛出**:
    * `ValidationError`, `APIError`。

#### 1.8. `set_shared_attributes()` (设置共享属性)

设置指定设备的共享属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `attributes` (Union[Dict[str, Any], List[Attribute]]): 要设置的共享属性数据。
* **返回**:
    * `bool` - 如果设置成功则返回 `True`。
* **抛出**:
    * `ValidationError`, `APIError`。

#### 1.9. `delete_attributes()` (删除属性)

删除指定设备、指定范围的一个或多个属性。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `scope` (`AttributeScope`): 要删除属性的范围。
    * `keys` (List[str]): 要删除的属性键列表。
* **返回**:
    * `bool` - 如果删除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `device_id`、`scope` 或 `keys` 参数无效。
    * `APIError`: 如果删除属性失败。

#### 1.10. `get_attribute_keys()` (获取属性键列表)

获取指定设备和指定范围内的所有属性键列表。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `scope` (`AttributeScope`): 要查询属性键的范围。
* **返回**:
    * `List[str]` - 属性键的字符串列表。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `APIError`: 如果获取属性键失败。

#### 1.11. `get_all_attributes()` (获取设备的所有属性)

一次性获取指定设备的所有属性，按客户端、服务端和共享范围分组。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
* **返回**:
    * `Dict[str, Dict[str, Any]]` - 一个嵌套字典，包含所有属性数据，外层键为 "client", "server", "shared"。
* **抛出**:
    * `ValidationError`: 如果 `device_id` 为空或无效。
    * `APIError`: 如果获取任何范围的属性失败。

#### 1.12. `update_attribute()` (更新单个属性)

更新指定设备、指定范围的单个属性。这是一个便捷方法，底层调用 `_set_attributes`。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `scope` (`AttributeScope`): 属性范围。
    * `key` (str): 属性键。
    * `value` (Any): 属性的新值。
* **返回**:
    * `bool` - 如果更新成功则返回 `True`。
* **抛出**:
    * `ValidationError`, `APIError`。

#### 1.13. `attribute_exists()` (检查属性是否存在)

检查指定设备、指定范围和键的属性是否存在。

* **参数**:
    * `device_id` (str): 设备的唯一标识符。
    * `scope` (`AttributeScope`): 属性范围。
    * `key` (str): 要检查的属性键。
* **返回**:
    * `bool` - 如果属性存在则返回 `True`，否则返回 `False`。