# main.py
######################################################################################
# The main program.
# The whole server program begins here.
######################################################################################

import sys
from server import *
import server_config as sconf
import logging_wrapper as logw

# Main function
def main():
    logger.debug('Begin main()')
    sconf.config_server()
    print 'Hostname: ' + sconf.HOST_ADDR
    print 'Port: ' + str(sconf.PORT_NO)
    start_server(sconf.HOST_ADDR, sconf.PORT_NO)

# Call main function.
if __name__ == "__main__":
    logger = logw.createLogger(__name__)
    exit(main())
