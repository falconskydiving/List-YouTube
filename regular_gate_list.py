try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import END
from tkinter.ttk import Button
import pickle

# from edit_playlist_name import EditPlaylistNameWindow

class RegularGateListWindow:
    count = 0
    def __init__(self, edit_playlist_name, parent, playlist_table):
        RegularGateListWindow.count = RegularGateListWindow.count + 1
        
        self.updateRegularGatesWindow = tk.Toplevel(parent)
        self.updateRegularGatesWindow.title("定型文メンテナンス")
        self.updateRegularGatesWindow.protocol("WM_DELETE_WINDOW", self.close_window)
        width_of_window = 500
        height_of_window = 350
        screen_width = self.updateRegularGatesWindow.winfo_screenwidth()
        screen_height = self.updateRegularGatesWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.updateRegularGatesWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.updateRegularGatesWindow.columnconfigure(0, weight=1)
        self.updateRegularGatesWindow.columnconfigure(1, weight=1)
        self.updateRegularGatesWindow.rowconfigure(0, weight=1)
        
        self.text_regular_gates = tk.Text(self.updateRegularGatesWindow, width=50, height=24)
        self.text_regular_gates.grid(row=0, column=0, rowspan=3, sticky='wnse')
        
        readFile = open('data/data_05', 'rb')
        rg_values = pickle.load(readFile)
        readFile.close()

        for rg in rg_values:
            print(rg)
            self.text_regular_gates.insert(END, rg + '\n')

        btnRegularGateFrame = tk.Frame(self.updateRegularGatesWindow)
        btnRegularGateFrame.grid(row=0, column=1, sticky='wn')
        
        btn_add_regular_gates = Button(btnRegularGateFrame, text = "OK", command = lambda: self.save_regular_gates(edit_playlist_name, playlist_table))
        btn_add_regular_gates.grid(row=0, column=0, sticky='wn', padx=(10, 0), pady=(10,10))
        btn_cancel_regular_gates = Button(btnRegularGateFrame, text = "キャンセル", command = self.close_window)
        btn_cancel_regular_gates.grid(row=1, column=0, sticky='wn', padx=(10, 0))

        btn_load_regular_gates = Button(btnRegularGateFrame, text = "Default", command = lambda: self.load_regular_gates())
        btn_load_regular_gates.grid(row=2, column=0, sticky='wn', padx=(10, 0), pady=(30,10))
    def save_regular_gates(self, edit_playlist_name, playlist_table):
        line_count = int(self.text_regular_gates.index('end-1c').split('.')[0])
        print("regular_gate_count", line_count)

        text = self.text_regular_gates.get('1.0', END).splitlines()
        regular_gate_values = []
        for line in text:
            print(line)
            regular_gate_values.append(line)

        writeFile = open('data/data_05', 'wb')
        pickle.dump(regular_gate_values, writeFile)
        writeFile.close()

        if edit_playlist_name.count > 0:
            self.refresh_cb_regular_gate(edit_playlist_name)
        playlist_table._load_data(playlist_table.dataVars)

        self.close_window()
    def refresh_cb_regular_gate(self, edit_playlist_name):
        readFile = open('data/data_05', 'rb')
        edit_playlist_name.cb_regular_gate['values'] = pickle.load(readFile)
        edit_playlist_name.cb_regular_gate.current(0)
        readFile.close()
    def load_regular_gates(self):
        rg_values = ["まとめ", "", "再生リスト", "一覧", "プレイリスト", "お気に入り"]
        self.text_regular_gates.delete('1.0', END)
        for i in range(len(rg_values)):
            if i < len(rg_values) - 1:
                self.text_regular_gates.insert(END, rg_values[i] + '\n')
            else:
                self.text_regular_gates.insert(END, rg_values[i])
    def close_window(self):
        RegularGateListWindow.count = RegularGateListWindow.count - 1
        self.updateRegularGatesWindow.destroy()