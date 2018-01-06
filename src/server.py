# server.py
######################################################################################
# This file contains the server code that is used to handle client requests.
######################################################################################

import socket
import sys
import threading
import time
from command_handler import parse_command
import server_config
import user
from exceptions_types import *

# TODO... Keep a global dictionary of all the server threads.
# There are many advantages in doing this. Example, when shutting down the
# server it will be easier to notify all the servers to terminate their
# communication.
# Key = '<ServerIP>:<ServerPORT>'
server_threads = {}

# Individual server threads for each client
class ServerThread(threading.Thread):

    def __init__(self, conn, remote_addr):
        threading.Thread.__init__(self)
        self.__sock = conn
        self.__remote_addr = remote_addr

        # TODO
        # For now we use a Dummy user for communication.
        self.__current_user = user.AdminUser(1111, 'irak101')

        # Set server thread name as <IP>:<PORT>. This will make it easy to
        # search for a particular server thread.
        addr_port = remote_addr[0] + ':' + str(remote_addr[1])
        self.name = '<TH>' + addr_port[:]
        server_threads[addr_port] = self
        print '--->' + server_threads[addr_port].name

        self.time_to_stop = False

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

            # TODO... Change this to exception handling instead of return value.
            # Execute command
            try:
                status = cmd.execute()
                # Errors may be handled withing execute(). Here error codes
                # are checked only to reply to the client.
                if status == 0:
                    self.__sock.sendall('OK')
                elif status == -1:
                    self.__sock.sendall('UNKNOWN_COMMAND')
                elif status == -2:
                    self.__sock.sendall('INVALID_ARGUMENT')
                # XXX... Any other code not yet checked.

            except ServerShutdownRequest as exc:
                # Verify privilege and take actions.
                if exc.privilege < 2:
                    self.__sock.sendall('OPERATION_NOT_ALLOWED')
                else:
                    self.__sock.sendall('GOODBYE ALL!')
                    server_config.server_shutdown = True
                    self.__close_connection()
                    # TODO...Also terminate connections to all other clients.
                    unblock_main()
                    return

            # Time to end the this thread
            if self.time_to_stop == True:
                self.__sock.sendall('BYE')
                self.__close_connection()
                return

    # Return the current_user
    def current_user(self):
        return self.__current_user


    # Logout the user
    def __close_connection(self):
        print 'Disconnecting ' + self.__remote_addr[0] + ':' + str(self.__remote_addr[1])
        #self.__sock.sendall('BYE')
        self.__sock.close()
        try:
            key = self.__remote_addr[0] + ':' + str(self.__remote_addr[1])
            del server_threads[key]
        except KeyError:
            pass # Silently delete the key

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
            print '\t\t\t\t\t#Clients: ' + str(len(server_threads))
            print 'Awaiting connection...'
            conn = None
            # wait to accept a connection
            # FIXME... Does not respond to keyboardinterrupt at all (Windows-only problem)
            (conn, addr) = init_sock.accept()
            if server_config.server_shutdown == True:
                print 'Shutting down server now.'
                raise ServerShutdownRequest(2)
            print 'Connected with ' + addr[0] + ':' + str(addr[1])

            # Create a new server thread
            server_thread = ServerThread(conn, addr)
            server_thread.start()

    except KeyboardInterrupt:
        print '[KeyboardInterrupt] Exiting server...'
    except ServerShutdownRequest as e:
        print repr(e)
    except Exception as e:
        print '[EXCEPTION]: ' + repr(e)
    finally:
        shutdown_server(init_sock)

def shutdown_server(sock):
    print 'Shutting down server...'
    if sock:
        sock.close()
    exit(0)

# Bring out the main thread from the socket.accpet() call.
def unblock_main():
    print 'In unblock_main()'
    import os
    cpid = os.fork()
    if cpid != 0:
        print 'Parent: {}'.format(os.getpid())
        return
    # Child process will do the rest.
    print 'Child: {}'.format(os.getpid())
    try:
        just_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        just_sock.bind(('localhost', server_config.UNBLOCKER_PORT))
        just_sock.connect((server_config.HOST_ADDR, server_config.PORT_NO))
        print '{} Connected to server'.format(os.getpid())
        just_sock.sendall("It's just me. Shutdown now!")
        just_sock.close()
    except socket.error as e:
        print e
        sys.exit()
