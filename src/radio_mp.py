#! /usr/bin/env python3

"""
Author: Nick Fan
Date: Feb 2023
Description: Multiprocessing program to receive piped commands
from stdin and execute camera commands in parallel.
Designed for completion of Payload Mission for NASA USLI
with Long Beach Rocketry.
"""

from multiprocessing import Process, Queue, freeze_support
from queue import Empty
from sys import stdin
from threading import Timer

import cam_module
from cam_module import Cam

# CONSTANTS ---------------------------------------------------|
CALLSIGN = "KN6WUV"
EXIT = "exit"
END = None

DIRECTORY = "/home/pi/"

HC_MISSION = "C3 A1 D4 C3 E5 A1 G7 C3 H8 A1 F6 C3"
HC_WAIT = 300 # change this to 300 (5 min) or whatever 

# CAMERA DICT -------------------------------------------------|
CASE = {
    "A1": cam_module.gimbal_right,
    "B2": cam_module.gimbal_left,
    "C3": cam_module.take_pic,
    "D4": cam_module.gscale_on,
    "E5": cam_module.gscale_off,
    "F6": cam_module.flip180,
    "G7": cam_module.sharpen,
    "H8": cam_module.reset_filters,
}

# FUNCTIONS ---------------------------------------------------|
def read_in(commands: Queue) -> None:
    """
    Continuously reads from stdin.
    @param commands(Queue): Queue of commands.
    @return None: None
    """
    std_in = open(0)
    while True:
        line = std_in.readline()
        if not line:
            continue
        print("Line in: " + line)
        # verify message begins with callsign, then split and remove
        if line[: len(CALLSIGN)] == CALLSIGN:
            line = line.split(f"{CALLSIGN} ")[1]
            if line[: len(EXIT)] == EXIT:
                commands.put(END)
                break
            # insert in queue
            commands.put(line)
    print("Read exit.")


def select(order: str, case: dict, camera: Cam) -> None:
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
        print(ret)


def cam_loop(commands: Queue, directory: str) -> None:
    """
    Continuosly loops and runs camera until exit signal is read.
    @param commands(Queue): Queue of commands.
    @param dir(str): directory for camera to work in
    @return None: None
    """
    camera = Cam(directory)
    while True:
        # read from queue
        command = commands.get()
        if not command:  # exit signal
            break
        for order in command.split(" "):
            try:
                select(order[:2], CASE, camera)
            except TypeError:
                continue
        cam_module.reset_filters(camera)
    camera.release()
    print("Camera exit.")


def close_queue(commands: Queue) -> None:
    """
    Cleans up and closes queue.
    @param commands(Queue): Queue of commands.
    @return None: None
    """
    while True:
        try:
            commands.get(block=False)
        except Empty:
            break
    commands.close()
    commands.join_thread()
    print("Queue closed.")


def timeout(commands: Queue, read: Process) -> None:
    """Hardcode commands + exit if radio transmission fails.
    @param commands(Queue): Queue of commands.
    @param(Process): the read process.
    @return None: None
    """
    def put():
        commands.put(f"{HC_MISSION}")
        commands.put(END)
        read.terminate()
    Timer(HC_WAIT, put).start()


if __name__ == "__main__":
    freeze_support()

    # create shared queue for commands
    com_queue = Queue()

    # start camera process and reading from stdin
    camera_p = Process(target=cam_loop, args=(com_queue, DIRECTORY))
    camera_p.start()
    read_p = Process(target=read_in, args=(com_queue,))
    read_p.start()
    timeout(com_queue, read_p)

    # wait for and clean up resources
    camera_p.join()
    read_p.join()

    close_queue(com_queue)

    # initialize arm folding

    print("Mission complete.")
