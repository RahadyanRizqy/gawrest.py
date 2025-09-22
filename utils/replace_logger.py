from loguru import logger
import logging

class UvicornInterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(exception=record.exc_info).log(level, record.getMessage())

logging.getLogger("uvicorn.access").handlers = [UvicornInterceptHandler()]
logging.getLogger("uvicorn.error").handlers = [UvicornInterceptHandler()]

logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
