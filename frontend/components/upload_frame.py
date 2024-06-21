import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import requests

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
        self.container_dropdown = OptionMenu(self, self.container_var, "Loading containers...")
        self.container_dropdown.pack(pady=10)

        self.start_button = tk.Button(self, text="Start Model", command=self.start_container)
        self.start_button.pack(pady=10)
        
        self.submit_button = tk.Button(self, text="Upload", command=self.upload_image)
        self.submit_button.pack(pady=20)
        
        self.file_path = None

        # Populate models on initialization
        self.populate_models()

    def populate_models(self):
        model_names = ["Pare", "ExPose", "4DHumans"]
        self.update_container_dropdown(model_names)

    def update_container_dropdown(self, container_names):
        self.container_dropdown['menu'].delete(0, 'end')
        for name in container_names:
            self.container_dropdown['menu'].add_command(label=name, command=tk._setit(self.container_var, name))
        
        if container_names:
            self.container_var.set(container_names[0])
        else:
            self.container_var.set("No containers found")

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if self.file_path:
            self.label.config(text=f"Selected file: {self.file_path}")
        
    def upload_image(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return
        
        container_name = self.container_var.get()
        try:
            with open(self.file_path, 'rb') as image_file:
                files = {'image': image_file}
                data = {'container': container_name}
                response = requests.post("http://localhost:5000/api/upload", files=files, data=data)
                
                if response.status_code == 200:
                    self.show_result_callback(response.json())
                else:
                    messagebox.showerror("Error", f"Failed to upload image: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
