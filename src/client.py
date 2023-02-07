import socket
import threading

from cam import cam
import logging as log


# EXECUTE CAMERA FUNCTIONS ---------------------------------------|
def runCam(f: str, dir: str):
    """
    Runs camera functions based on command sequence
    @param f - the command sequence
    @param dir - working directory
    """
    print("in cam")
    camera = cam(dir)
    com = f.split(" ") if len(seq) > 1 else seq
    while len(com) > 0:
        next = com.pop(0)
        next = next[:2]
        if next == "A1":
            pass  # gimbal 60 deg right
        elif next == "B2":
            pass  # gimbal 60 deg left
        elif next == "C3":
            if camera.snapshot():
                print(camera)
                log.log_event(f"Picture Taken: GS: {camera.lastState[0]} "
                    f"F: {camera.lastState[1]} S: {camera.lastState[2]}")
            else:
                print(False)
        elif next == "D4":  # grayscale on
            camera.lastState[0] = True
        elif next == "E5":  # grayscale off
            camera.lastState[0] = False
        elif next == "F6":  # flip 180 degrees
            camera.lastState[1] = True if not camera.lastState[1] else False
        elif next == "G7":  # apply filter
            camera.lastState[2] = True
        elif next == "H8":  # remove all filters
            camera.lastState[0] = False
            camera.lastState[2] = False
        elif next == "I9":
            camera.lastState = [False, False, False]
    camera.release()


if __name__ == "__main__":
    # Setup for connection
    DIRECTORY = "/home/pi/"
    SERVER = "/tmp/uds_socket"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Try to connect
    try:
        sock.connect(SERVER)
    except socket.error:
        print("Socket error")

    while True:
        numBytes = 36
        comm = None

        print(f"Connecting to: {SERVER}")
        m = sock.recv(numBytes)  # <num of bytes
        n = m.decode("utf-8")
        if n != "":
            comm = n
        else:
            continue
        print(comm)
        if comm[:1] == "X":
            seq = comm.split("XX4XXX ")[1]
            t = threading.Thread(target=runCam, args=(seq, DIRECTORY))
            t.start()
    sock.close()


    #seq = f.split("XX4XXX ")
    #print(f"in loop {seq}")
    #comms = seq[1].split(" ") if len(seq) > 1 else seq
