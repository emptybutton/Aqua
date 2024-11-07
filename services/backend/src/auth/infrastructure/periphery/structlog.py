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

prod_logger = structlog.wrap_logger(
    structlog.PrintLogger(),
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
)