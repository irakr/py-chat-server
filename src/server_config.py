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

# Setup the server using the file 'server.cfg'
def config_server():
    print 'In config_server()'
    try:
        config_file = open(server_conf_file, 'r')
    except IOError:
        print 'No config file detected. Default configurations will be applied.'
        return (None, None)

    global HOST_ADDR, PORT_NO

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
    config_file.close()
