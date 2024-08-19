import structlog


dev_logger = structlog.wrap_logger(structlog.PrintLogger())
