import tkinter as tk

class ResultFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.label = tk.Label(self, text="Model Output Results")
        self.label.pack(pady=10)
        
        self.result_text = tk.Text(self, wrap="word", height=10, width=50)
        self.result_text.pack(pady=10)

    def display_results(self, result):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result)
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Model Output Results")
    ResultFrame(root).pack(fill="both", expand=True)
    root.mainloop()




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
