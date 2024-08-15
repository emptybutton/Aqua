import loguru


logger = loguru.logger
logger.add(
    "logs/_{time:YYYY-MM-DD!UTC}.log",
    format="[{time:HH:mm.ss!UTC}] {level}: {message}",
    rotation="00:00",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
