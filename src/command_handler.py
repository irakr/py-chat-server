# command_handler.py
######################################################################################
# This module handles client request command related operations like -
# - Parsing command.
# - Executing command.
######################################################################################

# This is a class that represents a request command sent by the remote host.
# Having a solid object for a command will provide robust features.
class Command:
    'Stores a string command as a well formatted object'
    def __init__(self, __cmd_str):
        self.__cmd_str = __cmd_str[:]
        # TODO... break down command into appropriate components
        self.__parse_command()

    def __parse_command(self):

        ###########################################################################################
        # '=' refers to a command that requests modifying of data in the database of the server.
        # '?' refers to a command that requests retrieval of some info from the server.
        # '/' refers to server control commands (Special privilege is required for these commands).
        ###########################################################################################
        if (self.__cmd_str[0] != '=') and (self.__cmd_str[0] != '?') and (self.__cmd_str[0] != '%') and (self.__cmd_str[0] != '/'):
            print '[Error]: Invalid command: ' + self.__cmd_str
            self.__type = -1 # Invalid command
            return

        # Set command type
        no_args = False
        token = self.__cmd_str[0]
        if token == '?':
            self.__type = 0 # Info query command
        elif token == '=':
            self.__type = 1 # Value modifying command
        elif token == '%':
            self.__type = 2 # User control command
        elif token == '/':
            self.__type = 3 # Server control command (Needs administrative privilege)
        try:
            token = self.__cmd_str[1 : self.__cmd_str.index(' ')]
        except ValueError:
            token = self.__cmd_str[1:]
            no_args = True
        
        # Set command name
        self.__name = token[:]
        print 'Command: ' + self.__name
        
        # Parse out the command args if there is any
        if no_args == True:
            return
        token = self.__cmd_str[(self.__cmd_str.index(' ') + 1):]
        self.__args = token.split(' ')

    def type(self):
        return self.__type

    # Execute the corresponding action intended by the command.
    def execute(self):
        print 'In Command.execute()'
        
        # Info query '?'
        if self.__type == 0:
            pass

        # Database modification '='
        if self.__type == 1:
            pass

        # User control '%'
        if self.__type == 2:
            if self.__name == 'LOGOUT':
                print 'Logging out user...'
                return 1

        # Server control '/'
        if self.__type == 3:
            import server_commands
            if self.__name == 'SHUTDOWN':
                server_commands.server_shutdown = True
                return 1


# Parses and creates an appropriate 'Command' object which will be used
# for executing the command's intentions whenever necesesary.
def parse_command(cmd):
    cmd_obj = Command(cmd)
    return cmd_obj