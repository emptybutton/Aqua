import structlog


prod_logger = structlog.wrap_logger(
    structlog.PrintLogger(),
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
)
