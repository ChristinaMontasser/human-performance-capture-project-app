# import tkinter as tk
# import webbrowser

# class ResultFrame(tk.Frame):
#     def __init__(self, parent, output_path, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
        
#         self.label = tk.Label(self, text="Model Output Results")
#         self.label.pack(pady=10)
        
#         self.result_text = tk.Text(self, wrap="word", height=10, width=50)
#         self.result_text.pack(pady=10)

#         # Folder path where the results are saved
#         self.folder_path = output_path
        
#         # Add a label for completion message with a hyperlink
#         self.link_label = tk.Label(self, text="Process has successfully completed, please check this folder", fg="blue", cursor="hand2")
#         self.link_label.pack(pady=10)
        
#         # Bind the hyperlink click event
#         self.link_label.bind("<Button-1>", self.open_folder)

#     def display_results(self, result):
#         self.result_text.config(state="normal")
#         self.result_text.delete("1.0", "end")
#         self.result_text.insert("Process has successfully completed, please check this folder", result)
#         self.result_text.config(state="disabled")

#     def open_folder(self, event):
#         # Open the folder in the file explorer
#         webbrowser.open(f"file://{self.folder_path}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Model Output Results")
#     ResultFrame(root).pack(fill="both", expand=True)
#     root.mainloop()




# import tkinter as tk
# from PIL import Image, ImageTk
# import numpy as np
# import os

# class ResultFrame(tk.Frame):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
        
#         self.label = tk.Label(self, text="Model Output Results")
#         self.label.pack(pady=10)
        
#         self.result_text = tk.Text(self, wrap="word", height=10, width=50)
#         self.result_text.pack(pady=10)
        
#         self.image_label = tk.Label(self)
#         self.image_label.pack(pady=10)

#     def display_results(self, result):
#         self.result_text.config(state="normal")
#         self.result_text.delete("1.0", "end")
#         self.result_text.insert("1.0", result)
#         self.result_text.config(state="disabled")
        
#     def display_image(self, image_path):
#         image = Image.open(image_path)
#         image = ImageTk.PhotoImage(image)
#         self.image_label.config(image=image)
#         self.image_label.image = image

#     def display_npz(self, npz_path):
#         data = np.load(npz_path)
#         result = "NPZ File Content:\n"
#         for key, value in data.items():
#             result += f"{key}: {value}\n"
#         self.display_results(result)

#     def load_and_display_files(self, folder_path):
#         # Find npz file and image in the given folder
#         for file_name in os.listdir(folder_path):
#             if file_name.endswith('.npz'):
#                 npz_path = os.path.join(folder_path, file_name)
#                 self.display_npz(npz_path)
#             elif file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
#                 image_path = os.path.join(folder_path, file_name)
#                 self.display_image(image_path)

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Model Output Results")
    
#     result_frame = ResultFrame(root)
#     result_frame.pack(fill="both", expand=True)
    
#     # Specify the folder where the model outputs are saved
#     output_folder = "path_to_output_folder"  # replace with your output folder path
    
#     # Load and display files from the output folder
#     result_frame.load_and_display_files(output_folder)
    
#     root.mainloop()


import tkinter as tk
import os

class ResultFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        

        self.label = tk.Label(self, text="Model Output Results")
        self.label.pack(pady=10)
        
        self.result_text = tk.Text(self, wrap="word", height=10, width=50)
        self.result_text.pack(pady=10)

        self.open_folder_button = tk.Button(self, text="Open Results Folder", command=self.open_folder)
        self.open_folder_button.pack(pady=10)

    def display_results(self, result, folder_path):
        self.folder_path = folder_path

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
#        self.result_text.insert("1.0", result)
        self.result_text.insert("end", "\n\nProcess has successfully completed. Please check the folder.")
        self.result_text.config(state="disabled")

    def open_folder(self):
        # Open the folder in the file explorer
        if os.path.isdir(self.folder_path):
            os.startfile(self.folder_path)  # This works on Windows

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Model Output Results")