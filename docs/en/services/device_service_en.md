# thingsboardlink Device Service Module Documentation

This document provides a detailed description of the device service module (`device_service.py`) within the `thingsboardlink` package. This module encapsulates all API call functionalities related to device management with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Device Service Class Details**](#device-service-class-details)
    - [**1. `DeviceService` (Device Service Class)**](#1-deviceservice-device-service-class)
        - [**1.1. `__init__()` (Initialize Device Service)**](#11-__init__-initialize-device-service)
        - [**1.2. `create_device()` (Create Device)**](#12-create_device-create-device)
        - [**1.3. `get_device_by_id()` (Get Device by ID)**](#13-get_device_by_id-get-device-by-id)
        - [**1.4. `update_device()` (Update Device Information)**](#14-update_device-update-device-information)
        - [**1.5. `delete_device()` (Delete Device)**](#15-delete-device-delete-device)
        - [**1.6. `get_tenant_devices()` (Get Devices under Tenant)**](#16-get_tenant_devices-get-devices-under-tenant)
        - [**1.7. `get_device_credentials()` (Get Device Credentials)**](#17-get_device_credentials-get-device-credentials)
        - [**1.8. `get_devices_by_name()` (Search Devices by Name)**](#18-get_devices_by_name-search-devices-by-name)
        - [**1.9. `device_exists()` (Check if Device Exists)**](#19-device_exists-check-if-device-exists)

## Overview

The `thingsboardlink.services.device_service` module provides functionalities for managing device entities on the ThingsBoard platform. It encapsulates calls to ThingsBoard REST API `/api/device` and `/api/tenant/devices` endpoints, enabling developers to perform device creation, querying, updating, deletion, and credential management operations through type-safe Python methods. This module aims to simplify the management of the device lifecycle.

## Core Features

*   **Device CRUD Operations**: Provides basic functionalities for creating, retrieving by ID, updating, and deleting devices.
*   **Device Credential Management**: Allows retrieval of authentication credentials for specified devices.
*   **Batch Device Query**: Supports querying device lists by tenant, with pagination, text search, and sorting capabilities.
*   **Search Devices by Name**: Provides functionality to search for matching devices by device name, returning a list of matching devices.
*   **Device Existence Check**: Quickly determines if a device corresponding to a given device ID exists.
*   **Error Handling**: Converts errors returned by the ThingsBoard API into `thingsboardlink`'s custom exceptions (e.g., `NotFoundError`, `DeviceError`, `ValidationError`), providing clearer error messages.

## Device Service Class Details

### 1. `DeviceService` (Device Service Class)

The `DeviceService` class is the entry point for device management functionalities, through which you can perform all device-related operations.

#### 1.1. `__init__()` (Initialize Device Service)

The constructor initializes a `DeviceService` instance, requiring a configured `ThingsBoardClient` instance to send HTTP requests.

*   **Parameters**:
    *   `client`: A `ThingsBoardClient` instance, used for communication with the ThingsBoard platform.

#### 1.2. `create_device()` (Create Device)

Creates a new device on the ThingsBoard platform.

*   **Parameters**:
    *   `name` (str): The unique name of the device.
    *   `device_type` (str, default: "default"): The type identifier of the device.
    *   `label` (Optional[str]): The label of the device, used for identification or categorization.
    *   `additional_info` (Optional[Dict[str, Any]]): Additional JSON formatted information for the device.
*   **Returns**:
    *   `Device` - The successfully created device object.
*   **Raises**:
    *   `ValidationError`: If the device name is empty or invalid.
    *   `DeviceError`: If device creation fails (typically due to an API call error).

#### 1.3. `get_device_by_id()` (Get Device by ID)

Retrieves device details based on the device's unique ID.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
*   **Returns**:
    *   `Device` - The matching device object.
*   **Raises**:
    *   `ValidationError`: If the device ID is empty or invalid.
    *   `NotFoundError`: If no device with the specified ID exists.
    *   `DeviceError`: If retrieving the device fails.

#### 1.4. `update_device()` (Update Device Information)

Updates the attributes of an existing device. This method performs the update by sending a POST request containing the complete device object.

*   **Parameters**:
    *   `device` (`Device`): A device object containing the ID of the device to update and its new attribute values.
*   **Returns**:
    *   `Device` - The updated device object.
*   **Raises**:
    *   `ValidationError`: If the device object lacks an ID or the name is invalid.
    *   `DeviceError`: If device update fails.

#### 1.5. `delete_device()` (Delete Device)

Deletes a device on ThingsBoard based on its ID.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device to delete.
*   **Returns**:
    *   `bool` - Returns `True` if the deletion is successful.
*   **Raises**:
    *   `ValidationError`: If the device ID is empty or invalid.
    *   `DeviceError`: If device deletion fails.

#### 1.6. `get_tenant_devices()` (Get Devices under Tenant)

Retrieves a list of all devices under the current tenant, supporting pagination, text search, and sorting.

*   **Parameters**:
    *   `page_size` (int, default: 10): The number of devices to return per page.
    *   `page` (int, default: 0): The page number to retrieve (0-indexed).
    *   `text_search` (Optional[str]): Search text for fuzzy matching device names, types, or labels.
    *   `sort_property` (Optional[str]): The device property to sort by (e.g., "name", "type", "createdTime").
    *   `sort_order` (Optional[str]): The sort order, either "ASC" (ascending) or "DESC" (descending).
*   **Returns**:
    *   `PageData` - An object containing the device list and pagination information.
*   **Raises**:
    *   `ValidationError`: If `page_size` or `page` parameters are invalid.
    *   `DeviceError`: If retrieving the device list fails.

#### 1.7. `get_device_credentials()` (Get Device Credentials)

Retrieves authentication credentials for the specified device, such as the device access token.

*   **Parameters**:
    *   `device_id` (str): The unique identifier of the device.
*   **Returns**:
    *   `DeviceCredentials` - The device's credential object.
*   **Raises**:
    *   `ValidationError`: If the device ID is empty or invalid.
    *   `NotFoundError`: If credentials for the specified device do not exist.
    *   `DeviceError`: If retrieving device credentials fails.

#### 1.8. `get_devices_by_name()` (Search Devices by Name)

Searches for matching devices by device name under the current tenant. This method performs an exact (case-insensitive) match.

*   **Parameters**:
    *   `device_name` (str): The name of the device to search for.
*   **Returns**:
    *   `List[Device]` - A list of matching device objects.
*   **Raises**:
    *   `ValidationError`: If the device name is empty or invalid.
    *   `DeviceError`: If searching for devices fails.

#### 1.9. `device_exists()` (Check if Device Exists)

Checks if a device with the given ID exists on the ThingsBoard platform.

*   **Parameters**:
    *   `device_id` (str): The ID of the device to check.
*   **Returns**:
    *   `bool` - Returns `True` if the device exists, otherwise `False`.