try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import ttk
import time
import threading
from tkinter.ttk import Button
class ProgressbarWindow(tk.Tk):
    def __init__(self, parent):
        self.parent = parent
        self.parent.wm_attributes("-disabled", True)

        self.progressbarWindow = tk.Toplevel(self.parent)
        self.progressbarWindow.title("ローディング中...")
        self.progressbarWindow.resizable(0,0)
        self.progressbarWindow.protocol("WM_DELETE_WINDOW", self.disable_close_event)
        width_of_window = 400
        height_of_window = 120
        screen_width = self.progressbarWindow.winfo_screenwidth()
        screen_height = self.progressbarWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.progressbarWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.progressbarWindow.columnconfigure(0, weight=1)
        self.progressbarWindow.columnconfigure(1, weight=1)
        self.progressbarWindow.columnconfigure(2, weight=1)
        self.progressbarWindow.rowconfigure(0, weight=3)
        self.progressbarWindow.rowconfigure(1, weight=2)

        self.progressBar()
    def progressBar(self):
        self.progress_bar = ttk.Progressbar(self.progressbarWindow, orient = 'horizontal', length = 286, mode='indeterminate')
        self.progress_bar.grid(row = 0, column = 0, columnspan=3, sticky="")

        # self.btn_stop = Button(self.progressbarWindow, text = "Stop", command = lambda: self.stop_progressbar())
        # self.btn_stop.grid(row=1, column=0, columnspan=3, ipady=3, pady=(0, 0))
        self.start_progressbar()
    def start_progressbar(self):
        def real_traitement():
            self.progress_bar.start()
        threading.Thread(target=real_traitement).start()
    def stop_progressbar(self):
        self.close_window()
        # self.progress_bar.grid_forget()
    def close_window(self):
        self.parent.wm_attributes("-disabled", False)
        self.progress_bar.stop()
        self.progressbarWindow.destroy()        
    def disable_close_event(self):
        pass