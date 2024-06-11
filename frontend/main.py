import tkinter as tk
from components.upload_frame import UploadFrame
from components.result_frame import ResultFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D Body Parameter Estimation")
        self.geometry("800x600")
        
        # Initialize frames
        self.upload_frame = UploadFrame(self)
        self.result_frame = ResultFrame(self)
        
        self.upload_frame.pack(fill="both", expand=True)

    def show_result_frame(self, result):
        self.upload_frame.pack_forget()
        self.result_frame.pack(fill="both", expand=True)
        self.result_frame.show_result(result)

if __name__ == "__main__":
    app = App()
    app.mainloop()
