# command_types.py
#################################################################
# The class heirarchy of each command types.
#################################################################
import threading
import server
from exceptions_types import *
import logging_wrapper as logw
logger = logw.createLogger(__name__)

# Base class of all command types.
class CommandBase(object):
    # Execute the corresponding action intended by the command and list of args.
    def execute(self, cmd, args):
        pass

# Info query command
class QueryCommand(CommandBase):
    def execute(self, cmd, args):
        logger.debug('In QueryCommand.execute()')
        return 0

# Info updation command
class InfoUpdateCommand(CommandBase):
    def execute(self, cmd, args):
        logger.debug('In InfoUpdateCommand.execute()')
        return 0

# User control command
class UserControlCommand(CommandBase):
    def execute(self, cmd, args):
        logger.debug('In UserControlCommand.execute()')

        if cmd == 'TEST':
            print 'Testing...'

        elif cmd == 'PING':
            if len(args) == 0:
                logger.error('Argument NULL!!!')
                return -2
            print 'Pinging ' + args[0]
            # TODO... ping the requested user.

        elif cmd == 'LOGOUT':
            print 'Logging out user...'
            threading.current_thread().time_to_stop = True

        else:
            print 'Unknown command: ' + cmd
            return -1

        return 0

# Server control command (Needs administrative privilege)
class ServerControlCommand(CommandBase):
    def execute(self, cmd, args):
        logger.debug('In ServerControlCommand.execute()')

        if cmd == 'SHUTDOWN':
            raise ServerShutdownRequest(threading.current_thread().current_user().privilege)
        else:
            print 'Unknown command: ' + cmd
            return -1
        return 0
