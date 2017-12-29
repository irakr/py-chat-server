# command_handler.py
######################################################################################
# This module handles client request command related operations like -
# - Parsing command.
# - Executing command.
######################################################################################

# This is a class that represents a request command sent by the remote host.
# Having a solid object for a command will provide robust features.
class Command:
    def __init__(self, cmd_str):
        self.cmd_str = cmd_str[:]
        # TODO... break down command into appropriate components
        self.parse_command()

    def parse_command(self):
        pass

    # Execute the corresponding action intended by the command.
    def execute(self):
        if self.cmd_str == 'TEST':
            print 'CommandType: TEST'

# Parses and creates an appropriate 'Command' object which will be used
# for executing the command's intentions whenever necesesary.
def parse_command(cmd):
    cmd_obj = Command(cmd)
    return cmd_obj