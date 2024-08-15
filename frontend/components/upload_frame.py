import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import requests
import os, json 
import subprocess
import shlex
import sys

class UploadFrame(tk.Frame):
    def __init__(self, parent, show_result_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.show_result_callback = show_result_callback

        self.label = tk.Label(self, text="Choose an image or video...")
        self.label.pack(pady=10)
        
        self.upload_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.upload_button.pack(pady=10)
        
        self.container_label = tk.Label(self, text="Select Model:")
        self.container_label.pack(pady=10)
        
        self.container_var = tk.StringVar()
        self.container_var.set("Loading containers...")
        self.container_dropdown = OptionMenu(self, self.container_var, "Loading containers...", command=self.update_model_info)
        self.container_dropdown.pack(pady=10)

        self.model_info_label = tk.Label(self, text="")
        self.model_info_label.pack(pady=10)

        self.selection_label = tk.Label(self, text="Select Output Types:")
        self.selection_label.pack(pady=10)
        
        self.npz_var = tk.BooleanVar()
        self.image_var = tk.BooleanVar()

        self.npz_checkbox = tk.Checkbutton(self, text="npz", variable=self.npz_var)
        self.npz_checkbox.pack(pady=5)
        
        self.image_checkbox = tk.Checkbutton(self, text="image", variable=self.image_var)
        self.image_checkbox.pack(pady=5)

        self.output_label = tk.Label(self, text="Choose output path...")
        self.output_label.pack(pady=10)

        self.output_button = tk.Button(self, text="Save To", command=self.browse_output_folder)
        self.output_button.pack(pady=(10,0))

        self.output_path_label = tk.Label(self, text="")
        self.output_path_label.pack(pady=10)

        self.submit_button = tk.Button(self, text="Start", command=self.upload_input)
        self.submit_button.pack(pady=20)
        
        self.file_path = None
        self.folder_path = None
        self.output_path =None

        with open('model_description.json', 'r') as f:
            self.model_info = json.load(f)

        with open('model_input_data_type.json', 'r') as f:
            self.models = json.load(f)

        self.filter_models()
    
    def filter_models(self):
        combined_values = self.models["image"] + self.models["video"]
        model_names = list(set(combined_values))
        self.update_container_dropdown(model_names)

    def update_container_dropdown(self, model_names):
        self.container_dropdown['menu'].delete(0, 'end')
        for name in model_names:
            self.container_dropdown['menu'].add_command(label=name, command=tk._setit(self.container_var, name, self.update_model_info))
        
        if model_names:
            self.container_var.set(model_names[0])
            self.update_model_info(model_names[0])
        else:
            self.container_var.set("No containers found")

    def update_model_info(self, selected_model):
        info = self.model_info.get(selected_model, "No information available")
        self.model_info_label.config(text=info)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("JPG", "*.jpg"), ("PNG", "*.png"), ("JPEG", "*.jpeg"), ("MP4", "*.mp4"), ("AVI", "*.avi")])
        if self.file_path:
            self.label.config(text=f"Selected file: {self.file_path}")
            self.folder_path = None  # Reset folder path if a file is selected
            file_extension = os.path.splitext(self.file_path)[1].lower()
            if file_extension in [".jpg", ".jpeg", ".png"]:
                self.update_container_dropdown(self.models["image"])
            elif file_extension in [".mp4", ".avi"]:
                self.update_container_dropdown(self.models["video"])
            else:
                messagebox.showerror("Error", "Unsupported file type")
    
    def browse_output_folder(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            self.output_path_label.config(text=f"Selected output path: {self.output_path}")

    def check_single_person(self, video_path, conf_threshold=0.5):
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

    def upload_input(self):
        if not self.file_path and not self.folder_path:
            messagebox.showerror("Error", "No file or folder selected")
            return
        selected_model = self.container_var.get()
        if selected_model == "ExPose" and self.file_path and self.file_path.lower().endswith(('.mp4', '.avi')):
            loading_window = self.show_loading_window()
            self.after(100, self.check_person_and_proceed,loading_window)
        else:
            self.upload()


    def show_loading_window(self):
        loading_window = tk.Toplevel(self)
        loading_window.title("Processing")
        tk.Label(loading_window, text="Checking video for single person, please wait...").pack(padx=20, pady=20)
        return loading_window
        
    def close_loading_window(self, window):
        window.destroy()

    def check_person_and_proceed(self, loading_window ):
        person_check_result = self.check_single_person(self.file_path)
        self.close_loading_window(loading_window)

        if person_check_result == 1:
            messagebox.showerror("Error", "The selected video contains more than one person. Please select another video.")
            return
        elif person_check_result == 0:
            messagebox.showinfo("Success", "The video contains only one person and is suitable for processing.")
            self.upload()
        else:
            messagebox.showerror("Error", "There was an error processing the video. Please check the file and try again.")
            return

    def upload(self):
            selected_options = []
            if self.npz_var.get():
                selected_options.append("npz")
            if self.image_var.get():
                selected_options.append("image")

            if not selected_options:
                messagebox.showerror("Error", "No output types selected")
                return
        
            container_name = self.container_var.get()
            try:
                with open(self.file_path, 'rb') as image_file:
                    files = {'image': image_file}
                    data = {'model': container_name, 
                            'save_to_folder': self.output_path, 
                            'output_types': ','.join(selected_options)}  # Use 'model' to match the backend expectation

                    response = requests.post("http://127.0.0.1:5000/upload", files=files, data=data)
                    if response.status_code == 200:
                        self.show_result_callback(response.json())
                    else:
                        messagebox.showerror("Error", f"Failed to upload image: {response.json()}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Upload Image for Parameter Estimation")
    UploadFrame(root, lambda x: print(x)).pack(fill="both", expand=True)
    root.mainloop()
