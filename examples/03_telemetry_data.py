"""ThingsBoardLink 遥测数据示例

本示例演示如何使用 ThingsBoardLink 进行遥测数据操作。
包括遥测数据的上传、查询、删除以及时间序列数据处理等功能。

运行前请设置环境变量
export THINGSBOARD_URL="http://localhost:8080"
export THINGSBOARD_USERNAME="tenant@thingsboard.org"
export THINGSBOARD_PASSWORD="tenant"
"""

import os
import time
import uuid
import random
import json
from datetime import datetime
from typing import Optional

from src.thingsboardlink import (
    ThingsBoardClient,
    Device,
    ValidationError,
    NotFoundError
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
        device_name = f"telemetry_demo_device_{uuid.uuid4().hex[:8]}"
        device = client.device_service.create_device(
            name=device_name,
            device_type="sensor",
            label="遥测数据演示设备"
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


def example_upload_telemetry(client: ThingsBoardClient, device: Device):
    """上传遥测数据示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 上传遥测数据示例 ===")

    try:
        device_id = device.id
        print(f"为设备上传遥测数据: {device.name}")

        # 准备遥测数据
        current_time = int(time.time() * 1000)  # 毫秒时间戳

        telemetry_data = {
            "temperature": round(random.uniform(20.0, 35.0), 2),  # 温度
            "humidity": round(random.uniform(40.0, 80.0), 2),  # 湿度
            "pressure": round(random.uniform(1000.0, 1020.0), 2),  # 气压
            "battery": random.randint(60, 100),  # 电池电量
            "signal_strength": random.randint(-80, -30),  # 信号强度
            "status": "online"  # 状态
        }

        print(f"遥测数据: {json.dumps(telemetry_data, indent=2)}")
        print(f"时间戳: {current_time} ({datetime.fromtimestamp(current_time / 1000)})")

        # 上传遥测数据
        success = client.telemetry_service.post_telemetry(
            device_id=device_id,
            telemetry_data=telemetry_data,
            timestamp=current_time
        )

        if success:
            print("✅ 遥测数据上传成功！")
        else:
            print("❌ 遥测数据上传失败！")

        # 等待数据处理
        time.sleep(2)

    except ValidationError as e:
        print(f"❌ 验证错误: {e}")
        print(f"字段: {e.details.get('field')}")
    except Exception as e:
        print(f"❌ 上传遥测数据时发生错误: {e}")


def example_upload_telemetry_with_token(client: ThingsBoardClient, device: Device):
    """使用设备令牌上传遥测数据示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 使用设备令牌上传遥测数据示例 ===")

    try:
        device_id = device.id
        print(f"获取设备令牌: {device.name}")

        # 获取设备凭证
        credentials = client.device_service.get_device_credentials(device_id)

        if not credentials or not credentials.credentials_value:
            print("❌ 无法获取设备令牌")
            return

        device_token = credentials.credentials_value
        print(f"设备令牌: {device_token[:20]}...")

        # 准备遥测数据
        telemetry_data = {
            "cpu_usage": round(random.uniform(10.0, 90.0), 2),  # CPU 使用率
            "memory_usage": round(random.uniform(30.0, 80.0), 2),  # 内存使用率
            "disk_usage": round(random.uniform(20.0, 70.0), 2),  # 磁盘使用率
            "network_in": random.randint(1000, 10000),  # 网络入流量
            "network_out": random.randint(500, 5000),  # 网络出流量
            "uptime": random.randint(3600, 86400)  # 运行时间
        }

        print(f"遥测数据: {json.dumps(telemetry_data, indent=2)}")

        # 使用设备令牌上传遥测数据
        success = client.telemetry_service.post_telemetry_with_device_token(
            device_token=device_token,
            telemetry_data=telemetry_data
        )

        if success:
            print("✅ 使用设备令牌上传遥测数据成功！")
        else:
            print("❌ 使用设备令牌上传遥测数据失败！")

        # 等待数据处理
        time.sleep(2)

    except Exception as e:
        print(f"❌ 使用设备令牌上传遥测数据时发生错误: {e}")


def example_get_latest_telemetry(client: ThingsBoardClient, device: Device):
    """获取最新遥测数据示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 获取最新遥测数据示例 ===")

    try:
        device_id = device.id
        print(f"获取设备最新遥测数据: {device.name}")

        # 获取所有最新遥测数据
        latest_data = client.telemetry_service.get_latest_telemetry(device_id)

        if latest_data:
            print("✅ 获取最新遥测数据成功！")
            print("最新遥测数据:")

            for key, value in latest_data.items():
                if isinstance(value, dict) and 'value' in value and 'ts' in value:
                    timestamp = datetime.fromtimestamp(value['ts'] / 1000)
                    print(f"  {key}: {value['value']} (时间: {timestamp})")
                else:
                    print(f"  {key}: {value}")
        else:
            print("❌ 未找到最新遥测数据！")

        # 获取特定键的最新遥测数据
        print("\n获取特定键的最新遥测数据...")
        specific_keys = ["temperature", "humidity", "pressure"]

        specific_data = client.telemetry_service.get_latest_telemetry(
            device_id, keys=specific_keys
        )

        if specific_data:
            print("✅ 获取特定键遥测数据成功！")
            for key in specific_keys:
                if key in specific_data:
                    value = specific_data[key]
                    if isinstance(value, dict) and 'value' in value:
                        print(f"  {key}: {value['value']}")
                    else:
                        print(f"  {key}: {value}")
                else:
                    print(f"  {key}: 无数据")
        else:
            print("❌ 未找到特定键遥测数据！")

    except NotFoundError as e:
        print(f"❌ 设备不存在: {e}")
    except Exception as e:
        print(f"❌ 获取最新遥测数据时发生错误: {e}")


def example_get_timeseries_data(client: ThingsBoardClient, device: Device):
    """获取时间序列数据示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 获取时间序列数据示例 ===")

    try:
        device_id = device.id
        print(f"获取设备时间序列数据: {device.name}")

        # 设置时间范围
        end_time = int(time.time() * 1000)  # 当前时间
        start_time = end_time - (24 * 60 * 60 * 1000)  # 24小时前

        print(
            f"时间范围: {datetime.fromtimestamp(start_time / 1000)} 到")

        # 获取时间序列数据
        keys = ["temperature", "humidity", "pressure"]

        timeseries_data = client.telemetry_service.get_timeseries_telemetry(
            device_id=device_id,
            keys=keys,
            start_ts=start_time,
            end_ts=end_time,
            limit=100
        )

        if timeseries_data:
            print("✅ 获取时间序列数据成功！")

            for key, data_points in timeseries_data.items():
                print(f"\n{key} 数据点 ({len(data_points)} 个):")

                # 显示前5个数据点
                for i, point in enumerate(data_points[:5]):
                    if isinstance(point, dict) and 'value' in point and 'ts' in point:
                        timestamp = datetime.fromtimestamp(point['ts'] / 1000)
                        print(f"  {i + 1}. 值: {point['value']}, 时间: {timestamp}")
                    else:
                        print(f"  {i + 1}. {point}")

                if len(data_points) > 5:
                    print(
                        f"  ... 还有 {len(data_points) - 5} 个数据点")
        else:
            print("❌ 未找到时间序列数据！")

        # 获取聚合数据
        print("\n获取聚合数据...")

        aggregated_data = client.telemetry_service.get_timeseries_telemetry(
            device_id=device_id,
            keys=["temperature"],
            start_ts=start_time,
            end_ts=end_time,
            interval=3600000,  # 1小时间隔
            agg="AVG"  # 平均值聚合
        )

        if aggregated_data and "temperature" in aggregated_data:
            temp_data = aggregated_data["temperature"]
            print(
                f"✅ 获取温度聚合数据成功 ({len(temp_data)} 个点)")

            for i, point in enumerate(temp_data[:3]):
                if isinstance(point, dict) and 'value' in point and 'ts' in point:
                    timestamp = datetime.fromtimestamp(point['ts'] / 1000)
                    print(f"  {i + 1}. 平均温度: {point['value']}°C, 时间: {timestamp}")
        else:
            print("❌ 未找到聚合数据！")

    except Exception as e:
        print(f"❌ 获取时间序列数据时发生错误: {e}")


def example_get_telemetry_keys(client: ThingsBoardClient, device: Device):
    """获取遥测数据键示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 获取遥测数据键示例 ===")

    try:
        device_id = device.id
        print(f"获取设备遥测数据键: {device.name}")

        # 获取遥测数据键
        keys = client.telemetry_service.get_telemetry_keys(device_id)

        if keys:
            print(f"✅ 获取遥测数据键成功！ ({len(keys)} 个键)")
            print("遥测数据键列表:")

            for i, key in enumerate(keys, 1):
                print(f"  {i}. {key}")
        else:
            print("❌ 未找到遥测数据键！")

    except Exception as e:
        print(f"❌ 获取遥测数据键时发生错误: {e}")


def example_batch_upload_telemetry(client: ThingsBoardClient, device: Device):
    """批量上传遥测数据示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 批量上传遥测数据示例 ===")

    try:
        device_id = device.id
        print(f"批量上传遥测数据: {device.name}")

        # 生成历史数据
        current_time = int(time.time() * 1000)
        batch_data = []

        print("生成历史遥测数据...")

        for i in range(10):  # 生成10个数据点
            timestamp = current_time - (i * 60 * 1000)  # 每分钟一个数据点

            data_point = {
                "timestamp": timestamp,
                "data": {
                    "temperature": round(20 + random.uniform(-5, 15), 2),
                    "humidity": round(50 + random.uniform(-20, 30), 2),
                    "pressure": round(1013 + random.uniform(-10, 10), 2),
                    "wind_speed": round(random.uniform(0, 20), 2),
                    "wind_direction": random.randint(0, 360)
                }
            }

            batch_data.append(data_point)

        print(f"准备上传 {len(batch_data)} 个数据点")

        # 批量上传数据
        success_count = 0

        for i, data_point in enumerate(batch_data):
            try:
                success = client.telemetry_service.post_telemetry(
                    device_id=device_id,
                    telemetry_data=data_point["data"],
                    timestamp=data_point["timestamp"]
                )

                if success:
                    success_count += 1
                    timestamp_str = datetime.fromtimestamp(data_point["timestamp"] / 1000)
                    print(f"  ✅ 数据点 {i + 1} 上传成功 ({timestamp_str})")
                else:
                    print(f"  ❌ 数据点 {i + 1} 上传失败")

                # 短暂延迟避免过快请求
                time.sleep(0.1)

            except Exception as e:
                print(f"  ❌ 数据点 {i + 1} 上传错误: {e}")

        print(f"\n批量上传完成: {success_count}/{len(batch_data)} 成功")

        # 等待数据处理
        time.sleep(3)

    except Exception as e:
        print(f"❌ 批量上传遥测数据时发生错误: {e}")


def example_delete_telemetry(client: ThingsBoardClient, device: Device):
    """删除遥测数据示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 删除遥测数据示例 ===")

    try:
        device_id = device.id
        print(f"删除设备遥测数据: {device.name}")

        # 获取要删除的键
        keys_to_delete = ["wind_speed", "wind_direction"]

        print(f"准备删除的键: {keys_to_delete}")

        # 删除特定键的遥测数据
        success = client.telemetry_service.delete_telemetry(
            device_id=device_id,
            keys=keys_to_delete
        )

        if success:
            print("✅ 遥测数据删除成功！")

            # 验证删除
            time.sleep(2)
            remaining_keys = client.telemetry_service.get_telemetry_keys(device_id)

            if remaining_keys:
                print(f"剩余的遥测数据键: {remaining_keys}")

                # 检查删除的键是否还存在
                deleted_keys_found = [key for key in keys_to_delete if key in remaining_keys]

                if not deleted_keys_found:
                    print("✅ 删除验证成功，指定的键已被删除")
                else:
                    print(
                        f"⚠️ 删除验证失败，以下键仍然存在: {deleted_keys_found}")
            else:
                print("所有遥测数据键都已被删除")
        else:
            print("❌ 遥测数据删除失败！")

    except Exception as e:
        print(f"❌ 删除遥测数据时发生错误: {e}")


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
        print(f"❌ 清理演示设备时发生错误: {e}")


def main():
    """主函数"""
    print("ThingsBoardLink 遥测数据示例")
    print("=" * 40)

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
                # 1. 上传遥测数据
                example_upload_telemetry(client, demo_device)

                # 2. 使用设备令牌上传遥测数据
                example_upload_telemetry_with_token(client, demo_device)

                # 3. 批量上传遥测数据
                example_batch_upload_telemetry(client, demo_device)

                # 4. 获取遥测数据键
                example_get_telemetry_keys(client, demo_device)

                # 5. 获取最新遥测数据
                example_get_latest_telemetry(client, demo_device)

                # 6. 获取时间序列数据
                example_get_timeseries_data(client, demo_device)

                # 7. 删除遥测数据
                example_delete_telemetry(client, demo_device)

                # 清理演示设备
                cleanup_demo_device(client, demo_device)

            print("\n" + "=" * 40)
            print("✅ 所有遥测数据示例运行完成！")

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
