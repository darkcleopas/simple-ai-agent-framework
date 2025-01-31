import logging
import sys
from config.config import Config

def setup_logging(config: Config) -> logging.Logger:
    """
    Setup logging configuration based on the provided config
    
    Args:
        config (Config): Application configuration object
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('agent')
    
    # Set log level from config
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Add debug handler if debug mode is enabled
    if config.debug:
        debug_handler = logging.FileHandler('debug.log')
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)
    
    return logger 