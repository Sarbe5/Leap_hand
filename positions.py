#!/usr/bin/env python3
import numpy as np
import time
from leap_hand_utils.dynamixel_client import DynamixelClient

def main():
    motors = list(range(16))

    # Connect to LEAP Hand
    try:
        dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)
        dxl_client.connect()
        print("[INFO] Connected to /dev/ttyUSB0")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to connect to LEAP Hand: {e}")

    dxl_client.set_torque_enabled(motors, True)

    # Load captured poses
    try:
        poses = np.load("composed_poses.npy")
        print(f"[INFO] Loaded {len(poses)} poses from composed_poses.npy")
    except Exception as e:
        print(f"❌ Error loading poses: {e}")
        return

    # Run each pose on the hand with some delay
    try:
        for i, pose in enumerate(poses):
            print(f"Running pose #{i+1}")
            dxl_client.write_desired_pos(motors, pose)
            time.sleep(1.0)  # hold the pose for 1 second
    except Exception as e:
        print(f"❌ Error sending poses: {e}")

    print("[INFO] Finished running all poses.")
    dxl_client.set_torque_enabled(motors, False)

if __name__ == "__main__":
    main()

