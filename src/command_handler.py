# command_handler.py
######################################################################################
# This module handles client request command related operations like -
# - Parsing command.
# - Executing command.
######################################################################################
import command_types as ct

# This is a class that handles a command execution  of the type 'Command'.
# Having a solid object for a command will provide robust features.
class CommandHandler(object):
    '''
    This class is responsible for creating and calling the actual
    command type class, i.e., sub-class of the CommandBase class
    identified by the actual command string.
    '''
    def __init__(self, __cmd_str):
        self.__cmd_str = __cmd_str[:]
        self.__cmd = None # Callback object CommandBase
        self.__cmd_type = -1
        self.__cmd_name = ''
        self.__cmd_args = []
        self.__parse_command()

    def __parse_command(self):

        ###########################################################################################
        # '=' refers to a command that requests modifying of data in the database of the server.
        # '?' refers to a command that requests retrieval of some info from the server.
        # '%' user control commands
        # '/' refers to server control commands (Special privilege is required for these commands).
        ###########################################################################################
        if (self.__cmd_str[0] != '=') and (self.__cmd_str[0] != '?') and (self.__cmd_str[0] != '%') and (self.__cmd_str[0] != '/'):
            print '[Error]: Invalid command: ' + self.__cmd_str
            self.__cmd_type = -1 # Invalid command
            return

        # Set command type
        no_args = False
        token = self.__cmd_str[0]
        if token == '?':
            self.__cmd_type = 0 # Info query command
            self.__cmd = ct.QueryCommand()
        elif token == '=':
            self.__cmd_type = 1 # info modifying command
            self.__cmd = ct.InfoUpdateCommand()
        elif token == '%':
            self.__cmd_type = 2 # User control command
            self.__cmd = ct.UserControlCommand()
        elif token == '/':
            self.__cmd_type = 3 # Server control command (Needs administrative privilege)
            self.__cmd = ct.ServerControlCommand()

        # Extract command name
        try:
            token = self.__cmd_str[1 : self.__cmd_str.index(' ')]
        except ValueError:
            # This means no args are present
            token = self.__cmd_str[1:]
            no_args = True

        # Set command name
        self.__cmd_name = token[:]
        print 'Command: ' + self.__cmd_name

        # Parse out the command args if there is any.
        if no_args == True:
            return
        token = self.__cmd_str[(self.__cmd_str.index(' ') + 1):]
        self.__cmd_args = token.split(' ')

    # Accessor for __type
    def type(self):
        return self.__cmd_type

    # Execute the corresponding action intended by the command.
    def execute(self):
        print 'In CommandHandler.execute()'
        return self.__cmd.execute(self.__cmd_name, self.__cmd_args)

# Parses and creates an appropriate 'CommandHandler' object which will be used
# for executing the command's intentions whenever necesesary.
def parse_command(cmd):
    cmd_obj = CommandHandler(cmd)
    if cmd_obj.type() == -1:
        return None
    return cmd_obj
