# logging_wrapper.py
########################################################################
# Just a wrapper over logging module that provides an easier API and
# shorter code.
########################################################################
import logging

# Change these values to modify logger.
log_format = "[%(levelname)s][%(asctime)s] M/%(name)s \"\" %(message)s \"\""
log_level = logging.DEBUG

# A wrapper function to create a new logger instance
def createLogger(module='??'):
    logger = logging.getLogger(module)
    logger.setLevel(log_level)
    sh = logging.StreamHandler()
    sh.setLevel(log_level)
    formatter = logging.Formatter(log_format)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger
