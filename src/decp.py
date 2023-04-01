
import RPi.GPIO as GPIO
import time

from state_machine import States, StateMachine

class Protocol:
    """Pulse width map in seconds."""

    class Deployment:
        INFO_GET_STATE = 0.005
        DEPLOY_DIRTBRAKE = 0.010
        DEPLOY_REORIENT = 0.015
        DEPLOY_ARM = 0.020
        RETRACT_ARM = 0.025
        RETRACT_DIRTBRAKE = 0.030

class Decp:

    def __init__(self, pi_ack: int, stm_ack: int, pi_pulse: int) -> None:
        self.pi_ack = pi_ack
        self.stm_ack = stm_ack
        self.pulse = pi_pulse
        GPIO.setmode(GPIO.BCM)
        self.setup_outputs(self.pi_ack, self.pulse)
        self.setup_inputs(self.stm_ack)

    def setup_outputs(self, *pins: int) -> None:
        """Setup output pins.
        
        Args:
            *pins(int): any number of pins
        """
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
    
    def setup_inputs(self, *pins: int) -> None:
        """Setup output pins.
        
        Args:
            *pins(int): any number of pins
        """
        for pin in pins:
            GPIO.setup(pin, GPIO.IN)

    def request_STM(self, request_type: float):
        """
        Sends request to STM of specific type.

        Args:
            request_type(float): the request type
        """
        GPIO.output(self.pi_ack, GPIO.HIGH)  # ack high
        for _ in range(5):
            GPIO.output(self.pulse, GPIO.HIGH)
            time.sleep(request_type)
            GPIO.output(self.pulse, GPIO.LOW)
            time.sleep(0.000001)
        GPIO.output(self.pi_ack, GPIO.LOW)  # ack low

        while not GPIO.input(self.stm_ack):
            continue
        print("STM ack received")
