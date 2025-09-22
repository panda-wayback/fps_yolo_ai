import logging
import sys
from logging.handlers import RotatingFileHandler
from functools import wraps
import time


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
    
    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 控制台 Handler（带颜色）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    try:
        import colorlog
        console_handler.setFormatter(
            colorlog.ColoredFormatter(
                fmt="%(log_color)s%(asctime)s [%(levelname)-8s] %(filename)s:%(lineno)d - %(message)s",
                datefmt="%H:%M:%S",
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
_default_logger = setup_logger(level=logging.INFO)


def get_logger(name: str = "app") -> logging.Logger:
    """获取日志器"""
    if name == "app":
        return _default_logger
    return setup_logger(name)


def log_time(func):
    """记录函数执行时间的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start = time.time()
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} 执行时间: {time.time() - start:.3f}s")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} 执行失败: {e}")
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