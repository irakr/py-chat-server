# main.py
######################################################################################
# The main program.
######################################################################################

import sys
from server import *
import server_config as sconf

# Verify main file
if __name__ != "__main__":
    print 'Error: Not in main.py'
    exit(1)

# Main function
def main():
    sconf.config_server()
    print 'Hostname: ' + sconf.HOST_ADDR
    print 'Port: ' + str(sconf.PORT_NO)
    start_server(sconf.HOST_ADDR, sconf.PORT_NO)

# Call main function
exit(main())
