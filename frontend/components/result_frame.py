import tkinter as tk

class ResultFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.result_label = tk.Label(self, text="Results will be shown here")
        self.result_label.pack()

    def show_result(self, result):
        self.result_label.config(text=f"Model Output: {result}")
