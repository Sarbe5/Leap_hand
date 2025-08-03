#!/usr/bin/env python3
import time
import numpy as np
from leap_hand_utils.dynamixel_client import DynamixelClient

# Desired joint configuration (16 angles in radians)
target_config = [
    3.2, 5.0, 3.5, 5.1, 3.0, 5.0, 3.6, 5.0, 2.9, 4.9, 3.8, 5.0, 3.2, 3.2, 4.2, 3.5
]

# Motor IDs
motors = list(range(16))

try:
    dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)
    dxl_client.connect()
    dxl_client.set_torque_enabled(motors, True)
    print("[INFO] Connected and torque enabled.")
    
    print("[INFO] Locking position. Press Ctrl+C to release...")
    while True:
        dxl_client.write_desired_pos(motors, np.array(target_config))
        time.sleep(0.05)  # keep updating to hold position

except KeyboardInterrupt:
    print("\n[INFO] Keyboard interrupt received. Releasing motors...")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    dxl_client.set_torque_enabled(motors, False)
    print("[INFO] Torque disabled. Script ended.")
