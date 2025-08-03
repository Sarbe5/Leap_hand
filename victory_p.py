import numpy as np
from main import LeapNode  # adjust if your LeapNode is in a different path

# Initialize the LEAP hand node
leap = LeapNode()

# Victory sign pose in radians (example values)
# Thumb: curled, Index & Middle: extended, Ring & Little: curled
# Tune these values based on your specific hand kinematics
victory_pose = np.array([

3.2, 5.0, 3.5, 5.1, 3.0, 5.0, 3.6, 5.0, 2.9, 4.9, 3.8, 5.0, 3.2, 3.2, 4.2, 3.5

])

# Send the pose to the motors
leap.dxl.write_desired_pos(leap.motors, victory_pose)
