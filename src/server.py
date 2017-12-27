import socket
import sys
from thread import *

# Setup the server using the file 'server.cfg'
def config_server():
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
            # wait to accept a connection
            (conn, addr) = init_sock.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])

            # start new thread
            start_new_thread(client_comm_thread, (conn,))
    except KeyboardInterrupt:
        print 'Exiting server...'
    finally:
        conn.close()
        init_sock.close()

    #init_sock.close()


# This is a thread method that communicates with a client
def client_comm_thread(conn):
    #Sending message to connected client
    conn.send('Welcome to the py-chat-server. Receving Data...\n')

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        if data is None:
            conn.send('BAD\n')
            break
        print data
        conn.sendall('OK\n')

    conn.close()