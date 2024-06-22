import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import requests

class ModeLDescriptionFrame(tk.Frame):
    def __init__(self, parent, show_result_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


   