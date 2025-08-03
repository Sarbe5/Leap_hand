import time
import numpy as np
from leap_hand_utils.dynamixel_client import DynamixelClient

# === CONFIGURATION ===
SERVO_PORT = '/dev/ttyUSB0'  # Update if different
DELAY_SECONDS = 6

# === DEFINE SINGLE POSE ===
pose = np.array([3.2, 5.0, 3.5, 5.1, 3.0, 5.0, 3.6, 5.0, 2.9, 4.9, 3.8, 5.0, 3.2, 3.2, 4.2, 3.5])

# === CONNECT TO LEAP HAND ===
client = DynamixelClient(SERVO_PORT)
print(f"[INFO] Connected to {SERVO_PORT}")

# === SEND POSE ===
print("\n▶️ Executing Test Pose:")
print(pose)
client.send_joint_command_rad(pose)
time.sleep(DELAY_SECONDS)

print("\n✅ Test pose executed.")
