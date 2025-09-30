#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试两种单例模式的区别
"""

from utils.singleton import singleton, SingletonMeta


# 方式1: 装饰器单例
@singleton
class DecoratorSingleton:
    def __init__(self):
        self.value = "装饰器单例"


# 方式2: 元类单例
class MetaclassSingleton(metaclass=SingletonMeta):
    def __init__(self):
        self.value = "元类单例"


if __name__ == "__main__":
    print("=" * 60)
    print("单例模式测试")
    print("=" * 60)
    
    # 测试装饰器单例
    print("\n【装饰器单例】")
    d1 = DecoratorSingleton()
    d2 = DecoratorSingleton()
    print(f"d1 is d2: {d1 is d2}")  # True - 是同一个对象
    print(f"d1.value: {d1.value}")
    print(f"type(DecoratorSingleton): {type(DecoratorSingleton)}")  # function!
    print(f"isinstance(d1, DecoratorSingleton): 会报错")
    try:
        print(isinstance(d1, DecoratorSingleton))
    except TypeError as e:
        print(f"  错误: {e}")
    
    # 测试元类单例
    print("\n【元类单例】")
    m1 = MetaclassSingleton()
    m2 = MetaclassSingleton()
    print(f"m1 is m2: {m1 is m2}")  # True - 是同一个对象
    print(f"m1.value: {m1.value}")
    print(f"type(MetaclassSingleton): {type(MetaclassSingleton)}")  # SingletonMeta
    print(f"isinstance(m1, MetaclassSingleton): {isinstance(m1, MetaclassSingleton)}")  # True
    
    print("\n" + "=" * 60)
    print("结论：")
    print("  装饰器单例: 简单，但类变成了函数")
    print("  元类单例: 保持类的本质，更强大")
    print("=" * 60)
