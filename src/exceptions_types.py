# exceptions.py
#########################################################
# Exception class heirarchy.
#########################################################
import logging_wrapper as logw
dlogger = logw.DLogger(__name__)
elogger = logw.ELogger()

class PyChatException(Exception):
    ''' Base class for all exceptions of the py-chat-server. '''
    pass

class ServerShutdownRequest(PyChatException):
    """ Raised when a user requests to shutdown the server entirely.

    Attributes:
        privilege -- privilege level of the user who requested this operation.
        msg -- Just a message about the exception.
    """
    def __init__(self, privilege, msg='Server shutdown requested by a module'):
        self.msg = msg
        self.privilege = privilege
