import pyautogui
import json
import os
import time

pyautogui.FAILSAFE = True
DELAY_BETWEEN_PRESSES = 0.05

def load_inputs_map():
    """Loads the command-to-key mapping from inputs.json."""
    filename = "inputs.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading inputs.json: {e}")
    return {"w": "w", "s": "s", "a": "a", "d": "d"}

def handle_twitch_command(username: str, message: str):
    """
    Reads inputs.json dynamically and executes sequential keypresses 
    or mouse clicks based on the configuration map.
    """
    clean_msg = message.strip().lower()

    if not clean_msg.startswith("!"):
        return

    # Strip the '!' to get the raw chain (e.g., "112" or "w1w")
    chain = clean_msg[1:]
    
    inputs_map = load_inputs_map()

    # Verify every character in the chain exists in inputs.json keys
    if all(char in inputs_map for char in chain) and len(chain) > 0:
        print(f"🎮 [Action] {username} triggered chain: '{clean_msg}'")
        
        for char in chain:
            action = inputs_map[char]
            
            # Check if the mapped action is a special mouse click
            if action == "left_click":
                print(f"  -> Chat '{char}' -> 🖱️ Left Clicking")
                pyautogui.click()
            elif action == "right_click":
                print(f"  -> Chat '{char}' -> 🖱️ Right Clicking")
                pyautogui.rightClick()
            else:
                # Otherwise, treat it as a standard keyboard press
                print(f"  -> Chat '{char}' -> ⌨️ Pressing Keyboard '{action}'")
                pyautogui.press(action)
            
            time.sleep(DELAY_BETWEEN_PRESSES)
