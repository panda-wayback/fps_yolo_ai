import logging
import sys
from logging.handlers import RotatingFileHandler
from functools import wraps
import time
import inspect
import os
from datetime import datetime


def setup_logger(
    name: str = "app",
    log_file: str = "app.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
) -> logging.Logger:
    """
    创建一个既输出到控制台，又输出到文件的日志器
    - 控制台：彩色日志，适合开发
    - 文件：轮转日志，适合生产
    """
    
    # 避免重复创建
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    
    # 自定义格式化器，支持毫秒精度
    class MillisecondFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            ct = datetime.fromtimestamp(record.created)
            return ct.strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]  # 去掉最后3位，保留毫秒
    
    # 日志格式
    formatter = MillisecondFormatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    )
    
    # 控制台 Handler（带颜色）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    try:
        import colorlog
        # 自定义彩色格式化器，支持毫秒精度
        class ColoredMillisecondFormatter(colorlog.ColoredFormatter):
            def formatTime(self, record, datefmt=None):
                ct = datetime.fromtimestamp(record.created)
                return ct.strftime('%H:%M:%S.%f')[:-3]  # 去掉最后3位，保留毫秒
        
        console_handler.setFormatter(
            ColoredMillisecondFormatter(
                fmt="%(log_color)s%(asctime)s [%(levelname)-8s] %(filename)s:%(lineno)d - %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green", 
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                }
            )
        )
    except ImportError:
        pass  # 没装 colorlog 就用普通格式
    
    # 文件 Handler（自动轮转）
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    
    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# 全局默认日志器
_default_logger = setup_logger(level=logging.WARN)


def get_logger(name: str = "app") -> logging.Logger:
    """获取日志器"""
    if name == "app":
        return _default_logger
    return setup_logger(name)


def log_time(func):
    """记录函数执行时间的装饰器，显示文件路径和行号"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start = time.time()
        
        # 获取函数定义位置信息（更准确）
        try:
            filename = func.__code__.co_filename
            lineno = func.__code__.co_firstlineno
            
            # 获取相对路径，更简洁
            try:
                # 尝试获取相对于项目根目录的路径
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                rel_path = os.path.relpath(filename, project_root)
            except ValueError:
                # 如果无法获取相对路径，使用文件名
                rel_path = os.path.basename(filename)
            
            location = f"{rel_path}:{lineno}"
        except Exception:
            # 如果获取失败，尝试从调用栈获取
            try:
                frame = inspect.currentframe()
                caller_frame = frame.f_back.f_back
                
                # 继续向上查找，直到找到实际的文件调用位置
                while caller_frame:
                    filename = caller_frame.f_code.co_filename
                    # 跳过装饰器文件本身和Python内置文件
                    if (not filename.endswith('logger.py') and 
                        not filename.startswith('<') and 
                        not filename.endswith('>') and
                        'site-packages' not in filename):
                        break
                    caller_frame = caller_frame.f_back
                
                if caller_frame:
                    filename = caller_frame.f_code.co_filename
                    lineno = caller_frame.f_lineno
                    
                    try:
                        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                        rel_path = os.path.relpath(filename, project_root)
                    except ValueError:
                        rel_path = os.path.basename(filename)
                    
                    location = f"{rel_path}:{lineno}"
                else:
                    location = f"{func.__module__}.{func.__name__}"
            except:
                location = func.__name__
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start
            logger.info(f"[{location}] {func.__name__} 执行时间: {execution_time:.3f}s")
            return result
        except Exception as e:
            logger.error(f"[{location}] {func.__name__} 执行失败: {e}")
            raise
    return wrapper


def log_context(message: str):
    """日志上下文管理器"""
    class Context:
        def __init__(self, msg):
            self.msg = msg
            self.logger = get_logger()
            
        def __enter__(self):
            self.logger.info(f"开始: {self.msg}")
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                self.logger.error(f"异常: {self.msg} - {exc_val}")
            else:
                self.logger.info(f"完成: {self.msg}")
    
    return Context(message)


# 便捷函数
def debug(msg): _default_logger.debug(msg)
def info(msg): _default_logger.info(msg)
def warning(msg): _default_logger.warning(msg)
def error(msg): _default_logger.error(msg)
def critical(msg): _default_logger.critical(msg)


if __name__ == "__main__":
    # 测试
    logger = get_logger()
    logger.info("测试INFO")
    logger.error("测试ERROR")
    
    @log_time
    def test_func():
        time.sleep(0.1)
        return "完成"
    
    test_func()
    
    with log_context("测试上下文"):
        time.sleep(0.05)
    
    print("测试完成")