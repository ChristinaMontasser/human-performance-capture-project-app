import os
import subprocess
import shlex
import sys
from tkinter import messagebox
import tkinter as tk


def check_single_person(video_path, conf_threshold=0.5):
    script_path = os.path.join(os.path.dirname(__file__), 'detect_single_human.py')
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'yolov5s.pt')

    if not os.path.exists(script_path):
        print(f"Error: Script file {script_path} does not exist.")
        messagebox.showerror("Error", f"Script file {script_path} does not exist.")
        return 2  
    
    if not os.path.exists(model_path):
        print(f"Error: Model file {model_path} does not exist.")
        messagebox.showerror("Error", f"Model file {model_path} does not exist.")
        return 2  
        
    script_path_quoted = shlex.quote(script_path)
    print('i am testing the human in video')

    result = subprocess.run(
            [sys.executable, script_path, '--model_path', model_path, '--video_path', video_path], 
            env=os.environ.copy(), 
            check=True,
            capture_output=True,
            text=True
        )
    print('i am done with video')
    return result.returncode


def show_loading_window(parent):
    loading_window = tk.Toplevel(parent)
    loading_window.title("Processing")
    tk.Label(loading_window, text="Checking video for single person, please wait...").pack(padx=20, pady=20)
    return loading_window
        
def close_loading_window(window):
    window.destroy()
