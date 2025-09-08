# thingsboardlink RPC Service Module Documentation

This document provides a detailed description of the RPC service module (`rpc_service.py`) within the `thingsboardlink` package. This module encapsulates all API call functionalities related to Remote Procedure Calls (RPC) with the ThingsBoard platform.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**RPC Service Class Details**](#rpc-service-class-details)
    - [**1. `RpcService` (RPC Service Class)**](#1-rpcservice-rpc-service-class)
        - [**1.1. `__init__()` (Initialize RPC Service)**](#11-___init___-initialize-rpc-service)
        - [**1.2. `send_one_way_rpc()` (Send One-Way RPC Request)**](#12-send_one_way_rpc-send-one-way-rpc-request)
        - [**1.3. `send_two_way_rpc()` (Send Two-Way RPC Request)**](#13-send_two_way_rpc-send-two-way-rpc-request)
        - [**1.4. `send_rpc_with_retry()` (Send Two-Way RPC Request with Retry)**](#14-send_rpc_with_retry-send-two-way-rpc-request-with-retry)
        - [**1.5. `send_persistent_rpc()` (Send Persistent RPC Request)**](#15-send_persistent_rpc-send-persistent-rpc-request)
        - [**1.6. `get_persistent_rpc_response()` (Get Persistent RPC Response)**](#16-get_persistent_rpc_response-get-persistent-rpc-response)
        - [**1.7. `delete_persistent_rpc()` (Delete Persistent RPC Request)**](#17-delete_persistent_rpc-delete-persistent-rpc-request)
        - [**1.8. `wait_for_persistent_rpc_response()` (Wait for Persistent RPC Response)**](#18-wait_for_persistent_rpc_response-wait-for-persistent-rpc-response)

## Overview

The `thingsboardlink.services.rpc_service` module provides functionalities for performing Remote Procedure Calls (RPC) with devices on the ThingsBoard platform. It encapsulates calls to ThingsBoard REST API RPC-related endpoints, enabling developers to execute one-way, two-way, retriable, and persistent RPC requests through type-safe Python methods. This module aims to enable real-time control and data querying of devices.

## Core Features

*   **One-Way RPC**: Sends control commands without waiting for a device response.
*   **Two-Way RPC**: Sends requests and waits for a device response, suitable for scenarios requiring device status or data.
*   **Two-Way RPC with Retry**: Enhances the reliability of two-way RPC, automatically retrying when the device is temporarily offline or network fluctuations occur.
*   **Persistent RPC**: Allows sending requests that ThingsBoard stores and delivers to the device later, even if the device is currently offline.
*   **Persistent RPC Status Query**: Queries the current status and device response of a persistent RPC request.
*   **Persistent RPC Deletion**: Cleans up completed or no longer needed persistent RPC requests.
*   **Wait for Persistent RPC Response**: Provides a polling mechanism to wait for a persistent RPC request to complete and return a response.
*   **Error Handling**: Converts errors returned by the ThingsBoard API into `thingsboardlink`'s custom exceptions (e.g., `ValidationError`, `RPCError`, `TimeoutError`), providing clearer error messages.

## RPC Service Class Details

### 1. `RpcService` (RPC Service Class)

The `RpcService` class is the entry point for RPC call functionalities, through which you can perform all RPC-related operations.

#### 1.1. `__init__()` (Initialize RPC Service)

The constructor initializes an `RpcService` instance, requiring a configured `ThingsBoardClient` instance to send HTTP requests.

*   **Parameters**:
    *   `client`: A `ThingsBoardClient` instance, used for communication with the ThingsBoard platform.

#### 1.2. `send_one_way_rpc()` (Send One-Way RPC Request)

Sends a one-way RPC request to the specified device. This method does not wait for a device response and is suitable for "fire-and-forget" control commands.

*   **Parameters**:
    *   `device_id` (str): The ID of the target device.
    *   `method` (str): The name of the RPC method to call.
    *   `params` (Optional[Dict[str, Any]]): Parameters for the RPC method, a key-value pair dictionary.
*   **Returns**:
    *   `bool` - Returns `True` if the request was successfully sent (ThingsBoard accepted the request).
*   **Raises**:
    *   `ValidationError`: If `device_id` or `method` is empty or invalid.
    *   `RPCError`: If the RPC request fails to send.

#### 1.3. `send_two_way_rpc()` (Send Two-Way RPC Request)

Sends a two-way RPC request to the specified device and waits for a device response. This method is suitable for scenarios where a return result from the device is required.

*   **Parameters**:
    *   `device_id` (str): The ID of the target device.
    *   `method` (str): The name of the RPC method to call.
    *   `params` (Optional[Dict[str, Any]]): Parameters for the RPC method.
    *   `timeout_seconds` (float, default: 30.0): Timeout for waiting for a device response (in seconds).
*   **Returns**:
    *   `RPCResponse` - An RPC response object containing the device's response or error information.
*   **Raises**:
    *   `ValidationError`: If `device_id`, `method`, or `timeout_seconds` parameters are invalid.
    *   `RPCError`: If the RPC call fails.
    *   `TimeoutError`: If no device response is received within `timeout_seconds`.

#### 1.4. `send_rpc_with_retry()` (Send Two-Way RPC Request with Retry)

Sends a two-way RPC request with automatic retry support on failure. This improves the robustness of RPC calls.

*   **Parameters**:
    *   `device_id` (str): The ID of the target device.
    *   `method` (str): The name of the RPC method to call.
    *   `params` (Optional[Dict[str, Any]]): Parameters for the RPC method.
    *   `max_retries` (int, default: 3): Maximum number of retries.
    *   `timeout_seconds` (float, default: 30.0): Timeout for waiting for a device response for each attempt (in seconds).
    *   `retry_delay` (float, default: 1.0): Delay between retries (in seconds).
*   **Returns**:
    *   `RPCResponse` - The successful RPC response object.
*   **Raises**:
    *   `ValidationError`: If parameters are invalid.
    *   `RPCError`: If all retries fail, the error from the last attempt will be raised.
    *   `TimeoutError`: If a timeout occurs during the retry process.

#### 1.5. `send_persistent_rpc()` (Send Persistent RPC Request)

Sends a persistent RPC request to the specified device. ThingsBoard will store this request even if the device is currently offline and deliver it once the device comes online.

*   **Parameters**:
    *   `device_id` (str): The ID of the target device.
    *   `method` (str): The name of the RPC method to call.
    *   `params` (Optional[Dict[str, Any]]): Parameters for the RPC method.
    *   `expiration_time` (Optional[int]): Expiration time of the request (Unix timestamp in milliseconds). If the device does not come online or respond before this time, the request will expire.
*   **Returns**:
    *   `str` - The ID of the created persistent RPC request.
*   **Raises**:
    *   `ValidationError`: If `device_id` or `method` is empty or invalid.
    *   `RPCError`: If the RPC call fails.

#### 1.6. `get_persistent_rpc_response()` (Get Persistent RPC Response)

Queries the current status and device response of a specified persistent RPC request.

*   **Parameters**:
    *   `rpc_id` (str): The ID of the persistent RPC request.
*   **Returns**:
    *   `Optional[PersistentRPCRequest]` - The persistent RPC request object. Returns `None` if the request does not exist.
*   **Raises**:
    *   `ValidationError`: If `rpc_id` is empty or invalid.
    *   `RPCError`: If retrieving the persistent RPC response fails.

#### 1.7. `delete_persistent_rpc()` (Delete Persistent RPC Request)

Deletes the persistent RPC request with the specified ID. This is typically used to clean up completed, expired, or no longer needed persistent requests.

*   **Parameters**:
    *   `rpc_id` (str): The ID of the persistent RPC request to delete.
*   **Returns**:
    *   `bool` - Returns `True` if the deletion is successful.
*   **Raises**:
    *   `ValidationError`: If `rpc_id` is empty or invalid.
    *   `RPCError`: If the RPC call fails.

#### 1.8. `wait_for_persistent_rpc_response()` (Wait for Persistent RPC Response)

Polls the specified persistent RPC request until it completes, expires, or reaches the specified timeout. This method provides a mechanism to synchronously wait for asynchronous RPC results.

*   **Parameters**:
    *   `rpc_id` (str): The ID of the persistent RPC request.
    *   `timeout_seconds` (float, default: 60.0): Maximum waiting time (in seconds).
    *   `poll_interval` (float, default: 2.0): Interval for polling status checks (in seconds).
*   **Returns**:
    *   `Optional[PersistentRPCRequest]` - If completed or expired before timeout, returns the corresponding `PersistentRPCRequest` object. If timed out and not completed, raises `TimeoutError`.
*   **Raises**:
    *   `ValidationError`: If `rpc_id`, `timeout_seconds`, or `poll_interval` parameters are invalid.
    *   `RPCError`: If another RPC error occurs during waiting, or if the specified `rpc_id` does not exist.
    *   `TimeoutError`: If no completed or expired response is received within the specified time.