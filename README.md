# ThingsBoardLink

<div align="center">

[![PyPI Downloads](https://static.pepy.tech/badge/thingsboardlink)](https://pepy.tech/projects/thingsboardlink)
[![PyPI version](https://badge.fury.io/py/thingsboardlink.svg)](https://badge.fury.io/py/thingsboardlink)
[![Python Version](https://img.shields.io/pypi/pyversions/thingsboardlink.svg)](https://pypi.org/project/thingsboardlink/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A high-level IoT platform interaction toolkit designed for Python developers**

*IoT Cloud Platform • Developer-Friendly • Production-Ready*

[Chinese](README-zh_CN.md) | [Documentation]() | [Examples](#examples)

</div>

---

## 🚀 Why ThingsBoardLink?

ThingsBoardLink is a powerful Python package designed to simplify integration with the ThingsBoard IoT platform. It encapsulates ThingsBoard's REST API, providing object-oriented interfaces that allow developers to easily manage devices, process telemetry data, control alarms, and other core functions.

### ✨ Key Features

| Feature                          | Description                                                 | Advantages                                                                             |
|----------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------------|
| 🔐 **Authentication Management** | Automatic handling of JWT tokens and session management     | Enhanced security with stateless authentication                                        |
| 📱 **Device Management**         | Complete device CRUD operations and credential management   | Easy management of device lifecycle and access                                         |
| 📊 **Telemetry Data**            | Data upload, query, and historical data retrieval           | Efficient processing of time-series data, supporting real-time monitoring and analysis |
| ⚙️ **Attribute Management**      | Client-side, server-side, and shared attribute operations   | Flexible management of device metadata, supporting dynamic configuration               |
| 🚨 **Alarm Management**          | Alarm creation, query, acknowledgment, and clearance        | Timely response to abnormal events, ensuring system reliability                        |
| 🔄 **RPC Calls**                 | Support for both one-way and two-way remote procedure calls | Efficient command interaction between devices and the cloud                            |
| 🔗 **Relationship Management**   | Creation and management of relationships between entities   | Construct device topologies and implement complex business logic                       |
| 🛡️ **Error Handling**           | Comprehensive exception handling and error information      | Quick issue identification, improving system robustness                                |
| 📚 **Type Safety**               | Complete TypeScript-style type hints                        | Reduce development errors, enhance code quality and development efficiency             |
| 🚀 **Ease of Use**               | Clean API design and extensive documentation                | Lower learning curve, accelerate project development and integration                   |

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install thingsboardlink

# Or install with development dependencies
pip install thingsboardlink[dev]
```

### 30-Second Demo
```python
from thingsboardlink import ThingsBoardClient

# Connect to the corresponding cloud platform
with ThingsBoardClient(
    base_url="http://localhost:8080",
    username="tenant@thingsboard.org",
    password="tenant"
) as client:
    # Device ID
    device_id = "MY_DEVICE_ID"
    
    # Retrieve telemetry data for the corresponding device
    value = client.telemetry_service.get_latest_telemetry(device_id)
    print(value)
```

## 📚 Complete Usage Guide

### ...