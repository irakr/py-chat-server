import socket
import sys
import struct
import time
import threading
import server_config as sconf

class PingThread(threading.Thread):
    def run(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.settimeout(5)
        while 1:
            try:
                mesg, addr = udp_sock.recvfrom(1024)
            except socket.timeout as to:
                print 'socket.recvfrom() timed out.'
                time.sleep(1)
                continue
            if len(mesg) > 0:
                udp_sock.sendto('PING OK', (addr[0], addr[1]))

if(len(sys.argv) < 2) :
    print 'Usage : python client.py hostname'
    sys.exit()

sconf.config_server()

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

try:
    remote_ip = socket.gethostbyname( sconf.HOST_ADDR )
except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

try:
    s.connect((sconf.HOST_ADDR, sconf.PORT_NO))
except socket.error:
    print 'Server is currently offline.'
    sys.exit()

print 'Socket Connected to ' + sconf.HOST_ADDR + ' on ip ' + remote_ip

# FIXME... Some weird BUG.
# Run PING thread.
#PingThread().start()

# main loop
while 1:
    try :
        m = s.recv(1024)
        print 'SERVER: ' + m
        #Set the whole string
        while True:
            # Prompt user to enter a command to be sent to the server
            message = raw_input('> ')
            message.strip()
            # Ignore blank message
            if len(message) == 0:
                continue
            s.send(message)
            print 'Message sent successfully'
            m = s.recv(1024)
            if m == 'BYE':
                print 'Logging out...'
                break
            time.sleep(1)
            print 'SERVER: ' + m
    except socket.error, msg:
        #Send failed
        print msg
        sys.exit()

s.close()
