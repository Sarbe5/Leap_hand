#!/usr/bin/env python3
import os
import time
import numpy as np
import pyaudio
from vosk import Model, KaldiRecognizer
from leap_hand_utils.dynamixel_client import DynamixelClient

# Path to your Vosk model
VOSK_MODEL_PATH = "/home/sarbeswarnayak/vosk-model-small-en-us-0.15"

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

    # Load poses file
    try:
        poses = np.load("composed_poses.npy")
        print(f"[INFO] Loaded {len(poses)} poses from composed_poses.npy")
    except Exception as e:
        print(f"❌ Error loading poses: {e}")
        return

    # Initialize Vosk model
    if not os.path.exists(VOSK_MODEL_PATH):
        print(f"Model not found at {VOSK_MODEL_PATH}")
        return

    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("\n🎤 Speak commands like: 'action one', 'action two', ..., 'action ten'")
    print("Say 'exit' to quit.\n")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            # result is a JSON string like '{"text" : "action one"}'
            import json
            text = json.loads(result).get("text", "")
            if text:
                print(f"🔊 Recognized: '{text}'")

                if text == "exit":
                    print("👋 Exiting...")
                    break

                if text.startswith("action"):
                    parts = text.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        index = int(parts[1]) - 1
                        if 0 <= index < len(poses):
                            print(f"🖐️ Executing Action #{index+1}")
                            dxl_client.write_desired_pos(motors, poses[index])
                            time.sleep(1.0)
                        else:
                            print(f"⚠️ Invalid action number: {index+1}")
                    else:
                        print("⚠️ Please say 'action' followed by a number (1-10).")
                else:
                    print("⚠️ Unknown command. Try 'action 1' to 'action 10' or 'exit'.")

    dxl_client.set_torque_enabled(motors, False)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("[INFO] Finished.")

if __name__ == "__main__":
    main()
