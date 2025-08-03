# File: read_hand_position.py

from main import LeapNode  # adjust import if your file/module name is different
import numpy as np
import time

def main():
    leap_node = LeapNode()
    time.sleep(1)  # allow some time to initialize ##so in 1s it is becoming 

    try:
        current_pose = leap_node.read_pos()
        print("Current Motor Angles (radians):")
        for idx, angle in enumerate(current_pose):
            print(f"Motor {idx}: {angle:.4f} rad")
    except Exception as e:
        print(f"Error reading motor positions: {e}")

if __name__ == "__main__":
    main()
