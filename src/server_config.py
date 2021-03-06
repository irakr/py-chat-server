# server_config.py
######################################################
# Global server configuration flags
######################################################

# Shutdown the server
server_shutdown = False

# The main server config file.
server_conf_file = 'server.cfg'

# All values are set with default values.

# Host address of the server.
HOST_ADDR = ''

# Port no that the server will listen on.
PORT_NO = 9000

# Port no that will be used to unblock the accept() call in the main thread.
UNBLOCKER_PORT = 15000

# Number of backlogs for listen()
LISTEN_COUNT = 10

import logging_wrapper as logw
dlogger = logw.DLogger(__name__)
elogger = logw.ELogger()

# Setup the server using the file 'server.cfg'
def config_server():
    dlogger.log('Begin config_server()')
    try:
        config_file = open(server_conf_file, 'r')
    except IOError:
        dlogger.log('No config file detected. Default configurations will be applied.')
        return (None, None)

    global HOST_ADDR, PORT_NO

    try:
        # Parse and extract values from the file.
        #while config_file
        for line in config_file:
            line = line.strip()
            if line[0] == '#':
                # Comment line
                continue
                words = line.split('=')
                if words[0] == 'host':
                    HOST_ADDR = words[1]
                elif words[0] == 'port':
                    PORT_NO = int(words[1])
                elif words[0] == 'listen':
                    LISTEN_COUNT = int(words[1])
    except TypeError as te:
        elogger.log('[%s]', repr(te))
        elogger.log('--- Wrong information in server.cfg')
        # Reset to default values.
        PORT_NO = 9000
        UNBLOCKER_PORT = 15000
        LISTEN_COUNT = 10
    
    config_file.close()
