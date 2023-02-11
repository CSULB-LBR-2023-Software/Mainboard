import multiprocessing as mp
from sys import stdin
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import ShareableList

import myLogging as log
from cam import cam

# CONSTANTS ---------------------------------------------------|
BUFFSIZE = 7
BUFF_L = BUFFSIZE - 1
BUFF_SL = BUFFSIZE - 2

MAX_MSG_LEN = 29
CALLSIGN = "XX4XXX"

GRAYSCALE = cam.state.GRAYSCALE.value
FLIP = cam.state.FLIP.value
SHARPEN = cam.state.SHARPEN.value

DIRECTORY = "/home/pi/"

# FUNCTIONS ---------------------------------------------------|
def runCam(seq: str, camera: cam) -> tuple:
    """
    Runs camera functions based on command sequence
    @param seq: the command sequence
    @param camera: cam object
    @return (bool, cam): (status, camera)
    """
    print("in cam")
    if seq[:4] == "exit":
        return False, camera
    com = seq.split(" ") if len(seq) > 1 else seq
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
                log.log_event(
                    f"Picture Taken: {camera.dir}, "
                    f"GS: {camera.lastState[0]} "
                    f"F: {camera.lastState[1]} "
                    f"S: {camera.lastState[2]}"
                    )
            else:
                print(False)
        elif next == "D4":  # grayscale on
            camera.lastState[GRAYSCALE] = True
        elif next == "E5":  # grayscale off
            camera.lastState[GRAYSCALE] = False
        elif next == "F6":  # flip 180 degrees
            camera.lastState[FLIP] = not camera.lastState[FLIP]
        elif next == "G7":  # apply filter
            camera.lastState[SHARPEN] = True
        elif next == "H8":  # reset all filters
            camera.lastState = [False, False, False]
    camera.release()
    return True, camera

def camLoop(shName: str, dir: str) -> None:
    """
    Continuosly loops and runs camera until exit signal is read.
    @param shName: SharedMemory name for queue
    @param dir: directory for camera to work in
    @return None: None
    """
    queue = ShareableList(name=shName)
    cont = True
    count = 0
    camera = cam(dir)
    while cont:
        if count < queue[BUFF_SL]:
            cont, camera = runCam(queue[count % BUFF_SL], dir, camera)
            count += 1
    queue[BUFF_L] = False

def readIn(shName: str) -> None:
    """
    Continuously reads from stdin.
    @param shName: SharedMemory name for queue
    @return None: None
    """
    queue=ShareableList(name=shName)
    count = 0
    while queue[BUFF_L]:
        line = stdin.readline()
        if not line:
            continue
        print("Line in: " + line)
        if seq[:len(CALLSIGN)] == CALLSIGN:
            seq = seq.split(f"{CALLSIGN} ")[1]
            queue[count % BUFF_SL] = line
            count += 1
            queue[BUFF_SL] = count
    print("Read exit.")


if __name__ == "__main__":

    log.setup()

    with SharedMemoryManager() as smm:
        # setup shared memory
        smm.start()
        # allocate sufficient bytes, set up buffer
        emptyBuff = [' ' * MAX_MSG_LEN] * BUFFSIZE
        queue = smm.ShareableList([val if i < BUFF_SL else 0 for i, val in enumerate(emptyBuff)])
        queue[BUFF_L] = True  # set continuation index

        camP = mp.Process(target=camLoop, args=(queue.shm.name, DIRECTORY))
        camP.start()

        # continuously read in
        readIn(queue.shm.name)
