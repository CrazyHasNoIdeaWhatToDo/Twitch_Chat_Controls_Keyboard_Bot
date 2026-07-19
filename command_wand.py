import json
import os
import time
from datetime import datetime
import pydirectinput  # Handling both keys and mouse via DirectInput now

# Standard safety failsafe (pydirectinput honors this too)
pydirectinput.FAILSAFE = True
DELAY_BETWEEN_PRESSES = 0.05
HOLD_DURATION = 0.5  # ⏱️ The time to hold down each keyboard key


def get_timestamped_msg(text):
    """Prepends the current time to log messages."""
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"[{current_time}] {text}"


def load_inputs_map(log_callback=None):
    """Loads the command-to-key mapping from inputs.json."""
    filename = "inputs.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception as e:
            msg = f"❌ Error reading inputs.json: {e}"
            if log_callback: log_callback(get_timestamped_msg(msg))
            else: print(get_timestamped_msg(msg))
    return {"w": "w", "s": "s", "a": "a", "d": "d"}


def handle_twitch_command(username: str, message: str, log_callback=None):
    clean_msg = message.strip().lower()
    if not clean_msg.startswith("!"):
        return

    chain = clean_msg[1:]
    inputs_map = load_inputs_map(log_callback)

    # Helper function to handle logs seamlessly with timestamps
    def log(text):
        timestamped = get_timestamped_msg(text)
        if log_callback:
            log_callback(timestamped)
        else:
            print(timestamped)

    if all(char in inputs_map for char in chain) and len(chain) > 0:
        log(f"🎮 [Action] {username} triggered chain: '{clean_msg}'")
        
        for char in chain:
            action = inputs_map[char]
            
            if action == "left_click":
                log(f"  -> Chat '{char}' -> 🖱️ Left Clicking")
                pydirectinput.mouseDown()
                time.sleep(0.1)  # Gives the game engine enough frames to register the click
                pydirectinput.mouseUp()
                
            elif action == "right_click":
                log(f"  -> Chat '{char}' -> 🖱️ Right Clicking")
                pydirectinput.mouseDown(button='right')
                time.sleep(0.1)
                pydirectinput.mouseUp(button='right')
            else:
                log(f"  -> Chat '{char}' -> ⌨️ Holding Keyboard '{action}' for {HOLD_DURATION}s")
                pydirectinput.keyDown(action)
                time.sleep(HOLD_DURATION)
                pydirectinput.keyUp(action)
            
            time.sleep(DELAY_BETWEEN_PRESSES)


def release_all_keys(log_callback=None):
    """Safety feature to release all mapped keys and mouse clicks instantly."""
    inputs_map = load_inputs_map(log_callback)
    msg = "♻️ Releasing all held keys and mouse states..."
    
    if log_callback:
        log_callback(get_timestamped_msg(msg))
    else:
        print(get_timestamped_msg(msg))

    # Release mouse
    pydirectinput.mouseUp()
    pydirectinput.mouseUp(button='right')

    # Release any keyboard key found in your inputs map
    for action in inputs_map.values():
        if action not in ["left_click", "right_click"]:
            try:
                pydirectinput.keyUp(action)
            except Exception:
                pass
