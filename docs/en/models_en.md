# thingsboardlink Data Model Module Documentation

This document provides a detailed explanation of all data models defined in the `thingsboardlink` package, aiming to offer type-safe data structures and convenient data conversion methods for efficient interaction with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Data Model Details**](#data-model-details)
    - [**1. EntityType (Entity Type Enum)**](#1-entitytype-entity-type-enum)
    - [**2. AlarmSeverity (Alarm Severity Enum)**](#2-alarmseverity-alarm-severity-enum)
    - [**3. AlarmStatus (Alarm Status Enum)**](#3-alarmstatus-alarm-status-enum)
    - [**4. AttributeScope (Attribute Scope Enum)**](#4-attributescope-attribute-scope-enum)
    - [**5. RpcPersistentStatus (RPC Persistent Status Enum)**](#5-rpcpersistentstatus-rpc-persistent-status-enum)
    - [**6. EntityId (Entity ID Model)**](#6-entityid-entity-id-model)
    - [**7. Device (Device Model)**](#7-device-device-model)
    - [**8. DeviceCredentials (Device Credentials Model)**](#8-devicecredentials-device-credentials-model)
    - [**9. TelemetryData (Telemetry Data Model)**](#9-telemetrydata-telemetry-data-model)
    - [**10. Attribute (Attribute Model)**](#10-attribute-attribute-model)
    - [**11. Alarm (Alarm Model)**](#11-alarm-alarm-model)
    - [**12. RPCRequest (RPC Request Model)**](#12-rpcrequest-rpc-request-model)
    - [**13. RPCResponse (RPC Response Model)**](#13-rpcresponse-rpc-response-model)
    - [**14. PersistentRPCRequest (Persistent RPC Request Model)**](#14-persistentrpcrequest-persistent-rpc-request-model)
    - [**15. EntityRelation (Entity Relation Model)**](#15-entityrelation-entity-relation-model)
    - [**16. PageData (Paged Data Model)**](#16-pagedata-paged-data-model)
    - [**17. TimeseriesData (Time Series Data Model)**](#17-timeseriesdata-time-series-data-model)

## Overview

The `thingsboardlink` data model module (`models.py`) provides data structures corresponding to various entities, data types, and operations within the ThingsBoard platform. These models are implemented using Python's `dataclasses` and `Enum`, ensuring data type safety, readability, and ease of use. They encapsulate the JSON structure of the ThingsBoard API and provide convenient conversion methods, allowing developers to handle ThingsBoard data in an object-oriented manner.

## Core Features

* **Type Safety**: Uses `dataclasses` to define structures and leverages the `typing` module for type hints, enhancing code readability and robustness.
* **Enum Types**: Provides enumeration classes for common fixed values in ThingsBoard (e.g., entity types, alarm severities, attribute scopes), avoiding hardcoded strings.
* **Data Conversion**: All major data models provide `to_dict()` and `from_dict()` methods for easy conversion between Python objects and the JSON (dictionary) format required by the ThingsBoard API.
* **Business Logic Encapsulation**: Some models include convenient methods related to business logic, such as `TelemetryData.create_batch()` and `RPCResponse.is_success`.
* **Timestamp Handling**: Automatically handles timestamp conversions, typically from Unix timestamps in milliseconds in ThingsBoard to `datetime` objects in Python, or vice versa.

## Data Model Details

### 1. EntityType (Entity Type Enum)

Represents different entity types within the ThingsBoard platform.

* **Members**:
    * `DEVICE`: Device
    * `ASSET`: Asset
    * `USER`: User
    * `CUSTOMER`: Customer
    * `TENANT`: Tenant
    * `RULE_CHAIN`: Rule Chain
    * `RULE_NODE`: Rule Node
    * `DASHBOARD`: Dashboard
    * `WIDGET_TYPE`: Widget Type
    * `WIDGET_BUNDLE`: Widget Bundle
    * `ALARM`: Alarm

### 2. AlarmSeverity (Alarm Severity Enum)

Defines the severity levels for ThingsBoard alarms.

* **Members**:
    * `CRITICAL`: Critical level
    * `MAJOR`: Major level
    * `MINOR`: Minor level
    * `WARNING`: Warning level
    * `INDETERMINATE`: Indeterminate level

### 3. AlarmStatus (Alarm Status Enum)

Defines the lifecycle states of ThingsBoard alarms.

* **Members**:
    * `ACTIVE_UNACK`: Active and unacknowledged
    * `ACTIVE_ACK`: Active and acknowledged
    * `CLEARED_UNACK`: Cleared but unacknowledged
    * `CLEARED_ACK`: Cleared and acknowledged

### 4. AttributeScope (Attribute Scope Enum)

Defines different storage and access scopes for ThingsBoard entity attributes.

* **Members**:
    * `CLIENT_SCOPE`: Client-side attributes, set by the device and pushed to the server.
    * `SERVER_SCOPE`: Server-side attributes, set by the server and can be pushed to the device.
    * `SHARED_SCOPE`: Shared attributes, set by the server, visible to all clients.

### 5. RpcPersistentStatus (RPC Persistent Status Enum)

Defines the current status of a persistent RPC request.

* **Members**:
    * `QUEUED`: Queued - RPC has been created and saved to the database, not yet sent to the device.
    * `SENT`: Sent - ThingsBoard has attempted to send the RPC to the device.
    * `DELIVERED`: Delivered - The device has acknowledged the RPC (final state for one-way RPC).
    * `SUCCESSFUL`: Successful - ThingsBoard has received a reply for a two-way RPC.
    * `TIMEOUT`: Timeout - The transport layer detected an RPC timeout.
    * `EXPIRED`: Expired - The RPC was not delivered or no reply was received within the configured expiration time.
    * `FAILED`: Failed - The RPC could not be delivered within the configured retries, or the device does not support such commands.

### 6. EntityId (Entity ID Model)

A generic model used to represent the unique identifier of any entity in ThingsBoard, including its ID string and entity type.

* **Attributes**:
    * `id` (str): The unique ID string of the entity.
    * `entity_type` (EntityType): The type of the entity.
* **Methods**:
    * `to_dict() -> Dict[str, Any]`: Converts the `EntityId` object to the dictionary format expected by the ThingsBoard API.
    * `from_dict(data: Dict[str, Any]) -> 'EntityId'`: Creates an `EntityId` object from dictionary data.

### 7. Device (Device Model)

Represents a device entity in the ThingsBoard platform, including its basic information and metadata.

* **Attributes**:
    * `name` (str): Device name.
    * `type` (str, default: "default"): Device type.
    * `id` (Optional[str]): Unique ID of the device.
    * `label` (Optional[str]): Device label.
    * `additional_info` (Optional[Dict[str, Any]]): Dictionary of additional information.
    * `created_time` (Optional[datetime]): Device creation time.
    * `customer_id` (Optional[EntityId]): ID of the owning customer.
    * `tenant_id` (Optional[EntityId]): ID of the owning tenant.
* **Methods**:
    * `__post_init__()`: Post-initialization processing to ensure `additional_info` field is a dictionary.
    * `to_dict() -> Dict[str, Any]`: Converts the `Device` object to the dictionary format expected by the ThingsBoard API.
    * `from_dict(data: Dict[str, Any]) -> 'Device'`: Creates a `Device` object from dictionary data.

### 8. DeviceCredentials (Device Credentials Model)

Represents the authentication credentials for a device, typically used for device connection to ThingsBoard.

* **Attributes**:
    * `device_id` (str): ID of the device to which the credentials belong.
    * `credentials_type` (str, default: "ACCESS_TOKEN"): Type of credentials (e.g., "ACCESS_TOKEN").
    * `credentials_id` (Optional[str]): ID of the credentials.
    * `credentials_value` (Optional[str]): Value of the credentials (e.g., access token).
* **Methods**:
    * `to_dict() -> Dict[str, Any]`: Converts the `DeviceCredentials` object to the dictionary format expected by the ThingsBoard API.
    * `from_dict(data: Dict[str, Any]) -> 'DeviceCredentials'`: Creates a `DeviceCredentials` object from dictionary data, with special handling for `ACCESS_TOKEN` type `credentials_value`.

### 9. TelemetryData (Telemetry Data Model)

Represents a single telemetry data point uploaded by a device to ThingsBoard, including key-value pair and timestamp.

* **Attributes**:
    * `key` (str): Key name of the telemetry data.
    * `value` (Union[str, int, float, bool]): Value of the telemetry data.
    * `timestamp` (Optional[int]): Timestamp of data generation, defaults to current time (Unix timestamp in milliseconds).
* **Methods**:
    * `__post_init__()`: Post-initialization processing, automatically sets `timestamp` to current time if not specified.
    * `to_dict() -> Dict[str, Any]`: Converts the `TelemetryData` object to the dictionary format expected by the ThingsBoard API.
    * `from_dict(key: str, data: Dict[str, Any]) -> 'TelemetryData'`: Creates a `TelemetryData` object from dictionary data.
    * `create_batch(data: Dict[str, Union[str, int, float, bool]], timestamp: Optional[int] = None) -> List['TelemetryData']`: Static method to create a batch list of `TelemetryData` from a key-value dictionary.

### 10. Attribute (Attribute Model)

Represents an attribute of a ThingsBoard entity, with a key, value, and scope.

* **Attributes**:
    * `key` (str): Key name of the attribute.
    * `value` (Any): Value of the attribute.
    * `scope` (AttributeScope, default: `AttributeScope.SERVER_SCOPE`): Scope of the attribute (client-side, server-side, shared).
    * `last_update_ts` (Optional[int]): Timestamp of the last attribute update.
* **Methods**:
    * `to_dict() -> Dict[str, Any]`: Converts the `Attribute` object to the dictionary format expected by the ThingsBoard API.
    * `from_api_response(key: str, data: Dict[str, Any], scope: AttributeScope = AttributeScope.SERVER_SCOPE) -> 'Attribute'`: Creates an `Attribute` object from ThingsBoard API response data.
    * `create_batch(data: Dict[str, Any], scope: AttributeScope = AttributeScope.SERVER_SCOPE) -> List['Attribute']`: Static method to create a batch list of `Attribute` from a key-value dictionary.

### 11. Alarm (Alarm Model)

Represents an alarm in the ThingsBoard system, including its type, originator, severity, and status.

* **Attributes**:
    * `type` (str): Alarm type.
    * `originator_id` (str): ID of the entity that originated the alarm.
    * `severity` (AlarmSeverity, default: `AlarmSeverity.CRITICAL`): Alarm severity.
    * `status` (AlarmStatus, default: `AlarmStatus.ACTIVE_UNACK`): Alarm status.
    * `id` (Optional[str]): Unique ID of the alarm.
    * `start_ts` (Optional[int]): Timestamp when the alarm started.
    * `end_ts` (Optional[int]): Timestamp when the alarm ended.
    * `ack_ts` (Optional[int]): Timestamp when the alarm was acknowledged.
    * `clear_ts` (Optional[int]): Timestamp when the alarm was cleared.
    * `details` (Optional[Dict[str, Any]]): Detailed information about the alarm.
    * `propagate` (bool, default: `True`): Whether to propagate the alarm to related entities.
* **Methods**:
    * `__post_init__()`: Post-initialization processing, ensures `details` field is a dictionary and automatically sets `start_ts`.
    * `to_dict() -> Dict[str, Any]`: Converts the `Alarm` object to the dictionary format expected by ThingsBoard API requests.
    * `from_dict(data: Dict[str, Any]) -> 'Alarm'`: Creates an `Alarm` object from dictionary data.

### 12. RPCRequest (RPC Request Model)

Represents a Remote Procedure Call (RPC) request sent to a device.

* **Attributes**:
    * `method` (str): RPC method name.
    * `params` (Dict[str, Any], default: `dict()`): Parameters for the RPC method.