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
