import schedule
import time
import json
import os
import subprocess
from datetime import datetime
import logging
import sys
from utils import get_app_path, get_resource_path

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Get application root directory
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    app_root = os.path.dirname(sys.executable)
else:
    # Running as script
    app_root = os.path.dirname(os.path.dirname(__file__))

# Create logs directory if it doesn't exist
logs_dir = os.path.join(app_root, 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Create file handler
file_handler = logging.FileHandler(
    os.path.join(logs_dir, 'task_scheduler.log')
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Configure root logger
logging.getLogger('').setLevel(logging.INFO)
logging.getLogger('').addHandler(console_handler)
logging.getLogger('').addHandler(file_handler)

def load_config():
    try:
        config_path = get_app_path('config.json')
        if not os.path.exists(config_path):
            default_config = {"tasks": []}
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
        
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        return {"tasks": []}  # Return empty config instead of None

def run_task(task_name, script_path, interpreter):
    try:
        logging.info(f"Starting task: {task_name}")
        subprocess.run(
            [interpreter, script_path], 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        logging.info(f"Successfully completed task: {task_name}")
    except Exception as e:
        logging.error(f"Failed to run task {task_name}: {str(e)}")

def schedule_tasks():
    config = load_config()
    if not config:
        return

    schedule.clear()

    for task in config['tasks']:
        task_name = task['name']
        script_path = task['script_path']
        interpreter = task['interpreter']
        schedule_time = task['time']
        
        schedule.every().day.at(schedule_time).do(
            run_task, task_name, script_path, interpreter
        )