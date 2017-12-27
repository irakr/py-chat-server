import sys
from server import *

# Verify main file
if __name__ != "__main__":
    print 'Error: Not in main.py'
    exit()

# Main function
def main():
    (host, port) = config_server()
    if host is None or port is None:
        host = ''
        port = 8888
    start_server(host, port)

# Call main function
exit(main())