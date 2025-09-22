import logging
import sys
from logging.handlers import RotatingFileHandler

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

    # 日志格式：时间 等级 文件:行号 - 消息
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
        # 没装 colorlog 就用普通格式
        pass

    # 文件 Handler（自动轮转）
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 获取/创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加 handler
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    # 测试用例
    logger = setup_logger()
    logger.info("测试用例")
    logger.error("测试用例")
    logger.warning("测试用例")
    logger.debug("测试用例")
    logger.critical("测试用例")