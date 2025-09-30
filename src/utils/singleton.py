#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单例模式工具
提供装饰器和元类两种实现方式
"""

import threading
from functools import wraps


def singleton(cls):
    """
    单例装饰器（线程安全）
    
    使用方法：
    @singleton
    class MyClass:
        def __init__(self):
            pass
    """
    instances = {}
    lock = threading.Lock()
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


class SingletonMeta(type):
    """
    单例元类（线程安全）
    
    使用方法：
    class MyClass(metaclass=SingletonMeta):
        def __init__(self):
            pass
    """
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
