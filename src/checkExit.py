import sys

# CHECK FOR EXIT SIGNAL -----------|

if __name__ == "__main__":
    msg = sys.argv
    msg = msg[1].split("\n")
    print(msg)
    for val in msg:
        if val == "XX5XXX exit":
            sys.exit(1)
    
