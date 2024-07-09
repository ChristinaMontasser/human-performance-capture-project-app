import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import requests
import os

class UploadFrame(tk.Frame):
    def __init__(self, parent, show_result_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.show_result_callback = show_result_callback

        # Frames
        self.label_frame = tk.Frame(self)
        self.button_frame = tk.Frame(self, width=300, height=500)

        #Layout Configuration
        self.label_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=20)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.NONE, padx=(10, 20), pady=20)
        self.button_frame.pack_propagate(False)

        # Elements in label frame
        self.label = tk.Label(self.label_frame, text="Choose an image...")
        self.label.pack(pady=10)
        
        self.output_label = tk.Label(self.label_frame, text="Choose output path...")
        self.output_label.pack(pady=10)
        
        self.container_label = tk.Label(self.label_frame, text="Select Model:")
        self.container_label.pack(pady=(50,0))

        self.model_desc_label = tk.Label(self.label_frame, text="Selected Model Description:")
        self.model_desc_label.pack(pady=(80,0))

        # Elements in button frame
        self.upload_button = tk.Button(self.button_frame, text="Browse", command=self.browse_file)
        self.upload_button.pack(pady=10)

        self.output_button = tk.Button(self.button_frame, text="Save To", command=self.browse_output_folder)
        self.output_button.pack(pady=(10,0))

        self.output_label_path = tk.Label(self.button_frame, text="", width=300, height=3, wraplength=280)
        self.output_label_path.pack()
        
        self.container_var = tk.StringVar(self, "Loading containers...")
        self.container_dropdown = OptionMenu(self.button_frame, self.container_var, "Loading containers...")
        self.container_dropdown.pack()

        self.model_info_label = tk.Label(self.button_frame, text="", width=100, height=2)
        self.model_info_label.pack(pady=(60,0))

        self.start_button = tk.Button(self.button_frame, text="Start Model", command=self.start_container)
        self.start_button.pack(pady=(30,10))
        
        self.submit_button = tk.Button(self.button_frame, text="Upload", command=self.upload_input)
        self.submit_button.pack(pady=10)
        
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
            #print(self.models["folder"])
            #return self.folder_path

    def get_files_from_folder(self, folder_path):
        file_paths = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths
    
    def browse_output_folder(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            self.output_label_path.config(text=f"Selected output path: {self.output_path}")
            
    def upload_input(self):
        print('uploadinput')
        if not self.file_path and not self.folder_path:
            messagebox.showerror("Error", "No file or folder selected")
            return
        container_name = self.container_var.get()
        try:
            with open(self.file_path, 'rb') as image_file:
                print(self.output_path)
                files = {'image': image_file}
                data = {'model': container_name, 'save_to_folder': self.output_path}  # Use 'model' to match the backend expectation
                response = requests.post("http://127.0.0.1:5000/upload", files=files, data=data)
                print(data['model'])
                if response.status_code == 200:
                    self.show_result_callback(response.json())
                else:
                    messagebox.showerror("Error", f"Failed to upload image: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    #!!Just upload the data and then the backend will start the container based on the container name 
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