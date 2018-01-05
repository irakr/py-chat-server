# command_types.py
#################################################################
# The class heirarchy of each command types.
#################################################################

# Base class of all command types.
class CommandBase:
    # Execute the corresponding action intended by the command and list of args.
    def execute(self, cmd, args):
        pass

# Info query command
class QueryCommand(CommandBase):
    def execute(self, cmd, args):
        print 'In QueryCommand.execute()'
        return 0

# Info updation command
class InfoUpdateCommand(CommandBase):
    def execute(self, cmd, args):
        print 'In InfoUpdateCommand.execute()'
        return 0

# User control command
class UserControlCommand(CommandBase):
    def execute(self, cmd, args):
        print 'In UserControlCommand.execute()'
        if cmd == 'TEST':
            print 'Testing...'
        elif cmd == 'LOGOUT':
            print 'Logging out user...'
        else:
            print 'Unknown command: ' + cmd
            return -1
        return 0

# Server control command (Needs administrative privilege)
class ServerControlCommand(CommandBase):
    def execute(self, cmd, args):
        print 'In ServerControlCommand.execute()'
        import server_config
        if cmd == 'SHUTDOWN':
            server_config.server_shutdown = True
        else:
            print 'Unknown command: ' + cmd
            return -1
        return 0
