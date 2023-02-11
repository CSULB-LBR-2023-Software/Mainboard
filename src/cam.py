import datetime

import cv2
import numpy as np

# Camera class to access OpenCV library for camera "functions"

# CONSTANTS ------------------------------------------------------------------|
GRAYSCALE = 0
FLIP = 1
SHARPEN = 2
# CLASS ----------------------------------------------------------------------|


class cam:

    """
    OpenCV based camera object with picture taking and basic editing abilities
    """

    def __init__(self, path: str):
        """
        OpenCV based personal object for performing camera operations
        with Arducam
        \n\t - MUST USE R STRING FOR CONSTRUCTOR PARAM "path"
        \n\t - lastState = [grayscale, flip, sharp filter]
        """
        self.lastState = [False, False, False]
        print(self.lastState)
        self.cam = cv2.VideoCapture(-1)
        self.img_counter = 0
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
        if self.lastState[GRAYSCALE]:  # grayscale
            img = cam.gScale(img)
        if self.lastState[FLIP]:  # flipped 180 deg
            img = cam.flip(img)
        if self.lastState[SHARPEN]:  # sharpened filter
            img = cam.sharpF(img)
        cv2.imwrite(img_name, cam.timeStamp(time, img))
        self.img_counter += 1
        return True

    def iD(time: datetime) -> int:
        """
        Returns ID for image naming purposes
        @param time: current time
        @return int: ID
        """
        return (
            int(time.strftime("%m")) * 10000000
            + int(time.strftime("%d")) * 100000
            + int(time.strftime("%H")) * 1000
            + int(time.strftime("%M")) * 10
        )

    def timeStamp(time: datetime, img: cv2.Mat) -> cv2.Mat:
        """
        Timestamps and returns an existing image
        @param time: current time
        @param img: path for image (already read using cv2.imread())
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

    def flip(img: cv2.Mat) -> cv2.Mat:
        """
        Flips and returns existing image 180 degrees
        @param img: path for image (already read using cv2.imread())
        @return cv2.Mat: the edited image

        Radio Commands: F6
        """
        return cv2.flip(img, 0)

    def gScale(img: cv2.Mat) -> cv2.Mat:
        """
        Converts and returns existing image in grayscale
        Radio Commands: D4 - ON, E5 - OFF
        @param path for image (already read using cv2.imread())
        @return the edited image
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def sharpF(img: cv2.Mat) -> cv2.Mat:
        """
        Adds and returns existing image with 'sharpen' filter applied
        @param img: path for image (already read using cv2.imread())
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
        s += f"flip - {self.lastState[1]} | sharp - {self.lastState[2]}"
        return s

