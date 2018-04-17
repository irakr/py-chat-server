# logging_wrapper.py
########################################################################
# Just a wrapper over logging module that provides an easier API and
# shorter code.
########################################################################
import logging

# Default log filenames and properties
dlog_file = 'py-chat-dlog.log'
elog_file = 'py-chat-elog.log'
log_file_size = 1 << 20  # 1 MB
log_file_backups = 5

#### Wrapper classes and functions to create a new logger instances ####

# Just helper classes.

# Class used to log debug information only. (Only useful for developers)
class DLogger(object):
    log_format = "[%(levelname)s][%(asctime)s] M/%(name)s \"\" %(message)s \"\""
    log_level = logging.DEBUG

    def __init__(self, module='??', log_to_file=False):
        self.logger = logging.getLogger(module)
        self.logger.setLevel(DLogger.log_level)
        # log to file if True
        if log_to_file == True:
            sh = logging.RotatingFileHandler(dlog_file, maxBytes=log_file_size, backupCount=log_file_backups)
        else:
            sh = logging.StreamHandler()
        sh.setLevel(DLogger.log_level)

        formatter = logging.Formatter(DLogger.log_format)
        sh.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(sh)

    def log(self, mesg):
        self.logger.debug(mesg)

# Class used to log event information.
class ELogger(object):
    log_format = "[%(asctime)s] :: %(message)s"
    log_level = logging.INFO

    def __init__(self, log_to_file=False):
        self.logger = logging.getLogger('')
        self.logger.setLevel(ELogger.log_level)

        if log_to_file == True:
            sh = logging.RotatingFileHandler(dlog_file, maxBytes=log_file_size, backupCount=log_file_backups)
        else:
            sh = logging.StreamHandler()
        sh.setLevel(ELogger.log_level)

        formatter = logging.Formatter(ELogger.log_format)
        sh.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(sh)

    def log(self, mesg):
        self.logger.info(mesg)
