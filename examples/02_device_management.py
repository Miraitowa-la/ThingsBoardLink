"""
ThingsBoardLink 设备管理示例

本示例演示如何使用 ThingsBoardLink 进行设备管理操作。
包括设备的创建、查询、更新、删除以及设备凭证管理等功能。

运行前请设置环境变量 | Please set environment variables before running:
export THINGSBOARD_URL="http://localhost:8080"
export THINGSBOARD_USERNAME="tenant@thingsboard.org"
export THINGSBOARD_PASSWORD="tenant"
"""

import os
import time
import uuid
from typing import Optional, List


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


def example_create_device(client: ThingsBoardClient) -> Optional[Device]:
    """
    创建设备示例
    
    Args:
        client: ThingsBoard 客户端
        
    Returns:
        Device: 创建的设备对象
    """
    print("\n=== 创建设备示例 ===")

    try:
        # 生成唯一的设备名称
        device_name = f"demo_device_{uuid.uuid4().hex[:8]}"
        device_type = "sensor"
        device_label = "演示传感器设备"

        print(f"创建设备: {device_name}")
        print(f"设备类型: {device_type}")
        print(f"设备标签: {device_label}")

        # 创建设备
        device = client.device_service.create_device(
            name=device_name,
            device_type=device_type,
            label=device_label
        )

        if device:
            print("✅ 设备创建成功！")
            print(f"设备 ID: {device.id}")
            print(f"设备名称: {device.name}")
            print(f"设备类型: {device.type}")
            print(f"设备标签: {device.label}")
            print(f"创建时间: {device.created_time}")
            return device
        else:
            print("❌ 设备创建失败！")
            return None

    except ValidationError as e:
        print(f"❌ 验证错误: {e}")
        print(f"字段: {e.details.get('field')}")
        return None
    except Exception as e:
        print(f"❌ 创建设备时发生错误: {e}")
        return None


def example_get_device_by_id(client: ThingsBoardClient, device_id: str) -> Optional[Device]:
    """
    根据 ID 获取设备示例
    
    Args:
        client: ThingsBoard 客户端
        device_id: 设备 ID
        
    Returns:
        Device: 设备对象
    """
    print("\n=== 根据 ID 获取设备示例 ===")

    try:
        print(f"查询设备 ID: {device_id}")

        # 根据 ID 获取设备
        device = client.device_service.get_device_by_id(device_id)

        if device:
            print("✅ 设备查询成功！")
            print(f"设备名称: {device.name}")
            print(f"设备类型: {device.type}")
            print(f"设备标签: {device.label}")
            print(f"最后活动时间: {device.additional_info.get('lastActivityTime', 'N/A')}")
            return device
        else:
            print("❌ 设备未找到！")
            return None

    except NotFoundError as e:
        print(f"❌ 设备不存在: {e}")
        return None
    except Exception as e:
        print(f"❌ 查询设备时发生错误: {e}")
        return None


def example_get_device_by_name(client: ThingsBoardClient, device_name: str) -> Optional[Device]:
    """
    根据名称获取设备示例
    
    Args:
        client: ThingsBoard 客户端
        device_name: 设备名称
        
    Returns:
        Device: 设备对象
    """
    print("\n=== 根据名称获取设备示例 ===")

    try:
        print(f"查询设备名称: {device_name}")

        # 根据名称获取设备
        devices = client.device_service.get_devices_by_name(device_name)

        if devices:
            device = devices[0]  # 取第一个匹配的设备
            print("✅ 设备查询成功！")
            print(f"设备 ID: {device.id}")
            print(f"设备类型: {device.type}")
            print(f"设备标签: {device.label}")
            return device
        else:
            print("❌ 设备未找到！")
            return None

    except NotFoundError as e:
        print(f"❌ 设备不存在: {e}")
        return None
    except Exception as e:
        print(f"❌ 查询设备时发生错误: {e}")
        return None


def example_get_tenant_devices(client: ThingsBoardClient) -> List[Device]:
    """
    获取租户设备列表示例
    
    Args:
        client: ThingsBoard 客户端
        
    Returns:
        List[Device]: 设备列表
    """
    print("\n=== 获取租户设备列表示例 ===")

    try:
        # 获取设备列表（分页）
        page_size = 10
        page = 0

        print(f"获取设备列表 (page: {page}, size: {page_size})")

        page_data = client.device_service.get_tenant_devices(
            page_size=page_size,
            page=page,
            sort_property="name",
            sort_order="ASC"
        )

        if page_data and page_data.data:
            print(f"✅ 获取到 {len(page_data.data)} 个设备")
            print(f"总设备数: {page_data.total_elements}")
            print(f"总页数: {page_data.total_pages}")

            print("\n设备列表:")
            for i, device in enumerate(page_data.data, 1):
                print(f"  {i}. {device.name} ({device.type}) - ID: {device.id}")
                if device.label:
                    print(f"     标签: {device.label}")

            return page_data.data
        else:
            print("❌ 未找到设备！")
            return []

    except Exception as e:
        print(f"❌ 获取设备列表时发生错误: {e}")
        return []


def example_update_device(client: ThingsBoardClient, device: Device) -> Optional[Device]:
    """
    更新设备示例
    
    Args:
        client: ThingsBoard 客户端
        device: 要更新的设备
        
    Returns:
        Device: 更新后的设备对象
    """
    print("\n=== 更新设备示例 ===")

    try:
        print(f"更新设备: {device.name}")

        # 更新设备信息
        device.label = f"更新的设备标签 - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        device.additional_info = device.additional_info or {}
        device.additional_info.update({
            "description": "这是一个更新的演示设备",
            "location": "北京市朝阳区",
            "updated_by": "ThingsBoardLink 示例"
        })

        # 执行更新
        updated_device = client.device_service.update_device(device)

        if updated_device:
            print("✅ 设备更新成功！")
            print(f"新标签: {updated_device.label}")
            print(f"附加信息: {updated_device.additional_info}")
            return updated_device
        else:
            print("❌ 设备更新失败！")
            return None

    except ValidationError as e:
        print(f"❌ 验证错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 更新设备时发生错误: {e}")
        return None


def example_device_credentials(client: ThingsBoardClient, device: Device):
    """
    设备凭证管理示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
    """
    print("\n=== 设备凭证管理示例 ===")

    try:
        device_id = device.id
        print(f"管理设备凭证: {device.name}")

        # 获取设备凭证
        print("获取设备凭证...")
        credentials = client.device_service.get_device_credentials(device_id)

        if credentials:
            print("✅ 获取设备凭证成功！")
            print(f"设备 ID: {credentials.device_id}")
            print(f"凭证类型: {credentials.credentials_type}")
            print(f"凭证 ID: {credentials.credentials_id or 'N/A'}")
            print(f"凭证值: {credentials.credentials_value}")

            # 凭证信息展示完成
            print("\n💡 凭证管理说明:")
            print("   - 设备凭证用于设备连接认证")
            print("   - ACCESS_TOKEN 类型凭证最常用")
            print("   - 凭证更新需要谨慎操作，会影响设备连接")
            print("   - 在生产环境中建议通过 ThingsBoard UI 管理凭证")
            
            print("\n✅ 设备凭证管理示例完成！")
        else:
            print("❌ 获取设备凭证失败！")

    except Exception as e:
        print(f"❌ 管理设备凭证时发生错误: {e}")


def example_device_exists(client: ThingsBoardClient, device: Device) -> bool:
    """
    检查设备是否存在示例
    
    Args:
        client: ThingsBoard 客户端
        device: 设备对象
        
    Returns:
        bool: 设备是否存在
    """
    print("\n=== 检查设备是否存在示例 ===")

    try:
        device_id = device.id
        device_name = device.name
        print(f"检查设备是否存在: {device_name} (ID: {device_id})")

        exists = client.device_service.device_exists(device_id)

        if exists:
            print(f"✅ 设备存在: {device_name}")
        else:
            print(f"❌ 设备不存在: {device_name}")

        return exists

    except Exception as e:
        print(f"❌ 检查设备存在性时发生错误: {e}")
        return False


def example_delete_device(client: ThingsBoardClient, device: Device) -> bool:
    """
    删除设备示例
    
    Args:
        client: ThingsBoard 客户端
        device: 要删除的设备
        
    Returns:
        bool: 删除是否成功
    """
    print("\n=== 删除设备示例 ===")

    try:
        device_id = device.id
        device_name = device.name

        print(f"删除设备: {device_name} (ID: {device_id})")

        # 确认删除
        print("⚠️ 即将删除设备，这个操作不可逆！")

        # 执行删除
        success = client.device_service.delete_device(device_id)

        if success:
            print("✅ 设备删除成功！")

            # 验证删除
            time.sleep(1)  # 等待删除操作完成
            exists = client.device_service.device_exists(device_id)

            if not exists:
                print("✅ 删除验证成功，设备已不存在")
            else:
                print("⚠️ 删除验证失败，设备可能仍然存在")

            return True
        else:
            print("❌ 设备删除失败！")
            return False

    except NotFoundError as e:
        print(f"⚠️ 设备已不存在: {e}")
        return True  # 设备已不存在，可以认为删除成功
    except Exception as e:
        print(f"❌ 删除设备时发生错误: {e}")
        return False


def example_batch_operations(client: ThingsBoardClient):
    """
    批量操作示例
    
    Args:
        client: ThingsBoard 客户端
    """
    print("\n=== 批量操作示例 ===")

    created_devices = []

    try:
        # 批量创建设备
        print("批量创建设备...")

        device_configs = [
            {"name": f"batch_device_{i}", "type": "sensor", "label": f"批量设备 {i}"}
            for i in range(1, 4)
        ]

        for config in device_configs:
            try:
                device = client.device_service.create_device(
                    name=config["name"],
                    device_type=config["type"],
                    label=config["label"]
                )
                if device:
                    created_devices.append(device)
                    print(f"  ✅ 创建设备: {device.name}")
                else:
                    print(f"  ❌ 创建设备失败: {config['name']}")
            except Exception as e:
                print(f"  ❌ 创建设备时发生错误 {config['name']}: {e}")

        print(f"\n成功创建 {len(created_devices)} 个设备")

        # 批量查询设备信息
        print("\n批量查询设备信息...")
        for device in created_devices:
            try:
                queried_device = client.device_service.get_device_by_id(device.id)
                if queried_device:
                    print(f"  ✅ 查询设备: {queried_device.name}")
                else:
                    print(f"  ❌ 查询设备失败: {device.name}")
            except Exception as e:
                print(f"  ❌ 查询设备时发生错误 {device.name}: {e}")

        # 等待一段时间
        time.sleep(2)

    finally:
        # 清理创建的设备
        print("\n清理批量创建的设备...")
        for device in created_devices:
            try:
                success = client.device_service.delete_device(device.id)
                if success:
                    print(f"  ✅ 删除设备: {device.name}")
                else:
                    print(f"  ❌ 删除设备失败: {device.name}")
            except Exception as e:
                print(f"  ❌ 删除设备时发生错误 {device.name}: {e}")


def main():
    """主函数"""
    print("ThingsBoardLink 设备管理示例")
    print("=" * 40)

    config = get_config_from_env()

    try:
        # 使用上下文管理器
        with ThingsBoardClient(
                base_url=config["base_url"],
                username=config["username"],
                password=config["password"]
        ) as client:

            print("✅ 客户端连接成功！")

            # 1. 创建设备
            device = example_create_device(client)

            if device:
                # 2.根据 ID 获取设备
                example_get_device_by_id(client, device.id)

                # 3.根据名称获取设备
                example_get_device_by_name(client, device.name)

                # 4.更新设备
                updated_device = example_update_device(client, device)

                # 5.设备凭证管理
                example_device_credentials(client, updated_device or device)

                # 6.检查设备是否存在
                example_device_exists(client, updated_device or device)

                # 7.获取租户设备列表
                example_get_tenant_devices(client)

                # 8.批量操作
                example_batch_operations(client)

                # 9.删除设备
                example_delete_device(client, updated_device or device)

            print("\n" + "=" * 40)
            print("✅ 所有设备管理示例运行完成！")

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
