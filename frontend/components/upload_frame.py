import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import requests
import os

class UploadFrame(tk.Frame):
    def __init__(self, parent, show_result_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.show_result_callback = show_result_callback

        self.label = tk.Label(self, text="Choose an image...")
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
        
        # self.process_button = tk.Button(self, text="Upload and Start Model", command=self.upload_and_start_model)
        # self.process_button.pack(pady=20)
        
        self.file_path = None
        self.folder_path = None

        self.model_info = {
            "Pare": "Good at dealing with occlusion",
            "ExPose": "Fast and accurate model with precise hands and face\n<can only accept single image>",
            "4DHumans": "Track 4D humans"
        }

        self.models = {
            "image": ["ExPose"],
            "video": ["4DHumans", "Pare"]
        }

        self.populate_models()
    
    def populate_models(self):
        model_names = ["Pare", "ExPose", "4DHumans"]
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
        if self.file_path:
            self.folder_path = None  # Reset folder path if a file is selected
            self.label.config(text=f"Selected file: {self.file_path}")
            file_extension = os.path.splitext(self.file_path)[1].lower()
            if file_extension in [".jpg", ".jpeg", ".png"]:
                self.update_container_dropdown(self.models["image"])
            elif file_extension in [".mp4", ".avi"]:
                self.update_container_dropdown(self.models["video"])
            else:
                messagebox.showerror("Error", "Unsupported file type")
    
    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.file_path = None  # Reset file path if a folder is selected
            self.label.config(text=f"Selected folder: {self.folder_path}")
            self.update_container_dropdown(self.models["folder"])

    def get_files_from_folder(self, folder_path):
        file_paths = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths
    
    def upload_input(self):
        if not self.file_path and not self.folder_path:
            messagebox.showerror("Error", "No file or folder selected")
            return
        
        container_name = self.container_var.get()
        try:
            if self.file_path:
                with open(self.file_path, 'rb') as file:
                    files = {'file': file}
                    data = {'container': container_name}
                    response = requests.post("http://localhost:5000/api/upload", files=files, data=data)
            elif self.folder_path:
                files = [('file', (os.path.basename(f), open(f, 'rb'))) for f in self.get_files_from_folder(self.folder_path)]
                data = {'container': container_name}
                response = requests.post("http://localhost:5000/api/upload_folder", files=files, data=data)
            
            if response.status_code == 200:
                self.show_result_callback(response.json())
            else:
                messagebox.showerror("Error", f"Failed to upload item: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # def upload_image(self): 
    #     if not self.file_path:
    #         messagebox.showerror("Error", "No file selected")
    #         return
        
    #     container_name = self.container_var.get()
    #     try:
    #         with open(self.file_path, 'rb') as image_file:
    #             files = {'input': image_file}
    #             data = {'container': container_name}
    #             response = requests.post("http://localhost:5000/api/upload", files=files, data=data)
    #             if response.status_code == 200:
    #                 self.show_result_callback(response.json())
    #             else:
    #                 messagebox.showerror("Error", f"Failed to upload image: {response.json()}")
    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))

    
    # def upload_and_start_model(self):
    #     if not self.file_path:
    #         messagebox.showerror("Error", "No file selected")
    #         return
        
    #     container_name = self.container_var.get()
    #     try:
    #         with open(self.file_path, 'rb') as image_file:
    #             files = {'image': image_file}
    #             data = {'container': container_name}
    #             response = requests.post("http://localhost:5000/api/upload", files=files, data=data)
    #             if response.status_code == 200:
    #                 self.show_result_callback(response.json())
    #                 self.start_container(container_name)
    #             else:
    #                 messagebox.showerror("Error", f"Failed to upload image: {response.json()}")
    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))

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
