try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter.ttk import Button, Entry, Label, Combobox
from tkinter import END, Checkbutton, messagebox
import pickle
import pyperclip

import time
import threading
from subprocess_maximize import Popen
import random

from pynput.mouse import Listener as MListener, Button as MButton, Controller as MController
from pynput.keyboard import Listener as KListener, Key, Controller as KController

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkcalendar import DateEntry
from timepicker import TimePicker

from tube_table import TubeTable
from setting_new_playlist_positions import SettingNewPlaylistPositionsWindow
from setting_new_video_positions import SettingNewVideoPositionsWindow
from add_reservation import AddReservationWindow
from reservation_list import ReservationListWindow
from save_playlist_video import savePlaylistVideo
from edit_playlist_name import EditPlaylistNameWindow
from manual_input_url import ManualInputUrlWindow
from save_own_url_list import SaveOwnUrlListWindow

class MakePlaylistWindow(tk.Frame):
    count = 0
    def __init__(self, parent):
        MakePlaylistWindow.count = MakePlaylistWindow.count + 1
        self.rbAddOwnUrlValue = tk.IntVar()
        self.rbAddOwnUrlValue.set(1)

        self.playlistWindow = tk.Toplevel(parent)
        self.playlistWindow.title("YouTube再生リスト作成")
        self.playlistWindow.protocol("WM_DELETE_WINDOW", self.close_window)

        width_of_window = 1024
        height_of_window = 700
        screen_width = self.playlistWindow.winfo_screenwidth()
        screen_height = self.playlistWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.playlistWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.playlistWindow.columnconfigure(0, weight=2)
        self.playlistWindow.columnconfigure(1, weight=4)
        self.playlistWindow.columnconfigure(2, weight=1)
        self.playlistWindow.columnconfigure(3, weight=1)
        self.playlistWindow.columnconfigure(4, weight=6)
        self.playlistWindow.columnconfigure(5, weight=1)
        self.playlistWindow.columnconfigure(6, weight=1)
        # self.playlistWindow.columnconfigure(7, weight=1)
        self.playlistWindow.rowconfigure(0, weight=1)
        self.playlistWindow.rowconfigure(1, weight=1)
        self.playlistWindow.rowconfigure(2, weight=1)
        self.playlistWindow.rowconfigure(3, weight=1)
        self.playlistWindow.rowconfigure(4, weight=1)
        self.playlistWindow.rowconfigure(5, weight=1)
        self.playlistWindow.rowconfigure(6, weight=1)

    def _create_windowview(self, videoTable):
        self.playlistTable = TubeTable(self.playlistWindow, 0, 0, 3, 5, 5, 0, 5, 0)
        dataColummns = [['Url', 'Label', 15], ['タイトル', 'Label', 35], ['再生リスト名', 'Label', 25], ['定型文', 'Combobox', 12]]
        self.playlistTable._create_tableview(dataColummns, -1, True)
        
        dataVars = []
        for row in videoTable.get_selected_data_vars():
            dataVars.append([row[2], row[3], row[1], 0])
        if(len(dataVars) > 0):
            self.playlistTable._load_data(dataVars)
            self.playlistTable.select_row(0)
        #Frame
        playlistActionFrame = tk.Frame(self.playlistWindow)
        playlistActionFrame.grid(row=0, column=5, sticky='wne', rowspan=3)

        btn_moveup = Button(playlistActionFrame, text = "上に移動", command = lambda: self.playlistTable.move_up_selection())
        btn_moveup.grid(row=0, column=0, padx=5, ipady=3, pady=(10, 0), sticky='we')
        btn_movedown = Button(playlistActionFrame, text = "下に移動", command = lambda: self.playlistTable.move_down_selection() )
        btn_movedown.grid(row=1, column=0, pady=(10, 30), padx=5, ipady=3, sticky='we')
        
        btn_del_row = Button(playlistActionFrame, text = "１行削除",  command = lambda: self.playlistTable.delete_selection())
        btn_del_row.grid(row=2, column=0, padx=5, ipady=3, sticky='we')
        btn_del_all_rows = Button(playlistActionFrame, text = "全削除", command = lambda: self.playlistTable.clear_body())
        btn_del_all_rows.grid(row=3, column=0, pady=(10, 30), padx=5, ipady=3, sticky='we')

        btn_rename_playlist = Button(playlistActionFrame, text = "リスト名変更", command=self.edit_playlist_name)
        btn_rename_playlist.grid(row=4, column=0, padx=5, ipady=3, sticky='we')
        
        makePlaylistFrame = tk.Frame(self.playlistWindow)
        makePlaylistFrame.grid(row=0, column=6, sticky='e', rowspan=2, padx=(0, 0))

        # btn_make_playlist = Button(makePlaylistFrame, text = "再生リスト作成", command=lambda: savePlaylistVideo(self.playlistTable.dataVars))
        btn_make_playlist = Button(makePlaylistFrame, text = "再生リスト作成", command=self.save_playlist_video)
        btn_make_playlist.grid(row=0, column=0, sticky='wne', columnspan=2, padx=5, ipady=3, pady=(10, 0))

        setSpeedFrame = tk.Frame(makePlaylistFrame)
        setSpeedFrame.grid(row=1, column=0, sticky='wne', padx=(0, 0), pady=(5, 0))

        label_speed = tk.Label(setSpeedFrame, text="入力速度:")
        label_speed.grid(row=0, column=0, pady=(5, 0), sticky="w")

        readFile = open('data/data_07', 'rb')
        value_cb_speed = pickle.load(readFile)
        readFile.close()

        combo_set_speed = Combobox(setSpeedFrame, state="readonly", width=7)
        combo_set_speed['values'] = ["低", "中", "高"]
        combo_set_speed.current(value_cb_speed[0])
        combo_set_speed.grid(row=0, column=1, ipady=4, sticky="e", padx=6, pady=(5, 0))
        combo_set_speed.bind("<<ComboboxSelected>>", lambda e, obj=combo_set_speed: self.update_speed_combobox(e, obj))

        #settingNewPlaylistPositions
        btn_set_playlist_pos = Button(makePlaylistFrame, text = "プレイリストの座標設定", command=self.setting_new_playlist_positions)
        btn_set_playlist_pos.grid(row=3, column=0, sticky='wne', columnspan=2, padx=5, ipady=3, pady=(10, 0))

        btn_set_video_pos = Button(makePlaylistFrame, text = "動画の座標設定", command=self.setting_new_video_positions)
        btn_set_video_pos.grid(row=4, column=0, sticky='wne', columnspan=2, padx=5, ipady=3, pady=(10, 0))

        btn_add_reservation = Button(makePlaylistFrame, text = "予約リストに追加", command=self.add_reservation)
        btn_add_reservation.grid(row=5, column=0, sticky='wne', columnspan=2, padx=5, ipady=3, pady=(30, 0))

        btn_mng_reservations = Button(makePlaylistFrame, text = "予約リストメンテナンス", command=self.reservation_list)
        btn_mng_reservations.grid(row=6, column=0, sticky='wne', columnspan=2, padx=5, ipady=3, pady=(10, 0))

        middlePlaylistFrame =  tk.Frame(self.playlistWindow)
        middlePlaylistFrame.grid(row=3, column=0, columnspan=4, sticky='wnes', pady=(10, 5))

        label_add_url = Label(middlePlaylistFrame, text="任意追加URL")
        label_add_url.grid(row=0, column=0, padx=(0, 15))

        btn_save_own_url = Button(middlePlaylistFrame, text = "保存", command=lambda: self.save_own_url_list(combo_own_url))
        btn_save_own_url.grid(row=0, column=1, sticky='wn', padx=(0, 30), ipady=3)

        btn_load_own_url = Button(middlePlaylistFrame, text = "読込", command=lambda: self.load_own_url_list(combo_own_url))
        btn_load_own_url.grid(row=0, column=2, sticky='wn', padx=(0, 5), ipady=3)
        
        readFile = open('data/data_02', 'rb')
        values_soul = pickle.load(readFile)
        readFile.close()

        values_to_cb = []
        for row in values_soul:
            values_to_cb.append(row[0])

        combo_own_url = Combobox(middlePlaylistFrame, state="readonly",)
        if len(values_to_cb) == 0:
            combo_own_url['values']= [""]
        else:
            combo_own_url['values'] = values_to_cb

        combo_own_url.current(0)
        combo_own_url.grid(row=0, column=3, ipady=4)

        #TableFrame
        self.ownUrlListTable = TubeTable(self.playlistWindow, 4, 0, 3, 3, 5, 5, 0, 5)
        dataColummns = [['選択', 'CheckButton', 8], ['URL', 'Label', 20], ['タイトル', 'Label', 30]]
        self.ownUrlListTable._create_tableview(dataColummns, -1)

        btn_acquire_title = Button(self.playlistWindow, text = "タイトル取得", command=self.acquire_titles)
        btn_acquire_title.grid(row=4, column=3, sticky='wn', ipady=4)

        inputOwnUrlFrame = tk.Frame(self.playlistWindow)
        inputOwnUrlFrame.grid(row=5, column=3, rowspan=2, sticky='wne')

        btn_paste_url = Button(inputOwnUrlFrame, text = "貼り付け", command = self.paste_url)
        btn_paste_url.grid(row=0, column=0, sticky='we', ipady=3)
        btn_input_manual = Button(inputOwnUrlFrame, text = "手入力", command = self.manual_input_url)
        btn_input_manual.grid(row=1, column=0, sticky='we', pady=(5, 20), ipady=3, padx=(0, 0))
        # btn_delete_url = Button(inputOwnUrlFrame, text = "削除", command = lambda: self.ownUrlListTable.delete_selected_data_vars())
        btn_delete_url = Button(inputOwnUrlFrame, text = "削除", command = lambda: self.delete_own_url_list(combo_own_url))
        btn_delete_url.grid(row=2, column=0, sticky='we', ipady=3)

        #Frame
        radioAddOwnUrlFrame = tk.LabelFrame(self.playlistWindow, text='リストに追加')
        radioAddOwnUrlFrame.grid(row=4, column=4, columnspan=3, rowspan=3, sticky='wn')
        
        radiobutton1 = tk.Radiobutton(radioAddOwnUrlFrame, text="現在行の下に追加", value=1, variable=self.rbAddOwnUrlValue)
        radiobutton2 = tk.Radiobutton(radioAddOwnUrlFrame, text="最上行に追加", value=2, variable=self.rbAddOwnUrlValue)
        radiobutton3 = tk.Radiobutton(radioAddOwnUrlFrame, text="最下行に追加", value=3, variable=self.rbAddOwnUrlValue)
        radiobutton1.grid(row=0, column=0, sticky='w')
        radiobutton2.grid(row=1, column=0, sticky='w')
        radiobutton3.grid(row=2, column=0, sticky='w')

        radioPointedFrame = tk.Frame(radioAddOwnUrlFrame)
        radioPointedFrame.grid(row=3, column=0, sticky='w')
        
        radiobutton4 = tk.Radiobutton(radioPointedFrame, text="指定行に追加", value=4, variable=self.rbAddOwnUrlValue)
        radiobutton4.grid(row=0, column=0, sticky='w')
        spin_var = tk.StringVar()
        spin_var.set("1")
        spin_addownurl_pointed = tk.Spinbox(radioPointedFrame, from_=1, to=100, width=5, textvariable=spin_var)
        spin_addownurl_pointed.grid(row=0, column=1, sticky='w')
        
        radioFormPerFrame = tk.Frame(radioAddOwnUrlFrame)
        radioFormPerFrame.grid(row=4, column=0, sticky='w')

        radiobutton5 = tk.Radiobutton(radioFormPerFrame, text="", value=5, variable=self.rbAddOwnUrlValue)
        radiobutton5.grid(row=0, column=0, sticky='w')

        spin_var = tk.StringVar()
        spin_var.set("1")
        spin_addownurl_from = tk.Spinbox(radioFormPerFrame, from_=1, to=100, width=5, textvariable=spin_var)
        spin_addownurl_from.grid(row=0, column=1, sticky='w',)
        label_addownurl_from = tk.Label(radioFormPerFrame, text="行目から")
        label_addownurl_from.grid(row=0, column=2, sticky="w")

        spin_var = tk.StringVar()
        spin_var.set("1")
        spin_addownurl_per = tk.Spinbox(radioFormPerFrame, from_=1, to=100, width=5, textvariable=spin_var)
        spin_addownurl_per.grid(row=0, column=3, sticky='w', )
        label_addownurl_from = tk.Label(radioFormPerFrame, text="行おき")
        label_addownurl_from.grid(row=0, column=4, sticky="w")

        radiobutton6 = tk.Radiobutton(radioAddOwnUrlFrame, text="ランダムに追加", value=6, variable=self.rbAddOwnUrlValue)
        radiobutton6.grid(row=5, column=0, sticky='w')

        btn_add_url = Button(radioAddOwnUrlFrame, text = "追加", command=lambda: self.add_to_playlist(spin_addownurl_pointed, spin_addownurl_from, spin_addownurl_per))
        btn_add_url.grid(row=6, column=0, sticky='e', pady=5, padx=15, ipady=3)

    def load_own_url_list(self, combo_own_url):
        print("current index", combo_own_url.current())
        cb_text = combo_own_url['values'][combo_own_url.current()]

        readFile = open('data/data_02', 'rb')
        values_soul = pickle.load(readFile)
        readFile.close()        
        dataVars = []
        for row in values_soul[combo_own_url.current()][1]:
            print("row =========================== > ", row)
            ckValue = tk.BooleanVar()
            ckValue.set(True)
            dataVars.append([ckValue, row[0], row[1]])

        print("datavars ==============> ", dataVars)
        self.ownUrlListTable.dataVars = dataVars
        self.ownUrlListTable._load_data(self.ownUrlListTable.dataVars)
    def delete_own_url_list(self, combo_own_url):
        print(" +++++++++++ current own url delete ++++++++++++ ")
        print("current index", combo_own_url.current())

        readFile = open('data/data_02', 'rb')
        values_soul = pickle.load(readFile)
        readFile.close()
        if len(values_soul) > 0:
            del values_soul[combo_own_url.current()]

            writeFile = open('data/data_02', 'wb')
            pickle.dump(values_soul, writeFile)
            writeFile.close()

            values_to_cb = []
            for row in values_soul:
                values_to_cb.append(row[0])
            if len(values_to_cb) == 0:
                combo_own_url['values']= [""]
            else:
                combo_own_url['values'] = values_to_cb

            combo_own_url.current(0)
            
            if len(values_soul) > 0:
                dataVars = []
                for row in values_soul[combo_own_url.current()][1]:
                    print("row =========================== > ", row)
                    ckValue = tk.BooleanVar()
                    ckValue.set(True)
                    dataVars.append([ckValue, row[0], row[1]])
                
                self.ownUrlListTable.dataVars = dataVars
                self.ownUrlListTable._load_data(self.ownUrlListTable.dataVars)
            else:
                self.ownUrlListTable.clear_body()
        else:
            self.ownUrlListTable.clear_body()

    def paste_url(self):
        print("+++++++++++++++ pasteUrl +++++++++++++++++")
        # get clipboard data
        clipbard_text = pyperclip.paste()
        url = clipbard_text.split('https://www.youtube.com/watch?v=')[1]
        print(url)
        ckValue = tk.BooleanVar()
        ckValue.set(True)
        self.ownUrlListTable.dataVars.append([ckValue, url, ""])
        print(self.ownUrlListTable.dataVars)
        self.ownUrlListTable._load_data(self.ownUrlListTable.dataVars)
    def add_to_playlist(self, spin_addownurl_pointed, spin_addownurl_from, spin_addownurl_per):
        toAddRows = self.ownUrlListTable.get_selected_data_vars()
        if len(toAddRows) == 0:
            messagebox.showwarning('List Tube', '追加するデータを入力してください。')
        else:
            if len(self.playlistTable.dataVars) > 0:
                if self.rbAddOwnUrlValue.get() == 1:
                    print(self.playlistTable.index_selection)
                    if(self.playlistTable.index_selection >= 0):
                        insert_position = self.playlistTable.index_selection + 1
                        for row in reversed(toAddRows):
                            print(row)
                            self.playlistTable.dataVars.insert(insert_position, [row[1], row[2], self.playlistTable.dataVars[insert_position-1][2], self.playlistTable.dataVars[insert_position-1][3]])
                        self.playlistTable._load_data(self.playlistTable.dataVars)
                elif self.rbAddOwnUrlValue.get() == 2:
                    for row in reversed(toAddRows):
                        print(row)
                        self.playlistTable.dataVars.insert(0, [row[1], row[2], self.playlistTable.dataVars[0][2], self.playlistTable.dataVars[0][3]])
                    self.playlistTable._load_data(self.playlistTable.dataVars)
                    self.playlistTable.index_selection = self.playlistTable.index_selection + len(toAddRows)
                    self.playlistTable.select_row(self.playlistTable.index_selection)
                elif self.rbAddOwnUrlValue.get() == 3:
                    insert_position = len(self.playlistTable.dataVars)
                    for row in reversed(toAddRows):
                        print(row)
                        self.playlistTable.dataVars.insert(insert_position, [row[1], row[2], self.playlistTable.dataVars[insert_position-1][2], self.playlistTable.dataVars[insert_position-1][3]])
                    self.playlistTable._load_data(self.playlistTable.dataVars)    
                elif self.rbAddOwnUrlValue.get() == 4:
                    insert_position = int(spin_addownurl_pointed.get()) - 1
                    if(insert_position < len(self.playlistTable.dataVars)):
                        for row in reversed(toAddRows):
                            print(row)
                            if insert_position == 0 :
                                self.playlistTable.dataVars.insert(0, [row[1], row[2], self.playlistTable.dataVars[0][2], self.playlistTable.dataVars[0][3]])
                            else:                                #elif insert_position ==  len(self.playlistTable.dataVars) - 1:
                                self.playlistTable.dataVars.insert(insert_position, [row[1], row[2], self.playlistTable.dataVars[insert_position-1][2], self.playlistTable.dataVars[insert_position-1][3]])
                        self.playlistTable._load_data(self.playlistTable.dataVars)
                        if insert_position == 0 or self.playlistTable.index_selection >= insert_position:
                            self.playlistTable.index_selection = self.playlistTable.index_selection + len(toAddRows)
                            self.playlistTable.select_row(self.playlistTable.index_selection)                        
                elif self.rbAddOwnUrlValue.get() == 5:
                    insert_from_position = int(spin_addownurl_from.get()) - 1
                    per_value = int(spin_addownurl_per.get())
                    k = 0
                    for row in toAddRows:
                        insert_position = insert_from_position + (k * (per_value + 1))
                        if insert_position >= len(self.playlistTable.dataVars):
                            break
                        if insert_position == 0:
                            self.playlistTable.dataVars.insert(0, [row[1], row[2], self.playlistTable.dataVars[0][2], self.playlistTable.dataVars[0][3]])
                        else:
                            self.playlistTable.dataVars.insert(insert_position, [row[1], row[2], self.playlistTable.dataVars[insert_position-1][2], self.playlistTable.dataVars[insert_position-1][3]])
                        k = k + 1
                    self.playlistTable._load_data(self.playlistTable.dataVars)
                    self.playlistTable.index_selection = 0
                    self.playlistTable.select_row(0)
                elif self.rbAddOwnUrlValue.get() == 6:
                    for row in toAddRows:
                        insert_position = random.randint(0, len(self.playlistTable.dataVars) - 1)
                        if insert_position == 0:
                            self.playlistTable.dataVars.insert(0, [row[1], row[2], self.playlistTable.dataVars[0][2], self.playlistTable.dataVars[0][3]])
                        else:
                            self.playlistTable.dataVars.insert(insert_position, [row[1], row[2], self.playlistTable.dataVars[insert_position-1][2], self.playlistTable.dataVars[insert_position-1][3]])                    
                    self.playlistTable._load_data(self.playlistTable.dataVars)
                    self.playlistTable.index_selection = 0
                    self.playlistTable.select_row(0)
            else:
                messagebox.showwarning('List Tube', '再生リストテーブルにデータがありません。')
    def acquire_titles(self):
        if len(self.ownUrlListTable.dataVars) > 0:
            driver = webdriver.Chrome(executable_path=r"webdrivers\chromedriver.exe")
            # driver = webdriver.Chrome()
            wait = WebDriverWait(driver, 10)
            for i in range(len(self.ownUrlListTable.dataVars)):
                print(i)
                print(self.ownUrlListTable.dataVars[i])
                self.ownUrlListTable.dataVars[i][2] = self.get_title(i, self.ownUrlListTable.dataVars[i][1], driver, wait) 
            driver.close()
            self.ownUrlListTable.refresh(self.ownUrlListTable.dataVars)
        else:
            messagebox.showwarning('List Tube', '追加するデータを入力してください。')
    def get_title(self, i, url, driver, wait):
        url = "https://www.youtube.com/watch?v=" + url
        driver.get(url)
        v_title = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR,"#container > h1 > yt-formatted-string"))).text
        return v_title

    def setting_new_playlist_positions(self):
        if SettingNewVideoPositionsWindow.count > 0:
            messagebox.showwarning("List Tube", "「動画の座標設定」ウィンドウを閉じた後、起動してください。")
        else:
            if SettingNewPlaylistPositionsWindow.count == 0:
                new_playlist_positions = SettingNewPlaylistPositionsWindow(self.playlistWindow)
                new_playlist_positions._create_windowview()
    def setting_new_video_positions(self):
        if SettingNewPlaylistPositionsWindow.count > 0:
            messagebox.showwarning("List Tube", "「プレイリストの座標設定」ウィンドウを閉じた後、起動してください。")
        else:
            if SettingNewVideoPositionsWindow.count == 0:
                new_video_positions = SettingNewVideoPositionsWindow(self.playlistWindow)
                new_video_positions._create_windowview()
    def add_reservation(self):
        if AddReservationWindow.count == 0:
            add_reservation = AddReservationWindow(self.playlistWindow)
            add_reservation._create_windowview(self.playlistTable.dataVars)
    def reservation_list(self):
        if ReservationListWindow.count == 0:
            reservation_list = ReservationListWindow(self.playlistWindow)
            reservation_list._create_windowview()
    def edit_playlist_name(self):
        if EditPlaylistNameWindow.count == 0:
            edit_playlist_name = EditPlaylistNameWindow(self.playlistWindow)
            edit_playlist_name._create_windowview(self.playlistWindow, self.playlistTable)
    def manual_input_url(self):
        if ManualInputUrlWindow.count == 0:
            manual_input_url = ManualInputUrlWindow(self.playlistWindow, self.ownUrlListTable)
    def save_own_url_list(self, combo_own_url):
        if SaveOwnUrlListWindow.count == 0:
            save_own_url_list = SaveOwnUrlListWindow(self.playlistWindow, self.ownUrlListTable, combo_own_url)
    def update_speed_combobox(self, event, combo_set_speed):
        writeFile = open('data/data_07', 'wb')
        pickle.dump([combo_set_speed.current()], writeFile)
        writeFile.close()
    def save_playlist_video(self):
        if len(self.playlistTable.dataVars) > 0:
            savePlaylistVideo(self.playlistTable.dataVars)
            messagebox.showinfo("List Tube", "予約実行を完了しました。")
        else:
            messagebox.showwarning("List Tube", "再生リストテーブルにデータがありません。")
    def close_window(self):
        MakePlaylistWindow.count = MakePlaylistWindow.count - 1
        self.playlistWindow.destroy()