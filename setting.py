try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import pickle

# def openSettingWindow(parent):
class SettingWindow:
    count = 0
    def __init__(self, parent):
        SettingWindow.count = SettingWindow.count + 1

        self.settingWindow = tk.Toplevel(parent)
        self.settingWindow.title("設定")
        self.settingWindow.protocol("WM_DELETE_WINDOW", self.close_window)

        width_of_window = 400
        height_of_window = 250
        screen_width = self.settingWindow.winfo_screenwidth()
        screen_height = self.settingWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.settingWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.settingWindow.columnconfigure(0, weight=1)
        self.settingWindow.columnconfigure(1, weight=1)
        self.settingWindow.columnconfigure(2, weight=1)
        self.settingWindow.rowconfigure(0, weight=1)
        self.settingWindow.rowconfigure(1, weight=1)
        self.settingWindow.rowconfigure(2, weight=1)
        self.settingWindow.rowconfigure(3, weight=1)
        self.settingWindow.rowconfigure(4, weight=1)
        self.settingWindow.rowconfigure(5, weight=3)
        
        readFile = open('data/data_01', 'rb')
        self.registered_setting_values = pickle.load(readFile)
        readFile.close()
        print("original_data => ", self.registered_setting_values)

        self._create_windowview()
    def _create_windowview(self):
        label = tk.Label(self.settingWindow, text="メインキーワード取得件数")
        label.grid(row=0, column=0, padx=(15, 0), pady=(5, 0),  sticky="w")
        label = tk.Label(self.settingWindow, text="サジェストキーワード取得件数")
        label.grid(row=1, column=0, padx=(15, 0), pady=(5, 0), sticky="w")
        label = tk.Label(self.settingWindow, text="サジェストキーワード2取得件数")
        label.grid(row=2, column=0, padx=(15, 0), pady=(5, 0), sticky="w")
        label = tk.Label(self.settingWindow, text="５０音+アルファベットキーワード取得件数")
        label.grid(row=3, column=0, padx=(15, 0), pady=(5, 0), sticky="w")
        label = tk.Label(self.settingWindow, text="デフォルト動画取得件数")
        label.grid(row=4, column=0, padx=(15, 0), pady=(5, 0), sticky="w")

        spin_var = tk.StringVar()
        spin_var.set(self.registered_setting_values[0][1])
        self.spin_main_suggest_keyword_cnt = tk.Spinbox(self.settingWindow, from_=0, to=100, width=5, textvariable=spin_var)
        self.spin_main_suggest_keyword_cnt.grid(row=0, column=1, pady=(5, 0), sticky="w")

        spin_var = tk.StringVar()
        spin_var.set(self.registered_setting_values[1][1])
        self.spin_suggest_keyword_cnt_1 = tk.Spinbox(self.settingWindow, from_=0, to=100, width=5, textvariable=spin_var)
        self.spin_suggest_keyword_cnt_1.grid(row=1, column=1, pady=(5, 0), sticky="w")

        spin_var = tk.StringVar()
        spin_var.set(self.registered_setting_values[2][1])
        self.spin_suggest_keyword_cnt_2 = tk.Spinbox(self.settingWindow, from_=0, to=100, width=5, textvariable=spin_var)
        self.spin_suggest_keyword_cnt_2.grid(row=2, column=1, pady=(5, 0), sticky="w")

        spin_var = tk.StringVar()
        spin_var.set(self.registered_setting_values[3][1])
        self.spin_alphabet_keyword_cnt = tk.Spinbox(self.settingWindow, from_=0, to=100, width=5, textvariable=spin_var)
        self.spin_alphabet_keyword_cnt.grid(row=3, column=1, pady=(5, 0), sticky="w")

        spin_var = tk.StringVar()
        spin_var.set(self.registered_setting_values[4][1])
        self.spin_video_acquire_cnt = tk.Spinbox(self.settingWindow, from_=0, to=100, width=5, textvariable=spin_var)
        self.spin_video_acquire_cnt.grid(row=4, column=1, pady=(5, 0), sticky="w")
        
        settingBtnFrame = tk.Frame(self.settingWindow)
        settingBtnFrame.grid(row=0, column=2, rowspan=3, sticky='ens', columnspan=5)        

        btn_execute_setting = tk.ttk.Button(settingBtnFrame, text="設定", command=self.save_setting_info)
        btn_execute_setting.grid(sticky='wens', row=0, column=0, padx=5, ipady=3, pady=(15, 10))
        
        btn_execute_cancel = tk.ttk.Button(settingBtnFrame, text="キャンセル", command=self.close_window)
        btn_execute_cancel.grid(sticky='wens', row=1, column=0, padx=5, ipady=3, ipadx=5)
    def save_setting_info(self):
        setting_values = [['main_suggest_keyword_cnt', self.spin_main_suggest_keyword_cnt.get()], ['suggest_keyword_cnt_1', self.spin_suggest_keyword_cnt_1.get()], ['suggest_keyword_cnt_2', self.spin_suggest_keyword_cnt_2.get()], ['alphabet_keyword_cnt', self.spin_alphabet_keyword_cnt.get()], ['video_acquire_cnt', self.spin_video_acquire_cnt.get()]]
        writeFile = open('data/data_01', 'wb')
        pickle.dump(setting_values, writeFile)
        writeFile.close()
        self.close_window()
    def close_window(self):
        SettingWindow.count = SettingWindow.count - 1
        self.settingWindow.destroy()