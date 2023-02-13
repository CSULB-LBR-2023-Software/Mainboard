"""
Author: Nick Fan
Date: Feb 2023
Description: Multiprocessing program to receive piped commands
from stdin and execute camera commands in parallel.
"""

from sys import stdin
from multiprocessing import Process, Queue

import myLogging as log
from cam import cam

# CONSTANTS ---------------------------------------------------|
CALLSIGN = "XX4XXX"
EXIT = "exit"
END = None

GRAYSCALE = cam.state.GRAYSCALE.value
FLIP = cam.state.FLIP.value
SHARPEN = cam.state.SHARPEN.value

DIRECTORY = "/home/pi/"

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
        if line[:len(CALLSIGN)] == CALLSIGN:
            line = line.split(f"{CALLSIGN} ")[1]
            if line[:len(EXIT)] == EXIT:
                commands.put(END)
                break
            commands.put(line)
    print("Read exit.")

def run_cam(command: str, camera: cam) -> None:
    """
    Runs camera functions based on command sequence
    @param command(str): the command sequence
    @param camera(cam): cam object
    @return None: None
    """
    print("in cam")
    sequence = command.split(" ") if len(command) > 1 else command
    while len(sequence) > 0:
        next = sequence.pop(0)[:2]
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

def cam_loop(commands: Queue, directory: str) -> None:
    """
    Continuosly loops and runs camera until exit signal is read.
    @param commands(Queue): Queue of commands.
    @param dir(str): directory for camera to work in
    @return None: None
    """
    camera = cam(directory)
    while True:
        command = commands.get()
        if not command:
            break
        run_cam(command, camera)
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

    # join process, wait for completion
    camera_p.join()

    # initialize arm folding

    # mission complete
    print("Mission complete.")
