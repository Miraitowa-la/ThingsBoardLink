# thingsboardlink Attribute Service Module Documentation

This document provides a detailed description of the attribute service module (`attribute_service.py`) within the `thingsboardlink` package. This module encapsulates all API call functionalities related to attribute management with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Attribute Service Class Details**](#attribute-service-class-details)
    - [**1. `AttributeService` (Attribute Service Class)**](#1-attributeservice-attribute-service-class)
        - [**1.1. `__init__()` (Initialize Attribute Service)**](#11-__init__-initialize-attribute-service)
        - [**1.2. `_get_attributes()` (Get Attributes within a Specified Scope)**](#12-_get_attributes-get-attributes-within-a-specified-scope)
        - [**1.3. `_set_attributes()` (Set Attributes within a Specified Scope)**](#13-_set_attributes-set-attributes-within-a-specified-scope)
        - [**1.4. `get_client_attributes()` (Get Client Attributes)**](#14-get_client_attributes-get-client-attributes)
        - [**1.5. `get_server_attributes()` (Get Server Attributes)**](#15-get_server_attributes-get-server-attributes)
        - [**1.6. `get_shared_attributes()` (Get Shared Attributes)**](#16-get_shared_attributes-get-shared-attributes)
        - [**1.7. `set_server_attributes()` (Set Server Attributes)**](#17-set_server_attributes-set-server-attributes)
        - [**1.8. `set_shared_attributes()` (Set Shared Attributes)**](#18-set_shared_attributes-set-shared-attributes)
        - [**1.9. `delete_attributes()` (Delete Attributes)**](#19-delete_attributes-delete-attributes)
        - [**1.10. `get_attribute_keys()` (Get Attribute Key List)**](#110-get-attribute-keys-get-attribute-key-list)
        - [**1.11. `get_all_attributes()` (Get All Attributes of a Device)**](#111-get_all_attributes-get-all-attributes-of-a-device)
        - [**1.12. `update_attribute()` (Update Single Attribute)**](#112-update_attribute-update-single-attribute)
        - [**1.13. `attribute_exists()` (Check if Attribute Exists)**](#113-attribute_exists-check-if-attribute-exists)

## Overview

The `thingsboardlink.services.attribute_service` module provides functionalities for managing attributes of entities (primarily devices) on the ThingsBoard platform. It encapsulates calls to ThingsBoard REST API attribute-related endpoints, enabling developers to perform read, set, update, and delete operations for client, server, and shared attributes through type-safe Python methods. This module aims to simplify the management of device or entity metadata and configurations.

## Core Features

*   **Attribute Scope Support**: Full support for the three attribute scopes in ThingsBoard: Client-side attributes (`CLIENT_SCOPE`), Server-side attributes (`SERVER_SCOPE`), and Shared attributes (`SHARED_SCOPE`).
*   **Attribute CRUD Operations**: Provides basic functionalities for getting, setting (creating/updating), and deleting attributes.
*   **Batch Attribute Operations**: Supports getting or setting multiple attributes at once.
*   **Attribute Key List Retrieval**: Retrieves a list of all attribute keys within a specified scope.
*   **All Attributes Retrieval**: Capable of retrieving all attributes of a device across all scopes in a single operation.
*   **Attribute Existence Check**: Quickly determines if an attribute exists within a specified scope and key.
*   **Error Handling**: Converts errors returned by the ThingsBoard API into `thingsboardlink`'s custom exceptions (e.g., `ValidationError`, `NotFoundError`, `APIError`), providing clearer error messages.

## Attribute Service Class Details

### 1. `AttributeService` (Attribute Service Class)

The `AttributeService` class is the entry point for attribute management functionalities, through which you can perform all attribute-related operations.

#### 1.1. `__init__()` (Initialize Attribute Service)

The constructor initializes an `AttributeService` instance, requiring a configured `ThingsBoardClient` instance to send HTTP requests.

*   **Parameters**:
    *   `client`: A `ThingsBoardClient` instance, used for communication with the ThingsBoard platform.

#### 1.2. `_get_attributes()` (Get Attributes within a Specified Scope)

This is an internal helper method used to retrieve attribute data from ThingsBoard based on the specified device ID, attribute scope, and an optional list of keys. It processes the API response and converts it into a more user-friendly dictionary format.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `scope` (`AttributeScope`): The scope of attributes to retrieve.
    *   `keys` (Optional[List[str]]): A list of attribute keys to retrieve. If `None`, all attributes within that scope will be retrieved.
*   **Returns**:
    *   `Dict[str, Any]` - A dictionary where keys are attribute keys and values are dictionaries containing `value` and `lastUpdateTs`.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `NotFoundError`: If the device does not exist.
    *   `APIError`: If retrieving attributes fails.

#### 1.3. `_set_attributes()` (Set Attributes within a Specified Scope)

This is an internal helper method used to set (create or update) attributes based on the specified device ID, attribute scope, and attribute data.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `scope` (`AttributeScope`): The scope of attributes to set.
    *   `attributes` (Union[Dict[str, Any], List[Attribute]]): The attribute data to set. Can be:
        *   `Dict[str, Any]`: A key-value pair dictionary, e.g., `{"firmwareVersion": "1.0.1", "location": "Warehouse A"}`.
        *   `List[Attribute]`: A list of `Attribute` objects.
*   **Returns**:
    *   `bool` - Returns `True` if the setting is successful.
*   **Raises**:
    *   `ValidationError`: If `device_id` or `attributes` parameters are invalid, or if the `attributes` list contains non-`Attribute` objects.
    *   `APIError`: If setting attributes fails.

#### 1.4. `get_client_attributes()` (Get Client Attributes)

Retrieves client-side attributes for the specified device.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `keys` (Optional[List[str]]): A list of attribute keys to retrieve. If `None`, all client-side attributes will be retrieved.
*   **Returns**:
    *   `Dict[str, Any]` - Client-side attribute data.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `NotFoundError`: If the device does not exist.

#### 1.5. `get_server_attributes()` (Get Server Attributes)

Retrieves server-side attributes for the specified device.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `keys` (Optional[List[str]]): A list of attribute keys to retrieve. If `None`, all server-side attributes will be retrieved.
*   **Returns**:
    *   `Dict[str, Any]` - Server-side attribute data.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `NotFoundError`: If the device does not exist.

#### 1.6. `get_shared_attributes()` (Get Shared Attributes)

Retrieves shared attributes for the specified device.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `keys` (Optional[List[str]]): A list of attribute keys to retrieve. If `None`, all shared attributes will be retrieved.
*   **Returns**:
    *   `Dict[str, Any]` - Shared attribute data.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `NotFoundError`: If the device does not exist.

#### 1.7. `set_server_attributes()` (Set Server Attributes)

Sets server-side attributes for the specified device.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `attributes` (Union[Dict[str, Any], List[Attribute]]): The server-side attribute data to set.
*   **Returns**:
    *   `bool` - Returns `True` if the setting is successful.
*   **Raises**:
    *   `ValidationError`, `APIError`.

#### 1.8. `set_shared_attributes()` (Set Shared Attributes)

Sets shared attributes for the specified device.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `attributes` (Union[Dict[str, Any], List[Attribute]]): The shared attribute data to set.
*   **Returns**:
    *   `bool` - Returns `True` if the setting is successful.
*   **Raises**:
    *   `ValidationError`, `APIError`.

#### 1.9. `delete_attributes()` (Delete Attributes)

Deletes one or more attributes for the specified device and scope.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `scope` (`AttributeScope`): The scope of attributes to delete.
    *   `keys` (List[str]): A list of attribute keys to delete.
*   **Returns**:
    *   `bool` - Returns `True` if the deletion is successful.
*   **Raises**:
    *   `ValidationError`: If `device_id`, `scope`, or `keys` parameters are invalid.
    *   `APIError`: If deleting attributes fails.

#### 1.10. `get_attribute_keys()` (Get Attribute Key List)

Retrieves a list of all attribute keys for the specified device and scope.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `scope` (`AttributeScope`): The scope to query attribute keys from.
*   **Returns**:
    *   `List[str]` - A list of attribute keys as strings.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `APIError`: If retrieving attribute keys fails.

#### 1.11. `get_all_attributes()` (Get All Attributes of a Device)

Retrieves all attributes for the specified device at once, grouped by client, server, and shared scopes.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
*   **Returns**:
    *   `Dict[str, Dict[str, Any]]` - A nested dictionary containing all attribute data, with outer keys being "client", "server", "shared".
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `APIError`: If retrieving attributes for any scope fails.

#### 1.12. `update_attribute()` (Update Single Attribute)

Updates a single attribute for the specified device and scope. This is a convenience method that internally calls `_set_attributes`.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
    *   `scope` (`AttributeScope`): The attribute scope.
    *   `key` (str): The attribute key.
    *   `value` (Any): The new value for the attribute.
*   **Returns**:
    *   `bool` - Returns `True` if the update is successful.
*   **Raises**:
    *   `ValidationError`, `APIError`.

#### 1.13. `attribute_exists()` (Check if Attribute Exists)