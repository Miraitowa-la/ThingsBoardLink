"""
ThingsBoardLink RPC 调用示例

本示例演示如何使用 ThingsBoardLink 进行 RPC（远程过程调用）操作。
包括单向 RPC、双向 RPC、持久化 RPC 以及带重试机制的 RPC 调用等功能。

运行前请设置环境变量
export THINGSBOARD_URL="http://localhost:8080"
export THINGSBOARD_USERNAME="tenant@thingsboard.org"
export THINGSBOARD_PASSWORD="tenant"
"""

import os
import time
import uuid
import json
from typing import Optional

from src.thingsboardlink import (
    ThingsBoardClient,
    Device,
    RpcPersistentStatus,
    ValidationError,
    TimeoutError
)


def get_config_from_env() -> dict:
    """从环境变量获取配置"""
    return {
        "base_url": os.getenv("THINGSBOARD_URL", "http://localhost:8080"),
        "username": os.getenv("THINGSBOARD_USERNAME", "tenant@thingsboard.org"),
        "password": os.getenv("THINGSBOARD_PASSWORD", "tenant")
    }


def create_demo_device(client: ThingsBoardClient) -> Optional[Device]:
    """创建演示设备
    
    Args:
        client: ThingsBoard 客户端
        
    Returns:
        Device: 创建的设备对象
    """
    try:
        device_name = f"rpc_demo_device_{uuid.uuid4().hex[:8]}"
        device = client.device_service.create_device(
            name=device_name,
            device_type="controller",
            label="RPC 调用演示设备"
        )

        if device:
            print(f"✅ 创建演示设备成功: {device.name}")
            return device
        else:
            print("❌ 创建演示设备失败")
            return None

    except Exception as e:
        print(f"❌ 创建演示设备时发生错误: {e}")
        return None


def example_one_way_rpc(client: ThingsBoardClient, device: Device):
    """单向 RPC 调用示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 单向 RPC 调用示例 ===")

    try:
        device_id = device.id
        print(f"向设备发送单向 RPC 调用: {device.name}")

        # 定义不同类型的单向 RPC 调用
        rpc_calls = [
            {
                "method": "setLedState",
                "params": {
                    "led_id": 1,
                    "state": "on",
                    "brightness": 80,
                    "color": "#FF0000"
                },
                "description": "设置 LED 状态"
            },
            {
                "method": "updateConfiguration",
                "params": {
                    "sampling_rate": 30,
                    "reporting_interval": 300,
                    "power_saving_mode": True,
                    "debug_enabled": False
                },
                "description": "更新设备配置"
            },
            {
                "method": "executeCommand",
                "params": {
                    "command": "restart",
                    "delay_seconds": 5,
                    "reason": "定期维护重启"
                },
                "description": "执行设备命令"
            },
            {
                "method": "calibrateSensors",
                "params": {
                    "sensor_types": ["temperature", "humidity", "pressure"],
                    "calibration_mode": "auto",
                    "reference_values": {
                        "temperature": 25.0,
                        "humidity": 50.0,
                        "pressure": 1013.25
                    }
                },
                "description": "校准传感器"
            }
        ]

        # 发送单向 RPC 调用
        for i, rpc_call in enumerate(rpc_calls, 1):
            try:
                print(f"\n{i}. {rpc_call['description']}")
                print(f"   方法: {rpc_call['method']}")
                print(f"   参数: {json.dumps(rpc_call['params'], indent=4, ensure_ascii=False)}")

                success = client.rpc_service.send_one_way_rpc(
                    device_id=device_id,
                    method=rpc_call["method"],
                    params=rpc_call["params"]
                )

                if success:
                    print(f"   ✅ 单向 RPC 调用发送成功")
                else:
                    print(f"   ❌ 单向 RPC 调用发送失败")

                # 短暂延迟
                time.sleep(1)

            except ValidationError as e:
                print(f"   ❌ 验证错误: {e}")
                print(f"   字段: {e.details.get('field')}")
            except Exception as e:
                print(f"   ❌ 发送单向 RPC 调用时发生错误: {e}")

        print(f"\n单向 RPC 调用示例完成")

    except Exception as e:
        print(f"❌ 单向 RPC 调用示例发生错误: {e}")


def example_two_way_rpc(client: ThingsBoardClient, device: Device):
    """双向 RPC 调用示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 双向 RPC 调用示例 ===")

    try:
        device_id = device.id
        print(f"向设备发送双向 RPC 调用: {device.name}")

        # 定义不同类型的双向 RPC 调用
        rpc_calls = [
            {
                "method": "getDeviceStatus",
                "params": {
                    "include_sensors": True,
                    "include_network": True,
                    "include_battery": True
                },
                "timeout": 10.0,
                "description": "获取设备状态"
            },
            {
                "method": "readSensorData",
                "params": {
                    "sensor_types": ["temperature", "humidity"],
                    "format": "json",
                    "timestamp": True
                },
                "timeout": 15.0,
                "description": "读取传感器数据"
            },
            {
                "method": "performDiagnostics",
                "params": {
                    "test_types": ["connectivity", "sensors", "memory"],
                    "detailed_report": True
                },
                "timeout": 30.0,
                "description": "执行设备诊断"
            }
        ]

        # 发送双向 RPC 调用
        for i, rpc_call in enumerate(rpc_calls, 1):
            try:
                print(f"\n{i}. {rpc_call['description']}")
                print(f"   方法: {rpc_call['method']}")
                print(f"   参数: {json.dumps(rpc_call['params'], indent=4, ensure_ascii=False)}")
                print(f"   超时时间: {rpc_call['timeout']}s")

                response = client.rpc_service.send_two_way_rpc(
                    device_id=device_id,
                    method=rpc_call["method"],
                    params=rpc_call["params"],
                    timeout_seconds=rpc_call["timeout"]
                )

                if response:
                    print(f"   ✅ 双向 RPC 调用成功")
                    print(f"   响应: {response.response}")
                else:
                    print(f"   ❌ 双向 RPC 调用失败或无响应")

                # 短暂延迟
                time.sleep(2)

            except TimeoutError as e:
                print(f"   ⏰ RPC 调用超时: {e}")
                print(f"   超时时间: {e.details.get('timeout')}s")
            except ValidationError as e:
                print(f"   ❌ 验证错误: {e}")
                print(f"   字段: {e.details.get('field')}")
            except Exception as e:
                print(f"   ❌ 发送双向 RPC 调用时发生错误: {e}")

        print(f"\n双向 RPC 调用示例完成")

    except Exception as e:
        print(f"❌ 双向 RPC 调用示例发生错误: {e}")


def example_persistent_rpc(client: ThingsBoardClient, device: Device):
    """持久化 RPC 调用示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 持久化 RPC 调用示例 ===")

    try:
        device_id = device.id
        print(f"向设备发送持久化 RPC 调用: {device.name}")

        # 发送持久化 RPC 调用
        method = "firmwareUpdate"
        params = {
            "firmware_version": "2.1.0",
            "download_url": "https://example.com/firmware/v2.1.0.bin",
            "checksum": "sha256:abcd1234...",
            "update_schedule": "immediate",
            "backup_current": True,
            "reboot_after_update": True
        }
        expiration_time = (int(time.time()) + 30) * 1000

        print(f"方法: {method}")
        print(f"参数: {json.dumps(params, indent=2, ensure_ascii=False)}")

        # 发送持久化 RPC 请求
        rpc_id = client.rpc_service.send_persistent_rpc(
            device_id=device_id,
            method=method,
            params=params,
            expiration_time=expiration_time
        )

        if rpc_id:
            print(f"✅ 持久化 RPC 调用发送成功")
            print(f"RPC ID: {rpc_id}")

            # 等待响应
            print("\n等待设备响应...")

            max_wait_time = 60  # 最大等待时间（秒）
            check_interval = 5  # 检查间隔（秒）
            waited_time = 0

            while waited_time < max_wait_time:
                try:
                    # 获取持久化 RPC 响应
                    response = client.rpc_service.get_persistent_rpc_response(rpc_id)

                    if response.status == RpcPersistentStatus.SUCCESSFUL.value:
                        print(f"✅ 收到持久化 RPC 响应")
                        print(f"响应内容: {response.response}")
                        break
                    else:
                        print(
                            f"⏳ 等待响应中... ({waited_time}s/{max_wait_time}s)")
                        time.sleep(check_interval)
                        waited_time += check_interval

                except Exception as e:
                    print(f"❌ 获取持久化 RPC 响应时发生错误: {e}")
                    break

            if waited_time >= max_wait_time:
                print(f"⏰ 等待响应超时 ({max_wait_time}s)")

                # 尝试删除持久化 RPC 请求
                print("删除超时的持久化 RPC 请求...")
                delete_success = client.rpc_service.delete_persistent_rpc(rpc_id)

                if delete_success:
                    print("✅ 持久化 RPC 请求删除成功")
                else:
                    print("❌ 持久化 RPC 请求删除失败")
        else:
            print("❌ 持久化 RPC 调用发送失败")

    except Exception as e:
        print(f"❌ 持久化 RPC 调用示例发生错误: {e}")


def example_wait_for_persistent_rpc_response(client: ThingsBoardClient, device: Device):
    """等待持久化 RPC 响应示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 等待持久化 RPC 响应示例 ===")

    try:
        device_id = device.id
        print(f"发送持久化 RPC 并等待响应: {device.name}")

        # 发送持久化 RPC 调用
        method = "getSystemInfo"
        params = {
            "include_hardware": True,
            "include_software": True,
            "include_network": True,
            "format": "detailed"
        }

        expiration_time = (int(time.time()) + 30) * 1000

        print(f"方法: {method}")
        print(f"参数: {json.dumps(params, indent=2, ensure_ascii=False)}")

        # 发送持久化 RPC 请求
        rpc_id = client.rpc_service.send_persistent_rpc(
            device_id=device_id,
            method=method,
            params=params,
            expiration_time=expiration_time
        )

        if rpc_id:
            print(f"✅ 持久化 RPC 调用发送成功")
            print(f"RPC ID: {rpc_id}")

            # 使用便捷方法等待响应
            print("\n使用便捷方法等待响应...")

            timeout = 30.0  # 超时时间（秒）

            try:
                response = client.rpc_service.wait_for_persistent_rpc_response(
                    rpc_id=rpc_id,
                    timeout_seconds=timeout
                )

                if response:
                    print(f"✅ 收到持久化 RPC 响应")
                    print(f"响应内容: {response.response}")
                else:
                    print(f"❌ 未收到持久化 RPC 响应")

            except TimeoutError as e:
                print(f"⏰ 等待持久化 RPC 响应超时: {e}")
                print(f"超时时间: {e.details.get('timeout')}s")

                # 清理超时的请求
                print("清理超时的持久化 RPC 请求...")
                delete_success = client.rpc_service.delete_persistent_rpc(rpc_id)

                if delete_success:
                    print("✅ 超时请求清理成功")
                else:
                    print("❌ 超时请求清理失败")
        else:
            print("❌ 持久化 RPC 调用发送失败")

    except Exception as e:
        print(f"❌ 等待持久化 RPC 响应示例发生错误: {e}")


def example_rpc_with_retry(client: ThingsBoardClient, device: Device):
    """带重试机制的 RPC 调用示例
    
    Args:
        client: ThingsBoard 客户端t
        device: 设备对象
    """
    print("\n=== 带重试机制的 RPC 调用示例 ===")

    try:
        device_id = device.id
        print(f"向设备发送带重试机制的 RPC 调用: {device.name}")

        # 定义 RPC 调用参数
        method = "pingDevice"
        params = {
            "timeout_ms": 5000,
            "packet_size": 64,
            "count": 3
        }

        # 重试配置
        max_retries = 3
        timeout = 10.0
        retry_delay = 2.0

        print(f"方法: {method}")
        print(f"参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
        print(f"最大重试次数: {max_retries}")
        print(f"超时时间: {timeout}s")
        print(f"重试延迟: {retry_delay}s")

        # 发送带重试机制的双向 RPC 调用
        try:
            response = client.rpc_service.send_rpc_with_retry(
                device_id=device_id,
                method=method,
                params=params,
                timeout_seconds=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay
            )

            if response:
                print(f"✅ 带重试机制的 RPC 调用成功")
                print(f"响应内容: {response.response}")
            else:
                print(f"❌ 带重试机制的 RPC 调用失败")

        except TimeoutError as e:
            print(f"⏰ RPC 调用最终超时: {e}")
            print(f"重试次数: {e.details.get('retry_count', 0)}")
            print(f"总耗时: {e.details.get('total_duration')}s")
        except Exception as e:
            print(f"❌ 带重试机制的 RPC 调用发生错误: {e}")

        # 演示不同的重试策略
        print("\n演示不同的重试策略...")

        retry_strategies = [
            {
                "name": "快速重试",
                "max_retries": 5,
                "timeout": 5.0,
                "retry_delay": 0.5
            },
            {
                "name": "标准重试",
                "max_retries": 3,
                "timeout": 10.0,
                "retry_delay": 2.0
            },
            {
                "name": "耐心重试",
                "max_retries": 2,
                "timeout": 20.0,
                "retry_delay": 5.0
            }
        ]

        for i, strategy in enumerate(retry_strategies, 1):
            print(f"\n{i}. {strategy['name']}")
            print(f"   配置: 重试{strategy['max_retries']}次, "
                  f"超时{strategy['timeout']}s, "
                  f"延迟{strategy['retry_delay']}s")

            try:
                start_time = time.time()

                response = client.rpc_service.send_rpc_with_retry(
                    device_id=device_id,
                    method="quickPing",
                    params={"message": f"test_{i}"},
                    timeout_seconds=strategy["timeout"],
                    max_retries=strategy["max_retries"],
                    retry_delay=strategy["retry_delay"]
                )

                end_time = time.time()
                duration = end_time - start_time

                if response:
                    print(f"   ✅ 策略成功 (耗时 {duration:.2f}s)")
                    print(f"   响应: {response.response}")
                else:
                    print(f"   ❌ 策略失败 (耗时: {duration:.2f}s)")

            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                print(f"   ❌ 策略异常 (耗时: {duration:.2f}s): {e}")

            # 策略间延迟
            time.sleep(1)

    except Exception as e:
        print(f"❌ 带重试机制的 RPC 调用示例发生错误: {e}")


def example_batch_rpc_calls(client: ThingsBoardClient, device: Device):
    """批量 RPC 调用示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 批量 RPC 调用示例 ===")

    try:
        device_id = device.id
        print(f"向设备发送批量 RPC 调用: {device.name}")

        # 定义批量 RPC 调用
        batch_calls = [
            {
                "method": "getLedStatus",
                "params": {"led_id": 1},
                "type": "two_way",
                "timeout": 5.0
            },
            {
                "method": "setLedBrightness",
                "params": {"led_id": 1, "brightness": 50},
                "type": "one_way"
            },
            {
                "method": "getTemperature",
                "params": {"sensor_id": "temp_01", "unit": "celsius"},
                "type": "two_way",
                "timeout": 8.0
            },
            {
                "method": "resetCounters",
                "params": {"counter_types": ["error", "warning"]},
                "type": "one_way"
            },
            {
                "method": "getSystemMetrics",
                "params": {"metrics": ["cpu", "memory", "disk"]},
                "type": "two_way",
                "timeout": 12.0
            }
        ]

        print(f"准备发送 {len(batch_calls)} 个 RPC 调用")

        # 执行批量 RPC 调用
        results = []

        for i, call in enumerate(batch_calls, 1):
            try:
                print(f"\n{i}. 执行 RPC 调用: {call['method']}")
                print(f"   类型: {call['type']}")
                print(f"   参数: {json.dumps(call['params'], ensure_ascii=False)}")

                start_time = time.time()

                if call["type"] == "one_way":
                    # 单向 RPC 调用
                    success = client.rpc_service.send_one_way_rpc(
                        device_id=device_id,
                        method=call["method"],
                        params=call["params"]
                    )

                    end_time = time.time()
                    duration = end_time - start_time

                    result = {
                        "method": call["method"],
                        "type": "one_way",
                        "success": success,
                        "duration": duration
                    }

                    if success:
                        print(
                            f"   ✅ 单向 RPC 调用成功 (耗时: {duration:.2f}s)")
                    else:
                        print(f"   ❌ 单向 RPC 调用失败 (耗时: {duration:.2f}s)")

                elif call["type"] == "two_way":
                    # 双向 RPC 调用
                    response = client.rpc_service.send_two_way_rpc(
                        device_id=device_id,
                        method=call["method"],
                        params=call["params"],
                        timeout_seconds=call.get("timeout", 10.0)
                    )

                    end_time = time.time()
                    duration = end_time - start_time

                    result = {
                        "method": call["method"],
                        "type": "two_way",
                        "success": response is not None,
                        "response": response,
                        "duration": duration
                    }

                    if response:
                        print(
                            f"   ✅ 双向 RPC 调用成功 (耗时: {duration:.2f}s)")
                        print(f"   响应: {response.response}")
                    else:
                        print(f"   ❌ 双向 RPC 调用失败 (耗时: {duration:.2f}s)")

                results.append(result)

                # 调用间延迟
                time.sleep(0.5)

            except TimeoutError as e:
                end_time = time.time()
                duration = end_time - start_time
                print(f"   ⏰ RPC 调用超时 (耗时: {duration:.2f}s): {e}")

                results.append({
                    "method": call["method"],
                    "type": call["type"],
                    "success": False,
                    "error": "timeout",
                    "duration": duration
                })

            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                print(f"   ❌ RPC 调用错误 (耗时: {duration:.2f}s): {e}")

                results.append({
                    "method": call["method"],
                    "type": call["type"],
                    "success": False,
                    "error": str(e),
                    "duration": duration
                })

        # 统计结果
        print(f"\n批量 RPC 调用结果统计:")

        total_calls = len(results)
        successful_calls = sum(1 for r in results if r["success"])
        failed_calls = total_calls - successful_calls
        total_duration = sum(r["duration"] for r in results)

        print(f"  总调用数: {total_calls}")
        print(f"  成功调用: {successful_calls}")
        print(f"  失败调用: {failed_calls}")
        print(f"  成功率 : {(successful_calls / total_calls) * 100:.1f}%")
        print(f"  总耗时 : {total_duration:.2f}s")
        print(f"  平均耗时: {total_duration / total_calls:.2f}s")

    except Exception as e:
        print(f"❌ 批量 RPC 调用示例发生错误: {e}")


def cleanup_demo_device(client: ThingsBoardClient, device: Device):
    """清理演示设备
    
    Args:
        client: ThingsBoard 客户端
        device: 要清理的设备
    """
    try:
        print(f"\n清理演示设备: {device.name}")

        success = client.device_service.delete_device(device.id)

        if success:
            print("✅ 演示设备清理成功！")
        else:
            print("❌ 演示设备清理失败！")

    except Exception as e:
        print(f"❌ 清理演示设备时发生错误 : {e}")


def main():
    """主函数"""
    print("ThingsBoardLink RPC 调用示例")
    print("=" * 80)

    config = get_config_from_env()
    demo_device = None

    try:
        # 使用上下文管理器
        with ThingsBoardClient(
                base_url=config["base_url"],
                username=config["username"],
                password=config["password"]
        ) as client:

            print("✅ 客户端连接成功！")

            # 创建演示设备
            demo_device = create_demo_device(client)

            if demo_device:
                # 0. 获取设备凭证
                print("设备凭证:", client.device_service.get_device_credentials(demo_device.id).credentials_id)
                print("耐心等待10秒时间")
                time.sleep(10)

                # 1. 单向 RPC 调用
                # example_one_way_rpc(client, demo_device)

                # 2. 双向 RPC 调用
                # example_two_way_rpc(client, demo_device)

                # # 3. 持久化 RPC 调用
                # example_persistent_rpc(client, demo_device)

                # # 4. 等待持久化 RPC 响应
                # example_wait_for_persistent_rpc_response(client, demo_device)

                # # 5. 带重试机制的 RPC 调用
                # example_rpc_with_retry(client, demo_device)

                # # 6. 批量 RPC 调用
                example_batch_rpc_calls(client, demo_device)

                # 清理演示设备
                cleanup_demo_device(client, demo_device)

            print("\n" + "=" * 80)
            print("✅ 所有 RPC 调用示例运行完成！")

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
        if demo_device:
            try:
                with ThingsBoardClient(
                        base_url=config["base_url"],
                        username=config["username"],
                        password=config["password"]
                ) as client:
                    cleanup_demo_device(client, demo_device)
            except:
                pass
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()

        if demo_device:
            try:
                with ThingsBoardClient(
                        base_url=config["base_url"],
                        username=config["username"],
                        password=config["password"]
                ) as client:
                    cleanup_demo_device(client, demo_device)
            except:
                pass


if __name__ == "__main__":
    main()
