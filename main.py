import socket
import threading
import json
import os
import tkinter as tk
from tkinter import scrolledtext
import command_wand
from command_wand import handle_twitch_command

class TwitchChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitch Chat Monitor")
        self.root.geometry("600x450")
        
        # Connection state variables
        self.is_running = False
        self.sock = None
        self.chat_thread = None

        # --- Load Configuration from JSON ---
        self.config = self.load_config()

        # --- GUI Layout ---
        
        # Configuration Inputs Frame (Now Read-Only from JSON)
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10, fill=tk.X, padx=10)
        
        tk.Label(self.input_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5)
        self.username_entry = tk.Entry(self.input_frame)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.username_entry.insert(0, self.config.get("username", ""))

        tk.Label(self.input_frame, text="OAuth Token:").grid(row=1, column=0, sticky="w", padx=5)
        self.token_entry = tk.Entry(self.input_frame, show="*") 
        self.token_entry.grid(row=1, column=1, sticky="ew", padx=5)
        self.token_entry.insert(0, self.config.get("oauth_token", ""))

        tk.Label(self.input_frame, text="Channel:").grid(row=2, column=0, sticky="w", padx=5)
        self.channel_entry = tk.Entry(self.input_frame)
        self.channel_entry.grid(row=2, column=1, sticky="ew", padx=5)
        self.channel_entry.insert(0, self.config.get("channel", ""))

        # Buttons Frame
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=5)

        self.start_btn = tk.Button(self.btn_frame, text="Start", command=self.start_monitoring, bg="green", fg="white", width=10)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(self.btn_frame, text="Stop", command=self.stop_monitoring, bg="red", fg="white", width=10, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)

        # Refresh Button
        self.refresh_btn = tk.Button(self.btn_frame, text="Refresh", command=self.refresh_connection, bg="blue", fg="white", width=10)
        self.refresh_btn.grid(row=0, column=2, padx=5)

        # Chat Console Output
        tk.Label(root, text="Live Chat Output:").pack(anchor="w", padx=15)
        self.console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15)
        self.console.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        self.console.config(state=tk.DISABLED)

        # If config loaded successfully, print a confirmation
        if "error" not in self.config:
            self.log_to_console("✅ Configuration loaded from config.json successfully.")
        else:
            self.log_to_console("❌ Could not load config.json. Please make sure the file exists.")

    def load_config(self):
        """Loads credentials from config.json file."""
        config_filename = "config.json"
        if os.path.exists(config_filename):
            try:
                with open(config_filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                return {"error": str(e)}
        return {"error": "File not found"}

    def log_to_console(self, text):
        """Safely inserts text into the Tkinter console text area."""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def twitch_listener(self, server, port, token, username, channel):
        """Runs on a background thread to listen to Twitch chat."""
        try:
            self.sock = socket.socket()
            self.sock.connect((server, port))
            
            self.sock.send(f"PASS {token}\n".encode('utf-8'))
            self.sock.send(f"NICK {username}\n".encode('utf-8'))
            self.sock.send(f"JOIN {channel}\n".encode('utf-8'))
            
            self.log_to_console(f"🤖 Connected! Listening to {channel}...")

            while self.is_running:
                self.sock.settimeout(1.0) 
                try:
                    response = self.sock.recv(2048).decode('utf-8')
                except socket.timeout:
                    continue 

                if not response:
                    break

                if response.startswith('PING'):
                    self.sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                elif "PRIVMSG" in response:
                    try:
                        user = response.split('!')[0].replace(':', '')
                        msg = response.split('PRIVMSG')[1].split(':', 1)[1].strip()

                        # 1. Print raw chat message to Tkinter console
                        self.log_to_console(f"[{user}]: {msg}")

                        # 2. Pass control over to command_wand with the UI log callback
                        handle_twitch_command(user, msg, log_callback=self.log_to_console)

                    except IndexError:
                        pass

        except Exception as e:
            self.log_to_console(f"❌ Error: {str(e)}")
        finally:
            self.cleanup_socket()
            # If we disconnected unexpectedly, reset the button states safely
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def start_monitoring(self):
        """Triggered by the Start Button."""
        if self.is_running:
            return

        username = self.username_entry.get().strip()
        token = self.token_entry.get().strip()
        channel = self.channel_entry.get().strip()

        if not channel.startswith("#"):
            channel = f"#{channel}"

        if not username or not token:
            self.log_to_console("⚠️ Please fill out all configuration fields before starting.")
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.log_to_console("⚡ Connecting to Twitch IRC...")

        self.chat_thread = threading.Thread(
            target=self.twitch_listener, 
            args=("irc.chat.twitch.tv", 6667, token, username, channel),
            daemon=True 
        )
        self.chat_thread.start()

    def stop_monitoring(self):
        """Triggered by the Stop Button."""
        self.is_running = False
        self.log_to_console("🛑 Stopping stream...")
        
        # Call command_wand to release stuck keys and pass console logging
        try:
            if hasattr(command_wand, 'release_all_keys'):
                command_wand.release_all_keys(log_callback=self.log_to_console)
        except Exception as e:
            self.log_to_console(f"⚠️ Failed to release keys safely: {e}")

        self.cleanup_socket()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def refresh_connection(self):
        """Triggered by the Refresh Button. Restarts the stream connection smoothly."""
        self.log_to_console("🔄 Refreshing connection...")
        self.stop_monitoring()
        # Gives the socket a brief 500ms breather to close completely before turning back on
        self.root.after(500, self.start_monitoring)

    def cleanup_socket(self):
        """Safely shuts down the open socket connection."""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except Exception:
                pass
            self.sock = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TwitchChatApp(root)
    root.mainloop()
