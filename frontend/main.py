import tkinter as tk
from components.upload_frame import UploadFrame
from components.result_frame import ResultFrame

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Parameter Estimation")
        self.geometry("600x400")
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.upload_frame = UploadFrame(self.container, self.show_result)
        self.upload_frame.grid(row=0, column=0, sticky="nsew")
        
        self.result_frame = ResultFrame(self.container)
        self.result_frame.grid(row=0, column=0, sticky="nsew")

        ##!! Model Description 
        self.show_frame(self.upload_frame)
    
    def show_frame(self, frame):
        frame.tkraise()
    #!! Will be changed to show images or video 
    def show_result(self, result):
        self.result_frame.display_results(result)
        self.show_frame(self.result_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
