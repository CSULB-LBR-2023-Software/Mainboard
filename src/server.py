# TO RUN: python3 server.py "$(grep "XX4XXX" radio.txt)"

import os
import socket
import sys


# CREATE A SERVER --------------------------------------------|

if __name__ == "__main__":
    msg = sys.argv[1:]
    print(msg)
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
            for val in msg:
                client.send(bytes(val, "utf-8"))
        finally:
            print("Closing connection")
            sock.close()
