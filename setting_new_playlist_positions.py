try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import END
from tkinter.ttk import Button
import pickle
import threading
from pynput.mouse import Controller as MController
from pynput.keyboard import Listener as KListener, Key

class SettingNewPlaylistPositionsWindow:
    count = 0
    def __init__(self, parent):
        SettingNewPlaylistPositionsWindow.count = SettingNewPlaylistPositionsWindow.count + 1
        self.settingNPPWindow = tk.Toplevel(parent)
        self.settingNPPWindow.title("プレイリストの座標設定")
        self.settingNPPWindow.protocol("WM_DELETE_WINDOW", self.close_window)

        width_of_window = 600
        height_of_window = 200
        screen_width = self.settingNPPWindow.winfo_screenwidth()
        screen_height = self.settingNPPWindow.winfo_screenheight()
        x_coordinate = (screen_width*3/4) - (width_of_window/2)
        y_coordinate = (screen_height*3/4) - (height_of_window/2)

        self.settingNPPWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        self.settingNPPWindow.wm_attributes("-topmost", 1)
        
        self.settingNPPWindow.columnconfigure(0, weight=3)
        self.settingNPPWindow.columnconfigure(1, weight=1)
        self.settingNPPWindow.columnconfigure(2, weight=3)
        self.settingNPPWindow.columnconfigure(3, weight=1)
        self.settingNPPWindow.columnconfigure(4, weight=3)
        self.settingNPPWindow.columnconfigure(5, weight=3)
        self.settingNPPWindow.rowconfigure(0, weight=1)
        self.settingNPPWindow.rowconfigure(1, weight=1)
        self.settingNPPWindow.rowconfigure(2, weight=1)
        self.settingNPPWindow.rowconfigure(3, weight=1)
        self.settingNPPWindow.rowconfigure(4, weight=1)
        self.settingNPPWindow.rowconfigure(5, weight=1)
        
        self.rbPositionIndex = tk.IntVar()
        self.rbPositionIndex.set(1)

        readFile = open('data/data_03', 'rb')
        self.npp_values = pickle.load(readFile)
        readFile.close()
    def _create_windowview(self):
        #location bar
        rb_location_bar = tk.Radiobutton(self.settingNPPWindow, text="アドレスバー（URL）", value=1, variable=self.rbPositionIndex)
        rb_location_bar.grid(row=0, column=0, padx=5, sticky="w")

        lab_location_bar_x = tk.Label(self.settingNPPWindow, text="x:")
        lab_location_bar_x.grid(row=0, column=1, padx=5, sticky="e")
        
        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[0][0])
        self.spin_location_bar_x = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_location_bar_x.grid(row=0, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_location_bar_y = tk.Label(self.settingNPPWindow, text="y:")
        lab_location_bar_y.grid(row=0, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[0][1])
        self.spin_location_bar_y = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_location_bar_y.grid(row=0, column=4, sticky="w", padx=5, pady=(5, 0))

        #new playlist
        rb_new_playlist = tk.Radiobutton(self.settingNPPWindow, text="「新しい再生リスト」ボタン", value=2, variable=self.rbPositionIndex)
        rb_new_playlist.grid(row=1, column=0, padx=5, sticky="w")

        lab_new_playlist_x = tk.Label(self.settingNPPWindow, text="x:")
        lab_new_playlist_x.grid(row=1, column=1, padx=5, sticky="e")


        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[1][0])
        self.spin_new_playlist_x = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_new_playlist_x.grid(row=1, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_new_playlist_y = tk.Label(self.settingNPPWindow, text="y:")
        lab_new_playlist_y.grid(row=1, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[1][1])
        self.spin_new_playlist_y = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_new_playlist_y.grid(row=1, column=4, sticky="w", padx=5, pady=(5, 0))

        #playlist_title
        rb_playlist_title = tk.Radiobutton(self.settingNPPWindow, text="「再生リストのタイトル」入力窓", value=3, variable=self.rbPositionIndex)
        rb_playlist_title.grid(row=2, column=0, padx=5, sticky="w")

        lab_playlist_title_x = tk.Label(self.settingNPPWindow, text="x:")
        lab_playlist_title_x.grid(row=2, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[2][0])
        self.spin_playlist_title_x = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_playlist_title_x.grid(row=2, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_playlist_title_y = tk.Label(self.settingNPPWindow, text="y:")
        lab_playlist_title_y.grid(row=2, column=3, padx=5, sticky="e")


        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[2][1])
        self.spin_playlist_title_y = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_playlist_title_y.grid(row=2, column=4, sticky="w", padx=5, pady=(5, 0))

        #create btn
        rb_create_btn = tk.Radiobutton(self.settingNPPWindow, text="「作成」ボタン", value=4, variable=self.rbPositionIndex)
        rb_create_btn.grid(row=3, column=0, padx=5, sticky="w")

        lab_create_btn_x = tk.Label(self.settingNPPWindow, text="x:")
        lab_create_btn_x.grid(row=3, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[3][0])
        self.spin_create_btn_x = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_create_btn_x.grid(row=3, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_create_btn_y = tk.Label(self.settingNPPWindow, text="y:")
        lab_create_btn_y.grid(row=3, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.npp_values[3][1])
        self.spin_create_btn_y = tk.Spinbox(self.settingNPPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_create_btn_y.grid(row=3, column=4, sticky="w", padx=5, pady=(5, 0))

        settingBtnFrame = tk.Frame(self.settingNPPWindow)
        settingBtnFrame.grid(row=0, column=5, rowspan=3, sticky='wens')

        btn_execute_setting = Button(settingBtnFrame, text="設定", command=self.register_setting_info)
        btn_execute_setting.grid(sticky='wens', row=0, column=0, padx=5, ipady=3, pady=(10, 10))

        btn_execute_cancel = Button(settingBtnFrame, text="キャンセル", command=self.close_window)
        btn_execute_cancel.grid(sticky='wens', row=1, column=0, padx=5, ipady=3, ipadx=20)

        threading.Thread(target=self.get_position).start()

    def log_mouse_position(self, key):
        key = str(key)
        if key == 'Key.ctrl_l':
            print("inIfCondition")
            currentMouse = MController()
            print(currentMouse.position)
            
            print("rbPositionValue:", self.rbPositionIndex.get())
            if self.rbPositionIndex.get() == 1:
                self.spin_location_bar_x.delete(0, END)
                self.spin_location_bar_x.insert(0, currentMouse.position[0])
                self.spin_location_bar_y.delete(0, END)
                self.spin_location_bar_y.insert(0, currentMouse.position[1])
            elif self.rbPositionIndex.get() == 2:
                self.spin_new_playlist_x.delete(0, END)
                self.spin_new_playlist_x.insert(0, currentMouse.position[0])
                self.spin_new_playlist_y.delete(0, END)
                self.spin_new_playlist_y.insert(0, currentMouse.position[1])
            elif self.rbPositionIndex.get() == 3:
                self.spin_playlist_title_x.delete(0, END)
                self.spin_playlist_title_x.insert(0, currentMouse.position[0])
                self.spin_playlist_title_y.delete(0, END)
                self.spin_playlist_title_y.insert(0, currentMouse.position[1])
            elif self.rbPositionIndex.get() == 4:
                self.spin_create_btn_x.delete(0, END)
                self.spin_create_btn_x.insert(0, currentMouse.position[0])
                self.spin_create_btn_y.delete(0, END)
                self.spin_create_btn_y.insert(0, currentMouse.position[1])
    def get_position(self):
        with KListener(on_press=self.log_mouse_position) as kl:
            kl.join()        
    def register_setting_info(self):
        setting_values = [[self.spin_location_bar_x.get(), self.spin_location_bar_y.get()], [self.spin_new_playlist_x.get(), self.spin_new_playlist_y.get()], [self.spin_playlist_title_x.get(), self.spin_playlist_title_y.get()], [self.spin_create_btn_x.get(), self.spin_create_btn_y.get()]]
        writeFile = open('data/data_03', 'wb')
        pickle.dump(setting_values, writeFile)
        writeFile.close()
        self.close_window()
    def close_window(self):
        SettingNewPlaylistPositionsWindow.count = SettingNewPlaylistPositionsWindow.count - 1
        self.settingNPPWindow.destroy()