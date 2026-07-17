import pyautogui
import time

# PyAutoGUI fail-safe: slam mouse into any corner of the screen to abort
pyautogui.FAILSAFE = True

# Optional: Add a tiny delay (in seconds) between chained keypresses 
# so the game has time to register each individual stroke.
DELAY_BETWEEN_PRESSES = 0.05 

def handle_twitch_command(username: str, message: str):
    """
    Checks if a Twitch chat message starts with '!' and executes
    each valid movement character (w, a, s, d) sequentially.
    
    Examples:
    - "!www" -> presses 'w', 'w', 'w'
    - "!was" -> presses 'w', 'a', 's'
    """
    clean_msg = message.strip().lower()

    # Only process if it starts with our command prefix
    if not clean_msg.startswith("!"):
        return

    # Remove the '!' to look at just the characters (e.g., "www" or "was")
    chain = clean_msg[1:]
    
    # Define valid movement keys
    valid_keys = {'w', 'a', 's', 'd'}

    # Verify that the entire chain consists only of valid keys.
    # This prevents someone from typing "!w-something-random" and breaking things.
    if all(char in valid_keys for char in chain) and len(chain) > 0:
        print(f"🎮 [Action] {username} triggered chain: '{clean_msg}'")
        
        # Loop through each character one by one
        for key in chain:
            print(f"  -> Pressing '{key}'")
            pyautogui.press(key)
            
            # Brief pause so inputs don't happen instantly all at once
            time.sleep(DELAY_BETWEEN_PRESSES)
