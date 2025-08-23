#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Logging 模块完整演示程序

这个程序演示了 logging 模块的核心功能：
1. 创建 Logger
2. 配置多个 Handler（文件 + 控制台）
3. 设置不同的 Formatter
4. 演示各种日志级别
5. 展示日志的流转过程
"""

import logging
from datetime import datetime


def setup_logger():
    """
    配置并创建一个完整的日志系统
    """
    # 1. 创建 Logger（记录器）
    logger = logging.getLogger("TutorialDemo")
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 清除可能存在的旧 handlers（避免重复）
    if logger.handlers:
        logger.handlers.clear()

    # 2. 创建控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 及以上级别

    # 3. 创建文件 Handler
    log_filename = f"tutorial_demo_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename, encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别的日志

    # 4. 创建格式化器 (Formatter)
    # 控制台格式：简洁明了
    console_format = logging.Formatter(
        "%(levelname)-8s | %(funcName)s:%(lineno)s | %(message)s"
    )

    # 文件格式：详细信息
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 5. 将格式化器应用到对应的 Handler
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # 6. 将 Handlers 添加到 Logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger, log_filename


def demonstrate_log_levels(logger):
    """
    演示不同的日志级别
    """
    logger.info("=" * 50)
    logger.info("开始演示不同的日志级别")
    logger.info("=" * 50)

    # DEBUG: 详细的调试信息
    logger.debug("🔍 这是 DEBUG 级别：详细的调试信息，通常用于开发阶段")

    # INFO: 一般信息
    logger.info("ℹ️ 这是 INFO 级别：程序正常运行的信息")

    # WARNING: 警告信息
    logger.warning("⚠️ 这是 WARNING 级别：可能出现问题的警告")

    # ERROR: 错误信息
    logger.error("❌ 这是 ERROR 级别：程序出现错误但仍可继续运行")

    # CRITICAL: 严重错误
    logger.critical("🚨 这是 CRITICAL 级别：严重错误，程序可能无法继续运行")


def demonstrate_practical_examples(logger):
    """
    演示实际应用场景中的日志使用
    """
    logger.info("=" * 50)
    logger.info("演示实际应用场景")
    logger.info("=" * 50)

    # 1. 用户登录场景
    username = "张三"
    logger.info(f"用户尝试登录: {username}")

    # 模拟登录验证
    is_password_correct = True
    if is_password_correct:
        logger.info(f"用户 {username} 登录成功")
    else:
        logger.warning(f"用户 {username} 登录失败：密码错误")

    # 2. 数据库操作场景
    logger.debug("准备连接数据库")
    try:
        # 模拟数据库操作
        database_connected = True
        if not database_connected:
            raise ConnectionError("无法连接到数据库")

        logger.info("数据库连接成功")
        logger.debug("执行查询：SELECT * FROM users")

        # 模拟查询结果
        user_count = 150
        logger.info(f"查询完成，找到 {user_count} 个用户")

    except ConnectionError as e:
        logger.error(f"数据库操作失败: {e}")
    except Exception as e:
        logger.critical(f"未预期的严重错误: {e}")

    # 3. 文件处理场景
    filename = "important_data.txt"
    logger.debug(f"尝试读取文件: {filename}")

    try:
        # 模拟文件不存在的情况
        file_exists = False
        if not file_exists:
            raise FileNotFoundError(f"文件 {filename} 不存在")

        logger.info(f"成功读取文件: {filename}")

    except FileNotFoundError:
        logger.warning(f"文件 {filename} 不存在，将创建默认文件")
        logger.info(f"已创建默认文件: {filename}")

    # 4. 性能监控场景
    import time

    logger.debug("开始执行耗时操作")
    start_time = time.time()

    # 模拟耗时操作
    time.sleep(0.1)

    end_time = time.time()
    execution_time = end_time - start_time

    if execution_time > 0.05:
        logger.warning(f"操作耗时较长: {execution_time:.3f} 秒")
    else:
        logger.info(f"操作完成，耗时: {execution_time:.3f} 秒")


def demonstrate_logger_hierarchy():
    """
    演示 Logger 的层级结构
    """
    # 创建父 Logger
    parent_logger = logging.getLogger("MyApp")
    parent_logger.setLevel(logging.INFO)

    # 创建子 Logger
    child_logger = logging.getLogger("MyApp.module1")

    # 添加一个简单的 handler 到父 Logger
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    parent_logger.addHandler(handler)

    print("\n" + "=" * 50)
    print("演示 Logger 层级结构：")
    print("=" * 50)

    # 子 Logger 的消息会传播到父 Logger
    parent_logger.info("这是来自父 Logger 的消息")
    child_logger.info("这是来自子 Logger 的消息")  # 这个也会被父 Logger 处理

    # 清理 handlers
    parent_logger.handlers.clear()


def main():
    """
    主函数：运行完整的日志演示
    """
    print("🎯 Python Logging 模块演示程序")
    print("=" * 60)

    # 1. 设置日志系统
    logger, log_filename = setup_logger()

    logger.info("🚀 日志演示程序启动")
    logger.info(f"📁 日志文件: {log_filename}")

    # 2. 演示不同日志级别
    demonstrate_log_levels(logger)

    # 3. 演示实际应用场景
    demonstrate_practical_examples(logger)

    # 4. 演示 Logger 层级结构
    # demonstrate_logger_hierarchy()

    # 5. 程序结束
    logger.info("✅ 日志演示程序结束")

    print("\n" + "=" * 60)
    print("📋 演示总结：")
    print(f"1. 控制台输出：显示了 INFO 级别及以上的日志")
    print(f"2. 文件输出：保存了所有级别的日志到 {log_filename}")
    print(f"3. 不同格式：控制台和文件使用了不同的格式化器")
    print(f"4. 实际应用：展示了登录、数据库、文件操作等场景的日志使用")
    print("=" * 60)


# 额外的工具函数
def create_custom_filter_example():
    """
    演示自定义过滤器的使用
    """

    class SensitiveInfoFilter(logging.Filter):
        """自定义过滤器：过滤包含敏感信息的日志"""

        def filter(self, record):
            # 如果日志消息包含密码等敏感信息，就过滤掉
            sensitive_keywords = ["password", "密码", "token"]
            message = record.getMessage().lower()

            for keyword in sensitive_keywords:
                if keyword in message:
                    return False  # 过滤掉这条日志

            return True  # 允许这条日志通过

    # 创建 logger 和 handler
    logger = logging.getLogger("FilterDemo")
    handler = logging.StreamHandler()

    # 添加自定义过滤器
    handler.addFilter(SensitiveInfoFilter())

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    print("\n" + "=" * 50)
    print("演示自定义过滤器：")
    print("=" * 50)

    # 测试过滤器
    logger.info("正常的日志信息")  # 这个会显示
    logger.info("用户输入了 password: 123456")  # 这个会被过滤
    logger.info("系统运行正常")  # 这个会显示

    # 清理
    logger.handlers.clear()


if __name__ == "__main__":
    main()

    # 可选：演示自定义过滤器
    # create_custom_filter_example()
