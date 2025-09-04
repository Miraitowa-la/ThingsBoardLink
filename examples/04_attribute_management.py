"""
ThingsBoardLink 属性管理示例

本示例演示如何使用 ThingsBoardLink 进行属性管理操作。
包括客户端属性、服务端属性和共享属性的读取、设置、删除等功能。

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
from typing import Optional

from src.thingsboardlink import (
    ThingsBoardClient,
    Device,
    AttributeScope,
    ValidationError
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
        device_name = f"attribute_demo_device_{uuid.uuid4().hex[:8]}"
        device = client.device_service.create_device(
            name=device_name,
            device_type="sensor",
            label="属性管理演示设备"
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


def example_client_attributes(client: ThingsBoardClient, device: Device):
    """客户端属性示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 客户端属性示例 ===")

    try:
        device_id = device.id
        print(f"管理设备客户端属性: {device.name}")

        # 设置客户端属性
        print("\n1. 设置客户端属性...")

        # 凭证信息展示完成
        print("\n💡 设置客户端属性说明:")
        print("   - ThingsBoard的服务端REST API不支持直接设置客户端属性（CLIENT_SCOPE）")
        print("   - 客户端属性只能通过设备API使用设备访问令牌来设置")
        print("   - 后续客涉及到户端属性的内容都是空白的是正常的，")
        print("   - 假装我在设置客户端属性..\n")

        print("✅ 客户端属性设置成功！")

        # 等待属性处理
        time.sleep(2)

        # 获取客户端属性
        print("\n2. 获取客户端属性...")

        retrieved_attributes = client.attribute_service.get_client_attributes(device_id)

        if retrieved_attributes:
            print("✅ 获取客户端属性成功！")
            print("客户端属性:")

            for key, value in retrieved_attributes.items():
                if isinstance(value, dict):
                    print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")
                else:
                    print(f"  {key}: {value}")
        else:
            print("❌ 未找到客户端属性！")

        # 获取特定键的客户端属性
        print("\n3. 获取特定键的客户端属性...")

        specific_keys = ["firmware_version", "hardware_version", "location"]
        specific_attributes = client.attribute_service.get_client_attributes(
            device_id, keys=specific_keys
        )

        if specific_attributes:
            print("✅ 获取特定键客户端属性成功！")
            for key in specific_keys:
                if key in specific_attributes:
                    value = specific_attributes[key]
                    if isinstance(value, dict):
                        print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")
                    else:
                        print(f"  {key}: {value}")
                else:
                    print(f"  {key}: 无数据")
        else:
            print("❌ 未找到特定键客户端属性！")

    except ValidationError as e:
        print(f"❌ 验证错误: {e}")
        print(f"字段: {e.details.get('field')}")
    except Exception as e:
        print(f"❌ 管理客户端属性时发生错误: {e}")


def example_server_attributes(client: ThingsBoardClient, device: Device):
    """服务端属性示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 服务端属性示例 ===")

    try:
        device_id = device.id
        print(f"管理设备服务端属性: {device.name}")

        # 设置服务端属性
        print("\n1. 设置服务端属性...")

        server_attributes = {
            "device_status": "active",
            "last_maintenance": datetime.now().isoformat(),
            "maintenance_interval": 30,  # 天
            "warranty_expiry": "2025-12-31",
            "support_contact": "support@example.com",
            "device_group": "传感器组A",
            "priority_level": "high",
            "monitoring_enabled": True,
            "alert_thresholds": {
                "temperature": {
                    "min": -10,
                    "max": 50
                },
                "humidity": {
                    "min": 20,
                    "max": 90
                }
            },
            "data_retention_days": 365
        }

        print(f"服务端属性数据: {json.dumps(server_attributes, indent=2, ensure_ascii=False)}")

        success = client.attribute_service.set_server_attributes(
            device_id=device_id,
            attributes=server_attributes
        )

        if success:
            print("✅ 服务端属性设置成功！")
        else:
            print("❌ 服务端属性设置失败！")

        # 等待属性处理
        time.sleep(2)

        # 获取服务端属性
        print("\n2. 获取服务端属性...")

        retrieved_attributes = client.attribute_service.get_server_attributes(device_id)

        if retrieved_attributes:
            print("✅ 获取服务端属性成功！")
            print("服务端属性:")

            for key, value in retrieved_attributes.items():
                if isinstance(value, dict):
                    print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")
                else:
                    print(f"  {key}: {value}")
        else:
            print("❌ 未找到服务端属性！")

        # 更新单个服务端属性
        print("\n3. 更新单个服务端属性...")

        update_success = client.attribute_service.update_attribute(
            device_id=device_id,
            scope=AttributeScope.SERVER_SCOPE,
            key="device_status",
            value="maintenance"
        )

        if update_success:
            print("✅ 服务端属性更新成功！")

            # 验证更新
            updated_attributes = client.attribute_service.get_server_attributes(
                device_id, keys=["device_status"]
            )

            if updated_attributes and "device_status" in updated_attributes:
                print(f"更新后的状态: {updated_attributes['device_status']}")
            else:
                print("⚠️ 无法验证属性更新")
        else:
            print("❌ 服务端属性更新失败！")

    except Exception as e:
        print(f"❌ 管理服务端属性时发生错误: {e}")


def example_shared_attributes(client: ThingsBoardClient, device: Device):
    """共享属性示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 共享属性示例 ===")

    try:
        device_id = device.id
        print(f"管理设备共享属性: {device.name}")

        # 设置共享属性
        print("\n1. 设置共享属性...")

        shared_attributes = {
            "target_temperature": 25.0,
            "target_humidity": 60.0,
            "operating_mode": "auto",
            "reporting_interval": 300,  # 秒
            "power_saving_enabled": False,
            "calibration_offset": {
                "temperature": 0.5,
                "humidity": -2.0
            },
            "display_settings": {
                "brightness": 80,
                "language": "zh-CN",
                "units": "metric"
            },
            "network_config": {
                "wifi_ssid": "IoT_Network",
                "mqtt_broker": "mqtt.example.com",
                "update_server": "update.example.com"
            }
        }

        print(f"共享属性数据: {json.dumps(shared_attributes, indent=2, ensure_ascii=False)}")

        success = client.attribute_service.set_shared_attributes(
            device_id=device_id,
            attributes=shared_attributes
        )

        if success:
            print("✅ 共享属性设置成功！")
        else:
            print("❌ 共享属性设置失败！")

        # 等待属性处理
        time.sleep(2)

        # 获取共享属性
        print("\n2. 获取共享属性...")

        retrieved_attributes = client.attribute_service.get_shared_attributes(device_id)

        if retrieved_attributes:
            print("✅ 获取共享属性成功！")
            print("共享属性:")

            for key, value in retrieved_attributes.items():
                if isinstance(value, dict):
                    print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")
                else:
                    print(f"  {key}: {value}")
        else:
            print("❌ 未找到共享属性！")

        # 更新共享属性
        print("\n3. 更新共享属性...")

        updated_shared_attributes = {
            "target_temperature": 23.0,
            "operating_mode": "manual",
            "power_saving_enabled": True
        }

        update_success = client.attribute_service.set_shared_attributes(
            device_id=device_id,
            attributes=updated_shared_attributes
        )

        if update_success:
            print("✅ 共享属性更新成功！")

            # 验证更新
            time.sleep(1)
            updated_attributes = client.attribute_service.get_shared_attributes(
                device_id, keys=list(updated_shared_attributes.keys())
            )

            if updated_attributes:
                print("更新后的共享属性:")
                for key, value in updated_attributes.items():
                    print(f"  {key}: {value}")
            else:
                print("⚠️ 无法验证属性更新")
        else:
            print("❌ 共享属性更新失败！")

    except Exception as e:
        print(f"❌ 管理共享属性时发生错误: {e}")


def example_get_all_attributes(client: ThingsBoardClient, device: Device):
    """获取所有属性示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 获取所有属性示例 ===")

    try:
        device_id = device.id
        print(f"获取设备所有属性: {device.name}")

        # 获取所有属性
        all_attributes = client.attribute_service.get_all_attributes(device_id)

        if all_attributes:
            print("✅ 获取所有属性成功！")

            # 按作用域分组显示
            for scope, attributes in all_attributes.items():
                if attributes:
                    scope_name = {
                        "CLIENT_SCOPE": "客户端属性",
                        "SERVER_SCOPE": "服务端属性",
                        "SHARED_SCOPE": "共享属性"
                    }.get(scope, scope)

                    print(f"\n{scope_name} ({len(attributes)} 个):")

                    for key, value in attributes.items():
                        if isinstance(value, dict):
                            print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")
                        else:
                            print(f"  {key}: {value}")
                else:
                    print(f"\n{scope}: 无属性")
        else:
            print("❌ 未找到任何属性！")

    except Exception as e:
        print(f"❌ 获取所有属性时发生错误: {e}")


def example_get_attribute_keys(client: ThingsBoardClient, device: Device):
    """获取属性键示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 获取属性键示例 ===")

    try:
        device_id = device.id
        print(f"获取设备属性键: {device.name}")

        # 获取不同作用域的属性键
        scopes = [
            (AttributeScope.CLIENT_SCOPE, "客户端"),
            (AttributeScope.SERVER_SCOPE, "服务端"),
            (AttributeScope.SHARED_SCOPE, "共享")
        ]

        for scope, scope_name in scopes:
            print(f"\n{scope_name}属性键:")

            keys = client.attribute_service.get_attribute_keys(device_id, scope)

            if keys:
                print(f"  找到 {len(keys)} 个键:")
                for i, key in enumerate(keys, 1):
                    print(f"    {i}. {key}")
            else:
                print(f"  未找到{scope_name}属性键")

    except Exception as e:
        print(f"❌ 获取属性键时发生错误: {e}")


def example_attribute_exists(client: ThingsBoardClient, device: Device):
    """检查属性是否存在示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 检查属性是否存在示例 ===")

    try:
        device_id = device.id
        print(f"检查设备属性是否存在: {device.name}")

        # 检查不同属性是否存在
        test_cases = [
            (AttributeScope.CLIENT_SCOPE, "firmware_version", "客户端"),
            (AttributeScope.SERVER_SCOPE, "device_status", "服务端"),
            (AttributeScope.SHARED_SCOPE, "target_temperature", "共享")
        ]

        for scope, key, scope_name in test_cases:
            exists = client.attribute_service.attribute_exists(
                device_id=device_id,
                scope=scope,
                key=key
            )

            status = "✅ 存在" if exists else "❌ 不存在"
            print(f"  {scope_name}属性 '{key}': {status}")

    except Exception as e:
        print(f"❌ 检查属性存在性时发生错误: {e}")


def example_delete_attributes(client: ThingsBoardClient, device: Device):
    """删除属性示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 删除属性示例 ===")

    try:
        device_id = device.id
        print(f"删除设备属性: {device.name}")

        # 删除特定的客户端属性
        print("\n1. 删除客户端属性...")

        client_keys_to_delete = ["serial_number", "installation_date"]

        success = client.attribute_service.delete_attributes(
            device_id=device_id,
            scope=AttributeScope.CLIENT_SCOPE,
            keys=client_keys_to_delete
        )

        if success:
            print(f"✅ 客户端属性删除成功: {client_keys_to_delete}")
        else:
            print(f"❌ 客户端属性删除失败: {client_keys_to_delete}")

        # 删除特定的服务端属性
        print("\n2. 删除服务端属性...")

        server_keys_to_delete = ["support_contact", "data_retention_days"]

        success = client.attribute_service.delete_attributes(
            device_id=device_id,
            scope=AttributeScope.SERVER_SCOPE,
            keys=server_keys_to_delete
        )

        if success:
            print(f"✅ 服务端属性删除成功: {server_keys_to_delete}")
        else:
            print(f"❌ 服务端属性删除失败: {server_keys_to_delete}")

        # 删除特定的共享属性
        print("\n3. 删除共享属性...")

        shared_keys_to_delete = ["network_config", "display_settings"]

        success = client.attribute_service.delete_attributes(
            device_id=device_id,
            scope=AttributeScope.SHARED_SCOPE,
            keys=shared_keys_to_delete
        )

        if success:
            print(f"✅ 共享属性删除成功: {shared_keys_to_delete}")
        else:
            print(f"❌ 共享属性删除失败: {shared_keys_to_delete}")

        # 验证删除
        time.sleep(2)
        print("\n4. 验证属性删除...")

        all_keys_to_check = client_keys_to_delete + server_keys_to_delete + shared_keys_to_delete
        remaining_attributes = client.attribute_service.get_all_attributes(device_id)

        if remaining_attributes:
            all_remaining_keys = []
            for scope_attrs in remaining_attributes.values():
                if scope_attrs:
                    all_remaining_keys.extend(scope_attrs.keys())

            deleted_keys_found = [key for key in all_keys_to_check if key in all_remaining_keys]

            if not deleted_keys_found:
                print("✅ 删除验证成功，指定的属性已被删除")
            else:
                print(f"⚠️ 删除验证失败，以下属性仍然存在: {deleted_keys_found}")
        else:
            print("所有属性都已被删除")

    except Exception as e:
        print(f"❌ 删除属性时发生错误: {e}")


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
    print("ThingsBoardLink 属性管理示例")
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
                # 1. 客户端属性管理
                example_client_attributes(client, demo_device)

                # 2. 服务端属性管理
                example_server_attributes(client, demo_device)

                # 3. 共享属性管理
                example_shared_attributes(client, demo_device)

                # 4. 获取所有属性
                example_get_all_attributes(client, demo_device)

                # 5. 获取属性键
                example_get_attribute_keys(client, demo_device)

                # 6. 检查属性是否存在
                example_attribute_exists(client, demo_device)

                # 7. 删除属性
                example_delete_attributes(client, demo_device)

                # 清理演示设备
                cleanup_demo_device(client, demo_device)

            print("\n" + "=" * 40)
            print("✅ 所有属性管理示例运行完成！")

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
