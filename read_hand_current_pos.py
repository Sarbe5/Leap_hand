from main import LeapNode
import numpy as np

leap_node = LeapNode()
pos = leap_node.read_pos()

print("Current Motor Angles (radians):")
for i, angle in enumerate(pos):
    print(f"Motor {i}: {angle:.4f} rad")
