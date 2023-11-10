from loguru import logger as Logger

logger = Logger
cmp_logger = Logger.bind(name="cmp")
collect_logger = Logger.bind(name="collect")
