import logging

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def info_logger(function_name, message, **kwargs):
    """Log an informational message with additional context."""
    log_message = {"function_name": function_name, "message": message}
    if kwargs:
        log_message.update(kwargs)
    logger.info(log_message)

def error_logger(function_name, message, **kwargs):
    """Log an error message with additional context."""
    log_message = {"function_name": function_name, "message": message}
    if kwargs:
        log_message.update(kwargs)
    logger.error(log_message)


def log_route_access(function_name, route_path):
    """Log access to a specific route."""
    info_logger(function_name, f"Accessed route: {route_path}")