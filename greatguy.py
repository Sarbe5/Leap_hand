#!/usr/bin/env python3
import numpy as np
import time
from leap_hand_utils.dynamixel_client import DynamixelClient

# Motor IDs
motors = list(range(16))

# Connect to LEAP Hand at ttyUSB0
try:
    dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)
    dxl_client.connect()
    print("[INFO] Connected to /dev/ttyUSB0")
except Exception as e:
    raise RuntimeError(f"❌ Failed to connect to LEAP Hand: {e}")

# Optional: enable torque
dxl_client.set_torque_enabled(motors, True)
dxl_client.set_torque_enabled([12], False)


# Capture loop
captured_poses = []

print("\n=== Pose Capture ===")
print("Move the LEAP Hand manually or with another script.")
print("Press [Enter] to capture current joint positions.")
print("Type [q] and press [Enter] to quit.\n")

while True:
    user_input = input(">> Capture current pose? (Enter to capture / q to quit): ")
    if user_input.lower() == 'q':
        break

    pos = dxl_client.read_pos()
    print(f"Captured Pose #{len(captured_poses)+1}:")
    print(np.round(pos, 1))
    captured_poses.append(pos)
    print()

# ✅ Save captured poses
np.save("captured_poses.npy", np.array(captured_poses))
print(f"\n✅ Saved {len(captured_poses)} poses to captured_poses.npy")

