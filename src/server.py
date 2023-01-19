# TO RUN: python3 server.py "$(grep "XX4XXX" radio.txt)"

import os
import socket
import sys

CALLSIGN = "XX4XXX "

# PROCESS INCOMING DATA --------------------------------------|

def process(msg: str) -> list:
    """
    Processes incoming command string.
    @param string args
    @return list of commands
    """
    print(msg)
    for val in msg:
        seq = val.split(CALLSIGN)
        comms = seq[1].split(" ") if len(seq) > 1 else seq
    return comms


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
            line = sys.stdin.readline()
            if not line:
                continue
            elif line == "XX4XXX exit":
                break
            msg = process(line)
            for val in msg:
                if val == "X1":
                    sock.close()
                    break
                else:
                    client.send(bytes(val, "utf-8"))
        finally:
            print("Closing connection")
            sock.close()
