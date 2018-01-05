# server.py
######################################################################################
# This file contains the server code that is used to handle client requests.
######################################################################################

import socket
import sys
import threading
import time
from command_handler import *
import server_config
import user


# TODO... Keep a global dictionary of all the server threads.
# There are many advantages in doing this. Example, when shutting down the
# server it will be easier to notify all the servers to terminate their
# communication.
server_threads = {}

# Individual server threads for each client
class ServerThread(threading.Thread):

    def __init__(self, conn, remote_addr):
        threading.Thread.__init__(self)
        self.__sock = conn
        self.__remote_addr = remote_addr
        # Set server thread name as <IP>:<PORT>. This will make it easy to
        # search for a particular server thread.
        addr_port = remote_addr[0] + ':' + str(remote_addr[1])
        self.name = '<TH>' + addr_port[:]
        #server_threads.append(self)
        server_threads[addr_port] = self
        print '--->' + server_threads[addr_port].name


    def run(self):
        # Sending welcome message to connected client
        self.__sock.send('Welcome to the py-chat-server.')

        # Keep on receiving request commands from the remote host
        while True:

            # Receiving from client
            try:
                mesg = self.__sock.recv(4096)
            except socket.error as e:
                print "error {0}:{1}".format(e.errno, e.strerror)
                self.__close_connection()
                break
            if (mesg is None) or (len(mesg) == 0):
                print 'Lost connection with ' + self.__remote_addr[0] + ':' + str(self.__remote_addr[1])
                self.__close_connection()
                break

            # TODO...
            # Parse the message and take appropriate actions. For example, the data received may be request to
            # create a new user account, or even a simple text message to be sent to other user.
            # The py-chat-server understands a set of commands described in the file docs/commands.txt.
            mesg.strip()
            print '\n[' + self.__sock.getpeername()[0] + ']: ' + mesg

            # Get command type
            cmd = parse_command(mesg)

            # Invalid command type
            if cmd is None:
                self.__sock.sendall('UNKNOWN_COMMAND')
                continue

            # Execute command.
            status = cmd.execute()
            if status == 0:
                self.__sock.sendall('OK')
            elif status == -1:
                self.__sock.sendall('UNKNOWN_COMMAND')

    # Logout the user
    def __close_connection(self):
        print 'Disconnecting ' + self.__remote_addr[0] + ':' + str(self.__remote_addr[1])
        self.__sock.sendall('BYE')
        self.__sock.close()
        try:
            key = self.__remote_addr[0] + ':' + str(self.__remote_addr[1])
            del server_threads[key]
        except KeyError:
            pass # Silently delete the key

# Setup the server using the file 'server.cfg'
def config_server():
    return (None, None)
    '''
    print 'In config_server()'
    try:
        config_file = open('server.cfg', 'r')
    except IOError:
        print 'No config file detected. Default configurations will be applied.'
        return (None, None)

    host_name = '' #socket.gethostname()
    port_no = config_file.readline()
    print port_no
    config_file.close()
    return (host_name[:], int(port_no[:]))
    '''

# Start the server socket
def start_server(host, port):
    init_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Initial socket created'

    try:
        init_sock.bind((host, port))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print 'Socket bind complete'

    init_sock.listen(10)
    print 'Socket now listening'

    # Now keep accepting client requests
    try:
        while 1:
            # Check server commands
            if server_config.server_shutdown == True:
                # TODO... Try to interrupt accept()
                shutdown_server(init_sock)
                break

            print 'No of server threads currently active: ' + str(len(server_threads))
            print 'Waiting for connection...' + str(server_config.server_shutdown)
            conn = None
            # wait to accept a connection
            # FIXME... Does not respond to keyboardinterrupt at all (Windows-only problem)
            (conn, addr) = init_sock.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])

            # Create a new server thread
            server_thread = ServerThread(conn, addr)
            server_thread.start()

    except KeyboardInterrupt:
        print '[KeyboardInterrupt] Exiting server...'
    finally:
        shutdown_server(init_sock)

def shutdown_server(sock):
    print 'Shutting down server...'
    if sock:
        sock.close

    #sys.exit()
