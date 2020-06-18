try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter.ttk import Button, Entry, Style

# from tkinter import Y, BOTH, TOP, Checkbutton, VERTICAL, RIGHT, FALSE, Canvas, LEFT, TRUE, NW

from tkinter import LEFT, E, messagebox


from tube_table import TubeTable
from mk_dir_files import mkDirFiles
from setting import SettingWindow
# from make_playlist import openMakePlaylistWindow
from make_playlist import MakePlaylistWindow

import requests
import os
from _cffi_backend import callback

import pickle

from pandastable import Table, TableModel
import pandas as pd
import codecs
import time
import datetime
import threading
from multiprocessing import Process, Queue, Pool, Manager
# import tkFont

import numpy as np
import random
from bs4 import BeautifulSoup
import webbrowser
from subprocess_maximize import Popen

from pynput.mouse import Listener as MListener, Button as MButton, Controller as MController
from pynput.keyboard import Listener as KListener, Key, Controller as KController

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from progress_bar import ProgressbarWindow
from save_playlist_video import savePlaylistVideo

class ImgBtn:
    """button1 = Button("Testo", "4ce", 0, 0)"""
    def __init__(self, text, classe, func, row, col, image=""):
        image2 = tk.PhotoImage(file=image)        
        image3 = image2.subsample(5, 5)

        self.button = Button(
            headerFrame,
            text=text,
            image=image3,
            compound = LEFT,
            command=lambda: func(classe)
            )

        self.button.grid(row=row, column=col, pady=10, padx=2) # sticky=tkinter.NW,
        self.button.image = image3
    def execute_supplementary_function(v):
        print(v)
        if v == 1:
            print(entry_keyword.get())
            global keyword_search_progress
            keyword_search_progress = ProgressbarWindow(mainWindow)

            global thread_get_all_suggest_keywords
            thread_get_all_suggest_keywords = threading.Thread(target=getAllSuggestKeywords, args=(entry_keyword.get(),))
            thread_get_all_suggest_keywords.start()
        elif v == 2:
            if SettingWindow.count == 0:
                setting_window = SettingWindow(mainWindow)
        elif v == 3:
            videoTable.clear_body()
        elif v == 4:
            keyword_arr = []
            url_arr = []
            title_arr = []

            for row in videoTable.dataVars:
                keyword_arr.append(row[1])
                url_arr.append(row[2])
                title_arr.append(row[3])            
            current_date = datetime.date.today()
            hour = str(datetime.datetime.now().hour)
            minute = str(datetime.datetime.now().minute)
            df_excel = pd.DataFrame({'キーワード': keyword_arr, 'URL': url_arr, 'タイトル': title_arr})
            df_excel.to_excel('export/file_' + str(current_date) + "_" + hour + "-" + minute + '.xlsx', sheet_name='sheet1', index=False)
            messagebox.showinfo("List Tube", 'export/file_' + str(current_date) + "_" + hour + "-" + minute + '.xlsx')
class ImgBtnQuit:
    """button1 = Button("Testo", "4ce", 0, 0)"""
    def __init__(self, text, row, col, image=""):
        image2 = tk.PhotoImage(file=image)
        
        image3 = image2.subsample(5, 5)

        self.button = Button(
            mainWindow,
            text=text,
            image=image3,
            compound = LEFT,
            command=self.close_main_window
            )
        # self.button.pack()
        self.button.grid(row=row, column=col, pady=10, padx=2, sticky=E) # sticky=tkinter.NW,
        self.button.image = image3
    def close_main_window(self):
        mainWindow.destroy()
def extractKeywordsFromText(suggest_keywords_text, suggest_keyword_count, keyword):
    i = suggest_keywords_text.find("(")
    j = suggest_keywords_text.find("{")
    suggest_keywords_text = suggest_keywords_text[i+1:j-1]

    index = 0
    suggest_keywords = []

    while index >= 0:
        i = suggest_keywords_text.find("\"", index)
        index = i + 1
        j = suggest_keywords_text.find("\"", index)
        index = j + 1
        if i != -1 and j != -1:
            suggest_keyword = codecs.decode(suggest_keywords_text[i+1:j], 'unicode_escape')
            if suggest_keyword != keyword:
                if len(suggest_keywords) < suggest_keyword_count:
                    suggest_keywords.append(suggest_keyword)
                else:
                    break
        else:
            index = -1
    return suggest_keywords
def getSuggestKeywords(keyword, suggest_keyword_count):
    print("-------------------------- running keyword_search_progress ----------------------------")
    r = requests.get("https://clients1.google.com/complete/search?client=youtube&hl=en&ds=v&q="+keyword)
    content = r.text
    suggest_keywords = extractKeywordsFromText(content, suggest_keyword_count, keyword)
    return suggest_keywords
def getAllSuggestKeywords(keyword):
    readFile = open('data/data_01', 'rb')
    registered_setting_values = pickle.load(readFile)
    readFile.close()
    main_suggest_keyword_cnt = int(registered_setting_values[0][1])
    suggest_keyword_cnt_1 = int(registered_setting_values[1][1])
    suggest_keyword_cnt_2 = int(registered_setting_values[2][1])
    alphabet_keyword_cnt = int(registered_setting_values[3][1])
    video_acquire_cnt = int(registered_setting_values[4][1])

    main_suggest_keyword_arr = getSuggestKeywords(keyword, main_suggest_keyword_cnt)
    suggest_keyword_1_arr   =   []
    suggest_keyword_2_arr   =   []
    alphabet_keyword_arr    =   []
    
    for i in range(0, len(main_suggest_keyword_arr)):
        suggest_keyword_1_arr = suggest_keyword_1_arr + getSuggestKeywords(main_suggest_keyword_arr[i], suggest_keyword_cnt_1)
        
    for suggest_keyword_1_item in suggest_keyword_1_arr:
        suggest_keyword_2_arr = suggest_keyword_2_arr + getSuggestKeywords(suggest_keyword_1_item, suggest_keyword_cnt_2)
    
    # hiragana_alphabets = "あ,い,う,え,お,か,き,く,け,こ,さ,し,す,せ,そ,た,ち,つ,て,と,な,に,ぬ,ね,の,は,ひ,ふ,へ,ほ,ま,み,む,め,も,や,ゆ,よ,ら,り,る,れ,ろ,わ,ゐ,ゑ,を,ん"
    hiragana_alphabets = "あ,い,う,え,お"
    print(hiragana_alphabets)
    hiragana_alphabets = hiragana_alphabets.split(",")
    print(hiragana_alphabets)

    for alphabet in hiragana_alphabets:
        alphabet_keyword_arr = alphabet_keyword_arr + getSuggestKeywords(keyword+" "+ alphabet, alphabet_keyword_cnt)

    all_suggest_keywords = [keyword] + main_suggest_keyword_arr + suggest_keyword_1_arr + suggest_keyword_2_arr + alphabet_keyword_arr

    print("********************************* all_suggest_keywords ******************************")
    print(all_suggest_keywords)
    
    dataVars = []
    for suggest_keyword in all_suggest_keywords:
        print(suggest_keyword)
        ckValue = tk.BooleanVar()
        ckValue.set(False)
        dataVars.append([ckValue, suggest_keyword, video_acquire_cnt])
    print("***************** all_suggest_keywords end ******************************")

    keywordTable._load_data(dataVars)
    keyword_search_progress.close_window()
########################### acquiring video list - begin ################################

def scroll(driver, timeout, count):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # sub_video_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
        sub_video_data = driver.find_elements_by_xpath('//*[@id="video-title"]/yt-formatted-string')
        if len(sub_video_data) > count:
            break
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        # Wait to load page
        time.sleep(scroll_pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height
def getVideoInfos(keyword, count, driver):
    url = "https://www.youtube.com/results?search_query="+keyword
    driver.get(url)
    driver.implicitly_wait(30)
    scroll(driver, 4, count)

    video_data = driver.find_elements_by_xpath('//*[@id="video-title"]')

    print("count per page=======> ", len(video_data))
    videoInfos = []
    index = 0
    for i in video_data:
        if index < count:
            if i.get_attribute('href') is not None:
                row = []
                ckValue = tk.BooleanVar()
                ckValue.set(False)
                row.append(ckValue)
                row.append(keyword)
                # row.append(i.get_attribute('href').strip('https://www.youtube.com/watch?v='))
                row.append(i.get_attribute('href').split("https://www.youtube.com/watch?v=")[1])
                row.append(i.text)
                videoInfos.append(row)

                index = index + 1
        else:
            break
        # index = index + 1
    return videoInfos
def getAllVideoInfos(selected_keywords):
    print("begin driver ==========>")
    video_arr = []
    driver = webdriver.Chrome(executable_path=r"webdrivers\chromedriver.exe")
    # driver = webdriver.Chrome()
    allVideoInfos = []
    for row in selected_keywords:
        cur_keyword = row[1]
        cur_count = row[2]
        print("~~~~~~~~~~~~~~~~~~~~~")
        print("cur_keyword = > ", cur_keyword)
        print("~~~~~~~~~~~~~~~~~~~~~")
        if cur_keyword != "":
            allVideoInfos = allVideoInfos + getVideoInfos(cur_keyword, cur_count, driver)
    driver.close()
    videoTable._load_data(allVideoInfos)    

    mainWindow.wm_attributes("-disabled", False)
    video_info_acquire_progress.close_window()
def acquire_info():
    selected_keywords = keywordTable.get_selected_data_vars()
    print("**************************** get selected data vars for keywordTable*************************************")
    print(selected_keywords)
    print("*****************************************************************")
    if len(selected_keywords) > 0:
        global video_info_acquire_progress
        video_info_acquire_progress = ProgressbarWindow(mainWindow)

        global thread_get_all_video_infos
        thread_get_all_video_infos = threading.Thread(target=getAllVideoInfos, args=(selected_keywords,))
        thread_get_all_video_infos.start()
        mainWindow.wm_attributes("-disabled", True)
    else:
        messagebox.showwarning('List Tube', '選択されたキーワードがありません。')

def runReservation():
    btn_run_reservation.configure(text="予約実行停止", style="RStop.TButton")
    msgBox = messagebox.askquestion('List Tube', '予約実行をすると現在編集中のリスト内容が破棄されます。予約実行開始してよろしいですか？')
    if msgBox == 'yes':
        if make_playlist_window is not None:
            make_playlist_window.close_window()
        readFile = open('data/data_06', 'rb')
        values_reservation = pickle.load(readFile)
        readFile.close()

        if len(values_reservation) > 0:
            for row in values_reservation:
                playlist_data = row[4]
                if len(playlist_data) > 0:
                    print("*************", "reservation name =>", row[0], "***************")
                    savePlaylistVideo(playlist_data)
                else:
                    print("no playlist, video")

            messagebox.showinfo("List Tube", "全ての予約実行を完了しました。")

            # writeFile = open('data/data_06', 'wb')
            # pickle.dump([], writeFile)
            # writeFile.close()
        else:
            messagebox.showwarning("List Tube", "予約がありません。")
            print("no reservation")

        btn_run_reservation.configure(text="予約実行開始", style="RPlay.TButton")
    else:
        btn_run_reservation.configure(text="予約実行開始", style="RPlay.TButton")
def updateClock():    
    readFile = open('data/data_06', 'rb')
    values_reservation = pickle.load(readFile)
    readFile.close()
    if len(values_reservation) > 0:
        now = time.strftime("%H:%M:%S")
        print("------------------- 1 ------ 1 ----------------------")
        print(now)
        today = str(datetime.date.today())
        now_hour = int(time.strftime("%H"))
        now_minute = int(time.strftime("%M"))        

        for row in values_reservation:
            reservation_name = str(row[0])
            reservation_date = str(row[1])
            reservation_hour = int(row[2])
            reservation_minute = int(row[3])

            print("------------------- 2 ------ 2 ----------------------")

            if today == reservation_date and now_hour == reservation_hour and now_minute == reservation_minute:
                print("matching date hour min")
                messagebox.showinfo("reservation", row[0])
                playlist_data = row[4]
                savePlaylistVideo(playlist_data)
                break
            else:
                print("not matching")

    mainWindow.after(60000, updateClock)
    # else:
    #     return
################################################### acquiring video list - end ############################################
def openMakePlaylistWindow(parent, videoTable):
    if MakePlaylistWindow.count == 0:
        global make_playlist_window
        mainWindow.iconify()
        make_playlist_window = MakePlaylistWindow(parent)
        make_playlist_window._create_windowview(videoTable)

if __name__ == "__main__":

    mkDirFiles()
    
    global make_playlist_window
    make_playlist_window = None

    mainWindow = tk.Tk()
    mainWindow.title("List YouTube")

    width_of_window = 1024
    height_of_window = 700
    screen_width = mainWindow.winfo_screenwidth()
    screen_height = mainWindow.winfo_screenheight()
    x_coordinate = (screen_width/2) - (width_of_window/2)
    y_coordinate = (screen_height/2) - (height_of_window/2)

    mainWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

    updateClock()

    #Frame
    headerFrame = tk.Frame(mainWindow)
    headerFrame.grid(row=0, column=0, sticky='w', columnspan=5)

    label_keyword = tk.Label(headerFrame, text="キーワード")
    label_keyword.grid(row=0, column=0, padx=5)

    entry_keyword = Entry(headerFrame, width=30)
    entry_keyword.grid( row=0, column=1, sticky="ns", padx=2,pady=11)

    btn_search = ImgBtn("キーワード検索", "", lambda x: ImgBtn.execute_supplementary_function(1), 0, 2, image="images/search.png")
    btn_setting = ImgBtn("設定", "", lambda x: ImgBtn.execute_supplementary_function(2), 0, 3, image="images/setting.png")
    btn_del_search_result = ImgBtn("検索結果クリア", "", lambda x: ImgBtn.execute_supplementary_function(3), 0, 4, image="images/delete.png")
    btn_export_excel = ImgBtn("EXCEL形式でコピー", "", lambda x: ImgBtn.execute_supplementary_function(4), 0, 5, image="images/excel.png")

    style_btn_reservation_play = Style()
    style_btn_reservation_play.configure("RPlay.TButton", foreground="#ff0000")
    style_btn_reservation_stop = Style()
    style_btn_reservation_stop.configure("RStop.TButton", foreground="#0000ff")

    
    btn_run_reservation = Button(headerFrame, command=lambda : runReservation())
    btn_run_reservation.configure(text="予約実行開始", style="RPlay.TButton")
    # btn_run_reservation.configure(text="Play Reservation", style="RStop.TButton")
    btn_run_reservation.grid(row=0, column=6, padx=20, ipady=3)

    btn_quit = ImgBtnQuit("終了", 0, 5, image="images/close.png")

    #Frame
    middleFrame = tk.Frame(mainWindow)
    middleFrame.grid(row=1, column=0, sticky='wse', columnspan=3, pady=5)

    btn_vselect_all = Button(middleFrame, text="全選択", command = lambda: videoTable.select_all())
    btn_vselect_all.grid(sticky='wns', row=0, column=0, padx=5, ipady=3)
    btn_vunselect_all = Button(middleFrame, text="全解除", command = lambda: videoTable.unselect_all())
    btn_vunselect_all.grid(sticky='wns', row=0, column=1)

    

    btn_add_to_list = Button(middleFrame, text="リストに追加", command=lambda: openMakePlaylistWindow(mainWindow, videoTable))
    btn_add_to_list.grid(sticky='wns', row=0, column=2, padx=15, )
    btn_delete_selected = Button(middleFrame, text="選択行削除", command=lambda: videoTable.delete_selected_data_vars())
    btn_delete_selected.grid(sticky='wns', row=0, column=3, padx=50, )
    
    #Frame
    selFrame = tk.LabelFrame(mainWindow, text='選択パネル',)
    selFrame.grid(row=1, column=3, columnspan=3, sticky='wse', rowspan=2, padx=5, pady=(0,5))

    btn_kselect_all = Button(selFrame, text="全選択", command = lambda: keywordTable.select_all())
    btn_kselect_all.grid(sticky='w', row=0, column=0, padx=5, ipady=3)
    btn_kunselect_all = Button(selFrame, text="全解除", command = lambda: keywordTable.unselect_all())
    btn_kunselect_all.grid(sticky='w', row=0, column=1, ipady=3)
    btn_kdelete_selected = Button(selFrame, text="選択行削除", command=lambda: keywordTable.delete_selected_data_vars())
    btn_kdelete_selected.grid(sticky='w', row=0, column=2, padx=12, ipady=3 )
    btn_acquire_keywords = Button(selFrame, text="動画情報取得", command= lambda: acquire_info())
    btn_acquire_keywords.grid(sticky='w', row=1, column=0, padx=5, pady=5, ipady=3)

    mainWindow.columnconfigure(0, weight=5)
    mainWindow.columnconfigure(1, weight=5)
    mainWindow.columnconfigure(2, weight=5)
    mainWindow.columnconfigure(3, weight=1)
    mainWindow.columnconfigure(4, weight=1)
    mainWindow.columnconfigure(5, weight=1)
    mainWindow.rowconfigure(0, weight=1)
    mainWindow.rowconfigure(1, weight=1)
    mainWindow.rowconfigure(2, weight=8)
    mainWindow.rowconfigure(3, weight=40)
    mainWindow.rowconfigure(4, weight=40)

    #TableFrame
    videoTable = TubeTable(mainWindow, 2, 0, 3, 3, 5, 0, 0, 5)
    dataColummns = [['No', 'index', 5], ['選択', 'CheckButton', 5], ['キーワード', 'Label', 25], ['URL', 'Label', 15], ['タイトル', 'Label', 45]]
    videoTable._create_tableview(dataColummns, 0)
    
    keywordTable = TubeTable(mainWindow, 3, 3, 3, 3, 5, 5, 0, 5)
    dataColummns = [['選択', 'CheckButton', 5], ['キーワード', 'Label', 30], ['収集件数', 'Label', 9]]
    keywordTable._create_tableview(dataColummns, -1)

    mainWindow.mainloop()