"""
ThingsBoardLink 警报管理示例

本示例演示如何使用 ThingsBoardLink 进行警报管理操作。
包括警报的创建、查询、确认、清除、删除等功能。

运行前请设置环境变量
export THINGSBOARD_URL="http://localhost:8080"
export THINGSBOARD_USERNAME="tenant@thingsboard.org"
export THINGSBOARD_PASSWORD="tenant"
"""

import os
import time
import uuid
import json
from datetime import datetime
from typing import Optional, List

from src.thingsboardlink import (
    ThingsBoardClient,
    Device,
    Alarm,
    AlarmSeverity,
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
        device_name = f"alarm_demo_device_{uuid.uuid4().hex[:8]}"
        device = client.device_service.create_device(
            name=device_name,
            device_type="sensor",
            label="警报管理演示设备"
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


def example_create_alarms(client: ThingsBoardClient, device: Device) -> List[Alarm]:
    """创建警报示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象

    Returns:
        List[Alarm]: 创建的警报列表
    """
    print("\n=== 创建警报示例 ===")

    created_alarms = []

    try:
        device_id = device.id
        print(f"为设备创建警报: {device.name}")

        # 定义不同类型的警报
        alarm_configs = [
            {
                "type": "High Temperature",
                "severity": AlarmSeverity.CRITICAL,
                "message": "设备温度过高，当前温度: 45.2°C",
                "details": {
                    "message": "设备温度过高，当前温度: 45.2°C",
                    "threshold": 40.0,
                    "current_value": 45.2,
                    "sensor": "temperature_sensor_1",
                    "location": "机房A区"
                }
            },
            {
                "type": "Low Battery",
                "severity": AlarmSeverity.WARNING,
                "message": "设备电池电量低，当前电量: 15%",
                "details": {
                    "message": "设备电池电量低，当前电量: 15%",
                    "threshold": 20,
                    "current_value": 15,
                    "battery_type": "Li-ion",
                    "estimated_remaining_time": "2 hours"
                }
            },
            {
                "type": "Communication Error",
                "severity": AlarmSeverity.MAJOR,
                "message": "设备通信异常，连接超时",
                "details": {
                    "message": "设备通信异常，连接超时",
                    "error_code": "CONN_TIMEOUT",
                    "last_successful_communication": datetime.now().isoformat(),
                    "retry_count": 3,
                    "network_status": "unstable"
                }
            },
            {
                "type": "Sensor Malfunction",
                "severity": AlarmSeverity.MINOR,
                "message": "传感器读数异常",
                "details": {
                    "message": "传感器读数异常",
                    "sensor_id": "humidity_sensor_2",
                    "expected_range": "20-80%",
                    "current_reading": "105%",
                    "calibration_date": "2024-01-15"
                }
            },
            {
                "type": "Maintenance Required",
                "severity": AlarmSeverity.INDETERMINATE,
                "message": "设备需要定期维护",
                "details": {
                    "message": "设备需要定期维护",
                    "maintenance_type": "routine_check",
                    "last_maintenance": "2024-01-01",
                    "next_due_date": "2024-02-01",
                    "maintenance_items": ["清洁传感器", "检查连接"]
                }
            }
        ]

        # 创建警报
        for i, config in enumerate(alarm_configs, 1):
            try:
                print(f"\n{i}. 创建警报: {config['type']}")
                print(f"   严重程度: {config['severity'].value}")
                print(f"   消息: {config['message']}")

                alarm = client.alarm_service.create_alarm(
                    originator_id=device_id,
                    alarm_type=config["type"],
                    severity=config["severity"],
                    details=config["details"]
                )

                if alarm:
                    created_alarms.append(alarm)
                    print(f"   ✅ 警报创建成功: {alarm.id}")
                    print(f"   状态: {alarm.status.value}")
                    print(f"   创建时间: {datetime.fromtimestamp(alarm.start_ts / 1000)}")
                else:
                    print(f"   ❌ 警报创建失败: {config['type']}")

                # 短暂延迟
                time.sleep(0.5)

            except ValidationError as e:
                print(f"   ❌ 验证错误: {e}")
                print(f"   字段: {e.details.get('field')}")
            except Exception as e:
                print(f"   ❌ 创建警报时发生错误: {e}")

        print(f"\n成功创建 {len(created_alarms)} 个警报")
        return created_alarms

    except Exception as e:
        print(f"❌ 创建警报时发生错误: {e}")
        return created_alarms


def example_get_alarm_by_id(client: ThingsBoardClient, alarm: Alarm):
    """根据 ID 获取警报示例

    Args:
        client: ThingsBoard 客户端
        alarm: 警报对象
    """
    print("\n=== 根据 ID 获取警报示例 ===")

    try:
        alarm_id = alarm.id
        print(f"查询警报 ID: {alarm_id}")

        # 根据 ID 获取警报
        retrieved_alarm = client.alarm_service.get_alarm(alarm_id)

        if retrieved_alarm:
            print("✅ 警报查询成功！")
            print(f"警报类型: {retrieved_alarm.type}")
            print(f"严重程度: {retrieved_alarm.severity.value}")
            print(f"状态: {retrieved_alarm.status.value}")
            print(f"消息: {retrieved_alarm.details.get('message', 'N/A')}")
            print(f"发起者: {retrieved_alarm.originator.id}")

            if retrieved_alarm.details:
                print(f"详细信息: {json.dumps(retrieved_alarm.details, indent=2, ensure_ascii=False)}")

            # 时间信息
            if retrieved_alarm.start_ts:
                start_time = datetime.fromtimestamp(retrieved_alarm.start_ts / 1000)
                print(f"开始时间: {start_time}")

            if retrieved_alarm.end_ts:
                end_time = datetime.fromtimestamp(retrieved_alarm.end_ts / 1000)
                print(f"结束时间: {end_time}")

            if retrieved_alarm.ack_ts:
                ack_time = datetime.fromtimestamp(retrieved_alarm.ack_ts / 1000)
                print(f"确认时间: {ack_time}")

            if retrieved_alarm.clear_ts:
                clear_time = datetime.fromtimestamp(retrieved_alarm.clear_ts / 1000)
                print(f"清除时间: {clear_time}")
        else:
            print("❌ 警报未找到！")

    except NotFoundError as e:
        print(f"❌ 警报不存在: {e}")
    except Exception as e:
        print(f"❌ 查询警报时发生错误: {e}")


def example_get_alarms(client: ThingsBoardClient, device: Device):
    """获取警报列表示例

    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 获取警报列表示例 ===")

    try:
        device_id = device.id
        print(f"获取设备警报列表: {device.name}")

        # 获取设备的所有警报
        page_data = client.alarm_service.get_alarms(
            originator_id=device_id,
            page_size=20,
            page=0,
            sort_property="createdTime",
            sort_order="DESC"
        )

        if page_data and page_data.data:
            print(f"✅ 获取到 {len(page_data.data)} 个警报 {len(page_data.data)} alarms")
            print(f"总警报数: {page_data.total_elements}")
            print(f"总页数: {page_data.total_pages}")

            print("\n警报列表:")
            for i, alarm in enumerate(page_data.data, 1):
                start_time = datetime.fromtimestamp(alarm.start_ts / 1000) if alarm.start_ts else "N/A"
                print(f"  {i}. {alarm.type} - {alarm.severity.value} - {alarm.status.value}")
                print(f"     ID: {alarm.id}")
                print(f"     消息: {alarm.details.get('message', 'N/A')}")
                print(f"     开始时间: {start_time}")
                print()
        else:
            print("❌ 未找到警报！")

    except Exception as e:
        print(f"❌ 获取警报列表时发生错误: {e}")


def example_acknowledge_alarm(client: ThingsBoardClient, alarm: Alarm) -> bool:
    """确认警报示例

    Args:
        client: ThingsBoard 客户端
        alarm: 要确认的警报

    Returns:
        bool: 确认是否成功
    """
    print("\n=== 确认警报示例 ===")

    try:
        alarm_id = alarm.id
        print(f"确认警报: {alarm.type} (ID: {alarm_id})")
        print(f"当前状态: {alarm.status.value}")

        # 确认警报
        success = client.alarm_service.ack_alarm(alarm_id)

        if success:
            print("✅ 警报确认成功！")

            # 验证确认
            time.sleep(1)
            updated_alarm = client.alarm_service.get_alarm(alarm_id)

            if updated_alarm:
                print(f"更新后状态: {updated_alarm.status.value}")
                if updated_alarm.ack_ts:
                    ack_time = datetime.fromtimestamp(updated_alarm.ack_ts / 1000)
                    print(f"确认时间: {ack_time}")

            return True
        else:
            print("❌ 警报确认失败！")
            return False

    except Exception as e:
        print(f"❌ 确认警报时发生错误: {e}")
        return False


def example_clear_alarm(client: ThingsBoardClient, alarm: Alarm) -> bool:
    """清除警报示例

    Args:
        client: ThingsBoard 客户端
        alarm: 要清除的警报

    Returns:
        bool: 清除是否成功
    """
    print("\n=== 清除警报示例 ===")

    try:
        alarm_id = alarm.id
        print(f"清除警报: {alarm.type} (ID: {alarm_id})")
        print(f"当前状态: {alarm.status.value}")

        # 清除警报
        success = client.alarm_service.clear_alarm(alarm_id)

        if success:
            print("✅ 警报清除成功！")

            # 验证清除
            time.sleep(1)
            updated_alarm = client.alarm_service.get_alarm(alarm_id)

            if updated_alarm:
                print(f"更新后状态: {updated_alarm.status.value}")
                if updated_alarm.clear_ts:
                    clear_time = datetime.fromtimestamp(updated_alarm.clear_ts / 1000)
                    print(f"清除时间: {clear_time}")
                if updated_alarm.end_ts:
                    end_time = datetime.fromtimestamp(updated_alarm.end_ts / 1000)
                    print(f"结束时间: {end_time}")

            return True
        else:
            print("❌ 警报清除失败！")
            return False

    except Exception as e:
        print(f"❌ 清除警报时发生错误: {e}")
        return False


def example_delete_alarm(client: ThingsBoardClient, alarm: Alarm) -> bool:
    """删除警报示例

    Args:
        client: ThingsBoard 客户端
        alarm: 要删除的警报

    Returns:
        bool: 删除是否成功
    """
    print("\n=== 删除警报示例 ===")

    try:
        alarm_id = alarm.id
        alarm_type = alarm.type

        print(f"删除警报: {alarm_type} (ID: {alarm_id})")
        print(f"当前状态: {alarm.status.value}")

        # 确认删除
        print("⚠️ 即将删除警报，这个操作不可逆！")

        # 执行删除
        success = client.alarm_service.delete_alarm(alarm_id)

        if success:
            print("✅ 警报删除成功！")

            # 验证删除
            time.sleep(1)
            try:
                deleted_alarm = client.alarm_service.get_alarm(alarm_id)
                if deleted_alarm:
                    print("⚠️ 删除验证失败，警报可能仍然存在")
                else:
                    print("✅ 删除验证成功，警报已不存在")
            except NotFoundError:
                print("✅ 删除验证成功，警报已不存在")

            return True
        else:
            print("❌ 警报删除失败！")
            return False

    except NotFoundError as e:
        print(f"⚠️ 警报已不存在: {e}")
        return True  # 警报已不存在，可以认为删除成功
    except Exception as e:
        print(f"❌ 删除警报时发生错误: {e}")
        return False


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
    print("ThingsBoardLink 警报管理示例")
    print("=" * 80)

    config = get_config_from_env()
    demo_device = None
    created_alarms = []

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
                # 1. 创建警报
                created_alarms = example_create_alarms(client, demo_device)

                if created_alarms:
                    # 2. 根据 ID 获取警报
                    example_get_alarm_by_id(client, created_alarms[0])

                    # 3. 获取警报列表
                    example_get_alarms(client, demo_device)

                    # 5. 确认警报
                    if len(created_alarms) > 1:
                        example_acknowledge_alarm(client, created_alarms[1])

                    # 6. 清除警报
                    if len(created_alarms) > 2:
                        example_clear_alarm(client, created_alarms[2])

                    # 10. 删除部分警报
                    if len(created_alarms) > 3:
                        example_delete_alarm(client, created_alarms[3])

                # 清理演示设备（这会自动删除相关的警报）
                cleanup_demo_device(client, demo_device)

            print("\n" + "=" * 80)
            print("✅ 所有警报管理示例运行完成！")

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
