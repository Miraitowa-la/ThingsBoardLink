"""
ThingsBoardLink 连接和认证示例

本示例演示如何使用 ThingsBoardLink 连接到 ThingsBoard 服务器并进行用户认证。
包括客户端创建、登录、会话管理和安全退出等基本操作。

运行前请设置环境变量
export THINGSBOARD_URL="http://localhost:8080"
export THINGSBOARD_USERNAME="tenant@thingsboard.org"
export THINGSBOARD_PASSWORD="tenant"
"""

import os
import time

from src.thingsboardlink import (
    ThingsBoardClient,
    AuthenticationError,
    ConnectionError,
    ConfigurationError
)


def get_config_from_env() -> dict:
    """
    从环境变量获取配置
    
    Returns:
        dict: 配置字典
    """
    return {
        "base_url": os.getenv("THINGSBOARD_URL", "http://localhost:8080"),
        "username": os.getenv("THINGSBOARD_USERNAME", "tenant@thingsboard.org"),
        "password": os.getenv("THINGSBOARD_PASSWORD", "tenant"),
        "timeout": float(os.getenv("THINGSBOARD_TIMEOUT", "30.0")),
        "verify_ssl": os.getenv("THINGSBOARD_VERIFY_SSL", "true").lower() == "true"
    }


def example_basic_connection():
    """基本连接示例"""
    print("\n=== 基本连接示例 ===")

    config = get_config_from_env()

    try:
        # 创建客户端
        print(f"创建客户端，连接到: {config['base_url']}")
        client = ThingsBoardClient(
            base_url=config["base_url"],
            username=config["username"],
            password=config["password"],
            timeout=config["timeout"],
            verify_ssl=config["verify_ssl"]
        )

        # 检查初始认证状态
        print(f"初始认证状态: {client.is_authenticated}")

        # 用户登录
        print("正在登录...")
        login_success = client.login()

        if login_success:
            print("✅ 登录成功！")
            print(f"认证状态: {client.is_authenticated}")

            # 模拟一些操作
            print("执行一些操作...")
            time.sleep(2)

            # 安全退出
            print("正在退出...")
            logout_success = client.logout()

            if logout_success:
                print("✅ 退出成功！")
            else:
                print("⚠️ 退出可能失败，但本地会话已清除")

            print(f"最终认证状态: {client.is_authenticated}")
        else:
            print("❌ 登录失败！")

    except AuthenticationError as e:
        print(f"❌ 认证错误: {e}")
        print(f"错误详情: {e.details}")

    except ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        print(f"服务器 URL: {e.details.get('server_url', 'Unknown')}")

    except Exception as e:
        print(f"❌ 未知错误: {e}")


def example_context_manager():
    """上下文管理器示例"""
    print("\n=== 上下文管理器示例 ===")

    config = get_config_from_env()

    try:
        # 使用上下文管理器自动处理登录和退出
        print("使用上下文管理器...")

        with ThingsBoardClient(
                base_url=config["base_url"],
                username=config["username"],
                password=config["password"]
        ) as client:
            print("✅ 自动登录成功！")
            print(f"认证状态: {client.is_authenticated}")

            # 在这里执行业务逻辑
            print("执行业务逻辑...")
            time.sleep(1)

            # 可以访问所有服务
            print("可用的服务:")
            print(f"  - 设备服务: {client.device_service.__class__.__name__}")
            print(f"  - 遥测服务: {client.telemetry_service.__class__.__name__}")
            print(f"  - 属性服务: {client.attribute_service.__class__.__name__}")
            print(f"  - 警报服务: {client.alarm_service.__class__.__name__}")
            print(f"  - RPC 服务: {client.rpc_service.__class__.__name__}")
            print(f"  - 关系服务: {client.relation_service.__class__.__name__}")

        # 退出上下文后自动登出
        print("✅ 自动退出成功！| Auto-logout successful!")

    except Exception as e:
        print(f"❌ 上下文管理器错误: {e}")


def example_advanced_configuration():
    """高级配置示例"""
    print("\n=== 高级配置示例 ===")

    config = get_config_from_env()

    try:
        # 创建具有高级配置的客户端
        print("创建高级配置客户端...")

        client = ThingsBoardClient(
            base_url=config["base_url"],
            username=config["username"],
            password=config["password"],
            timeout=60.0,  # 更长的超时时间
            max_retries=5,  # 更多重试次数
            retry_backoff_factor=0.5,  # 重试退避因子
            verify_ssl=config["verify_ssl"]  # SSL 验证
        )

        print("配置信息:")
        print(f"  - 基础 URL: {client.base_url}")
        print(f"  - 超时时间: {client.timeout}s")
        print(f"  - SSL 验证: {client.verify_ssl}")

        # 登录测试
        if client.login():
            print("✅ 高级配置客户端登录成功！")

            # 测试会话状态
            print(f"会话状态: {client.is_authenticated}")

            # 退出
            client.logout()
            print("✅ 高级配置客户端退出成功！")
        else:
            print("❌ 高级配置客户端登录失败！")

    except Exception as e:
        print(f"❌ 高级配置错误: {e}")


def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例")

    # 测试各种错误情况

    # 1. 无效的服务器 URL
    print("\n1. 测试无效服务器 URL")
    try:
        client = ThingsBoardClient(
            base_url="http://invalid-server:9999",
            username="test",
            password="test",
            timeout=5.0  # 短超时用于快速失败
        )
        client.login()
    except ConnectionError as e:
        print(f"✅ 正确捕获连接错误: {e}")
    except Exception as e:
        print(f"⚠️ 其他错误: {e}")

    # 2. 无效的认证信息
    print("\n2. 测试无效认证信息")
    try:
        config = get_config_from_env()
        client = ThingsBoardClient(
            base_url=config["base_url"],
            username="invalid_user",
            password="invalid_password"
        )
        client.login()
    except AuthenticationError as e:
        print(f"✅ 正确捕获认证错误: {e}")
        print(f"状态码: {e.details.get('status_code')}")
    except Exception as e:
        print(f"⚠️ 其他错误: {e}")

    # 3. 配置错误
    print("\n3. 测试配置错误")
    try:
        client = ThingsBoardClient(
            base_url="http://localhost:8080",
            username="",  # 空用户名
            password=""
        )
        client.login()
    except ConfigurationError as e:
        print(f"✅ 正确捕获配置错误: {e}")
        print(f"配置键: {e.details.get('config_key')}")
    except Exception as e:
        print(f"⚠️ 其他错误: {e}")


def main():
    print("ThingsBoardLink 连接和认证示例")
    print("=" * 40)

    # 检查环境变量
    config = get_config_from_env()
    print(f"配置信息:")
    print(f"  - 服务器 URL: {config['base_url']}")
    print(f"  - 用户名: {config['username']}")
    print(f"  - 密码: {'*' * len(config['password'])}")
    print(f"  - 超时时间: {config['timeout']}s")
    print(f"  - SSL 验证: {config['verify_ssl']}")

    try:
        # 运行所有示例
        example_basic_connection()
        example_context_manager()
        example_advanced_configuration()
        example_error_handling()

        print("\n" + "=" * 40)
        print("✅ 所有示例运行完成！")

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
