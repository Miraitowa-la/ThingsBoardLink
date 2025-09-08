# thingsboardlink Exception Handling Module Documentation

This document provides a detailed explanation of the various custom exception classes defined in the `thingsboardlink` package, aiming to help developers understand and utilize these exceptions for robust error handling.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**Exception Class Details**](#exception-class-details)
    - [**1. ThingsBoardError**](#1-thingsboarderror)
    - [**2. AuthenticationError**](#2-authenticationerror)
    - [**3. NotFoundError**](#3-notfounderror)
    - [**4. ValidationError**](#4-validationerror)
    - [**5. APIError**](#5-apierror)
    - [**6. ConnectionError**](#6-connectionerror)
    - [**7. TimeoutError**](#7-timeouterror)
    - [**8. ConfigurationError**](#8-configurationerror)
    - [**9. RateLimitError**](#9-ratelimiterror)
    - [**10. DeviceError**](#10-deviceerror)
    - [**11. TelemetryError**](#11-telemetryerror)
    - [**12. AlarmError**](#12-alarmerror)
    - [**13. RPCError**](#13-rpcerror)

## Overview

The `thingsboardlink` exception handling module (`exceptions.py`) centrally defines all custom exceptions that the `thingsboardlink` package might encounter during interaction with the ThingsBoard platform. These exception classes provide a structured way to report and handle errors, helping developers diagnose issues more accurately and implement more robust applications through detailed error messages and hierarchical inheritance.

## Core Features

* **Unified Exception Base Class**: Provides `ThingsBoardError` as the base class for all `thingsboardlink`-related exceptions, facilitating unified exception catching and handling.
* **Fine-grained Error Classification**: Divides potential error scenarios into multiple specific exception subclasses, such as authentication, resource not found, API call failure, connection issues, data validation, etc., making error types clear at a glance.
* **Rich Error Details**: Each exception class supports storing attributes like `message` (error message) and `details` (detailed dictionary) to obtain more comprehensive context information when catching exceptions.
* **Easy Construction**: Exception constructors typically accept error-specific parameters, such as resource type, field name, status code, etc., to automatically generate meaningful error messages and details.
* **HTTP Response Integration**: `APIError` provides a `from_response` class method that can directly construct an exception from an HTTP response object, simplifying API error handling.

## Exception Class Details

### 1. ThingsBoardError

`ThingsBoardError` is the base class for all `thingsboardlink` exceptions. It provides a unified exception handling interface and basic functionalities, including an error message (`message`) and an optional error details dictionary (`details`).

* **Inherits**: `Exception`
* **Constructor**:
    * `message` (str): The primary error message.
    * `details` (Optional[Dict[str, Any]]): A dictionary containing additional error context information.
* **Attributes**:
    * `message`: Stores the passed error message.
    * `details`: Stores the passed error details dictionary.

### 2. AuthenticationError

This exception is raised when user authentication fails, such as login failure, token expiration, or insufficient permissions.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str, default: "Authentication failed"): Description of the authentication failure.
    * `details` (Optional[Dict[str, Any]]): Additional details about the authentication failure.

### 3. NotFoundError

This exception is raised when the requested ThingsBoard resource (e.g., device, user, alarm) does not exist.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `resource_type` (str, default: "Resource"): Type of the resource not found.
    * `resource_id` (Optional[str]): Specific ID of the resource not found.
    * `message` (Optional[str]): Error message, automatically generated based on `resource_type` and `resource_id` if not provided.

### 4. ValidationError

This exception is raised when input data does not conform to the expected format or constraints, such as incorrect parameter type, out-of-range value, or missing required fields.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `field_name` (Optional[str]): Name of the field where the validation error occurred.
    * `expected_type` (Optional[str]): Expected data type of the field.
    * `actual_value` (Any): Actual value of the field.
    * `message` (Optional[str]): Error message, automatically generated based on `field_name` and `expected_type` if not provided.

### 5. APIError

This exception is raised when an API call returns an error status code (e.g., HTTP 4xx, 5xx). It includes detailed HTTP status code, response data, request URL, and request method.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str): Error message.
    * `status_code` (Optional[int]): HTTP status code.
    * `response_data` (Optional[Dict[str, Any]]): JSON data from the server response.
    * `request_url` (Optional[str]): URL of the sent request.
    * `request_method` (Optional[str]): HTTP method used for the request.
* **Attributes**:
    * `status_code`: HTTP status code.
    * `response_data`: Server response data.
    * `request_url`: URL of the request.
    * `request_method`: HTTP method of the request.
* **Class Method**:
    * `from_response(cls, response, message: Optional[str] = None)`: Creates an `APIError` instance from an HTTP response object (e.g., `requests.Response`). It automatically parses the status code, response data, URL, and method.

### 6. ConnectionError

This exception is raised when unable to connect to the ThingsBoard server, such as network connection failure or server unreachable.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str, default: "Unable to connect to ThingsBoard server"): Description of the connection error.
    * `server_url` (Optional[str]): Address of the server attempted to connect to.
    * `details` (Optional[Dict[str, Any]]): Additional details.

### 7. TimeoutError

This exception is raised when a request operation times out (e.g., connection timeout or read timeout).

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str, default: "Request timed out"): Description of the timeout error.
    * `timeout_seconds` (Optional[float]): Configured timeout duration (in seconds).
    * `operation` (Optional[str]): Specific operation that timed out.

### 8. ConfigurationError

This exception is raised when configuration parameters are invalid or missing, such as incorrect server address configuration or missing authentication information.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str, default: "Configuration error"): Description of the configuration error.
    * `config_key` (Optional[str]): Key name of the configuration item where the error occurred.
    * `expected_value` (Optional[str]): Expected value or format of the configuration item.

### 9. RateLimitError

This exception is raised when API calls exceed the rate limit set by the ThingsBoard server. It is a subclass of `APIError`, usually accompanied by an HTTP 429 status code.

* **Inherits**: `APIError`
* **Constructor**:
    * `message` (str, default: "API call rate limit exceeded"): Description of the rate limit.
    * `retry_after` (Optional[int]): Suggested number of seconds to wait before retrying.
    * `limit_type` (Optional[str]): Type of rate limit (e.g., by IP, by user, etc.).

### 10. DeviceError

Handles errors related to device operations, such as device creation failure, abnormal device status, or device attribute operation failure.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str): Error message.
    * `device_id` (Optional[str]): ID of the device involved.
    * `device_name` (Optional[str]): Name of the device involved.

### 11. TelemetryError

Handles errors related to telemetry data operations, such as incorrect data format or telemetry data upload failure.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str): Error message.
    * `data_key` (Optional[str]): Key in the telemetry data.
    * `data_value` (Any): Value of the telemetry data.

### 12. AlarmError

Handles errors related to alarm operations, such as alarm creation failure or alarm status update failure.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str): Error message.
    * `alarm_id` (Optional[str]): ID of the alarm involved.
    * `alarm_type` (Optional[str]): Type of the alarm involved.

### 13. RPCError

Handles errors related to Remote Procedure Call (RPC), such as RPC call timeout, device unresponsiveness, or malformed RPC request.

* **Inherits**: `ThingsBoardError`
* **Constructor**:
    * `message` (str): Error message.
    * `method_name` (Optional[str]): Name of the RPC method called.
    * `device_id` (Optional[str]): ID of the target device.
    * `timeout_seconds` (Optional[float]): Timeout duration (in seconds) for the RPC call.