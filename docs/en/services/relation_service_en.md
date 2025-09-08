# thingsboardlink Relation Service Module Documentation

This document provides a detailed description of the relation service module (`relation_service.py`) within the `thingsboardlink` package. This module encapsulates all API call functionalities related to entity relation management with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Relation Service Class Details**](#relation-service-class-details)
    - [**1. `RelationService` (Relation Service Class)**](#1-relationservice-relation-service-class)
        - [**1.1. `__init__()` (Initialize Relation Service)**](#11-___init___-initialize-relation-service)
        - [**1.2. `create_relation()` (Create Entity Relation)**](#12-create_relation-create-entity-relation)
        - [**1.3. `delete_relation()` (Delete Entity Relation)**](#13-delete_relation-delete-entity-relation)
        - [**1.4. `get_relation()` (Get Entity Relation)**](#14-get_relation-get-entity-relation)
        - [**1.5. `find_by_from()` (Find All Relations from a Specified Entity)**](#15-find_by_from-find-all-relations-from-a-specified-entity)
        - [**1.6. `find_by_to()` (Find All Relations Pointing to a Specified Entity)**](#16-find_by_to-find-all-relations-pointing-to-a-specified-entity)
        - [**1.7. `relation_exists()` (Check if Entity Relation Exists)**](#17-relation_exists-check-if-entity-relation-exists)
        - [**1.8. `delete_relations()` (Delete All Relations of an Entity)**](#18-delete_relations-delete-all-relations-of-an-entity)

## Overview

The `thingsboardlink.services.relation_service` module provides functionalities for managing relationships between entities on the ThingsBoard platform. It encapsulates calls to ThingsBoard REST API `/api/relation` and `/api/relations` endpoints, enabling developers to perform creation, deletion, and querying of entity relations through type-safe Python methods. This module aims to simplify the management of ThingsBoard entity topology.

## Core Features

*   **Relation Creation**: Allows creating new relations between ThingsBoard entities.
*   **Relation Deletion**: Supports deleting a specified single entity relation, or deleting all incoming and outgoing relations of an entity.
*   **Relation Query**: Provides functionality to query relations based on source entity, target entity, or specific relation type.
*   **Relation Existence Check**: Quickly determines if a specific relation exists between two entities.
*   **Error Handling**: Converts errors returned by the ThingsBoard API into `thingsboardlink`'s custom exceptions (e.g., `ValidationError`, `APIError`), providing clearer error messages.

## Relation Service Class Details

### 1. `RelationService` (Relation Service Class)

The `RelationService` class is the entry point for relation management functionalities, through which you can perform all entity relation-related operations.

#### 1.1. `__init__()` (Initialize Relation Service)

The constructor initializes a `RelationService` instance, requiring a configured `ThingsBoardClient` instance to send HTTP requests.

*   **Parameters**:
    *   `client`: A `ThingsBoardClient` instance, used for communication with the ThingsBoard platform.

#### 1.2. `create_relation()` (Create Entity Relation)

Creates a new relation between two entities on the ThingsBoard platform.

*   **Parameters**:
    *   `from_id` (str): The ID of the source entity.
    *   `from_type` (`EntityType`): The type of the source entity.
    *   `to_id` (str): The ID of the target entity.
    *   `to_type` (`EntityType`): The type of the target entity.
    *   `relation_type` (str): The type of the relation, e.g., "Contains", "Manages".
    *   `type_group` (str, default: "COMMON"): The relation type group, defaults to "COMMON".
    *   `additional_info` (Optional[Dict[str, Any]]): Additional JSON formatted information for the relation.
*   **Returns**:
    *   `EntityRelation` - The successfully created relation object.
*   **Raises**:
    *   `ValidationError`: If `from_id`, `to_id`, or `relation_type` is empty or invalid.
    *   `APIError`: If relation creation fails (typically due to an API call error).

#### 1.3. `delete_relation()` (Delete Entity Relation)

Deletes a specified single relation between two entities on ThingsBoard.

*   **Parameters**:
    *   `from_id` (str): The ID of the source entity.
    *   `from_type` (`EntityType`): The type of the source entity.
    *   `to_id` (str): The ID of the target entity.
    *   `to_type` (`EntityType`): The type of the target entity.
    *   `relation_type` (str): The type of the relation to delete.
    *   `type_group` (str, default: "COMMON"): The relation type group.
*   **Returns**:
    *   `bool` - Returns `True` if the deletion is successful.
*   **Raises**:
    *   `ValidationError`: If `from_id`, `to_id`, or `relation_type` is empty or invalid.
    *   `APIError`: If relation deletion fails.

#### 1.4. `get_relation()` (Get Entity Relation)

Retrieves details of a specified single relation between two entities on ThingsBoard.

*   **Parameters**:
    *   `from_id` (str): The ID of the source entity.
    *   `from_type` (`EntityType`): The type of the source entity.
    *   `to_id` (str): The ID of the target entity.
    *   `to_type` (`EntityType`): The type of the target entity.
    *   `relation_type` (str): The type of the relation to retrieve.
    *   `type_group` (str, default: "COMMON"): The relation type group.
*   **Returns**:
    *   `Optional[EntityRelation]` - Returns the relation object if the relation exists, otherwise `None`.
*   **Raises**:
    *   `ValidationError`: If `from_id`, `to_id`, or `relation_type` is empty or invalid.
    *   `APIError`: If retrieving the relation fails.

#### 1.5. `find_by_from()` (Find All Relations from a Specified Entity)

Finds all relations where the specified entity is the source (`from`).

*   **Parameters**:
    *   `from_id` (str): The ID of the source entity.
    *   `from_type` (`EntityType`): The type of the source entity.
    *   `relation_type_group` (str, default: "COMMON"): The relation type group.
*   **Returns**:
    *   `List[EntityRelation]` - A list of relations originating from this entity.
*   **Raises**:
    *   `ValidationError`: If `from_id` is empty or invalid.
    *   `APIError`: If finding relations fails.

#### 1.6. `find_by_to()` (Find All Relations Pointing to a Specified Entity)

Finds all relations where the specified entity is the target (`to`).

*   **Parameters**:
    *   `to_id` (str): The ID of the target entity.
    *   `to_type` (`EntityType`): The type of the target entity.
    *   `relation_type_group` (str, default: "COMMON"): The relation type group.
*   **Returns**:
    *   `List[EntityRelation]` - A list of relations pointing to this entity.
*   **Raises**:
    *   `ValidationError`: If `to_id` is empty or invalid.
    *   `APIError`: If finding relations fails.

#### 1.7. `relation_exists()` (Check if Entity Relation Exists)

Checks if a relation with the specified type and type group exists between two entities.

*   **Parameters**:
    *   `from_id` (str): The ID of the source entity.
    *   `from_type` (`EntityType`): The type of the source entity.
    *   `to_id` (str): The ID of the target entity.
    *   `to_type` (`EntityType`): The type of the target entity.
    *   `relation_type` (str): The type of the relation to check.
    *   `type_group` (str, default: "COMMON"): The relation type group.
*   **Returns**:
    *   `bool` - Returns `True` if the relation exists, otherwise `False`.

#### 1.8. `delete_relations()` (Delete All Relations of an Entity)

Deletes all incoming and outgoing relations of the specified entity, with selective deletion based on direction (`FROM`, `TO`, `BOTH`).

*   **Parameters**:
    *   `entity_id` (str): The ID of the entity whose relations are to be deleted.
    *   `entity_type` (`EntityType`): The type of the entity whose relations are to be deleted.
    *   `direction` (str, default: "FROM"): The direction of relations to delete. Possible values include "FROM" (deletes all relations originating from this entity), "TO" (deletes all relations pointing to this entity), "BOTH" (deletes all incoming and outgoing relations).
*   **Returns**:
    *   `bool` - Returns `True` if all specified deletion operations are successful.
*   **Raises**:
    *   `ValidationError`: If `entity_id` or `direction` parameters are invalid.
    *   `APIError`: If deleting relations fails.