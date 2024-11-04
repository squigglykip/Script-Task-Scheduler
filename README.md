# Task Scheduler

A lightweight Python-based task scheduler that runs in the background and executes scripts at specified times.

## Features

- Run Python scripts at scheduled times
- Configure tasks through a simple JSON file
- Background execution with no GUI
- Comprehensive logging system
- Automatic startup with Windows

## Installation

1. Clone this repository or download the files:
   - `main.py`
   - `config.json`

2. Install required package:

   ```bash
   pip install schedule
   ```

## Configuration

### 1. Configure Your Tasks

Edit `config.json` to specify your tasks:

   ```json
   {
     "tasks": [
       {
         "name": "Task Name",
         "interpreter": "python",
         "script_path": "C:/path/to/your/script.py",
         "time": "HH:MM"
       }
     ]
   }
   ```

- `name`: A descriptive name for your task
- `interpreter`: The programme to run the script (e.g., "python", "node", "cmd", "powershell")
- `script_path`: Full path to the script (use forward slashes)
- `time`: 24-hour format (e.g., "09:00" for 9 AM, "23:00" for 11 PM)

### Supported Interpreters
- `python`: For Python scripts (.py)
- `node`: For Node.js scripts (.js)
- `cmd`: For batch files (.bat)
- `powershell`: For PowerShell scripts (.ps1)
- Add more as needed for your use case

### 2. Setup Auto-Start

#### Method 1: Using a BAT File (Recommended)

1. Create a new text file and paste the following:

   ```batch
   @echo off
   pythonw "C:\path\to\your\main.py"
   ```

2. Save the file as `task_scheduler.bat`

3. Place the BAT file in the Windows Startup folder:
   - Press `Win + R`
   - Type `shell:startup`
   - Copy your BAT file to this folder

#### Method 2: Direct Script Shortcut

1. Right-click `main.py` → Create shortcut
2. Press `Win + R`, type `shell:startup`
3. Move the shortcut to the startup folder

## Logging

The scheduler creates a `task_scheduler.log` file in the same directory as `main.py`. The log includes:
- Scheduler start/stop events
- Task execution attempts
- Errors and exceptions

Example log entry:
2024-03-21 09:00:01 - INFO - Task scheduler started
2024-03-21 09:00:01 - INFO - Scheduled task: Daily Backup at 23:00
2024-03-21 09:00:01 - INFO - Scheduled task: Data Processing at 09:00

## How It Works

The task scheduler uses the `schedule` package to manage task timings. It reads the configuration from `config.json`, schedules tasks based on the specified times, and runs the corresponding Python scripts using the `subprocess` module. The scheduler continuously checks for pending tasks every minute and logs all activities and errors.

## Troubleshooting

1. **Script Not Running:**
   - Check `task_scheduler.log` for errors
   - Verify Python paths in the BAT file
   - Ensure all file paths in `config.json` are correct

2. **Tasks Not Executing:**
   - Confirm script paths in `config.json` are valid
   - Check file permissions
   - Verify time format is correct (24-hour format)

3. **Console Window Shows:**
   - Ensure you're using `pythonw` instead of `python` in the BAT file

## Best Practices

1. Use absolute paths in `config.json`
2. Keep logs for monitoring and debugging
3. Test scripts individually before scheduling
4. Use descriptive task names
5. Maintain consistent time formats

## Requirements

- Python 3.6 or higher
- Windows OS
- `schedule` package

## Licence

This project is open source and available under the MIT Licence.