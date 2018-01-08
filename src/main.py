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
    dlogger.log('Begin main()')
    sconf.config_server()
    elogger.log('Hostname: ' + sconf.HOST_ADDR)
    elogger.log('Port: ' + str(sconf.PORT_NO))
    start_server(sconf.HOST_ADDR, sconf.PORT_NO)

# Call main function.
if __name__ == "__main__":
    dlogger = logw.DLogger(__name__)
    elogger = logw.ELogger()
    exit(main())
