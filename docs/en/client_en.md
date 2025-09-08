# thingsboardlink Core Client Module Documentation

This document details the core client class `ThingsBoardClient` in the `thingsboardlink` package. As the central hub for interacting with the ThingsBoard platform, it handles authentication management, HTTP request processing, unified error handling, and access to various service modules.

## Table of Contents

- [**Overview**](#overview)
- [**Core Features**](#core-features)
- [**ThingsBoardClient Details**](#thingsboardclient-details)
    - [**1. Client Initialization (`__init__`)**](#1-client-initialization-__init__)
    - [**2. Service Module Properties**](#2-service-module-properties)
        - [**2.1. `device_service` (Device Service)**](#21-device_service-device-service)
        - [**2.2. `telemetry_service` (Telemetry Service)**](#22-telemetry_service-telemetry-service)
        - [**2.3. `attribute_service` (Attribute Service)**](#23-attribute_service-attribute-service)
        - [**2.4. `alarm_service` (Alarm Service)**](#24-alarm_service-alarm-service)
        - [**2.5. `rpc_service` (RPC Service)**](#25-rpc_service-rpc-service)
        - [**2.6. `relation_service` (Relation Service)**](#26-relation_service-relation-service)
    - [**3. Authentication Methods**](#3-authentication-methods)
        - [**3.1. `login()` (User Login)**](#31-login-user-login)
        - [**3.2. `is_authenticated` (Check Authentication Status)**](#32-is_authenticated-check-authentication-status)
        - [**3.3. `logout()` (User Logout)**](#33-logout-user-logout)
        - [**3.4. `refresh_token()` (Refresh Access Token)**](#34-refresh_token-refresh-access-token)
        - [**3.5. `_ensure_authenticated()` (Ensure Client is Authenticated)**](#35-_ensure_authenticated-ensure-client-is-authenticated)
    - [**4. HTTP Request Methods**](#4-http-request-methods)
        - [**4.1. `request()` (Send HTTP Request)**](#41-request-send-http-request)
        - [**4.2. `get()` (Send GET Request)**](#42-get-send-get-request)
        - [**4.3. `post()` (Send POST Request)**](#43-post-send-post-request)
        - [**4.4. `put()` (Send PUT Request)**](#44-put-send-put-request)
        - [**4.5. `delete()` (Send DELETE Request)**](#45-delete-send-delete-request)
    - [**5. Resource Management Methods**](#5-resource-management-methods)
        - [**5.1. `close()` (Close Client Connection)**](#51-close-close-client-connection)
        - [**5.2. `__enter__()` (Context Manager Entry)**](#52-__enter__-context-manager-entry)
        - [**5.3. `__exit__()` (Context Manager Exit)**](#53-__exit__-context-manager-exit)

## Overview

The `ThingsBoardClient` class is the core of the `thingsboardlink` library, encapsulating all low-level details for interacting with the ThingsBoard RESTful API. It establishes and maintains connections with the ThingsBoard server, handles user authentication (including JWT token acquisition, refresh, and management), sends HTTP requests, and provides a unified error handling mechanism. Additionally, it offers convenient access to various ThingsBoard services (such as devices, telemetry, alarms, etc.) through properties.

## Core Features

* **Centralized Authentication Management**: Automatically handles user login, JWT token storage, expiration checks, and refresh to ensure API call continuity.
* **Robust HTTP Requests**: Built on the `requests` library, supporting request timeouts, SSL verification, and configurable request retry policies to improve network operation reliability.
* **Unified Error Handling**: Converts underlying `requests` exceptions and ThingsBoard API errors into `thingsboardlink` custom exception types, simplifying error capture and handling logic for developers.
* **Service Module Integration**: Provides seamless access to advanced service modules like devices, telemetry, attributes, alarms, RPC, and relations through lazy-loaded properties.
* **Context Manager Support**: Allows the client to be used in `with` statements, ensuring automatic logout and connection closure when exiting the scope.
* **Flexible Configuration**: Supports configuration of ThingsBoard base URL, authentication credentials, timeout durations, retry policies, and SSL verification.

## ThingsBoardClient Details

### 1. Client Initialization (`__init__`)

The constructor initializes a `ThingsBoardClient` instance, configuring basic parameters required for communication with the ThingsBoard server.

* **Parameters**:
    * `base_url` (str): Base URL of the ThingsBoard server (e.g., `http://localhost:8080`).
    * `username` (Optional[str]): ThingsBoard username for login.
    * `password` (Optional[str]): ThingsBoard password for login.
    * `timeout` (float, default: 30.0): Default timeout duration (in seconds) for all HTTP requests.
    * `max_retries` (int, default: 3): Maximum retry attempts for retryable HTTP status codes (e.g., 429, 5xx).
    * `retry_backoff_factor` (float, default: 0.3): Backoff factor between retries. Wait time increases exponentially with this factor.
    * `verify_ssl` (bool, default: `True`): Whether to verify the ThingsBoard server's SSL certificate. Setting to `False` disables SSL verification but is not recommended in production environments.
* **Internal Processing**:
    * Initializes internal authentication-related states like `_jwt_token`, `_refresh_token`, and `_token_expires_at`.
    * Creates a `requests.Session` object for persistent connections and session state.
    * Configures `HTTPAdapter` to implement request retry logic for specific status codes and HTTP methods.
    * Sets default `Content-Type` and `Accept` headers to `application/json`.
    * Lazily imports and initializes instances of various service modules to avoid circular imports and improve performance.

### 2. Service Module Properties

These properties provide access to different ThingsBoard service modules. They follow a **lazy-loading** pattern, meaning the corresponding service instances are created only upon first access.

#### 2.1. `device_service` (Device Service)

* **Returns**: `DeviceService` instance
* **Description**: Used for device-related operations such as creating, retrieving, updating, and deleting devices, as well as managing device credentials.

#### 2.2. `telemetry_service` (Telemetry Service)

* **Returns**: `TelemetryService` instance
* **Description**: Used for uploading, retrieving, and managing device telemetry data.

#### 2.3. `attribute_service` (Attribute Service)

* **Returns**: `AttributeService` instance
* **Description**: Used for getting, setting, and deleting client-side, server-side, and shared attributes of entities (e.g., devices, assets).

#### 2.4. `alarm_service` (Alarm Service)

* **Returns**: `AlarmService` instance
* **Description**: Used for creating, querying, acknowledging, and clearing alarms in ThingsBoard.

#### 2.5. `rpc_service` (RPC Service)

* **Returns**: `RpcService` instance
* **Description**: Used for sending synchronous or asynchronous remote procedure call (RPC) requests to devices and handling their responses.

#### 2.6. `relation_service` (Relation Service)

* **Returns**: `RelationService` instance
* **Description**: Used for managing relationships between ThingsBoard entities.

### 3. Authentication Methods

#### 3.1. `login()` (User Login)

Authenticates with the ThingsBoard platform using a username and password, obtaining and storing JWT access and refresh tokens.

* **Parameters**:
    * `username` (Optional[str]): Username for this login. If not provided, uses the username from client initialization.
    * `password` (Optional[str]): Password for this login. If not provided, uses the password from client initialization.
* **Returns**:
    * `bool` - Returns `True` if login succeeds, otherwise `False`.
* **Raises**:
    * `ConfigurationError`: If username or password is not provided.
    * `AuthenticationError`: If authentication fails (e.g., incorrect username/password or server returns non-200 status code).
    * `ConnectionError`: If unable to connect to the ThingsBoard server.
    * `TimeoutError`: If the login request times out.
* **Side Effects**: Upon successful login, internally sets `_jwt_token` and `_refresh_token`, and updates the `requests.Session`'s `X-Authorization` header.

#### 3.2. `is_authenticated` (Check Authentication Status)

A property that checks whether the client is currently authenticated and the access token is not expired.

* **Returns**: `bool` - Returns `True` if authenticated and token is valid, otherwise `False`.

#### 3.3. `logout()` (User Logout)

Invalidates the current JWT access token and clears all authentication information stored internally by the client.

* **Returns**: `bool` - Whether the logout operation succeeded (local credentials are cleared even if server notification fails due to network issues).
* **Side Effects**: Clears `_jwt_token`, `_refresh_token`, and `_token_expires_at`, and removes the `X-Authorization` header from `requests.Session`.

#### 3.4. `refresh_token()` (Refresh Access Token)

Uses the refresh token (`_refresh_token`) to obtain a new JWT access token from the ThingsBoard server.

* **Returns**: `bool` - Returns `True` if token refresh succeeds, otherwise `False`.
* **Side Effects**: If refresh succeeds, updates `_jwt_token`, `_refresh_token`, and `_token_expires_at`, and updates the `requests.Session`'s `X-Authorization` header.

#### 3.5. `_ensure_authenticated()` (Ensure Client is Authenticated)

An internal method called before sending authenticated requests. It checks the current authentication status, attempts to refresh the token if expired, and tries to re-login if refresh fails.

* **Raises**: `AuthenticationError`: If authentication cannot be established after refresh and re-login attempts.

### 4. HTTP Request Methods

`ThingsBoardClient` provides general methods and convenience wrappers for sending various HTTP requests.

#### 4.1. `request()` (Send HTTP Request)

The underlying general HTTP request method. All `get/post/put/delete` methods ultimately call this method.

* **Parameters**:
    * `method` (str): HTTP request method (e.g., "GET", "POST", "PUT", "DELETE").
    * `endpoint` (str): Relative path of the ThingsBoard API (e.g., `"/api/device"`).
    * `data` (Optional[Union[Dict[str, Any], str]]): Request body data, which can be a dictionary (will be JSON-serialized) or a string.
    * `params` (Optional[Dict[str, Any]]): URL query parameter dictionary.
    * `headers` (Optional[Dict[str, str]]): Additional request header dictionary.
    * `require_auth` (bool, default: `True`): Whether authentication is required. If `True`, calls `_ensure_authenticated()` before sending the request.
    * `timeout` (Optional[float]): Timeout duration (in seconds) for this request. If not provided, uses the client instance's default `timeout`.
* **Returns**:
    * `requests.Response` - The raw HTTP response object.
* **Raises**:
    * `AuthenticationError`: If `require_auth` is `True` but the client is not authenticated.
    * `APIError`: If the ThingsBoard API returns a 4xx or 5xx status code.
    * `ConnectionError`: If a network connection error occurs.
    * `TimeoutError`: If the request times out.

#### 4.2. `get()` (Send GET Request)

A convenience method for sending HTTP GET requests.

* **Parameters**: `**kwargs` - All additional parameters passed to `request()` (e.g., `endpoint`, `params`, `headers`, `require_auth`, `timeout`).
* **Returns**: `requests.Response`.

#### 4.3. `post()` (Send POST Request)

A convenience method for sending HTTP POST requests.

* **Parameters**: `**kwargs` - All additional parameters passed to `request()` (e.g., `endpoint`, `data`, `params`, `headers`, `require_auth`, `timeout`).
* **Returns**: `requests.Response`.

#### 4.4. `put()` (Send PUT Request)

A convenience method for sending HTTP PUT requests.

* **Parameters**: `**kwargs` - All additional parameters passed to `request()` (e.g., `endpoint`, `data`, `params`, `headers`, `require_auth`, `timeout`).
* **Returns**: `requests.Response`.

#### 4.5. `delete()` (Send DELETE Request)

A convenience method for sending HTTP DELETE requests.

* **Parameters**: `**kwargs` - All additional parameters passed to `request()` (e.g., `endpoint`, `params`, `headers`, `require_auth`, `timeout`).
* **Returns**: `requests.Response`.

### 5. Resource Management Methods