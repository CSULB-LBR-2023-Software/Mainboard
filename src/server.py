
import os
import socket
import sys
import time

import lib.logging as log


# COMMUNICATION --------------------------------------|

def readSendLoop() -> None:
    """
    Continuously read from stdin and send to client.
    """
    while True:
        line = sys.stdin.readline()
        if not line:
            continue
        print("Line:", line)
        time.sleep(4)
        client.send(bytes(line, "utf-8"))


# CREATE A SERVER --------------------------------------------|

if __name__ == "__main__":
    SERVER = "/tmp/uds_socket"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        os.unlink(SERVER)
    except OSError:
        if os.path.exists(SERVER):
            raise

    # Bind server to client
    sock.bind(SERVER)
    sock.listen(4)

    while True:
        try:
            client, client_addy = sock.accept()
            print(f"Connection to {client_addy} established.")
            if not client:
                continue
            readSendLoop()
        except KeyboardInterrupt:
            sock.close()
            print("Closing connection")
    sock.close()
