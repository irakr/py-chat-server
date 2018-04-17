# operations.py
###########################################################################
# Here we define the classes and methods that actually implement the
# operations performed by the server.
###########################################################################
import socket
import threading
import server_config as sconf
import logging_wrapper as logw
dlogger = logw.DLogger(__name__)
elogger = logw.ELogger()

# Base class for all types of operations.
class ServerOperation(object):

    # States of an operation
    STARTED     = 1
    RUNNING     = 2
    PAUSED      = 3
    FINISHED    = 0

    """
    Params:
        args (list) --- list() of arguments to the command.
    """
    def __init__(self, args):
        self.__state = ServerOperation.RUNNING
        self._args = args[:]

    def do_it(self):
        pass

    # This is a very handy and common operation needed.
    def __get_listenning_sock(self):
        try:
            init_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
        except socket.error as e:
            dlogger.log(e)
            sys.exit()

        sock.listen(10)

# The operation for the PING command
## Syntax of PING commdand:
## ---   %PING 192.168.40.5 12720
## ---   %PING <Host> <Port>
####################################
class PingOperation(ServerOperation):
    def __init__(self, *args):
        super(PingOperation, self).__init__(*args)

    def do_it(self):
        dlogger.log('In PingOperation.do_it()')
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ## ----------------                  <Host_addr>      <Port_no>
        udp_sock.sendto("PING FROM {} {}".format(sconf.HOST_ADDR, sconf.PORT_NO), (self._args[0], int(self._args[1])))
        udp_sock.settimeout(5)

        # Try pinging.
        attempts = 3
        buff = ''
        for attempt in xrange(0, attempts):
            elogger.log('Attempting... ' + str(attempt + 1))
            if attempt > attempts:
                break
            try:
                buff, ret_addr = udp_sock.recvfrom(1024)
            except socket.timeout as to:
                continue
            if len(buff) > 0:
                break

        caller_addr = threading.current_thread().remote_addr()
        udp_sock_ret = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if len(buff) > 0:
            if buff == 'PING OK':
                elogger.log('Perfect!')
                udp_sock_ret.sendto('PING OK', (caller_addr[0], caller_addr[1]))
        else:
            elogger.log('No response!')
            return -1
            #udp_sock_ret.sendto('PING FAILED', (caller_addr[0], caller_addr[1]))

        udp_sock.close()
        udp_sock_ret.close()

        self.__state = ServerOperation.FINISHED
        return 0
