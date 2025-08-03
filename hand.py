#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np
import time
from leap_hand_utils.dynamixel_client import DynamixelClient

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# Setup LEAP Hand
motors = list(range(16))
dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)
dxl_client.connect()
dxl_client.set_torque_enabled(motors, True)
print("[INFO] Connected to LEAP Hand.")

# Freeze sideways motors
frozen_pose = dxl_client.read_pos()
side_dof_indices = [0, 4, 8, 12]

# Mapping: MediaPipe finger tip & pip indices (excluding index)
finger_landmarks = {
    "middle": (12, 10),
    "ring":   (16, 14),
    "pinky":  (20, 18),
    "thumb":  (4, 2)
}

# Corresponding motor base index (each finger has 4 motors)
motor_map = {
    "middle": 4,
    "ring": 8,
    "pinky": 12,
    "thumb": 0
}

def compute_flexion_angle(pip, tip):
    # Vector from pip to tip
    vec = np.array(tip) - np.array(pip)
    norm = np.linalg.norm(vec)
    return np.clip(norm, 0.0, 1.0)

def mirror_hand_to_leap(landmarks):
    desired_pos = np.copy(frozen_pose)

    for finger, (tip_idx, pip_idx) in finger_landmarks.items():
        tip = [landmarks[tip_idx].x, landmarks[tip_idx].y]
        pip = [landmarks[pip_idx].x, landmarks[pip_idx].y]
        flexion = compute_flexion_angle(pip, tip)

        base = motor_map[finger]
        for i in range(1, 4):  # skip side DOF (index 0 in each group)
            motor_idx = base + i
            desired_pos[motor_idx] = 180 + flexion * 30  # adjust as per calibration

    return desired_pos

# Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("❌ Could not open webcam.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0].landmark
            leap_pose = mirror_hand_to_leap(landmarks)
            dxl_client.write_desired_pos(motors, leap_pose)

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n[INFO] Stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    dxl_client.set_torque_enabled(motors, False)
    print("[INFO] Torque disabled and camera released.")