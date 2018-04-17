# command_types.py
#_____________________________________________________________________________
#############################################################################
# The class heirarchy of each command types.
# These classes provide a very structured interface to the actual operations
# that the server executes according to the commands.
#############################################################################
import threading
import server
from exceptions_types import *
import operations
import logging_wrapper as logw
dlogger = logw.DLogger(__name__)
elogger = logw.ELogger()

# Base class of all command types.
class CommandBase(object):
    # Execute the corresponding action intended by the command and list of args.
    def execute(self, cmd, args):
        pass

# Info query command
class QueryCommand(CommandBase):
    def execute(self, cmd, args):
        dlogger.log('In QueryCommand.execute()')
        return 0

# Info updation command
class InfoUpdateCommand(CommandBase):
    def execute(self, cmd, args):
        dlogger.log('In InfoUpdateCommand.execute()')
        return 0

# User control command
class UserControlCommand(CommandBase):
    def execute(self, cmd, args):
        dlogger.log('In UserControlCommand.execute()')

        if cmd == 'TEST':
            print elogger.log('Testing...')

        elif cmd == 'PING':
            if len(args) == 0:
                dlogger.log('Argument NULL!!!')
                return -2
            elogger.log('Pinging ' + str(args))
            # TODO... Change the return value scheme
            if operations.PingOperation(args).do_it() != 0:
                return -3

        elif cmd == 'LOGOUT':
            elogger.log('Logging out user...')
            threading.current_thread().time_to_stop = True

        else:
            elogger.log('Unknown command: ' + cmd)
            return -1

        return 0

# Server control command (Needs administrative privilege)
class ServerControlCommand(CommandBase):
    def execute(self, cmd, args):
        dlogger.log('In ServerControlCommand.execute()')

        if cmd == 'SHUTDOWN':
            raise ServerShutdownRequest(threading.current_thread().current_user().privilege)
        else:
            print 'Unknown command: ' + cmd
            return -1
        return 0
