import socket
import sys

from cam import cam
# from gimbal import gimbal


# EXECUTE CAMERA FUNCTIONS ---------------------------------------|
def runCam(f: str, dir: str):
    """
    Runs camera functions based on command sequence
    @param f - the command sequence
    @param dir - working directory
    """
    camera = cam(dir)
    seq = f.split("XX4XXX ")
    print(f"in loop {seq}")
    comms = seq[1].split(" ") if len(seq) > 1 else seq
    while len(comms) > 0:
        next = comms.pop(0)
        if len(next) > 2:
            next = next[:2]
        if next == "A1":
            pass  # gimbal 60 deg right
        elif next == "B2":
            pass  # gimbal 60 deg left
        elif next == "C3":
            if camera.snapshot():
                print(camera)
            else:
                print(False)
        elif next == "D4":
            camera.lastState[0] = True
        elif next == "E5":
            camera.lastState[0] = False
        elif next == "F6":
            camera.lastState[1] = True if not camera.lastState[1] else False
        elif next == "G7":
            camera.lastState[2] = True
        elif next == "H8":
            camera.lastState[2] = False
        elif next == "clear":
            camera.lastState = [False, False, False]
        elif next == "exit!":
            # archaic, will eventually remove
            return False
    camera.release()


if __name__ == "__main__":
    DIRECTORY = "/home/pi/"
    SERVER = "/tmp/uds_socket"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind server to client
    try:
        sock.connect(SERVER)
    except socket.error:
        print(sys.stderr)
        sys.exit(1)

    received = 0
    expected = 3
    numBytes = 36
    msgs = []

    print(f"Connecting to: {SERVER}")
    while received <= expected:
        received += 1
        m = sock.recv(numBytes)  # <num of bytes
        n = m.decode("utf-8")
        if n != "":
            msgs.append(n)

    sock.close()
    print("Closing connection.")
    print(msgs)

    for val in msgs:
        runCam(val, DIRECTORY)
