"""
Logging module to help log events in subprocesses throughout the main programs.
Note: Setup function only compatible with linux machines.
"""

import subprocess
import datetime

def setup() -> int:
    '''
    Compiles logger if it is not yet compiled.
    @returns compilation status
    '''
    check = subprocess.Popen(["test", "-f", "logger.exe"])
    check.wait()
    if check.returncode == 1: 
        compile = subprocess.Popen(["g++", "-o", "logger.exe", "logger.cpp"])
        compile.wait()
        return compile.returncode
    return 2

def log_event(event_description: str) -> None:
    '''
    Logs a single message with a timestamp.
    @param string description message to log
    @returns none
    '''
    subprocess.Popen(["./logger.exe", f"{datetime.datetime.now()}, {event_description}"])