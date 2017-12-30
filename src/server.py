# server.py
######################################################################################
# This file contains the server code that is used to handle client requests.
######################################################################################

import socket
import sys
import threading
import time
from command_handler import *
import server_commands

class ServerThread(threading.Thread):
    def __init__(self, threadID, name, conn):
        threading.Thread.__init__(self)
        self.thread_id = threadID
        self.thread_name = name
        self.sock = conn

    def run(self):
        # Sending welcome message to connected client
        self.sock.send('Welcome to the py-chat-server.\n')
        reply = 'NULL'
        # Keep on receiving request commands from the remote host
        while True:

            # Receiving from client
            try:
                mesg = self.sock.recv(4096)
            except socket.error, msg:
                print msg
                print 'Closing connection now'
                break
            if (mesg is None) or (len(mesg) == 0):
                self.sock.sendall(reply + '\n')
                break
            
            # TODO...
            # Parse the message and take appropriate actions. For example, the data received may be request to
            # create a new user account, or even a simple text message to be sent to other user.
            # The py-chat-server understands a set of commands described in the file docs/commands.txt.
            mesg.strip()
            print 'Mesg: ' + mesg
            status = 0
            cmd = parse_command(mesg)
            if cmd.type() != -1:
                status = cmd.execute()
                reply = 'OK'
            else:
                reply = 'UNKNOWN_COMMAND'
                del cmd
            self.sock.sendall(reply + '\n')
            # Disconnect
            if status == 1:
                self.sock.close()
                break

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

    tid = 0
    # Now keep accepting client requests
    try:
        while 1:
            # Check server commands
            if server_commands.server_shutdown == True:
                shutdown_server(init_sock)
                break

            print 'Waiting for connection...' + str(server_commands.server_shutdown)
            conn = None
            # wait to accept a connection
            # FIXME... Does not respond to keyboardinterrupt at all (Windows-only problem)
            (conn, addr) = init_sock.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])

            server_thread = ServerThread(tid, 'ServerThread'+str(tid), conn)
            tid += 1
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