#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from leap_hand_utils.dynamixel_client import DynamixelClient
import time

# List of all 16 motors (0 to 15)
motors = list(range(16))

# Try connecting to hand on common serial ports
ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
dxl_client = None
for port in ports:
    try:
        dxl_client = DynamixelClient(motors, port, 4000000)
        dxl_client.connect()
        print(f"[INFO] Connected to {port}")
        break
    except Exception as e:
        print(f"[WARNING] Failed to connect to {port}: {e}")
if dxl_client is None:
    raise RuntimeError("Could not connect to LEAP Hand on any USB port.")

# Enable torque and set initial position
dxl_client.set_torque_enabled(motors, True)
dxl_client.write_desired_pos(motors, np.zeros(16))

# Setup plotting
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(range(16), np.zeros(16), 'b-o')
ax.set_ylim(0, 360)
ax.set_title("LEAP Hand Joint Angles")
ax.set_xlabel("Joint ID")
ax.set_ylabel("Angle (degrees)")

# Live update loop
try:
    while True:
        joint_positions = dxl_client.read_pos()  # returns np.array of 16 values
        line.set_ydata(joint_positions)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.05)  # ~20 Hz
except KeyboardInterrupt:
    print("Exiting...")
finally:
    dxl_client.set_torque_enabled(motors, False)
