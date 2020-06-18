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

class SettingNewVideoPositionsWindow:
    count = 0
    def __init__(self, parent):
        SettingNewVideoPositionsWindow.count = SettingNewVideoPositionsWindow.count + 1

        self.settingNVPWindow = tk.Toplevel(parent)
        self.settingNVPWindow.title("動画の座標設定")
        self.settingNVPWindow.protocol("WM_DELETE_WINDOW", self.close_window)
        
        width_of_window = 600
        height_of_window = 300
        screen_width = self.settingNVPWindow.winfo_screenwidth()
        screen_height = self.settingNVPWindow.winfo_screenheight()
        x_coordinate = (screen_width*3/4) - (width_of_window/2)
        y_coordinate = (screen_height*3/4) - (height_of_window/2)

        self.settingNVPWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        self.settingNVPWindow.wm_attributes("-topmost", 1)

        self.settingNVPWindow.columnconfigure(0, weight=3)
        self.settingNVPWindow.columnconfigure(1, weight=1)
        self.settingNVPWindow.columnconfigure(2, weight=3)
        self.settingNVPWindow.columnconfigure(3, weight=1)
        self.settingNVPWindow.columnconfigure(4, weight=3)
        self.settingNVPWindow.columnconfigure(5, weight=3)
        self.settingNVPWindow.rowconfigure(0, weight=1)
        self.settingNVPWindow.rowconfigure(1, weight=1)
        self.settingNVPWindow.rowconfigure(2, weight=1)
        self.settingNVPWindow.rowconfigure(3, weight=1)
        self.settingNVPWindow.rowconfigure(4, weight=1)
        self.settingNVPWindow.rowconfigure(5, weight=1)
        self.settingNVPWindow.rowconfigure(6, weight=1)
        self.settingNVPWindow.rowconfigure(7, weight=1)
        self.settingNVPWindow.rowconfigure(8, weight=1)

        readFile = open('data/data_04', 'rb')
        self.nvp_values = pickle.load(readFile)
        readFile.close()
        print("original_data => ", self.nvp_values)

        self.rbVPositionIndex = tk.IntVar()
        self.rbVPositionIndex.set(1)

    def _create_windowview(self):
        #title edit btn
        rb_title_eidt_btn = tk.Radiobutton(self.settingNVPWindow, text="「タイトルを編集」ボタン", value=1, variable=self.rbVPositionIndex)
        rb_title_eidt_btn.grid(row=0, column=0, padx=5, sticky="w")

        lab_title_edit_btn_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_title_edit_btn_x.grid(row=0, column=1, padx=5, sticky="e")
        
        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[0][0])
        self.spin_title_edit_btn_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_title_edit_btn_x.grid(row=0, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_title_edit_btn_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_title_edit_btn_y.grid(row=0, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[0][1])
        self.spin_title_edit_btn_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_title_edit_btn_y.grid(row=0, column=4, sticky="w", padx=5, pady=(5, 0))

        #share btn
        rb_share_btn = tk.Radiobutton(self.settingNVPWindow, text="「共有(↗)」ボタン", value=2, variable=self.rbVPositionIndex)
        rb_share_btn.grid(row=1, column=0, padx=5, sticky="w")

        lab_share_btn_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_share_btn_x.grid(row=1, column=1, padx=5, sticky="e")
        
        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[1][0])
        self.spin_share_btn_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_share_btn_x.grid(row=1, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_share_btn_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_share_btn_y.grid(row=1, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[1][1])
        self.spin_share_btn_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_share_btn_y.grid(row=1, column=4, sticky="w", padx=5, pady=(5, 0))

        #more btn
        rb_more_btn = tk.Radiobutton(self.settingNVPWindow, text="メニュー(…)」ボタン", value=3, variable=self.rbVPositionIndex)
        rb_more_btn.grid(row=2, column=0, padx=5, sticky="w")

        lab_more_btn_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_more_btn_x.grid(row=2, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[2][0])
        self.spin_more_btn_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_more_btn_x.grid(row=2, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_more_btn_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_more_btn_y.grid(row=2, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[2][1])
        self.spin_more_btn_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_more_btn_y.grid(row=2, column=4, sticky="w", padx=5, pady=(5, 0))

        #drop plus btn
        rb_drop_plus_btn = tk.Radiobutton(self.settingNVPWindow, text="「動画を追加する(+)」ボタン", value=4, variable=self.rbVPositionIndex)
        rb_drop_plus_btn.grid(row=3, column=0, padx=5, sticky="w")

        lab_drop_plus_btn_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_drop_plus_btn_x.grid(row=3, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[3][0])
        self.spin_drop_plus_btn_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_drop_plus_btn_x.grid(row=3, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_drop_plus_btn_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_drop_plus_btn_y.grid(row=3, column=3, padx=5, sticky="e")


        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[3][1])
        self.spin_drop_plus_btn_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_drop_plus_btn_y.grid(row=3, column=4, sticky="w", padx=5, pady=(5, 0))

        #URL Tab
        rb_url_tab = tk.Radiobutton(self.settingNVPWindow, text="「URL」タブ", value=5, variable=self.rbVPositionIndex)
        rb_url_tab.grid(row=4, column=0, padx=5, sticky="w")

        lab_url_tab_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_url_tab_x.grid(row=4, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[4][0])
        self.spin_url_tab_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_url_tab_x.grid(row=4, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_url_tab_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_url_tab_y.grid(row=4, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[4][1])
        self.spin_url_tab_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_url_tab_y.grid(row=4, column=4, sticky="w", padx=5, pady=(5, 0))

        #URL to paste
        rb_paste_url = tk.Radiobutton(self.settingNVPWindow, text="「YouTubeのURLを…」入力窓", value=6, variable=self.rbVPositionIndex)
        rb_paste_url.grid(row=5, column=0, padx=5, sticky="w")

        lab_paste_url_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_paste_url_x.grid(row=5, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[5][0])
        self.spin_paste_url_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_paste_url_x.grid(row=5, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_paste_url_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_paste_url_y.grid(row=5, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[5][1])
        self.spin_paste_url_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_paste_url_y.grid(row=5, column=4, sticky="w", padx=5, pady=(5, 0))

        #Add vidoes btn        
        rb_add_videos = tk.Radiobutton(self.settingNVPWindow, text="「動画を追加」ボタン", value=7, variable=self.rbVPositionIndex)
        rb_add_videos.grid(row=6, column=0, padx=5, sticky="w")

        lab_add_videos_x = tk.Label(self.settingNVPWindow, text="x:")
        lab_add_videos_x.grid(row=6, column=1, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[6][0])
        self.spin_add_videos_x = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_add_videos_x.grid(row=6, column=2, sticky="w", padx=5, pady=(5, 0))

        lab_add_videos_y = tk.Label(self.settingNVPWindow, text="y:")
        lab_add_videos_y.grid(row=6, column=3, padx=5, sticky="e")

        spin_var = tk.StringVar()
        spin_var.set(self.nvp_values[6][1])
        self.spin_add_videos_y = tk.Spinbox(self.settingNVPWindow, from_=0, to=2000, width=10, textvariable=spin_var)
        self.spin_add_videos_y.grid(row=6, column=4, sticky="w", padx=5, pady=(5, 0))

        settingVBtnFrame = tk.Frame(self.settingNVPWindow)
        settingVBtnFrame.grid(row=0, column=5, rowspan=3, sticky='wens')

        btn_execute_setting = Button(settingVBtnFrame, text="設定", command=self.register_setting_info)
        btn_execute_setting.grid(sticky='wens', row=0, column=0, padx=5, ipady=3, pady=(10, 10))

        btn_execute_cancel = Button(settingVBtnFrame, text="キャンセル", command=self.close_window)
        btn_execute_cancel.grid(sticky='wens', row=1, column=0, padx=5, ipady=3, ipadx=20)

        threading.Thread(target=self.get_position).start()
    def log_mouse_position(self, key):
        key = str(key)    
        if key == 'Key.ctrl_l':
            print("inIfCondition")
            currentMouse = MController()
            print(currentMouse.position)
            
            print("rbPositionValue:", self.rbVPositionIndex.get())
            if self.rbVPositionIndex.get() == 1:
                self.spin_title_edit_btn_x.delete(0, END)
                self.spin_title_edit_btn_x.insert(0, currentMouse.position[0])
                self.spin_title_edit_btn_y.delete(0, END)
                self.spin_title_edit_btn_y.insert(0, currentMouse.position[1])
            elif self.rbVPositionIndex.get() == 2:
                self.spin_share_btn_x.delete(0, END)
                self.spin_share_btn_x.insert(0, currentMouse.position[0])
                self.spin_share_btn_y.delete(0, END)
                self.spin_share_btn_y.insert(0, currentMouse.position[1])
            elif self.rbVPositionIndex.get() == 3:
                self.spin_more_btn_x.delete(0, END)
                self.spin_more_btn_x.insert(0, currentMouse.position[0])
                self.spin_more_btn_y.delete(0, END)
                self.spin_more_btn_y.insert(0, currentMouse.position[1])
            elif self.rbVPositionIndex.get() == 4:
                self.spin_drop_plus_btn_x.delete(0, END)
                self.spin_drop_plus_btn_x.insert(0, currentMouse.position[0])
                self.spin_drop_plus_btn_y.delete(0, END)
                self.spin_drop_plus_btn_y.insert(0, currentMouse.position[1])
            elif self.rbVPositionIndex.get() == 5:
                self.spin_url_tab_x.delete(0, END)
                self.spin_url_tab_x.insert(0, currentMouse.position[0])
                self.spin_url_tab_y.delete(0, END)
                self.spin_url_tab_y.insert(0, currentMouse.position[1])
            elif self.rbVPositionIndex.get() == 6:
                self.spin_paste_url_x.delete(0, END)
                self.spin_paste_url_x.insert(0, currentMouse.position[0])
                self.spin_paste_url_y.delete(0, END)
                self.spin_paste_url_y.insert(0, currentMouse.position[1])
            elif self.rbVPositionIndex.get() == 7:
                self.spin_add_videos_x.delete(0, END)
                self.spin_add_videos_x.insert(0, currentMouse.position[0])
                self.spin_add_videos_y.delete(0, END)
                self.spin_add_videos_y.insert(0, currentMouse.position[1])

    def get_position(self):
        with KListener(on_press=self.log_mouse_position) as vkl:
            vkl.join()
    def register_setting_info(self):
        setting_values = [[self.spin_title_edit_btn_x.get(), self.spin_title_edit_btn_y.get()], [self.spin_share_btn_x.get(), self.spin_share_btn_y.get()], [self.spin_more_btn_x.get(), self.spin_more_btn_y.get()], [self.spin_drop_plus_btn_x.get(), self.spin_drop_plus_btn_y.get()], [self.spin_url_tab_x.get(), self.spin_url_tab_y.get()], [self.spin_paste_url_x.get(), self.spin_paste_url_y.get()], [self.spin_add_videos_x.get(), self.spin_add_videos_y.get()]]

        writeFile = open('data/data_04', 'wb')
        pickle.dump(setting_values, writeFile)
        writeFile.close()
        self.close_window()
    def close_window(self):
        SettingNewVideoPositionsWindow.count = SettingNewVideoPositionsWindow.count - 1
        self.settingNVPWindow.destroy()