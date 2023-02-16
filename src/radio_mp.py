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

import cam_module
import my_logging as log
from cam_module import cam

# CONSTANTS ---------------------------------------------------|
CALLSIGN = "XX4XXX"
EXIT = "exit"
END = None

DIRECTORY = "/home/pi/"

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
    while True:
        line = stdin.readline()
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
                select(order[:2], CASE, camera)
            except TypeError:
                continue
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


if __name__ == "__main__":
    freeze_support()

    # setup logger
    log.setup()

    # create shared queue for commands
    com_queue = Queue()

    # start camera process and reading from stdin
    camera_p = Process(target=cam_loop, args=(com_queue, DIRECTORY))
    camera_p.start()
    read_in(com_queue)

    # wait for and clean up resources
    camera_p.join()
    close_queue(com_queue)

    # initialize arm folding

    print("Mission complete.")
