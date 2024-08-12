import loguru


logger = loguru.logger
logger.add(
    "_{time}.log",
    format="[{time}] {level}: {message}",
    rotation="00:00",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
