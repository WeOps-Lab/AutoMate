import os.path
import sys

from core.settings import settings

LOGURU_CONFIG = {
    "handlers": [
        {
            "sink": sys.stdout,
            "level": settings.logging_level,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {thread.name} | "
            "<level>{level}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>"
            ":<cyan>{line}</cyan> - <level>{message}</level>",
        },
        {
            "sink": os.path.join(settings.logging_dir, "automate.log"),
            "level": settings.logging_level,
            "enqueue": True,  # 多进程安全
            "rotation": "100 MB",
            "retention": "1 week",
            "encoding": "utf-8",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} "
            ": {function}:{line} -  {message}",
        },
        {
            "sink": os.path.join(settings.logging_dir, "error.log"),
            "enqueue": True,
            "level": "ERROR",
            "retention": "1 week",
            "rotation": "100 MB",
            "encoding": "utf-8",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} "
            ": {function}:{line} -  {message}",
        },
    ],
}

LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")
