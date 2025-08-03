import time
import numpy as np
from leap_hand_utils.dynamixel_client import DynamixelClient

# === CONFIGURATION ===
SERVO_PORT = '/dev/ttyUSB0'  # Update if different
POSES_FILE = 'composed_poses.npy'
DELAY_SECONDS = 6

# === LOAD POSES ===
try:
    poses = np.load(POSES_FILE)
    if poses.ndim == 1:
        poses = np.expand_dims(poses, axis=0)
    print(f"✅ Loaded {len(poses)} poses from {POSES_FILE}")
except Exception as e:
    print(f"❌ Failed to load poses: {e}")
    exit()

# === CONNECT TO LEAP HAND ===
client = DynamixelClient(SERVO_PORT)
print(f"[INFO] Connected to {SERVO_PORT}")

# === EXECUTE EACH POSE ===
for i, pose in enumerate(poses):
    print(f"\n▶️ Executing Pose #{i+1}:")
    print(pose)

    # Send each joint angle (in radians)
    client.send_joint_command_rad(pose)

    # Delay to hold pose
    time.sleep(DELAY_SECONDS)

print("\n✅ All poses executed.")
