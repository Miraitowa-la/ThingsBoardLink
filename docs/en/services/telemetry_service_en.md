# thingsboardlink Telemetry Service Module Documentation

This document provides a detailed description of the telemetry service module (`telemetry_service.py`) within the `thingsboardlink` package. This module encapsulates all API call functionalities related to telemetry data management with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Telemetry Service Class Details**](#telemetry-service-class-details)
    - [**1. `TelemetryService` (Telemetry Service Class)**](#1-telemetryservice-telemetry-service-class)
        - [**1.1. `__init__()` (Initialize Telemetry Service)**](#11-___init___-initialize-telemetry-service)
        - [**1.2. `post_telemetry()` (Upload Telemetry Data)**](#12-post_telemetry-upload-telemetry-data)
        - [**1.3. `post_telemetry_with_device_token()` (Upload Telemetry Data with Device Token)**](#13-post_telemetry_with_device_token-upload-telemetry-data-with-device-token)
        - [**1.4. `get_latest_telemetry()` (Get Latest Telemetry Data)**](#14-get_latest_telemetry-get-latest-telemetry-data)
        - [**1.5. `get_timeseries_telemetry()` (Get Time-Series Telemetry Data)**](#15-get_timeseries_telemetry-get-time-series-telemetry-data)
        - [**1.6. `delete_telemetry()` (Delete Telemetry Data)**](#16-delete_telemetry-delete-telemetry-data)
        - [**1.7. `get_telemetry_keys()` (Get All Telemetry Data Keys for a Device)**](#17-get_telemetry_keys-get-all-telemetry-data-keys-for-a-device)

## Overview

The `thingsboardlink.services.telemetry_service` module provides functionalities for managing telemetry data on the ThingsBoard platform. It encapsulates calls to ThingsBoard REST API telemetry data-related endpoints, enabling developers to perform operations such as uploading telemetry data, retrieving the latest data, querying historical data, and deleting data through type-safe Python methods. This module aims to simplify the process of device data reporting and analysis.

## Core Features

*   **Telemetry Data Upload**: Supports uploading telemetry data in various formats (dictionary, single `TelemetryData` object, list of `TelemetryData` objects).
*   **Upload by Device ID**: Provides functionality to automatically obtain credentials via device ID and upload data using that token.
*   **Upload by Device Token**: Allows direct data upload using a device access token, suitable for device-side integrations.
*   **Latest Telemetry Data Retrieval**: Retrieves the latest telemetry data point for a specified device or specific keys.
*   **Historical Time-Series Data Query**: Supports querying device telemetry data within a specified time range, with aggregation capabilities (e.g., MIN, MAX, AVG, etc.).
*   **Telemetry Data Deletion**: Allows deleting telemetry data for specific keys or within a time range.
*   **Telemetry Data Key List Retrieval**: Queries all currently existing telemetry data keys for a device.
*   **Error Handling**: Converts errors returned by the ThingsBoard API into `thingsboardlink`'s custom exceptions (e.g., `ValidationError`, `TelemetryError`, `NotFoundError`), providing clearer error messages.

## Telemetry Service Class Details

### 1. `TelemetryService` (Telemetry Service Class)

The `TelemetryService` class is the entry point for telemetry data management functionalities, through which you can perform all telemetry data-related operations.

#### 1.1. `__init__()` (Initialize Telemetry Service)

The constructor initializes a `TelemetryService` instance, requiring a configured `ThingsBoardClient` instance to send HTTP requests.

*   **Parameters**:
    *   `client`: A `ThingsBoardClient` instance, used for communication with the ThingsBoard platform.

#### 1.2. `post_telemetry()` (Upload Telemetry Data)

Uploads telemetry data using the device ID. This method automatically calls `client.device_service.get_device_credentials()` to obtain the device access token, then uses that token to upload the data.

*   **Parameters**:
    *   `device_id` (str): The ID of the device to upload data for.
    *   `telemetry_data` (Union[Dict[str, Any], List[TelemetryData], TelemetryData]): The telemetry data to upload. Can be:
        *   `Dict[str, Any]`: A key-value pair dictionary, e.g., `{"temperature": 25.5, "humidity": 60}`.
        *   `TelemetryData`: A single `TelemetryData` object.
        *   `List[TelemetryData]`: A list of `TelemetryData` objects.
    *   `timestamp` (Optional[int]): The timestamp of the telemetry data (Unix timestamp in milliseconds). If not provided, the current time will be used.
*   **Returns**:
    *   `bool` - Returns `True` if the upload is successful.
*   **Raises**:
    *   `ValidationError`: If `device_id` or `telemetry_data` parameters are invalid.
    *   `TelemetryError`: If unable to obtain the device access token or if telemetry data upload fails.
    *   `NotFoundError`: If the device does not exist.

#### 1.3. `post_telemetry_with_device_token()` (Upload Telemetry Data with Device Token)

Directly uploads telemetry data using a device access token. This method is suitable for scenarios where the device access token is already available, such as in device-side or edge gateway applications.

*   **Parameters**:
    *   `device_token` (str): The access token of the device.
    *   `telemetry_data` (Union[Dict[str, Any], List[TelemetryData], TelemetryData]): The telemetry data to upload, in the same format as `post_telemetry`.
    *   `timestamp` (Optional[int]): The timestamp of the telemetry data (Unix timestamp in milliseconds). If not provided, the current time will be used.
*   **Returns**:
    *   `bool` - Returns `True` if the upload is successful.
*   **Raises**:
    *   `ValidationError`: If `device_token` or `telemetry_data` parameters are invalid.
    *   `TelemetryError`: If telemetry data upload fails.

#### 1.4. `get_latest_telemetry()` (Get Latest Telemetry Data)

Retrieves the latest telemetry data for the specified device. You can specify the keys to retrieve; if not specified, the latest values for all telemetry keys will be retrieved.

*   **Parameters**:
    *   `device_id` (str): The ID of the device to retrieve data for.
    *   `keys` (Optional[List[str]]): A list of telemetry data keys to retrieve. If `None` or an empty list, the latest values for all available keys will be retrieved.
*   **Returns**:
    *   `Dict[str, Any]` - A dictionary where keys are telemetry data keys and values are dictionaries containing `value` and `timestamp`.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `NotFoundError`: If the device does not exist.
    *   `TelemetryError`: If retrieving the latest telemetry data fails.

#### 1.5. `get_timeseries_telemetry()` (Get Time-Series Telemetry Data)

Retrieves historical time-series telemetry data for the specified device within a specific time range. Supports aggregation.

*   **Parameters**:
    *   `device_id` (str): The ID of the device to retrieve data for.
    *   `keys` (List[str]): A list of time-series data keys to retrieve.
    *   `start_ts` (int): The start timestamp of the query (Unix timestamp in milliseconds).
    *   `end_ts` (int): The end timestamp of the query (Unix timestamp in milliseconds).
    *   `interval` (Optional[int]): Aggregation interval (in milliseconds). For example, setting to 3600000 (1 hour) can retrieve aggregated data per hour.
    *   `limit` (Optional[int]): Maximum number of data points to return.
    *   `agg` (Optional[str]): Aggregation type. Possible values include "MIN", "MAX", "AVG", "SUM", "COUNT".
*   **Returns**:
    *   `Dict[str, TimeseriesData]` - A dictionary where keys are telemetry data keys and values are `TimeseriesData` objects, containing a list of time-series data for that key.
*   **Raises**:
    *   `ValidationError`: If `device_id`, `keys`, `start_ts`, or `end_ts` parameters are invalid.
    *   `TelemetryError`: If retrieving time-series telemetry data fails.

#### 1.6. `delete_telemetry()` (Delete Telemetry Data)

Deletes historical data for one or more telemetry data keys of the specified device. Can delete data within a specific time range or all data for a certain key.

*   **Parameters**:
    *   `device_id` (str): The ID of the device to delete data for.
    *   `keys` (List[str]): A list of telemetry data keys to delete.
    *   `delete_all_data_for_keys` (bool, default: `True`): If `True`, all data for the specified keys will be deleted. If `False`, `start_ts` and `end_ts` must be provided to specify the deletion range.
    *   `start_ts` (Optional[int]): Start timestamp of the deletion range (in milliseconds). Only valid when `delete_all_data_for_keys` is `False`.
    *   `end_ts` (Optional[int]): End timestamp of the deletion range (in milliseconds). Only valid when `delete_all_data_for_keys` is `False`.
*   **Returns**:
    *   `bool` - Returns `True` if the deletion is successful.
*   **Raises**:
    *   `ValidationError`: If `device_id` or `keys` parameters are invalid, or if the time range is not provided when `delete_all_data_for_keys` is `False`.
    *   `TelemetryError`: If deleting telemetry data fails.

#### 1.7. `get_telemetry_keys()` (Get All Telemetry Data Keys for a Device)

Retrieves a list of all existing telemetry data keys with time-series data for the specified device.

*   **Parameters**:
    *   `device_id` (str): The ID of the device to query.
*   **Returns**:
    *   `List[str]` - A list of telemetry data keys as strings.
*   **Raises**:
    *   `ValidationError`: If `device_id` is empty or invalid.
    *   `TelemetryError`: If retrieving telemetry data keys fails.