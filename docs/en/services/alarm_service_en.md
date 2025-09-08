# thingsboardlink Alarm Service Module Documentation

This document details the alarm service module (`alarm_service.py`) in the `thingsboardlink` package, which encapsulates all API call functionalities related to alarm management with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Alarm Service Class Details**](#alarm-service-class-details)
    - [**1. `AlarmService` (Alarm Service Class)**](#1-alarmservice-alarm-service-class)
        - [**1.1. `__init__()` (Initialize Alarm Service)**](#11-___init___-initialize-alarm-service)
        - [**1.2. `create_alarm()` (Create Alarm)**](#12-create_alarm-create-alarm)
        - [**1.3. `get_alarm()` (Get Alarm by ID)**](#13-get_alarm-get-alarm-by-id)
        - [**1.4. `get_alarms()` (Get Alarm List)**](#14-get_alarms-get-alarm-list)
        - [**1.5. `ack_alarm()` (Acknowledge Alarm)**](#15-ack_alarm-acknowledge-alarm)
        - [**1.6. `clear_alarm()` (Clear Alarm)**](#16-clear_alarm-clear-alarm)
        - [**1.7. `delete_alarm()` (Delete Alarm)**](#17-delete_alarm-delete-alarm)
        - [**1.8. `alarm_exists()` (Check if Alarm Exists)**](#18-alarm_exists-check-if-alarm-exists)

## Overview

The `thingsboardlink.services.alarm_service` module provides functionalities for managing alarm entities on the ThingsBoard platform. It encapsulates calls to the ThingsBoard REST API's alarm-related endpoints, enabling developers to perform alarm creation, querying, acknowledgment, clearing, and deletion operations through type-safe Python methods. This module aims to simplify the management and monitoring of alarm lifecycles.

## Core Features

* **Alarm Creation**: Allows creating new alarms with specified type, originator, severity, and details.
* **Alarm Query**: Supports retrieving a single alarm by ID, or querying a list of alarms based on various conditions such as originator ID, time range, status, severity, and type, with pagination and sorting capabilities.
* **Alarm Status Management**: Provides functions to acknowledge (ACK) and clear (CLEAR) alarms to manage their lifecycle.
* **Alarm Deletion**: Allows permanent deletion of alarms on ThingsBoard.
* **Alarm Existence Check**: Quickly determines if an alarm corresponding to a given alarm ID exists.
* **Error Handling**: Converts errors returned by the ThingsBoard API into `thingsboardlink` custom exceptions (e.g., `ValidationError`, `AlarmError`, `NotFoundError`), providing clearer error messages.

## Alarm Service Class Details

### 1. `AlarmService` (Alarm Service Class)

The `AlarmService` class is the entry point for alarm management functionalities, through which you can perform all alarm-related operations.

#### 1.1. `__init__()` (Initialize Alarm Service)

The constructor initializes an `AlarmService` instance, which requires a configured `ThingsBoardClient` instance to send HTTP requests.

* **Parameters**:
    * `client`: `ThingsBoardClient` instance, used for communication with the ThingsBoard platform.

#### 1.2. `create_alarm()` (Create Alarm)

Creates a new alarm on the ThingsBoard platform.

* **Parameters**:
    * `alarm_type` (str): Type of the alarm (e.g., "HIGH_TEMPERATURE").
    * `originator_id` (str): ID of the alarm originator, typically a device or asset ID.
    * `severity` (`AlarmSeverity`, default: `AlarmSeverity.CRITICAL`): Severity of the alarm.
    * `details` (Optional[Dict[str, Any]]): Detailed information about the alarm, in JSON format.
    * `propagate` (bool, default: `True`): Whether to propagate the alarm to related entities.
* **Returns**:
    * `Alarm` - The successfully created alarm object.
* **Raises**:
    * `ValidationError`: If `alarm_type` or `originator_id` is empty or invalid.
    * `AlarmError`: If alarm creation fails (usually due to API call errors).

#### 1.3. `get_alarm()` (Get Alarm by ID)

Retrieves alarm details based on the alarm's unique ID.

* **Parameters**:
    * `alarm_id` (str): Unique identifier of the alarm.
* **Returns**:
    * `Alarm` - The matching alarm object.
* **Raises**:
    * `ValidationError`: If `alarm_id` is empty or invalid.
    * `NotFoundError`: If the alarm with the specified ID does not exist.
    * `AlarmError`: If retrieving the alarm fails.

#### 1.4. `get_alarms()` (Get Alarm List)

Retrieves a list of alarms associated with a specified originator, supporting various filtering, pagination, and sorting options.

* **Parameters**:
    * `originator_id` (str): ID of the alarm originator.
    * `page_size` (int, default: 10): Number of alarms to return per page.
    * `page` (int, default: 0): Page number to retrieve (0-indexed).
    * `text_search` (Optional[str]): Search text for fuzzy matching alarm types or details.
    * `sort_property` (Optional[str]): Alarm property to sort by (e.g., "startTs", "severity", "type").
    * `sort_order` (Optional[str]): Sort order, either "ASC" (ascending) or "DESC" (descending).
    * `start_time` (Optional[int]): Start timestamp for the query (Unix timestamp in milliseconds).
    * `end_time` (Optional[int]): End timestamp for the query (Unix timestamp in milliseconds).
    * `fetch_originator` (bool, default: `False`): Whether to include originator entity information in the response.
    * `status_list` (Optional[List[AlarmStatus]]): List of alarm statuses to filter by.
    * `severity_list` (Optional[List[AlarmSeverity]]): List of alarm severities to filter by.
    * `type_list` (Optional[List[str]]): List of alarm types to filter by.
* **Returns**:
    * `PageData` - An object containing the alarm list and pagination information.
* **Raises**:
    * `ValidationError`: If `originator_id`, `page_size`, or `page` parameters are invalid.
    * `AlarmError`: If retrieving the alarm list fails.

#### 1.5. `ack_alarm()` (Acknowledge Alarm)

Acknowledges the alarm with the specified ID. This operation changes the alarm status from `ACTIVE_UNACK` to `ACTIVE_ACK` or `CLEARED_UNACK` to `CLEARED_ACK`.

* **Parameters**:
    * `alarm_id` (str): ID of the alarm to acknowledge.
* **Returns**:
    * `bool` - Returns `True` if acknowledgment is successful.
* **Raises**:
    * `ValidationError`: If `alarm_id` is empty or invalid.
    * `AlarmError`: If alarm acknowledgment fails.

#### 1.6. `clear_alarm()` (Clear Alarm)

Clears the alarm with the specified ID. This operation changes the alarm status from `ACTIVE_UNACK` or `ACTIVE_ACK` to `CLEARED_UNACK` or `CLEARED_ACK`.

* **Parameters**:
    * `alarm_id` (str): ID of the alarm to clear.
* **Returns**:
    * `bool` - Returns `True` if clearing is successful.
* **Raises**:
    * `ValidationError`: If `alarm_id` is empty or invalid.
    * `AlarmError`: If alarm clearing fails.

#### 1.7. `delete_alarm()` (Delete Alarm)

Deletes an alarm on ThingsBoard by its ID.

* **Parameters**:
    * `alarm_id` (str): Unique identifier of the alarm to delete.
* **Returns**:
    * `bool` - Returns `True` if deletion is successful.
* **Raises**:
    * `ValidationError`: If `alarm_id` is empty or invalid.
    * `AlarmError`: If alarm deletion fails.

#### 1.8. `alarm_exists()` (Check if Alarm Exists)

Checks if an alarm with the given ID exists on the ThingsBoard platform.

* **Parameters**:
    * `alarm_id` (str): ID of the alarm to check.
* **Returns**:
    * `bool` - Returns `True` if the alarm exists, otherwise `False`.