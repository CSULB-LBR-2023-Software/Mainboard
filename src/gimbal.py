import RPi.GPIO
import spidev


class gimbal:

    """
    Class to direct STM32 via SPI to rotate gimbal
    """

    def __init__(self):
        pass

    def rotate(self, direction):
        """
        Rotates gimbal 60 degrees and returns once rotation is complete
        @param direction - direction to rotate in
        """
        pass

        # def rotate_right(self):
        """
        Rotates gimbal 60 degrees right and returns once rotation is complete
        """
        pass

        # def rotate_left(self):
        """
        Rotates gimbal 60 degrees left and returns once rotation is complete
        """
        pass
