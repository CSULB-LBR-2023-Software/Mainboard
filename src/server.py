# TO RUN: python3 server.py "$(grep "XX4XXX" radio.txt)"

import os
import socket
import sys

default_msg = "XX4XXX D4 F6 G7 C3 E5 F6 H8 C3 break"

# EXIT CALL CHECK --------------------------------------------|
def check_cont(msg: str) -> bool:
    """
    Checks for exit signal
    @param string args
    @return false if signal found, otherwise true
    """
    msg = msg[1].split("\n")
    print(msg)
    for val in msg:
        if val == "XX5XXX exit":
            return False
    return True


if __name__ == "__main__":
    msg = sys.argv
    if not check_cont(msg):
        sys.exit(0)

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
