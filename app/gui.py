import customtkinter as ctk
from PIL import Image, ImageTk
import pystray
import threading
from datetime import datetime, timedelta
import schedule
import json
import logging
import time
from main import schedule_tasks, run_task, load_config, app_root
import os
from tkinter import filedialog
import sys
from utils import get_app_path, get_resource_path

class TaskSchedulerGUI:
    def __init__(self):
        # Add this near the top of __init__, before using weights
        self.headers = ["Task Name", "Interpreter", "Next Run", "Time Remaining", "Actions"]
        self.weights = [4, 2, 2, 2, 2]  # Removed Script Path, adjusted weights
        
        self.root = ctk.CTk()
        self.root.title("Task Scheduler")
        self.root.geometry("1024x768")
        
        # Set window icon
        icon_path = get_resource_path(os.path.join('assets', 'scheduler.png'))
        try:
            if os.path.exists(icon_path):
                # Load and resize image
                icon = Image.open(icon_path)
                icon = icon.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(icon)
                self.root.iconphoto(True, photo)
            else:
                logging.warning(f"Icon file not found at: {icon_path}")
        except Exception as e:
            logging.error(f"Failed to load icon: {str(e)}")
        
        # Header frame
        self.header = ctk.CTkFrame(self.root)
        self.header.pack(fill="x", padx=10, pady=5)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header,
            text="Task Scheduler",
            font=("Epilogue", 24, "bold")
        )
        self.title_label.pack(side="left", padx=10)
        
        # Clock
        self.clock_label = ctk.CTkLabel(
            self.header,
            text="",
            font=("Source Sans Pro", 16)
        )
        self.clock_label.pack(side="right", padx=10)
        
        # Main container
        self.container = ctk.CTkFrame(self.root)
        self.container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Task list frame with title
        self.task_frame = ctk.CTkFrame(self.container)
        self.task_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.task_title = ctk.CTkLabel(
            self.task_frame,
            text="Scheduled Tasks",
            font=("Epilogue", 14, "bold"),
            anchor="w"
        )
        self.task_title.pack(side="left", padx=10, pady=2)
        
        # Task table frame
        self.task_frame = ctk.CTkFrame(self.container)
        self.task_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Table headers
        self.headers_frame = ctk.CTkFrame(self.task_frame)
        self.headers_frame.pack(fill="x", padx=5, pady=2)
        
        # Configure grid columns with weights
        for i, weight in enumerate(self.weights):
            self.headers_frame.grid_columnconfigure(i, weight=weight)
        
        for i, (header, weight) in enumerate(zip(self.headers, self.weights)):
            header_label = ctk.CTkLabel(
                self.headers_frame,
                text=header,
                font=("Epilogue", 12, "bold"),
                anchor="w",
                padx=10
            )
            header_label.grid(row=0, column=i, sticky="ew", padx=5)
        
        # Scrollable table content
        self.table_frame = ctk.CTkScrollableFrame(self.task_frame)
        self.table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Control buttons
        self.button_frame = ctk.CTkFrame(self.container)
        self.button_frame.pack(fill="x", padx=5, pady=5)
        
        self.add_button = ctk.CTkButton(
            self.button_frame, 
            text="Add Task", 
            command=self.add_task
        )
        self.add_button.pack(side="left", padx=5)
        
        self.refresh_button = ctk.CTkButton(
            self.button_frame,
            text="Refresh Tasks",
            command=self.refresh_tasks
        )
        self.refresh_button.pack(side="left", padx=5)
        
        # Status bar
        self.status = ctk.CTkLabel(
            self.container,
            text="Starting scheduler..."
        )
        self.status.pack(pady=5)
        
        # Logs section
        self.logs_frame = ctk.CTkFrame(self.container)
        self.logs_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.logs_title = ctk.CTkLabel(
            self.logs_frame,
            text="Task Logs",
            font=("Epilogue", 14, "bold"),
            anchor="w"
        )
        self.logs_title.pack(side="left", padx=10, pady=2)

        self.logs_text = ctk.CTkTextbox(self.logs_frame)
        self.logs_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Start update threads
        self.update_clock()
        self.refresh_tasks()
        self.update_logs()
        
        # Start scheduler in background
        self.scheduler_thread = threading.Thread(
            target=self.run_scheduler, 
            daemon=True
        )
        self.scheduler_thread.start()
        
    def update_clock(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        self.clock_label.configure(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def refresh_tasks(self):
        # Clear existing tasks
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Load and display tasks
        config = load_config()
        if config and 'tasks' in config:
            for task in config['tasks']:
                row_frame = ctk.CTkFrame(self.table_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                
                # Calculate time until next run
                now = datetime.now()
                task_time = datetime.strptime(task['time'], '%H:%M').time()
                task_datetime = datetime.combine(now.date(), task_time)
                if task_datetime < now:
                    task_datetime = datetime.combine(now.date() + timedelta(days=1), task_time)
                time_until = task_datetime - now
                
                hours, remainder = divmod(time_until.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                
                # Row data
                data = [
                    task['name'],
                    task['interpreter'],
                    task['time'],
                    f"{hours}h {minutes}m"
                ]
                
                self.create_task_row(row_frame, data, self.weights)
        
        # Update every minute instead of every second
        self.root.after(60000, self.refresh_tasks)
    
    def create_task_row(self, row_frame, data, weights):
        # Configure grid columns with weights
        for i, weight in enumerate(weights):
            row_frame.grid_columnconfigure(i, weight=weight)
        
        # Create cells for data
        for i, (item, weight) in enumerate(zip(data, weights[:-1])):
            cell = ctk.CTkLabel(
                row_frame,
                text=item,
                font=("Source Sans Pro", 12),
                anchor="w",
                padx=10
            )
            cell.grid(row=0, column=i, sticky="ew", padx=5)
        
        # Add actions frame
        actions_frame = ctk.CTkFrame(row_frame)
        actions_frame.grid(row=0, column=len(data), sticky="ew", padx=5)
        
        # Add edit link
        edit_link = ctk.CTkLabel(
            actions_frame,
            text="edit",
            text_color="#3B8ED0",
            cursor="hand2",
            anchor="w",
            padx=5
        )
        edit_link.pack(side="left", padx=5)
        edit_link.bind("<Button-1>", lambda e, name=data[0]: self.edit_task(name))
        
        # Add separator
        separator = ctk.CTkLabel(actions_frame, text="|", padx=2)
        separator.pack(side="left")
        
        # Add delete link
        delete_link = ctk.CTkLabel(
            actions_frame,
            text="delete",
            text_color="#3B8ED0",
            cursor="hand2",
            anchor="w",
            padx=5
        )
        delete_link.pack(side="left", padx=5)
        delete_link.bind("<Button-1>", lambda e, name=data[0]: self.delete_task(name))
        
        # Add hover effects
        for link in [edit_link, delete_link]:
            link.bind("<Enter>", lambda e, l=link: l.configure(font=("Source Sans Pro", 13, "underline")))
            link.bind("<Leave>", lambda e, l=link: l.configure(font=("Source Sans Pro", 13)))
    
    def add_task(self):
        dialog = AddTaskDialog(self.root)
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                new_task = dialog.result
                config = load_config()
                config['tasks'].append(new_task)
                config_path = get_app_path('config.json')
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=4)
                schedule_tasks()
                self.refresh_tasks()
            except Exception as e:
                logging.error(f"Error adding task: {str(e)}")
    
    def run_scheduler(self):
        schedule_tasks()  # Your existing scheduler function
        while True:
            schedule.run_pending()
            self.update_status()
            time.sleep(60)
            
    def update_status(self):
        # Update GUI with current status
        self.status.configure(
            text=f"Last check: {datetime.now().strftime('%H:%M')}"
        )
    
    def update_logs(self):
        try:
            log_path = get_app_path(os.path.join('logs', 'task_scheduler.log'))
            with open(log_path, 'r') as f:
                logs = f.read()
                self.logs_text.delete('1.0', 'end')
                self.logs_text.insert('1.0', logs)
        except Exception as e:
            logging.error(f"Error reading logs: {str(e)}")
        
        # Update logs every 5 seconds
        self.root.after(5000, self.update_logs)
    
    def delete_task(self, task_name):
        try:
            config = load_config()
            config['tasks'] = [task for task in config['tasks'] if task['name'] != task_name]
            config_path = get_app_path('config.json')
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            schedule_tasks()
            self.refresh_tasks()
        except Exception as e:
            logging.error(f"Error deleting task: {str(e)}")
    
    def edit_task(self, task_name):
        config = load_config()
        task = next((t for t in config['tasks'] if t['name'] == task_name), None)
        if task:
            dialog = AddTaskDialog(self.root, task)  # Pass the task for editing
            self.root.wait_window(dialog)
            
            if dialog.result:
                try:
                    # Remove old task
                    config['tasks'] = [t for t in config['tasks'] if t['name'] != task_name]
                    # Add updated task
                    config['tasks'].append(dialog.result)
                    config_path = get_app_path('config.json')
                    with open(config_path, 'w') as f:
                        json.dump(config, f, indent=4)
                    schedule_tasks()
                    self.refresh_tasks()
                except Exception as e:
                    logging.error(f"Error updating task: {str(e)}")

class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, task=None):
        super().__init__(parent)
        self.title("Edit Task" if task else "Add Task")
        
        # Initialize result variables
        self.result = None
        self.interpreters = ["python", "node", "cmd", "powershell"]
        
        # Create all widgets first
        # Name Field
        self.name_label = ctk.CTkLabel(self, text="Task Name:")
        self.name_label.pack(padx=20, pady=(20,5), anchor="w")
        self.name_entry = ctk.CTkEntry(self, width=400)
        self.name_entry.pack(padx=20, pady=(0,15))
        
        # Interpreter Dropdown
        self.interpreter_label = ctk.CTkLabel(self, text="Interpreter:")
        self.interpreter_label.pack(padx=20, pady=(5,5), anchor="w")
        self.interpreter_var = ctk.StringVar(value=self.interpreters[0])
        self.interpreter_dropdown = ctk.CTkOptionMenu(
            self,
            values=self.interpreters,
            variable=self.interpreter_var,
            width=400
        )
        self.interpreter_dropdown.pack(padx=20, pady=(0,15))
        
        # Script Path Field with Browse Button
        self.path_label = ctk.CTkLabel(self, text="Script Path:")
        self.path_label.pack(padx=20, pady=(5,5), anchor="w")
        
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(fill="x", padx=20, pady=(0,15))
        
        self.path_entry = ctk.CTkEntry(self.path_frame, width=300)
        self.path_entry.pack(side="left", padx=(0,10))
        
        self.browse_button = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            width=90,
            command=self.browse_file
        )
        self.browse_button.pack(side="right")
        
        # Time Selection
        self.time_label = ctk.CTkLabel(self, text="Time (24-hour):")
        self.time_label.pack(padx=20, pady=(5,5), anchor="w")
        
        self.time_frame = ctk.CTkFrame(self)
        self.time_frame.pack(fill="x", padx=20, pady=(0,15))
        
        # Generate time values
        hours = [f"{h:02d}" for h in range(24)]
        minutes = [f"{m:02d}" for m in range(0, 60, 5)]
        
        self.hour_var = ctk.StringVar(value="00")
        self.hour_dropdown = ctk.CTkOptionMenu(
            self.time_frame,
            values=hours,
            variable=self.hour_var,
            width=190
        )
        self.hour_dropdown.pack(side="left", padx=(0,10))
        
        self.minute_var = ctk.StringVar(value="00")
        self.minute_dropdown = ctk.CTkOptionMenu(
            self.time_frame,
            values=minutes,
            variable=self.minute_var,
            width=190
        )
        self.minute_dropdown.pack(side="right")
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=20, pady=(20,20))
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.cancel,
            width=190
        )
        self.cancel_button.pack(side="left")
        
        self.ok_button = ctk.CTkButton(
            self.button_frame,
            text="Add Task",
            command=self.ok,
            width=190
        )
        self.ok_button.pack(side="right")
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # If editing, populate fields with existing task data
        if task:
            self.name_entry.insert(0, task['name'])
            self.interpreter_var.set(task['interpreter'])
            self.path_entry.insert(0, task['script_path'])
            hour, minute = task['time'].split(':')
            self.hour_var.set(hour)
            self.minute_var.set(minute)
    
    def browse_file(self):
        filetypes = [
            ("All Scripts", "*.py;*.js;*.bat;*.ps1"),
            ("Python Files", "*.py"),
            ("JavaScript Files", "*.js"),
            ("Batch Files", "*.bat"),
            ("PowerShell Scripts", "*.ps1"),
            ("All Files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, filename)
    
    def ok(self):
        self.result = {
            "name": self.name_entry.get(),
            "interpreter": self.interpreter_var.get(),
            "script_path": self.path_entry.get(),
            "time": f"{self.hour_var.get()}:{self.minute_var.get()}"
        }
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()

if __name__ == "__main__":
    app = TaskSchedulerGUI()
    app.root.mainloop()