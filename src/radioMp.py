import multiprocessing as mp
import sys
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import ShareableList

import myLogging as log
from cam import cam


# FUNCTIONS -------------------------------------------------|
def runCam(seq: str, directory: str) -> bool:
    """
    Runs camera functions based on command sequence
    @param f - the command sequence
    @param dir - working directory
    """
    print("in cam")
    if seq[:1] == "X":
        seq = seq.split("XX4XXX ")[1]
    if seq[:4] == "exit":
        return False
    com = seq.split(" ") if len(seq) > 1 else seq
    camera = cam(directory)
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
                log.log_event(f"Picture Taken: {camera.dir}, GS: {camera.lastState[0]} "
                    f"F: {camera.lastState[1]} S: {camera.lastState[2]}")
            else:
                print(False)
        elif next == "D4":  # grayscale on
            camera.lastState[0] = True
        elif next == "E5":  # grayscale off
            camera.lastState[0] = False
        elif next == "F6":  # flip 180 degrees
            camera.lastState[1] = not camera.lastState[1]
        elif next == "G7":  # apply filter
            camera.lastState[2] = True
        elif next == "H8":  # reset all filters
            camera.lastState = [False, False, False]
    camera.release()
    return True

def camLoop(shName: str, dir: str) -> None:
    """
    Continuosly loops and runs camera until exit signal is read.
    @param shName - SharedMemory name for queue
    @param dir - directory for camera to work in
    @returns None
    """
    queue = ShareableList(name=shName)
    cont = True
    count = 0
    while cont:
        if count < queue[18]:
            cont = runCam(queue[count % 18], dir)
            count += 1
    queue[19] = False

def readIn(shName: str) -> None:
    """
    Continuously reads from stdin.
    @param shName - SharedMemory name for queue
    @returns None
    """
    queue=ShareableList(name=shName)
    count = 0
    while queue[BUFF_L]:  # not reading this as False correctly?
        line = sys.stdin.readline()
        if not line:
            continue
        print("Line in: " + line)
        queue[count % BUFF_SL] = line
        count += 1
        queue[BUFF_SL] = count
    # does not seem to be able to break out of this while loop.
    print("Read exit.")


if __name__ == "__main__":
    BUFFSIZE = 20
    BUFF_L = BUFFSIZE - 1
    BUFF_SL = BUFFSIZE - 2
    DIRECTORY = "/home/pi/"

    log.setup()

    with SharedMemoryManager() as smm:
        # setup shared memory
        smm = SharedMemoryManager()
        smm.start()
        queue = smm.ShareableList([' ' * 36] * BUFFSIZE)  # allocate sufficient bytes
        queue[19] = True  # set continuation index

        camP = mp.Process(target=camLoop, args=(queue.shm.name, DIRECTORY))
        camP.start()

        # continuously read in
        readIn(queue.shm.name)
