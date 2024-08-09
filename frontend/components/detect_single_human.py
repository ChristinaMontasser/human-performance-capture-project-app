# import cv2
# import torch
# import argparse
# import os
# import sys


# def detect_single_person_in_video(model, video_path, conf_threshold=0.5):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print(f"Error opening video file: {video_path}")
#         return False

#     frame_count = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame_count += 1
#         results = model(frame)
#         persons = [d for d in results.xyxy[0] if int(d[-1]) == 0 and d[4] > conf_threshold]
#         if len(persons) != 1:
#             cap.release()
#             return False

#     cap.release()
#     return True


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Detect if a video contains a single person.')
#     parser.add_argument('--model_path', type=str, required=True, help='Path to the .pt model file')
#     parser.add_argument('--video_path', type=str, required=True, help='Path to the video file')
#     parser.add_argument('--conf_threshold', type=float, default=0.5, help='Confidence threshold for detecting persons')

#     args = parser.parse_args()

#     model = torch.hub.load('ultralytics/yolov5', 'custom', path=args.model_path)

#     is_single_person = detect_single_person_in_video(model, args.video_path, args.conf_threshold)
#     print(f"Video {os.path.basename(args.video_path)} contains a single person: {is_single_person}")

#     if is_single_person:
#         sys.exit(0)
#     else:
#         sys.exit(1)


import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import requests
import os
import cv2
import torch

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
        
        self.start_button = tk.Button(self, text="Start Model", command=self.start_container)
        self.start_button.pack(pady=10)
        
        self.submit_button = tk.Button(self, text="Upload", command=self.upload_input)
        self.submit_button.pack(pady=20)

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
        
        self.file_path = None
        self.folder_path = None

        self.model_info = {
            "Pare": "Dealing with occlusion",
            "ExPose": "Fast and accurate model\n<only accept video with single person or image>",
            "4DHumans": "Track multiple person"
        }

        self.models = {
            "image": ["ExPose", "4DHumans", "Pare"],
            "video": ["ExPose", "4DHumans", "Pare"]
        }

        self.populate_models()
    
    def populate_models(self):
        model_names = ["ExPose", "4DHumans", "Pare"]
        self.update_container_dropdown(model_names)

    def update_container_dropdown(self, container_names):
        self.container_dropdown['menu'].delete(0, 'end')
        for name in container_names:
            self.container_dropdown['menu'].add_command(label=name, command=tk._setit(self.container_var, name, self.update_model_info))
        
        if container_names:
            self.container_var.set(container_names[0])
            self.update_model_info(container_names[0])
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

    def detect_single_person_in_video(self, model, video_path, conf_threshold=0.5):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return False

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            results = model(frame)
            persons = [d for d in results.xyxy[0] if int(d[-1]) == 0 and d[4] > conf_threshold]
            if len(persons) != 1:
                cap.release()
                return False

        cap.release()
        return True

    def check_single_person(self, video_path, conf_threshold=0.5):
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'yolov5s.pt')

        if not os.path.exists(model_path):
            print(f"Error: Model file {model_path} does not exist.")
            messagebox.showerror("Error", f"Model file {model_path} does not exist.")
            return 2  

        try:
            # Load the model
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
            
            # Perform detection
            is_single_person = self.detect_single_person_in_video(model, video_path, conf_threshold)
            
            # Return 0 if a single person is detected, else return 1
            if is_single_person:
                print(f"Video {os.path.basename(video_path)} contains a single person: True")
                return 0
            else:
                print(f"Video {os.path.basename(video_path)} contains a single person: False")
                return 1
        
        except Exception as e:
            print(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred during detection:\n{e}")
            return 2

    def upload_input(self):
        if not self.file_path and not self.folder_path:
            messagebox.showerror("Error", "No file or folder selected")
            return

        selected_model = self.container_var.get()

        def show_loading_window():
            loading_window = tk.Toplevel(self)
            loading_window.title("Processing")
            tk.Label(loading_window, text="Checking video for single person, please wait...").pack(padx=20, pady=20)
            return loading_window

        def close_loading_window(window):
            window.destroy()

        def check_person_and_proceed():
            person_check_result = self.check_single_person(self.file_path)
            close_loading_window(loading_window)

            if person_check_result == 1:
                messagebox.showerror("Error", "The selected video contains more than one person. Please select another video.")
                return
            elif person_check_result == 0:
                messagebox.showinfo("Success", "The video contains only one person and is suitable for processing.")
                proceed_with_upload()
            else:
                messagebox.showerror("Error", "There was an error processing the video. Please check the file and try again.")
                return

        def proceed_with_upload():
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

        if selected_model == "ExPose" and self.file_path and self.file_path.lower().endswith(('.mp4', '.avi')):
            loading_window = show_loading_window()
            self.after(100, check_person_and_proceed)
        else:
            proceed_with_upload()

    def start_container(self, container_name=None):
        if container_name is None:
            container_name = self.container_var.get()

        try:
            data = {'container_name': container_name}
            response = requests.post("http://localhost:5000/start", json=data)
           
            if response.status_code == 200:
                messagebox.showinfo("Success", f"Started container: {container_name}")
            else:
                messagebox.showerror("Error", f"Failed to start container: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Upload Image for Parameter Estimation")
    UploadFrame(root, lambda x: print(x)).pack(fill="both", expand=True)
    root.mainloop()
