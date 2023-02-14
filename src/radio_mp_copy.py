"""
Author: Nick Fan
Date: Feb 2023
Description: Multiprocessing program to receive piped commands
from stdin and execute camera commands in parallel.
** V2: implements dictionary to hash string commands to functions.
"""

from multiprocessing import Process, Queue
from sys import stdin

import my_logging as log
import cam_module
from cam_module import cam

# CONSTANTS ---------------------------------------------------|
CALLSIGN = "XX4XXX"
EXIT = "exit"
END = None

DIRECTORY = "/home/pi/"

# CAMERA MAP --------------------------------------------------|
case = {
    "A1": cam_module.gimbal_right,
    "B2": cam_module.gimbal_left,
    "C3": cam_module.take_pic,
    "D4": cam_module.gscale_on,
    "E5": cam_module.gscale_off,
    "F6": cam_module.flip180,
    "G7": cam_module.sharpen,
    "H8": cam_module.reset_filters
}

# FUNCTIONS ---------------------------------------------------|

def read_in(commands: Queue) -> None:
    """
    Continuously reads from stdin.
    @param commands(Queue): Queue of commands.
    @return None: None
    """
    while True:
        line = stdin.readline()
        if not line:
            continue
        print("Line in: " + line)
        # verify message begins with callsign, then split and remove
        if line[:len(CALLSIGN)] == CALLSIGN:
            line = line.split(f"{CALLSIGN} ")[1]
            if line[:len(EXIT)] == EXIT:
                commands.put(END)
                break
            # insert in queue
            commands.put(line)
    print("Read exit.")

def select(order: str, case: dict, camera: cam) -> None:
    """
    Selects and executes respective function based 
    on next order in sequence.
    @param order(str): next order in sequence
    @param case(dict): dictionary mapping orders to functions
    @param camera(cam): camera to operate with
    @return None: None
    """
    ret = case.get(order)(camera)
    if ret:
        log.log_event(ret)

def cam_loop(commands: Queue, directory: str) -> None:
    """
    Continuosly loops and runs camera until exit signal is read.
    @param commands(Queue): Queue of commands.
    @param dir(str): directory for camera to work in
    @return None: None
    """
    camera = cam(directory)
    while True:
        # read from queue
        command = commands.get()
        if not command:  # exit signal
            break
        for order in command.split(" "):
            try:
                select(order[:2], case, camera)
            except TypeError:
                continue
    camera.release()
    print("Camera exit.")

if __name__ == "__main__":
    # setup logger
    log.setup()

    # create shared queue for commands
    com_queue = Queue()

    # start camera process
    camera_p = Process(target=cam_loop, args=(com_queue, DIRECTORY))
    camera_p.start()

    # start reading from stdin
    read_in(com_queue)

    # wait for camera execution completion
    camera_p.join()

    # initialize arm folding

    print("Mission complete.")
