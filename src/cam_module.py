import datetime
from enum import Enum

import cv2
import numpy as np

# Camera class to access OpenCV library for camera "functions"
# CLASS ----------------------------------------------------------------------|

class state(int, Enum):
    """
    Enum to indicate indexes of cam object state tracker.
    """
    GRAYSCALE = 0
    FLIP = 1
    SHARPEN = 2

class cam:
    """
    OpenCV based camera object with picture taking and basic editing abilities
    """

    def __init__(self, path: str):
        """
        OpenCV based personal object for performing camera operations
        with Arducam
        @param path(str): path of working directory
        \n\t - MUST USE R STRING FOR CONSTRUCTOR PARAM "path"
        \n\t - lastState = [grayscale, flip, sharp filter]
        """
        self.lastState = [False, False, False]
        self.cam = cv2.VideoCapture(-1)
        self.img_counter = 0
        self.rotation = 0
        self.dir = rf"{path}"

    def snapshot(self) -> bool:
        """
        Takes a photo
        @return bool: True if photo taken

        Radio Commands: C3
        Last State: 0 - grayscale, 1 - Flipped 180 deg, 2 - sharpened filter
        """
        ret, frame = self.cam.read()
        if not ret:
            print("failed to grab frame")
            return False
        time = datetime.datetime.now()
        img_name = f"arducam_{cam.iD(time) + self.img_counter}.png"
        print(img_name)
        cv2.imwrite(img_name, frame)
        # raw and format string
        path = rf"{self.dir}/{img_name}"  # ADD YOUR PATH HERE
        img = cv2.imread(path)
        if self.lastState[state.GRAYSCALE.value]:  # grayscale
            img = cam.g_scale(img)
        if self.lastState[state.FLIP.value]:  # flipped 180 deg
            img = cam.flip(img)
        if self.lastState[state.SHARPEN.value]:  # sharpened filter
            img = cam.sharp_f(img)
        cv2.imwrite(img_name, cam.timestamp(time, img))
        self.img_counter += 1
        return True

    @staticmethod
    def iD(time: datetime) -> int:
        """
        Returns ID for image naming purposes
        @param time(datetime): current time
        @return int: ID
        """
        return (
            int(time.strftime("%m")) * 10000000
            + int(time.strftime("%d")) * 100000
            + int(time.strftime("%H")) * 1000
            + int(time.strftime("%M")) * 10
        )

    @staticmethod
    def timestamp(time: datetime, img: cv2.Mat) -> cv2.Mat:
        """
        Timestamps and returns an existing image
        @param time(datetime): current time
        @param img(cv2.Mat): path for image (already read using cv2.imread())
        @return cv2.Mat: the edited image
        """
        return cv2.putText(
            img,
            f"{time}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

    @staticmethod
    def flip(img: cv2.Mat) -> cv2.Mat:
        """
        Flips and returns existing image 180 degrees
        @param img(cv2.Mat): path for image (already read using cv2.imread())
        @return cv2.Mat: the edited image

        Radio Commands: F6
        """
        return cv2.flip(img, 0)

    @staticmethod
    def g_scale(img: cv2.Mat) -> cv2.Mat:
        """
        Converts and returns existing image in grayscale
        Radio Commands: D4 - ON, E5 - OFF
        @param img(cv2.Mat): path for image (already read using cv2.imread())
        @return cv2.Mat: the edited image
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def sharp_f(img: cv2.Mat) -> cv2.Mat:
        """
        Adds and returns existing image with 'sharpen' filter applied
        @param img(cv2.Mat): path for image (already read using cv2.imread())
        @return cv2.Mat: the edited image

        Radio Commands: G7 - ON, H8 - OFF
        """
        kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
        return cv2.filter2D(img, -1, kernel)

    def release(self) -> None:
        """
        Releases camera
        @return None: None
        """
        self.cam.release()

    def __str__(self):
        s = f"path - {self.dir}\nstate: gScal - {self.lastState[0]} |  "
        s += f"flip - {self.lastState[1]} | sharp - {self.lastState[2]} | "
        s += f"rotation - {self.rotation}"
        return s


# ADDITIONAL FUNCTIONS -------------------------------------------------------|
def gimbal_right(camera: cam) -> str:
    """
    Rotates gimbal 60 degrees right.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    print("gimb right")
    camera.rotation += 60
    pass
    return "Gimbal rotated 60 degrees right."

def gimbal_left(camera: cam) -> None:
    """
    Rotates gimbal 60 degrees left.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    print("gimb left")
    camera.rotation -= 60
    pass
    return "Gimbal rotated 60 degrees left."

def take_pic(camera: cam) -> str:
    """
    Takes picture and logs picture.
    @param camera(cam): camera to operate with.
    @return str: summary of picture taken
    """
    if camera.snapshot():
        print(camera)
    else:
        print(False)
        return "Snapshot failed."
    ret = f"Picture Taken: {camera.dir}, GS: {camera.lastState[state.GRAYSCALE]}, "
    ret += f"F: {camera.lastState[state.FLIP]}, S: {camera.lastState[state.SHARPEN]}, "
    ret += f"R: {camera.rotation}"
    return ret

def gscale_on(camera: cam) -> str:
    """
    Turns grayscale filter on.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    camera.lastState[state.GRAYSCALE] = True
    return "Grayscale filter activated."

def gscale_off(camera: cam) -> str:
    """
    Turns grayscale filter off.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    camera.lastState[state.GRAYSCALE] = False
    return "Grayscale filter deactivated."

def flip180(camera: cam) -> str:
    """
    Flips camera view 180 degrees.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    camera.lastState[state.FLIP] = not camera.lastState[state.FLIP]
    return "Camera view flipped 180 degrees."

def sharpen(camera: cam) -> str:
    """
    Turns sharpen filter on.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    camera.lastState[state.SHARPEN] = True
    return "Sharpen filter activated."

def reset_filters(camera: cam) -> str:
    """
    Removes all filters.
    @param camera(cam): camera to operate with.
    @param str: Summary of action.
    """
    camera.lastState = [False, False, False]
    return "Filters reset"
