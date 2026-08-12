import logging
import sys
from app.config import settings


def setup_logging() -> logging.Logger:
    """
    Configures application logging with clean, structured formatting.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Prevent duplicate handlers if re-initialized
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    else:
        root_logger.handlers = [handler]

    app_logger = logging.getLogger("duolingo")
    app_logger.info(f"Logging initialized. App: {settings.APP_NAME} | Env: {settings.APP_ENV} | Debug: {settings.DEBUG}")
    
    return app_logger
