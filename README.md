# Deep Work Scripts

This repository contains Python scripts designed to help you focus during deep work sessions by blocking distracting websites and applications.

## Features

- **Cross-Platform:** Includes separate scripts for Windows (`deepwork_windows.py`) and Linux (`deepwork_linux.py`).
- **Website Blocking:** Modifies the system's `hosts` file to redirect common distracting websites (social media, news, etc.) to localhost.
- **Application Blocking:**
    - **Windows:** Terminates specified applications (e.g., Discord, Telegram) repeatedly.
    - **Linux:** Kills specified application processes repeatedly.
- **Interactive Control:** Allows toggling the blocking "on" and "off" via simple commands in the terminal.
- **Admin/Root Privileges:** Automatically requests necessary permissions (Administrator on Windows, expects to be run with `sudo` on Linux).
- **DNS Flushing (Windows):** Flushes the DNS cache after modifying the hosts file to ensure changes take effect quickly.
- **Commitment Prompt (Linux):** Requires typing a commitment phrase before turning off blocking mode.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd deepwork-scripts # Or your chosen directory name
    ```
2.  **Review Configuration:**
    - **Windows (`deepwork_windows.py`):**
        - Update `WEBSITES_TO_BLOCK` with any additional sites you want to block.
        - **Crucially:** Verify and update the paths in `APP_PATHS` to match the locations of the applications you want to block on *your* system. The defaults might not be correct for your installation.
    - **Linux (`deepwork_linux.py`):**
        - Modify `blocked_etc_host_file_content` and `unblocked_etc_host_file_content` directly to control which websites are blocked. The current implementation overwrites `/etc/hosts` entirely with these strings.
        - Update `app_list` with the process names (as seen by `pkill`) of the applications you want to block.

## Usage

### Windows (`deepwork_windows.py`)

1.  Open PowerShell or Command Prompt **as Administrator**.
2.  Navigate to the script's directory: `cd path\to\scripts`
3.  Run the script: `python deepwork_windows.py`
4.  The script will start in 'on' (blocking) mode.
5.  Enter commands:
    - `on`: Ensure blocking is active (terminates apps, blocks hosts).
    - `off`: Disable blocking (stops terminating apps, unblocks hosts).
    - `exit`: Disable blocking and exit the script.
6.  Use `Ctrl+C` to exit gracefully (also disables blocking).

**Note:** The Windows script needs Administrator privileges to modify the hosts file and kill processes effectively. It will attempt to re-launch itself with elevation if not run as admin initially.

### Linux (`deepwork_linux.py`)

1.  Open your terminal.
2.  Navigate to the script's directory: `cd path/to/scripts`
3.  Run the script with `sudo`: `sudo python3 deepwork_linux.py`
4.  The script will start in 'on' (blocking) mode.
5.  Enter commands:
    - `on`: Ensure blocking is active (kills processes, blocks hosts).
    - `off`: Disable blocking (stops killing processes, unblocks hosts). Requires typing a commitment phrase.
6.  Use `Ctrl+C` to interrupt the script (blocking might remain active depending on when you interrupt; it's better to use the `off` command).

**Note:** The Linux script requires root (`sudo`) privileges to modify the `/etc/hosts` file and kill processes owned by other users if necessary.

## Disclaimer

- Modifying system files like `hosts` requires care. Ensure you understand the changes being made.
- The application blocking mechanism relies on repeatedly killing processes, which might not be foolproof for all applications, especially those with aggressive restart mechanisms.
- Use these scripts responsibly. 