try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter.ttk import Button, Entry
import pickle

class SaveOwnUrlListWindow:
    count = 0
    def __init__(self, parent, own_url_list_table, combo_own_url):
        SaveOwnUrlListWindow.count = SaveOwnUrlListWindow.count + 1
        self.saveOwnUrlListWindow =  tk.Toplevel(parent)
        self.saveOwnUrlListWindow.title("任意URL")
        self.saveOwnUrlListWindow.protocol("WM_DELETE_WINDOW", self.close_window)

        width_of_window = 500
        height_of_window = 150
        screen_width = self.saveOwnUrlListWindow.winfo_screenwidth()
        screen_height = self.saveOwnUrlListWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.saveOwnUrlListWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        # self.saveOwnUrlListWindow.wm_attributes("-topmost", 1)
        self.saveOwnUrlListWindow.columnconfigure(0, weight=4)
        self.saveOwnUrlListWindow.columnconfigure(1, weight=1)
        self.saveOwnUrlListWindow.rowconfigure(0, weight=1)
        self.saveOwnUrlListWindow.rowconfigure(1, weight=1)
        self.saveOwnUrlListWindow.rowconfigure(2, weight=1)
        self.saveOwnUrlListWindow.rowconfigure(3, weight=1)

        label =  tk.Label(self.saveOwnUrlListWindow, text="Please input name!")
        label.grid(row=0, column=0, sticky="w", padx=10)

        self.entry_save_ul_name = Entry(self.saveOwnUrlListWindow)
        self.entry_save_ul_name.grid( row=3, column=0, columnspan=2, sticky="we", padx=(10, 10), pady=(5, 0), ipady=3)

        settingBtnFrame = tk.Frame(self.saveOwnUrlListWindow)
        settingBtnFrame.grid(row=0, column=1, rowspan=3, sticky='ens', padx=10)        

        btn_ok = Button(settingBtnFrame, text="OK", command=lambda: self.save_own_url_list(own_url_list_table, combo_own_url))
        btn_ok.grid(sticky='wens', row=0, column=0, ipady=0, pady=(10, 10))
        
        btn_cancel = Button(settingBtnFrame, text="キャンセル", command=self.close_window)
        btn_cancel.grid(sticky='wens', row=1, column=0, ipady=0, ipadx=0)
    def save_own_url_list(self, own_url_list_table, combo_own_url):
        readFile = open('data/data_02', 'rb')
        values = pickle.load(readFile)
        readFile.close()

        name = self.entry_save_ul_name.get()
        new_value = [name, []]

        for row in own_url_list_table.dataVars:
            new_value[1].append([row[1], row[2]])        
        values.append(new_value)
        
        writeFile = open('data/data_02', 'wb')
        pickle.dump(values, writeFile)
        writeFile.close()
        cb_values = []
        for row in values:
            cb_values.append(row[0])
        combo_own_url['values'] = cb_values
        combo_own_url.current(len(cb_values) - 1)
        self.close_window()
    def close_window(self):
        SaveOwnUrlListWindow.count = SaveOwnUrlListWindow.count - 1
        self.saveOwnUrlListWindow.destroy()