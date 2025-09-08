# thingsboardlink 关系服务模块说明文档

本文档详细介绍了 `thingsboardlink` 软件包中的关系服务模块 (`relation_service.py`)，该模块封装了与 ThingsBoard
平台进行实体关系管理相关的所有 API 调用功能。

## 目录

- [**概述**](#概述)
- [**核心功能**](#核心功能)
- [**关系服务类详解**](#关系服务类详解)
    - [**1. `RelationService` (关系服务类)**](#1-relationservice-关系服务类)
        - [**1.1. `__init__()` (初始化关系服务)**](#11-___init___-初始化关系服务)
        - [**1.2. `create_relation()` (创建实体关系)**](#12-create_relation-创建实体关系)
        - [**1.3. `delete_relation()` (删除实体关系)**](#13-delete_relation-删除实体关系)
        - [**1.4. `get_relation()` (获取实体关系)**](#14-get_relation-获取实体关系)
        - [**1.5. `find_by_from()` (查找从指定实体出发的所有关系)**](#15-find_by_from-查找从指定实体出发的所有关系)
        - [**1.6. `find_by_to()` (查找指向指定实体的所有关系)**](#16-find_by_to-查找指向指定实体的所有关系)
        - [**1.7. `relation_exists()` (检查实体关系是否存在)**](#17-relation_exists-检查实体关系是否存在)
        - [**1.8. `delete_relations()` (删除实体的所有关系)**](#18-delete_relations-删除实体的所有关系)

## 概述

`thingsboardlink.services.relation_service` 模块提供了用于管理 ThingsBoard 平台上实体间关系的功能。它封装了对 ThingsBoard REST API `/api/relation` 和 `/api/relations` 等端点的调用，使得开发者能够通过类型安全的 Python 方法执行实体关系的创建、删除和查询等操作。该模块旨在简化对 ThingsBoard 实体拓扑结构的管理。

## 核心功能

* **关系创建**: 允许在 ThingsBoard 实体之间创建新的关系。
* **关系删除**: 支持删除指定的单个实体关系，或删除某个实体的所有出入关系。
* **关系查询**: 提供根据源实体、目标实体或特定关系类型来查询关系的功能。
* **关系存在性检查**: 快速判断两个实体之间是否存在某种特定关系。
* **错误处理**: 将 ThingsBoard API 返回的错误转换为 `thingsboardlink` 自定义的异常（如 `ValidationError`, `APIError`），提供更清晰的错误信息。

## 关系服务类详解

### 1. `RelationService` (关系服务类)

`RelationService` 类是关系管理功能的入口点，通过它您可以执行所有与实体关系相关的操作。

#### 1.1. `__init__()` (初始化关系服务)

构造函数用于初始化 `RelationService` 实例，它需要一个已配置的 `ThingsBoardClient` 实例来发送 HTTP 请求。

* **参数**:
    * `client`: `ThingsBoardClient` 实例，用于与 ThingsBoard 平台进行通信。

#### 1.2. `create_relation()` (创建实体关系)

在 ThingsBoard 平台上创建两个实体之间的新关系。

* **参数**:
    * `from_id` (str): 源实体的 ID。
    * `from_type` (`EntityType`): 源实体的类型。
    * `to_id` (str): 目标实体的 ID。
    * `to_type` (`EntityType`): 目标实体的类型。
    * `relation_type` (str): 关系的类型，例如 "Contains", "Manages" 等。
    * `type_group` (str, default: "COMMON"): 关系类型组，默认为 "COMMON"。
    * `additional_info` (Optional[Dict[str, Any]]): 关系的额外 JSON 格式信息。
* **返回**:
    * `EntityRelation` - 创建成功的关系对象。
* **抛出**:
    * `ValidationError`: 如果 `from_id`, `to_id` 或 `relation_type` 为空或无效。
    * `APIError`: 如果关系创建失败（通常是由于 API 调用错误）。

#### 1.3. `delete_relation()` (删除实体关系)

删除 ThingsBoard 上两个实体之间指定的单个关系。

* **参数**:
    * `from_id` (str): 源实体的 ID。
    * `from_type` (`EntityType`): 源实体的类型。
    * `to_id` (str): 目标实体的 ID。
    * `to_type` (`EntityType`): 目标实体的类型。
    * `relation_type` (str): 要删除的关系类型。
    * `type_group` (str, default: "COMMON"): 关系类型组。
* **返回**:
    * `bool` - 如果删除成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `from_id`, `to_id` 或 `relation_type` 为空或无效。
    * `APIError`: 如果关系删除失败。

#### 1.4. `get_relation()` (获取实体关系)

获取 ThingsBoard 上两个实体之间指定的单个关系详情。

* **参数**:
    * `from_id` (str): 源实体的 ID。
    * `from_type` (`EntityType`): 源实体的类型。
    * `to_id` (str): 目标实体的 ID。
    * `to_type` (`EntityType`): 目标实体的类型。
    * `relation_type` (str): 要获取的关系类型。
    * `type_group` (str, default: "COMMON"): 关系类型组。
* **返回**:
    * `Optional[EntityRelation]` - 如果关系存在则返回关系对象，否则返回 `None`。
* **抛出**:
    * `ValidationError`: 如果 `from_id`, `to_id` 或 `relation_type` 为空或无效。
    * `APIError`: 如果获取关系失败。

#### 1.5. `find_by_from()` (查找从指定实体出发的所有关系)

查找所有以指定实体为源 (`from`) 的关系。

* **参数**:
    * `from_id` (str): 源实体的 ID。
    * `from_type` (`EntityType`): 源实体的类型。
    * `relation_type_group` (str, default: "COMMON"): 关系类型组。
* **返回**:
    * `List[EntityRelation]` - 从该实体出发的关系列表。
* **抛出**:
    * `ValidationError`: 如果 `from_id` 为空或无效。
    * `APIError`: 如果查找关系失败。

#### 1.6. `find_by_to()` (查找指向指定实体的所有关系)

查找所有以指定实体为目标 (`to`) 的关系。

* **参数**:
    * `to_id` (str): 目标实体的 ID。
    * `to_type` (`EntityType`): 目标实体的类型。
    * `relation_type_group` (str, default: "COMMON"): 关系类型组。
* **返回**:
    * `List[EntityRelation]` - 指向该实体的关系列表。
* **抛出**:
    * `ValidationError`: 如果 `to_id` 为空或无效。
    * `APIError`: 如果查找关系失败。

#### 1.7. `relation_exists()` (检查实体关系是否存在)

检查两个实体之间是否存在具有指定类型和类型组的关系。

* **参数**:
    * `from_id` (str): 源实体的 ID。
    * `from_type` (`EntityType`): 源实体的类型。
    * `to_id` (str): 目标实体的 ID。
    * `to_type` (`EntityType`): 目标实体的类型。
    * `relation_type` (str): 要检查的关系类型。
    * `type_group` (str, default: "COMMON"): 关系类型组。
* **返回**:
    * `bool` - 如果关系存在则返回 `True`，否则返回 `False`。

#### 1.8. `delete_relations()` (删除实体的所有关系)

删除指定实体的所有出入关系，可以根据方向 (`FROM`, `TO`, `BOTH`) 进行选择性删除。

* **参数**:
    * `entity_id` (str): 要删除关系的实体 ID。
    * `entity_type` (`EntityType`): 要删除关系的实体类型。
    * `direction` (str, default: "FROM"): 删除关系的方向。可选值包括 "FROM" (删除所有从该实体出发的关系), "TO" (删除所有指向该实体的关系), "BOTH" (删除所有出入关系)。
* **返回**:
    * `bool` - 如果所有指定的删除操作都成功则返回 `True`。
* **抛出**:
    * `ValidationError`: 如果 `entity_id` 或 `direction` 参数无效。
    * `APIError`: 如果删除关系失败。