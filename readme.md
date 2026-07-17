# Twitch Plays Bot 🎮

This is a Python-based Twitch chat reader that translates chat commands directly into keyboard presses and mouse clicks using a clean Tkinter GUI. 

-------------------------------------------------------------------------------------

## 🚀 Setup Instructions

### 1. Install Prerequisites
Make sure you have **Python 3.8+** installed on your system. During installation, ensure you check the box that says **"Add Python to PATH"**.

Next, open your terminal or Command Prompt and run the following command to install the required libraries:

(Note: tkinter, json, socket, and threading are built into Python, so you do not need to install them separately!)

-------------------------------------------------------------------------------------
2. Get Your Twitch Token

To allow the bot to read your stream's chat, you need an Access Token:

Go to https://twitchtokengenerator.com (or a similar trusted token generator).

Generate a Chat Bot Token or Token with chat access scopes.

Authenticate with your Twitch account.

Copy the Access Token generated for you.

-------------------------------------------------------------------------------------
3. Configure Your Credentials

Inside your project folder, open the config.json file and fill in your details:
pip install pyautogui

{
  "username": "your_twitch_username",
  "oauth_token": "oauth:your_copied_access_token_here",
  "channel": "#your_channel_name"
}

Make sure to include oauth: right before your token string if it isn't already there.
-------------------------------------------------------------------------------------

4. Customize Your Custom Inputs (Optional)

Open inputs.json to configure what buttons chat can press. You can dynamically modify this file even while the bot is running!

{
  "w": "w",
  "s": "s",
  "a": "a",
  "d": "d",
  "k": "c",
  "1": "left_click",
  "2": "right_click"
}

Keyboard keys: Set the chat letter on the left, and the physical key on the right.

Mouse clicks: Use "left_click" or "right_click" as the target value.
-------------------------------------------------------------------------------------
🎮 How to Play
Running the Bot

Simply double-click the RunBot.bat file in your folder. The Tkinter GUI application will launch completely in the background without cluttering your screen with a command prompt.

Click Start to connect to Twitch chat.

Click inside your game window to give it focus.

Watch chat take control! Click Stop at any time to pause inputs.

Chat Command Rules

Users trigger commands by typing an exclamation mark followed by their sequence (e.g., !w).

Chaining is supported! Chatters can combine commands in a single message (e.g., !www to move forward 3 times, or !w1 to step forward and left-click).

Invalid letters or unsafe characters within a chain will be ignored automatically.
-------------------------------------------------------------------------------------
⚠️ Important Notes & Safety

Fail-Safe: If the bot goes out of control, slam your physical mouse cursor into any of the four corners of your screen. This will instantly force-abort the input loop.

Window Focus: PyAutoGUI presses keys globally. Ensure your game is in focus and running in windowed/borderless windowed mode for best results.

Privacy: Never share your config.json file or stream your Access Token!
