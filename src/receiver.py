import sys
import time

while True:
    line = sys.stdin.readline()
    if not line:
        continue
    sys.stdout.write(line)
    sys.stdout.flush()
    time.sleep(1)

    
