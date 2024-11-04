import schedule
import time
import json
import os
import subprocess
from datetime import datetime
import logging

logging.basicConfig(
    filename='task_scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        return None

def run_task(task_name, script_path, interpreter):
    try:
        logging.info(f"Running task: {task_name}")
        subprocess.run(
            [interpreter, script_path], 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        logging.info(f"Task completed: {task_name}")
    except Exception as e:
        logging.error(f"Error running task {task_name}: {str(e)}")

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
        logging.info(f"Scheduled task: {task_name} at {schedule_time} using {interpreter}")

def main():
    logging.info("Task scheduler started")
    schedule_tasks()
    
    print(f"Scheduler started at: {datetime.now().strftime('%H:%M:%S')}")
    print("Scheduled tasks:")
    
    for job in schedule.get_jobs():
        print(f"- Next run at: {job.next_run}")
    
    while True:
        current_time = datetime.now().strftime('%H:%M')
        print(f"\rCurrent time: {current_time} - Checking for tasks...", end="")
        
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
