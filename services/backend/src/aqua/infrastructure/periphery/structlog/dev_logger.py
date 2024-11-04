import structlog


dev_logger = structlog.wrap_logger(
    structlog.PrintLogger(),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(fmt="%H:%M:%S.%f", utc=False),
        structlog.dev.ConsoleRenderer(),
    ],
)
