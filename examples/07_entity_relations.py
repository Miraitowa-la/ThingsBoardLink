"""
ThingsBoardLink 实体关系管理示例

本示例演示如何使用 ThingsBoardLink 进行实体关系管理操作。
包括关系的创建、查询、删除以及复杂的关系查找等功能。

运行前请设置环境变量
export THINGSBOARD_URL="http://localhost:8080"
export THINGSBOARD_USERNAME="tenant@thingsboard.org"
export THINGSBOARD_PASSWORD="tenant"
"""

import os
import time
import uuid
import json
from typing import List

from src.thingsboardlink import (
    ThingsBoardClient,
    Device,
    EntityRelation,
    EntityId,
    EntityType,
    ThingsBoardError,
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


def create_demo_devices(client: ThingsBoardClient) -> List[Device]:
    """创建演示设备
    
    Args:
        client: ThingsBoard 客户端
        
    Returns:
        List[Device]: 创建的设备列表
    """
    devices = []

    try:
        # 创建不同类型的设备
        device_configs = [
            {
                "name": f"gateway_device_{uuid.uuid4().hex[:8]}",
                "type": "gateway",
                "label": "网关设备"
            },
            {
                "name": f"sensor_device_1_{uuid.uuid4().hex[:8]}",
                "type": "sensor",
                "label": "温度传感器"
            },
            {
                "name": f"sensor_device_2_{uuid.uuid4().hex[:8]}",
                "type": "sensor",
                "label": "湿度传感器"
            },
            {
                "name": f"actuator_device_{uuid.uuid4().hex[:8]}",
                "type": "actuator",
                "label": "执行器设备"
            },
            {
                "name": f"controller_device_{uuid.uuid4().hex[:8]}",
                "type": "controller",
                "label": "控制器设备"
            }
        ]

        print("创建演示设备...")

        for i, config in enumerate(device_configs, 1):
            try:
                device = client.device_service.create_device(
                    name=config["name"],
                    device_type=config["type"],
                    label=config["label"]
                )

                if device:
                    devices.append(device)
                    print(f"  {i}. ✅ 创建设备成功: {device.name} ({device.type})")
                else:
                    print(f"  {i}. ❌ 创建设备失败: {config['name']}")

            except Exception as e:
                print(f"  {i}. ❌ 创建设备时发生错误 {config['name']}: {e}")

        print(f"\n成功创建 {len(devices)} 个演示设备")
        return devices

    except Exception as e:
        print(f"❌ 创建演示设备时发生错误: {e}")
        return devices


def example_create_relations(client: ThingsBoardClient, devices: List[Device]) -> List[EntityRelation]:
    """创建实体关系示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
        
    Returns:
        List[EntityRelation]: 创建的关系列表
    """
    print("\n=== 创建实体关系示例 ===")

    created_relations = []

    try:
        if len(devices) < 5:
            print("❌ 设备数量不足，无法创建关系")
            return created_relations

        # 获取不同类型的设备
        gateway = next((d for d in devices if d.type == "gateway"), None)
        sensors = [d for d in devices if d.type == "sensor"]
        actuator = next((d for d in devices if d.type == "actuator"), None)
        controller = next((d for d in devices if d.type == "controller"), None)

        if not all([gateway, sensors, actuator, controller]):
            print("❌ 缺少必要的设备类型")
            return created_relations

        print(f"使用设备创建关系:")
        print(f"  网关: {gateway.name}")
        print(f"  传感器: {[s.name for s in sensors]}")
        print(f"  执行器: {actuator.name}")
        print(f"  控制器: {controller.name}")

        # 定义要创建的关系
        relations_to_create = [
            {
                "from": gateway,
                "to": sensors[0],
                "type": "Contains",
                "description": "网关包含温度传感器"
            },
            {
                "from": gateway,
                "to": sensors[1] if len(sensors) > 1 else sensors[0],
                "type": "Contains",
                "description": "网关包含湿度传感器"
            },
            {
                "from": gateway,
                "to": actuator,
                "type": "Contains",
                "description": "网关包含执行器"
            },
            {
                "from": controller,
                "to": gateway,
                "type": "Manages",
                "description": "控制器管理网关"
            },
            {
                "from": sensors[0],
                "to": actuator,
                "type": "Triggers",
                "description": "传感器触发执行器"
            },
            {
                "from": controller,
                "to": sensors[0],
                "type": "Monitors",
                "description": "控制器监控传感器"
            }
        ]

        # 创建关系
        for i, relation_config in enumerate(relations_to_create, 1):
            try:
                print(f"\n{i}. 创建关系: {relation_config['description']}")
                print(f"   从: {relation_config['from'].name} ({relation_config['from'].type})")
                print(f"   到: {relation_config['to'].name} ({relation_config['to'].type})")
                print(f"   关系类型: {relation_config['type']}")

                success = client.relation_service.create_relation(
                    from_id=relation_config["from"].id,
                    from_type=EntityType.DEVICE,
                    to_id=relation_config["to"].id,
                    to_type=EntityType.DEVICE,
                    relation_type=relation_config["type"]
                )

                if success:
                    print(f"   ✅ 关系创建成功")

                    relation = EntityRelation(
                        from_id=EntityId(id=relation_config["from"].id, entity_type=EntityType.DEVICE),
                        to_id=EntityId(id=relation_config["to"].id, entity_type=EntityType.DEVICE),
                        type=relation_config["type"]
                    )

                    created_relations.append(relation)
                else:
                    print(f"   ❌ 关系创建失败")

                # 短暂延迟
                time.sleep(0.5)

            except ValidationError as e:
                print(f"   ❌ 验证错误: {e}")
                print(f"   字段: {e.details.get('field')}")
            except Exception as e:
                print(f"   ❌ 创建关系时发生错误: {e}")

        print(f"\n成功创建 {len(created_relations)} 个关系")
        return created_relations

    except Exception as e:
        print(f"❌ 创建实体关系时发生错误: {e}")
        return created_relations


def example_get_relation(client: ThingsBoardClient, devices: List[Device]):
    """获取关系示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
    """
    print("\n=== 获取关系示例 ===")

    try:
        if len(devices) < 2:
            print("❌ 设备数量不足")
            return

        # 选择两个设备来查询关系
        from_device = devices[0]
        to_device = devices[1]
        relation_type = "Contains"

        print(f"查询关系:")
        print(f"  从设备: {from_device.name} ({from_device.type})")
        print(f"  到设备: {to_device.name} ({to_device.type})")
        print(f"  关系类型: {relation_type}")

        # 获取关系
        relation = client.relation_service.get_relation(
            from_id=from_device.id,
            from_type=EntityType.DEVICE,
            to_id=to_device.id,
            to_type=EntityType.DEVICE,
            relation_type=relation_type
        )

        if relation:
            print("✅ 关系查询成功")
            print(f"关系信息:")
            print(f"  从实体: {relation.from_id.id} ({relation.from_id.entity_type.value})")
            print(f"  到实体: {relation.to_id.id} ({relation.to_id.entity_type.value})")
            print(f"  关系类型: {relation.type}")

            if relation.additional_info:
                print(f"  附加信息: {json.dumps(relation.additional_info, indent=2, ensure_ascii=False)}")
        else:
            print("❌ 未找到关系")

    except NotFoundError as e:
        print(f"❌ 关系不存在: {e}")
    except Exception as e:
        print(f"❌ 获取关系时发生错误: {e}")


def example_find_relations_by_from(client: ThingsBoardClient, devices: List[Device]):
    """根据源实体查找关系示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
    """
    print("\n=== 根据源实体查找关系示例 ===")

    try:
        # 选择网关设备作为源实体
        gateway = next((d for d in devices if d.type == "gateway"), None)

        if not gateway:
            print("❌ 未找到网关设备")
            return

        print(f"查找源实体的所有关系: {gateway.name}")

        # 根据源实体查找关系
        relations = client.relation_service.find_by_from(
            from_id=gateway.id,
            from_type=EntityType.DEVICE
        )

        if relations:
            print(f"✅ 找到 {len(relations)} 个关系")

            print("\n关系列表:")
            for i, relation in enumerate(relations, 1):
                print(f"  {i}. 关系类型: {relation.type}")
                print(f"     到实体: {relation.to_id.id} ({relation.to_id.entity_type.value})")

                # 尝试获取目标设备的详细信息
                try:
                    target_device = client.device_service.get_device_by_id(relation.to_entity.id)
                    if target_device:
                        print(f"     目标设备: {target_device.name} ({target_device.type})")
                except:
                    pass

                print()
        else:
            print("❌ 未找到关系")

        # 按关系类型过滤
        print(f"\n按关系类型过滤: 'Contains'")

        contains_relations = client.relation_service.find_by_from(
            from_id=gateway.id,
            from_type=EntityType.DEVICE,
            relation_type_group="Contains"
        )

        if contains_relations:
            print(f"✅ 找到 {len(contains_relations)} 个 'Contains' 关系")

            for i, relation in enumerate(contains_relations, 1):
                print(f"  {i}. 包含设备: {relation.to_id.id}")
        else:
            print("❌ 未找到 'Contains' 关系")

    except Exception as e:
        print(f"❌ 根据源实体查找关系时发生错误: {e}")


def example_find_relations_by_to(client: ThingsBoardClient, devices: List[Device]):
    """根据目标实体查找关系示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
    """
    print("\n=== 根据目标实体查找关系示例 ===")

    try:
        # 选择传感器设备作为目标实体
        sensor = next((d for d in devices if d.type == "sensor"), None)

        if not sensor:
            print("❌ 未找到传感器设备")
            return

        print(f"查找目标实体的所有关系: {sensor.name}")

        # 根据目标实体查找关系
        relations = client.relation_service.find_by_to(
            to_id=sensor.id,
            to_type=EntityType.DEVICE
        )

        if relations:
            print(f"✅ 找到 {len(relations)} 个关系")

            print("\n关系列表:")
            for i, relation in enumerate(relations, 1):
                print(f"  {i}. 关系类型: {relation.type}")
                print(f"     从实体y: {relation.from_id.id} ({relation.from_id.entity_type.value})")

                # 尝试获取源设备的详细信息
                try:
                    source_device = client.device_service.get_device_by_id(relation.from_id.id)
                    if source_device:
                        print(f"     源设备: {source_device.name} ({source_device.type})")
                except:
                    pass

                print()
        else:
            print("❌ 未找到关系")

        # 按关系类型过滤
        print(f"\n按关系类型过滤: 'Monitors'")

        monitors_relations = client.relation_service.find_by_to(
            to_id=sensor.id,
            to_type=EntityType.DEVICE,
            relation_type_group="Monitors"
        )

        if monitors_relations:
            print(f"✅ 找到 {len(monitors_relations)} 个 'Monitors' 关系")

            for i, relation in enumerate(monitors_relations, 1):
                print(f"  {i}. 监控来源: {relation.from_id.id}")
        else:
            print("❌ 未找到 'Monitors' 关系")

    except Exception as e:
        print(f"❌ 根据目标实体查找关系时发生错误: {e}")


def example_find_related_entities(client: ThingsBoardClient, devices: List[Device]):
    """查找相关实体示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
    """
    print("\n=== 查找相关实体示例 ===")

    try:
        # 选择网关设备
        gateway = next((d for d in devices if d.type == "gateway"), None)

        if not gateway:
            print("❌ 未找到网关设备")
            return

        print(f"查找相关实体: {gateway.name}")

        # 查找网关包含的所有设备
        print("\n1. 查找网关包含的设备")

        contained_entities = client.relation_service.find_by_query(
            entity_id=gateway.id,
            entity_type=EntityType.DEVICE,
            relation_type_group="Contains",
            direction="FROM"
        )

        if contained_entities:
            print(f"✅ 找到 {len(contained_entities)} 个包含的实体")

            for i, entity_id in enumerate(contained_entities, 1):
                try:
                    device = client.device_service.get_device_by_id(entity_id.id)
                    if device:
                        print(f"  {i}. {device.name} ({device.type}) - ID: {device.id}")
                    else:
                        print(f"  {i}. 实体 ID: {entity_id.id}")
                except:
                    print(f"  {i}. 实体 ID: {entity_id.id}")
        else:
            print("❌ 未找到包含的实体")

        # 查找管理网关的实体
        print("\n2. 查找管理网关的实体")

        managing_entities = client.relation_service.find_related_entities(
            from_id=gateway.id,
            from_type=EntityType.DEVICE,
            relation_type="Manages",
            direction="TO"
        )

        if managing_entities:
            print(f"✅ 找到 {len(managing_entities)} 个管理实体")

            for i, entity_id in enumerate(managing_entities, 1):
                try:
                    device = client.device_service.get_device_by_id(entity_id.id)
                    if device:
                        print(f"  {i}. {device.name} ({device.type}) - ID: {device.id}")
                    else:
                        print(f"  {i}. 实体 ID: {entity_id.id}")
                except:
                    print(f"  {i}. 实体 ID: {entity_id.id}")
        else:
            print("❌ 未找到管理实体")

        # 查找所有相关实体（不限制关系类型）
        print("\n3. 查找所有相关实体")

        all_related_from = client.relation_service.find_related_entities(
            from_id=gateway.id,
            from_type=EntityType.DEVICE,
            direction="FROM"
        )

        all_related_to = client.relation_service.find_related_entities(
            from_id=gateway.id,
            from_type=EntityType.DEVICE,
            direction="TO"
        )

        total_related = len(all_related_from or []) + len(all_related_to or [])

        print(f"相关实体统计:")
        print(f"  出向关系: {len(all_related_from or [])}")
        print(f"  入向关系: {len(all_related_to or [])}")
        print(f"  总相关实体: {total_related}")

    except Exception as e:
        print(f"❌ 查找相关实体时发生错误: {e}")


def example_relation_exists(client: ThingsBoardClient, devices: List[Device]):
    """检查关系是否存在示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
    """
    print("\n=== 检查关系是否存在示例 ===")

    try:
        if len(devices) < 2:
            print("❌ 设备数量不足")
            return

        # 测试不同的关系组合
        test_cases = [
            {
                "from": devices[0],
                "to": devices[1],
                "type": "Contains",
                "description": "网关包含传感器"
            },
            {
                "from": devices[1],
                "to": devices[0],
                "type": "Contains",
                "description": "传感器包含网关（反向）"
            },
            {
                "from": devices[0],
                "to": devices[1],
                "type": "NonExistentRelation",
                "description": "不存在的关系类型"
            }
        ]

        print("检查关系是否存在:")

        for i, test_case in enumerate(test_cases, 1):
            try:
                print(f"\n{i}. {test_case['description']}")
                print(f"   从: {test_case['from'].name} ({test_case['from'].type})")
                print(f"   到: {test_case['to'].name} ({test_case['to'].type})")
                print(f"   关系类型: {test_case['type']}")

                exists = client.relation_service.relation_exists(
                    from_id=test_case["from"].id,
                    from_type=EntityType.DEVICE,
                    to_id=test_case["to"].id,
                    to_type=EntityType.DEVICE,
                    relation_type=test_case["type"]
                )

                status = "✅ 存在" if exists else "❌ 不存在"
                print(f"   结果: {status}")

            except Exception as e:
                print(f"   ❌ 检查关系时发生错误: {e}")

        # 批量检查关系存在性
        print("\n批量检查关系存在性:")

        batch_checks = [
            (devices[0], devices[1], "Contains"),
            (devices[0], devices[2] if len(devices) > 2 else devices[1], "Contains"),
            (devices[1], devices[0], "Triggers") if len(devices) > 1 else (devices[0], devices[1], "Triggers")
        ]

        existing_relations = 0
        total_checks = len(batch_checks)

        for i, (from_dev, to_dev, rel_type) in enumerate(batch_checks, 1):
            try:
                exists = client.relation_service.relation_exists(
                    from_id=from_dev.id,
                    from_type=EntityType.DEVICE,
                    to_id=to_dev.id,
                    to_type=EntityType.DEVICE,
                    relation_type=rel_type
                )

                if exists:
                    existing_relations += 1
                    print(f"  ✅ 关系 {i}: {from_dev.name} --{rel_type}--> {to_dev.name}")
                else:
                    print(f"  ❌ 关系 {i}: {from_dev.name} --{rel_type}--> {to_dev.name}")

            except Exception as e:
                print(f"  ❌ 检查关系 {i} 时发生错误: {e}")

        print(f"\n批量检查结果: {existing_relations}/{total_checks} 个关系存在")

    except Exception as e:
        print(f"❌ 检查关系是否存在时发生错误: {e}")


def example_delete_relations(client: ThingsBoardClient, devices: List[Device]):
    """删除关系示例
    
    Args:
        client: ThingsBoard 客户端
        devices: 设备列表
    """
    print("\n=== 删除关系示例 ===")

    try:
        if len(devices) < 2:
            print("❌ 设备数量不足")
            return

        # 删除特定关系
        print("1. 删除特定关系")

        from_device = devices[0]
        to_device = devices[1]
        relation_type = "Contains"

        print(f"删除关系:")
        print(f"  从: {from_device.name} ({from_device.type})")
        print(f"  到: {to_device.name} ({to_device.type})")
        print(f"  关系类型: {relation_type}")

        # 先检查关系是否存在
        exists_before = client.relation_service.relation_exists(
            from_id=from_device.id,
            from_type=EntityType.DEVICE,
            to_id=to_device.id,
            to_type=EntityType.DEVICE,
            relation_type=relation_type
        )

        print(f"删除前关系状态: {'存在' if exists_before else '不存在'}")

        if exists_before:
            # 删除关系
            success = client.relation_service.delete_relation(
                from_id=from_device.id,
                from_type=EntityType.DEVICE,
                to_id=to_device.id,
                to_type=EntityType.DEVICE,
                relation_type=relation_type
            )

            if success:
                print("✅ 关系删除成功")

                # 验证删除
                time.sleep(1)
                exists_after = client.relation_service.relation_exists(
                    from_id=from_device.id,
                    from_type=EntityType.DEVICE,
                    to_id=to_device.id,
                    to_type=EntityType.DEVICE,
                    relation_type=relation_type
                )

                if not exists_after:
                    print("✅ 删除验证成功，关系已不存在")
                else:
                    print("⚠️ 删除验证失败，关系可能仍然存在")
            else:
                print("❌ 关系删除失败")
        else:
            print("⚠️ 关系不存在，无需删除")

        # 删除实体的所有关系
        print("\n2. 删除实体的所有关系")

        if len(devices) > 2:
            target_device = devices[2]
            print(f"删除设备的所有关系: {target_device.name}")

            # 先查看有多少关系
            outgoing_relations = client.relation_service.find_by_from(
                from_id=target_device.id,
                from_type=EntityType.DEVICE
            )

            incoming_relations = client.relation_service.find_by_to(
                to_id=target_device.id,
                to_type=EntityType.DEVICE
            )

            total_relations = len(outgoing_relations or []) + len(incoming_relations or [])
            print(f"删除前关系总数: {total_relations}")
            print(f"  出向关系: {len(outgoing_relations or [])}")
            print(f"  入向关系: {len(incoming_relations or [])}")

            if total_relations > 0:
                # 删除所有关系
                success = client.relation_service.delete_relations(
                    entity_id=target_device.id,
                    entity_type=EntityType.DEVICE
                )

                if success:
                    print("✅ 实体所有关系删除成功")

                    # 验证删除
                    time.sleep(1)

                    remaining_outgoing = client.relation_service.find_by_from(
                        from_id=target_device.id,
                        from_type=EntityType.DEVICE
                    )

                    remaining_incoming = client.relation_service.find_by_to(
                        to_id=target_device.id,
                        to_type=EntityType.DEVICE
                    )

                    remaining_total = len(remaining_outgoing or []) + len(remaining_incoming or [])

                    if remaining_total == 0:
                        print("✅ 删除验证成功，所有关系已被删除")
                    else:
                        print(
                            f"⚠️ 删除验证失败，仍有 {remaining_total} 个关系存在, {remaining_total} relations still exist")
                else:
                    print("❌ 实体关系删除失败")
            else:
                print("⚠️ 实体没有关系，无需删除")

    except Exception as e:
        print(f"❌ 删除关系时发生错误: {e}")


def cleanup_demo_devices(client: ThingsBoardClient, devices: List[Device]):
    """清理演示设备
    
    Args:
        client: ThingsBoard 客户端
        devices: 要清理的设备列表
    """
    try:
        print(f"\n清理演示设备 ({len(devices)} 个 )...")

        success_count = 0

        for i, device in enumerate(devices, 1):
            try:
                success = client.device_service.delete_device(device.id)

                if success:
                    success_count += 1
                    print(f"  {i}. ✅ 删除设备成功: {device.name}")
                else:
                    print(f"  {i}. ❌ 删除设备失败: {device.name}")

            except Exception as e:
                print(f"  {i}. ❌ 删除设备时发生错误 {device.name}: {e}")

        print(f"\n清理完成: {success_count}/{len(devices)} 个设备删除成功")

    except Exception as e:
        print(f"❌ 清理演示设备时发生错误: {e}")


def main():
    """主函数"""
    print("ThingsBoardLink 实体关系管理示例")
    print("=" * 80)

    config = get_config_from_env()
    demo_devices = []

    try:
        # 使用上下文管理器
        with ThingsBoardClient(
                base_url=config["base_url"],
                username=config["username"],
                password=config["password"]
        ) as client:

            print("✅ 客户端连接成功！")

            # 创建演示设备
            demo_devices = create_demo_devices(client)

            if len(demo_devices) >= 2:
                # 1. 创建实体关系
                created_relations = example_create_relations(client, demo_devices)

                # 2. 获取关系
                example_get_relation(client, demo_devices)

                # 3. 根据源实体查找关系
                example_find_relations_by_from(client, demo_devices)

                # 4. 根据目标实体查找关系
                example_find_relations_by_to(client, demo_devices)

                # # 5. 查找相关实体
                example_find_related_entities(client, demo_devices)

                # # 6. 检查关系是否存在
                example_relation_exists(client, demo_devices)

                # 7. 删除关系
                example_delete_relations(client, demo_devices)

                # 清理演示设备
                cleanup_demo_devices(client, demo_devices)
            else:
                print("❌ 演示设备数量不足，跳过关系管理示例")
                if demo_devices:
                    cleanup_demo_devices(client, demo_devices)

            print("\n" + "=" * 80)
            print("✅ 所有实体关系管理示例运行完成！")

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
        if demo_devices:
            try:
                with ThingsBoardClient(
                        base_url=config["base_url"],
                        username=config["username"],
                        password=config["password"]
                ) as client:
                    cleanup_demo_devices(client, demo_devices)
            except:
                pass
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()

        if demo_devices:
            try:
                with ThingsBoardClient(
                        base_url=config["base_url"],
                        username=config["username"],
                        password=config["password"]
                ) as client:
                    cleanup_demo_devices(client, demo_devices)
            except:
                pass


if __name__ == "__main__":
    main()
