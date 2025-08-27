# -*- coding: utf-8 -*-
"""
线程池 + LRU缓存 综合应用示例
===========================

演示如何将线程池和LRU缓存结合使用
"""

import time
import threading
import concurrent.futures
from functools import lru_cache
import random
from typing import Dict, List, Any


class DataService:
    """数据服务类 - 模拟实际业务场景"""
    
    def __init__(self):
        # 模拟数据库
        self.users_db = {
            i: {
                "id": i,
                "name": f"用户_{i}",
                "level": random.choice(["普通", "VIP", "钻石"]),
                "city": random.choice(["北京", "上海", "广州", "深圳"])
            }
            for i in range(1, 21)
        }
        
        self.products_db = {
            i: {
                "id": i,
                "name": f"商品_{i}",
                "price": random.randint(50, 500),
                "category": random.choice(["电子", "服装", "食品", "图书"])
            }
            for i in range(1, 11)
        }
    
    @lru_cache(maxsize=128)
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """获取用户信息 - 使用缓存优化"""
        print(f"    查询用户数据库: user_id={user_id}")
        time.sleep(0.05)  # 模拟数据库查询延迟
        return self.users_db.get(user_id, {"error": "用户不存在"})
    
    @lru_cache(maxsize=64)
    def get_product_info(self, product_id: int) -> Dict[str, Any]:
        """获取商品信息 - 使用缓存优化"""
        print(f"    查询商品数据库: product_id={product_id}")
        time.sleep(0.03)  # 模拟数据库查询延迟
        return self.products_db.get(product_id, {"error": "商品不存在"})
    
    @lru_cache(maxsize=32)
    def calculate_discount(self, user_level: str, product_category: str) -> float:
        """计算折扣 - 使用缓存优化复杂计算"""
        print(f"    计算折扣: {user_level} + {product_category}")
        time.sleep(0.02)  # 模拟复杂计算
        
        # 折扣规则
        discounts = {
            ("VIP", "电子"): 0.15,
            ("VIP", "服装"): 0.20, 
            ("VIP", "食品"): 0.10,
            ("钻石", "电子"): 0.25,
            ("钻石", "服装"): 0.30,
            ("钻石", "食品"): 0.15,
        }
        
        return discounts.get((user_level, product_category), 0.05)


def process_single_order(service: DataService, order: Dict[str, Any]) -> Dict[str, Any]:
    """处理单个订单"""
    order_id = order["order_id"]
    user_id = order["user_id"]
    product_id = order["product_id"]
    quantity = order["quantity"]
    
    try:
        # 获取用户信息（可能命中缓存）
        user_info = service.get_user_info(user_id)
        if "error" in user_info:
            return {"order_id": order_id, "status": "失败", "error": "用户不存在"}
        
        # 获取商品信息（可能命中缓存）
        product_info = service.get_product_info(product_id)
        if "error" in product_info:
            return {"order_id": order_id, "status": "失败", "error": "商品不存在"}
        
        # 计算折扣（可能命中缓存）
        discount = service.calculate_discount(user_info["level"], product_info["category"])
        
        # 计算最终价格
        original_price = product_info["price"] * quantity
        final_price = original_price * (1 - discount)
        
        # 模拟订单处理时间
        time.sleep(0.01)
        
        return {
            "order_id": order_id,
            "user_name": user_info["name"],
            "product_name": product_info["name"],
            "quantity": quantity,
            "original_price": original_price,
            "discount": f"{discount*100:.1f}%",
            "final_price": round(final_price, 2),
            "status": "成功",
            "thread": threading.current_thread().name
        }
        
    except Exception as e:
        return {
            "order_id": order_id,
            "status": "失败", 
            "error": str(e)
        }


def demo_serial_processing():
    """串行处理演示"""
    print("=== 1. 串行处理演示 ===")
    
    service = DataService()
    
    # 生成测试订单（有重复的用户和商品ID）
    orders = []
    for i in range(1, 21):
        orders.append({
            "order_id": f"ORD_{i:03d}",
            "user_id": random.randint(1, 5),      # 5个用户，高重复率
            "product_id": random.randint(1, 3),   # 3个商品，高重复率
            "quantity": random.randint(1, 3)
        })
    
    print(f"串行处理 {len(orders)} 个订单...")
    start = time.time()
    
    results = []
    for order in orders:
        result = process_single_order(service, order)
        results.append(result)
        if result["status"] == "成功":
            print(f"  订单 {result['order_id']} 完成: {result['final_price']}元")
    
    serial_time = time.time() - start
    successful = len([r for r in results if r["status"] == "成功"])
    
    print(f"\n串行处理结果:")
    print(f"  成功: {successful}/{len(orders)} 个")
    print(f"  耗时: {serial_time:.2f}秒")
    print(f"  用户查询缓存: {service.get_user_info.cache_info()}")
    print(f"  商品查询缓存: {service.get_product_info.cache_info()}")
    print(f"  折扣计算缓存: {service.calculate_discount.cache_info()}")
    
    return serial_time


def demo_parallel_processing():
    """并行处理演示"""
    print("\n\n=== 2. 并行处理演示 ===")
    
    service = DataService()
    
    # 生成相同的测试订单
    orders = []
    for i in range(1, 21):
        orders.append({
            "order_id": f"ORD_{i:03d}",
            "user_id": random.randint(1, 5),      # 5个用户，高重复率
            "product_id": random.randint(1, 3),   # 3个商品，高重复率
            "quantity": random.randint(1, 3)
        })
    
    print(f"并行处理 {len(orders)} 个订单 (4个线程)...")
    start = time.time()
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有订单处理任务
        future_to_order = {
            executor.submit(process_single_order, service, order): order["order_id"]
            for order in orders
        }
        
        # 按完成顺序收集结果
        for future in concurrent.futures.as_completed(future_to_order):
            order_id = future_to_order[future]
            try:
                result = future.result()
                results.append(result)
                if result["status"] == "成功":
                    print(f"  订单 {result['order_id']} 完成: {result['final_price']}元 - 线程: {result['thread']}")
            except Exception as e:
                print(f"  订单 {order_id} 异常: {e}")
    
    parallel_time = time.time() - start
    successful = len([r for r in results if r["status"] == "成功"])
    
    print(f"\n并行处理结果:")
    print(f"  成功: {successful}/{len(orders)} 个")
    print(f"  耗时: {parallel_time:.2f}秒")
    print(f"  用户查询缓存: {service.get_user_info.cache_info()}")
    print(f"  商品查询缓存: {service.get_product_info.cache_info()}")
    print(f"  折扣计算缓存: {service.calculate_discount.cache_info()}")
    
    return parallel_time


def demo_cache_effectiveness():
    """缓存效果演示"""
    print("\n\n=== 3. 缓存效果演示 ===")
    
    # 无缓存版本的服务
    class NoCacheDataService:
        def __init__(self, cached_service):
            self.users_db = cached_service.users_db
            self.products_db = cached_service.products_db
        
        def get_user_info(self, user_id: int) -> Dict[str, Any]:
            time.sleep(0.05)  # 模拟数据库查询
            return self.users_db.get(user_id, {"error": "用户不存在"})
        
        def get_product_info(self, product_id: int) -> Dict[str, Any]:
            time.sleep(0.03)  # 模拟数据库查询
            return self.products_db.get(product_id, {"error": "商品不存在"})
        
        def calculate_discount(self, user_level: str, product_category: str) -> float:
            time.sleep(0.02)  # 模拟复杂计算
            discounts = {
                ("VIP", "电子"): 0.15,
                ("钻石", "电子"): 0.25,
            }
            return discounts.get((user_level, product_category), 0.05)
    
    # 创建相同的测试数据
    test_queries = [
        (1, 1), (2, 1), (1, 2), (3, 1), (1, 1),  # 重复查询
        (2, 2), (1, 1), (4, 1), (2, 1), (1, 2)   # 更多重复
    ]
    
    # 测试有缓存版本
    cached_service = DataService()
    start = time.time()
    for user_id, product_id in test_queries:
        user_info = cached_service.get_user_info(user_id)
        product_info = cached_service.get_product_info(product_id)
        discount = cached_service.calculate_discount(user_info["level"], product_info["category"])
    cached_time = time.time() - start
    
    # 测试无缓存版本
    no_cache_service = NoCacheDataService(cached_service)
    start = time.time()
    for user_id, product_id in test_queries:
        user_info = no_cache_service.get_user_info(user_id)
        product_info = no_cache_service.get_product_info(product_id)
        discount = no_cache_service.calculate_discount(user_info["level"], product_info["category"])
    no_cache_time = time.time() - start
    
    print("缓存效果对比:")
    print(f"  无缓存耗时: {no_cache_time:.2f}秒")
    print(f"  有缓存耗时: {cached_time:.2f}秒")
    print(f"  缓存提升: {no_cache_time/cached_time:.1f}倍")
    
    # 显示缓存统计
    print(f"\n缓存统计:")
    print(f"  用户查询: {cached_service.get_user_info.cache_info()}")
    print(f"  商品查询: {cached_service.get_product_info.cache_info()}")
    print(f"  折扣计算: {cached_service.calculate_discount.cache_info()}")


def main():
    """主函数"""
    print("🔄 线程池 + LRU缓存 综合应用示例")
    print("="*60)
    
    # 运行演示
    serial_time = demo_serial_processing()
    parallel_time = demo_parallel_processing()
    demo_cache_effectiveness()
    
    # 总结
    print("\n" + "="*60)
    print("📊 性能对比总结:")
    print(f"  串行处理耗时: {serial_time:.2f}秒")
    print(f"  并行处理耗时: {parallel_time:.2f}秒")
    print(f"  并行性能提升: {serial_time/parallel_time:.1f}倍")
    
    print("\n💡 关键收益:")
    print("1. 线程池：通过并发执行提升整体处理速度")
    print("2. LRU缓存：避免重复的数据库查询和计算")
    print("3. 两者结合：获得最佳的性能优化效果")
    print("4. 线程安全：lru_cache 是线程安全的")


if __name__ == "__main__":
    main()