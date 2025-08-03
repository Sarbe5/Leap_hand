#!/usr/bin/env python3
import numpy as np
import time
import speech_recognition as sr
import pyttsx3
from leap_hand_utils.dynamixel_client import DynamixelClient

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    motors = list(range(16))

    # Connect to LEAP Hand
    try:
        dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)
        dxl_client.connect()
        print("[INFO] Connected to /dev/ttyUSB0")
        speak("Connected to Leap Hand")
    except Exception as e:
        speak("Failed to connect to Leap Hand")
        raise RuntimeError(f"❌ Failed to connect to LEAP Hand: {e}")

    dxl_client.set_torque_enabled(motors, True)

    # Load poses
    try:
        poses = np.load("composed_poses.npy")
        speak(f"{len(poses)} actions loaded")
    except Exception as e:
        speak("Error loading poses")
        print(f"❌ Error loading poses: {e}")
        return

    # Setup speech recognizer
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    speak("Say action number to execute. Say exit to quit.")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎧 Listening...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"🔊 You said: {command}")

            if command in ['exit', 'quit', 'stop']:
                speak("Exiting now.")
                print("👋 Exiting...")
                break

            if command.startswith('action '):
                try:
                    index = int(command.split()[1]) - 1
                    if 0 <= index < len(poses):
                        speak(f"Executing action {index+1}")
                        dxl_client.write_desired_pos(motors, poses[index])
                        time.sleep(1.0)
                    else:
                        speak("Invalid action number")
                        print(f"⚠️ Invalid action number: {index+1}")
                except ValueError:
                    speak("Could not understand action number")
                    print("⚠️ Couldn't parse action number.")
            else:
                speak("Unknown command")
                print("⚠️ Unknown command. Try 'action 1' to 'action 10' or 'exit'.")

        except sr.UnknownValueError:
            speak("I didn't catch that")
            print("🤷 Couldn't understand. Please try again.")
        except sr.RequestError as e:
            speak("Speech service error")
            print(f"🌐 Speech service error: {e}")

    dxl_client.set_torque_enabled(motors, False)
    speak("Finished. Hand released.")
    print("[INFO] Finished.")

if __name__ == "__main__":
    main()
