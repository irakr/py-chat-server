# main.py
######################################################################################
# The main program.
######################################################################################

import sys
from server import *

# Verify main file
if __name__ != "__main__":
    print 'Error: Not in main.py'
    exit()

# Main function
def main():
    (host, port) = config_server()
    # Use default settings
    if host is None or port is None:
        host = ''
        port = 9000
    print 'Hostname: ' + str(host)
    print 'Port: ' + str(port)
    start_server(host, port)

# Call main function
exit(main())