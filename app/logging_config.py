import logging
from structlog import configure, processors, get_logger

configure(
    processors=[
        processors.add_log_level,
        processors.TimeStamper(fmt="iso"),
        processors.format_exc_info,
        processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=logging.getLogger,
)