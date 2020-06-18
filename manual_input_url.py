try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import END
from tkinter.ttk import Button

class ManualInputUrlWindow:
    count = 0
    def __init__(self, parent, own_url_list_table):
        ManualInputUrlWindow.count = ManualInputUrlWindow.count + 1

        self.manualInputUrlWindow = tk.Toplevel(parent)
        self.manualInputUrlWindow.title("URL任意追加")
        self.manualInputUrlWindow.protocol("WM_DELETE_WINDOW", self.close_window)

        width_of_window = 500
        height_of_window = 350
        screen_width = self.manualInputUrlWindow.winfo_screenwidth()
        screen_height = self.manualInputUrlWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.manualInputUrlWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.manualInputUrlWindow.columnconfigure(0, weight=1)
        self.manualInputUrlWindow.columnconfigure(1, weight=1)
        self.manualInputUrlWindow.rowconfigure(0, weight=1)
        
        self.text_multi_url = tk.Text(self.manualInputUrlWindow, width=50, height=24)
        self.text_multi_url.grid(row=0, column=0, rowspan=3, sticky='wnse')

        btnMultiUrlFrame = tk.Frame(self.manualInputUrlWindow)
        btnMultiUrlFrame.grid(row=0, column=1, sticky='wn')
        
        btn_add_multi_url = Button(btnMultiUrlFrame, text = "追加", command = lambda: self.add_multi_url(own_url_list_table))
        btn_add_multi_url.grid(row=0, column=0, sticky='wn', padx=(10, 0), pady=(10,10))
        btn_cancel_multi_url = Button(btnMultiUrlFrame, text = "キャンセル", command = self.close_window)
        btn_cancel_multi_url.grid(row=1, column=0, sticky='wn', padx=(10, 0))
    def add_multi_url(self, own_url_list_table):
        line_count = int(self.text_multi_url.index('end-1c').split('.')[0])
        print("line_count", line_count)
        text = self.text_multi_url.get('1.0', END).splitlines()
        if len(text) > 0 and text[0] != "":
            for line in text:
                print(line)
                url = line.split("https://www.youtube.com/watch?v=")[1]
                print(url)
                ckValue = tk.BooleanVar()
                ckValue.set(True)
                own_url_list_table.dataVars.append([ckValue, url, ""])
            own_url_list_table._load_data(own_url_list_table.dataVars)
            self.close_window()
        else:
            print("no data")
    def close_window(self):
        ManualInputUrlWindow.count = ManualInputUrlWindow.count - 1
        self.manualInputUrlWindow.destroy()