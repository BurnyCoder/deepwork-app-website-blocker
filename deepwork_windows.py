import sys
import os
import subprocess
import ctypes
import argparse
import platform
import time
import threading
# --- Configuration ---

# Websites to block (add more if needed)
WEBSITES_TO_BLOCK = [
    "facebook.com",
    "www.facebook.com",
    "linkedin.com",
    "www.linkedin.com",
    "www.facebook.com",
    "facebook.com",
    "www.discord.com",
    "discord.com",
    "reddit.com",
    "www.reddit.com",
    "boards.4chan.org",
    "www.4chan.org",
    "news.ycombinator.com",
    "www.ycombinator.com",
    "ycombinator.com",
    "www.ycombinator.com",
    "linkedin.com",
    "www.linkedin.com",
    "lesswrong.com",
    "www.lesswrong.com",
    "alignmentforum.org",
    "www.alignmentforum.org",
    "bsky.app",
    "www.bsky.app",
    "www.x.com",
    "x.com",
    "www.twitter.com",
    "www.twittter.com",
    "www.twttr.com",
    "www.twitter.fr",
    "www.twitter.jp",
    "www.twitter.rs",
    "www.twitter.uz",
    "twitter.biz",
    "twitter.dk",
    "twitter.events",
    "twitter.ie",
    "twitter.je",
    "twitter.mobi",
    "twitter.nu",
    "twitter.pro",
    "twitter.su",
    "twitter.vn",
    "twitter.com",
    "*.twitter.com",
    "twitter.gd",
    "twitter.im",
    "twitter.hk",
    "twitter.jp",
    "twitter.ch",
    "twitter.pt",
    "twitter.rs",
    "www.twitter.com.br",
    "twitter.ae",
    "twitter.eus",
    "twitter.hk",
    "ns1.p34.dynect.net",
    "ns2.p34.dynect.net",
    "ns3.p34.dynect.net",
    "ns4.p34.dynect.net",
    "d01-01.ns.twtrdns.net",
    "d01-02.ns.twtrdns.net",
    "a.r06.twtrdns.net",
    "b.r06.twtrdns.net",
    "c.r06.twtrdns.net",
    "d.r06.twtrdns.net",
    "api-34-0-0.twitter.com",
    "api-47-0-0.twitter.com",
    "cheddar.twitter.com",
    "goldenglobes.twitter.com",
    "mx003.twitter.com",
    "pop-api.twitter.com",
    "spring-chicken-an.twitter.com",
    "spruce-goose-ae.twitter.com",
    "takeflight.twitter.com",
    "www2.twitter.com",
    "m.twitter.com",
    "mobile.twitter.com",
    "api.twitter.com",
]

# Applications to block (Executable Name: Full Path)
# !! IMPORTANT !! Update these paths if your installations are different!
# Common locations are used below. Check your system.
# Note: The key (e.g., "Discord") is only used for logging/display.
# The script now uses the *filename* from the path to kill the process.
APP_PATHS = {
    "Discord": os.path.expandvars(r"%LocalAppData%\Discord\Discord.exe"), # Target Discord.exe directly
    # Alternative Discord path if Update.exe doesn't work: find the latest app-X.Y.Z\Discord.exe
    # "DiscordApp": os.path.expandvars(r"%LocalAppData%\Discord\app-X.Y.Z\Discord.exe"), # Replace X.Y.Z
    "Telegram": os.path.expandvars(r"%AppData%\Telegram Desktop\Telegram.exe"),
    # Alternative Telegram Path:
    # "TelegramPF": r"C:\Program Files\Telegram Desktop\Telegram.exe",
    "Steam": r"C:\Program Files (x86)\Steam\Steam.exe",
}

# Hosts file path
HOSTS_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1" # Or "0.0.0.0"
HOSTS_MARKER = "# BLOCKED_BY_SCRIPT" # Marker to identify lines added by this script

# --- Helper Functions ---

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with administrative privileges."""
    if sys.platform == 'win32':
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0) # Exit the non-admin instance
        except Exception as e:
            print(f"Error requesting admin privileges: {e}")
            sys.exit(1)
    else:
        print("This script requires Windows and administrator privileges.")
        sys.exit(1)

def flush_dns():
    """Flush the DNS cache."""
    try:
        print("Flushing DNS cache...")
        subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True, text=True)
        print("DNS cache flushed successfully.")
    except FileNotFoundError:
        print("Error: 'ipconfig' command not found. Is it in your system's PATH?")
    except subprocess.CalledProcessError as e:
        print(f"Error flushing DNS cache: {e}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred during DNS flush: {e}")

def modify_hosts(block=True):
    """Add or remove entries from the hosts file."""
    print(f"{'Blocking' if block else 'Unblocking'} websites in hosts file...")
    try:
        with open(HOSTS_FILE_PATH, 'r') as f:
            lines = f.readlines()

        # Filter out existing blocked lines first
        filtered_lines = [line for line in lines if HOSTS_MARKER not in line]

        if block:
            # Add new block lines
            for site in WEBSITES_TO_BLOCK:
                filtered_lines.append(f"{REDIRECT_IP}\t{site}\t\t{HOSTS_MARKER}\n")
            action = "blocked"
        else:
            # Just keep the filtered lines (removes the blocks)
            action = "unblocked"

        # Write the modified content back
        with open(HOSTS_FILE_PATH, 'w') as f:
            f.writelines(filtered_lines)

        print(f"Websites {action} successfully.")
        if block or any(HOSTS_MARKER in line for line in lines): # Flush DNS if blocking or if unblocking previously blocked sites
             flush_dns()

    except FileNotFoundError:
        print(f"Error: Hosts file not found at {HOSTS_FILE_PATH}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied writing to {HOSTS_FILE_PATH}. Run as Administrator.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred modifying the hosts file: {e}")
        sys.exit(1)

def kill_target_processes():
    """Find and terminate processes listed in APP_PATHS."""
    killed_any = False
    for app_name, app_path in APP_PATHS.items():
        executable_name = os.path.basename(app_path)
        if not executable_name:
            print(f"Warning: Could not determine executable name for {app_name} from path '{app_path}'. Skipping.")
            continue

        command = ["taskkill", "/F", "/IM", executable_name, "/T"]
        try:
            creationflags = subprocess.CREATE_NO_WINDOW
            result = subprocess.run(command, check=False, capture_output=True, text=True, creationflags=creationflags) # check=False because it errors if process not found

            if result.returncode == 0:
                print(f"Successfully sent termination signal to processes matching {executable_name}.")
                killed_any = True
            elif result.returncode == 128 and "not found" in result.stderr.lower():
                pass
            else:
                 is_discord_termination_error = (
                     executable_name.lower() == "discord.exe" and
                     result.returncode != 0 and
                     ("could not be terminated" in result.stderr.lower() or
                      "could not be terminated" in result.stdout.lower())
                 )

                 if not is_discord_termination_error:
                     print(f"Error attempting to kill {executable_name}:")
                     print(f"  Return Code: {result.returncode}")
                     if result.stdout: print(f"  Stdout: {result.stdout.strip()}")
                     if result.stderr: print(f"  Stderr: {result.stderr.strip()}")
                 # else: If it is the specific Discord error, do nothing (silence it)

        except FileNotFoundError:
             print(f"Error: 'taskkill' command not found. Is it in your system's PATH?")
        except Exception as e:
            print(f"An unexpected error occurred while trying to kill {executable_name}: {e}")

# --- Process Killer Thread ---
def process_killer_loop(stop_event):
    """Continuously attempts to kill target processes until stop_event is set."""
    print("Process killer thread started.")
    while not stop_event.is_set():
        kill_target_processes()
        # Check stop_event frequently for responsiveness
        time.sleep(0.1) # Check every 100ms
        if stop_event.wait(timeout=0.9): # Wait for up to 0.9s
            break # Exit loop if event is set during wait
    print("Process killer thread stopped.")

# --- Main Execution ---

if __name__ == "__main__":
    # Check OS
    if platform.system() != "Windows":
        print("Error: This script is designed for Windows only.")
        sys.exit(1)

    # Check and request admin privileges
    if not is_admin():
        print("Administrator privileges required. Requesting elevation...")
        run_as_admin() # This will exit the current script if elevation is successful/attempted

    # --- Interactive Mode ---
    current_mode = "on" # Start in 'on' mode
    killer_thread = None
    stop_event = threading.Event()

    print("--- Initializing: Ensuring system is in 'on' mode ---")
    modify_hosts(block=True) # Ensure blocked state initially
    # Start the killer thread immediately for the initial 'on' state
    print("Starting process killer thread...")
    killer_thread = threading.Thread(target=process_killer_loop, args=(stop_event,), daemon=True)
    killer_thread.start()

    print("\n--- Deep Work Script Interactive Mode ---")
    print("Enter 'on' to block, 'off' to unblock, or 'exit' to quit.")

    try:
        while True:
            try:
                # Add a newline before the prompt for cleaner output
                user_input = input(f"\nCurrent mode: {current_mode}. Enter command (on/off/exit): ").strip().lower()
            except EOFError: # Handle Ctrl+Z or pipe closing
                print("\nEOF received, exiting...")
                user_input = "exit"

            if user_input == "on":
                if current_mode == "on":
                    print("Already in 'on' mode.")
                    continue
                print("--- Switching to Block ('on' mode) ---")
                modify_hosts(block=True)
                current_mode = "on"
                # Start the killer thread if it's not running
                if killer_thread is None or not killer_thread.is_alive():
                    print("Starting process killer thread...")
                    stop_event.clear() # Ensure event is clear before starting
                    killer_thread = threading.Thread(target=process_killer_loop, args=(stop_event,), daemon=True) # Use daemon thread
                    killer_thread.start()
                print("--- Block ('on' mode) activated ---")

            elif user_input == "off":
                if current_mode == "off":
                    print("Already in 'off' mode.")
                    continue
                print("--- Switching to Unblock ('off' mode) ---")

                # Confirmation prompt
                confirmation_phrase = "I will not stop cool deepwork session"
                try:
                    confirm_input = input(f"Please type the following phrase exactly to confirm: '{confirmation_phrase}'\nEnter phrase: ")
                except EOFError:
                    print("\nEOF received during confirmation, cancelling 'off' switch.")
                    continue # Go back to the main loop

                if confirm_input.strip() != confirmation_phrase:
                    print("Confirmation failed. Staying in 'on' mode.")
                    continue # Skip unblocking

                # Stop the killer thread if it's running
                if killer_thread is not None and killer_thread.is_alive():
                    print("Stopping process killer thread...")
                    stop_event.set()
                    killer_thread.join(timeout=5.0) # Wait max 5s for thread to stop
                    if killer_thread.is_alive():
                        print("Warning: Process killer thread did not stop gracefully.")
                    killer_thread = None
                else:
                     print("Process killer thread was not running.") # Added for clarity
                modify_hosts(block=False)
                current_mode = "off"
                print("--- Unblock ('off' mode) activated ---")

            elif user_input == "exit":
                print("--- Exiting Script ---")
                # Ensure everything is unblocked on exit
                if current_mode == "on":
                    print("Switching to 'off' mode before exiting...")
                    if killer_thread is not None and killer_thread.is_alive():
                        print("Stopping process killer thread...")
                        stop_event.set()
                        killer_thread.join(timeout=5.0)
                        if killer_thread.is_alive():
                            print("Warning: Process killer thread did not stop gracefully on exit.")
                        killer_thread = None
                    modify_hosts(block=False)
                    current_mode = "off" # Update status for final message
                    print("'off' mode restored.")
                print("Exiting.")
                break # Exit the main loop

            else:
                print(f"Invalid command: '{user_input}'. Please use 'on', 'off', or 'exit'.")

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting gracefully...")
        # Perform cleanup similar to 'exit' command
        if current_mode == "on":
            print("Switching to 'off' mode before exiting...")
            if killer_thread is not None and killer_thread.is_alive():
                print("Stopping process killer thread...")
                stop_event.set()
                # Don't wait indefinitely on Ctrl+C, give it a short time
                killer_thread.join(timeout=2.0)
            modify_hosts(block=False)
            print("'off' mode restored.")
        print("Exiting.")
    finally:
        # Final check to ensure thread is stopped if still alive somehow
        if killer_thread is not None and killer_thread.is_alive():
            print("Final check: Stopping lingering process killer thread...")
            stop_event.set()
            # No long join here, as we are force exiting

        print("\nScript finished.")
        # No need for input("Press Enter...") in interactive mode