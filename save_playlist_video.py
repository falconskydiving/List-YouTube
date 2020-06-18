
import pickle
import os

import time
from subprocess_maximize import Popen
import random

from pynput.mouse import Button as MButton, Controller as MController
from pynput.keyboard import Key, Controller as KController

def savePlaylistVideo(playlist_data):
    dataVars=[]
    readFile = open('data/data_05', 'rb')
    regular_gates = pickle.load(readFile)
    readFile.close()
    
    readFile = open('data/data_07', 'rb')
    value_cb_speed = pickle.load(readFile)
    readFile.close() 
    speed = 1
    if value_cb_speed[0] == 0:
        speed = 3
    elif value_cb_speed[0] == 1:
        speed = 2
    else:
        speed = 1

    index_playlist = 0
    for i in range(len(playlist_data)):
        url = playlist_data[i][0]
        regular_gate = regular_gates[playlist_data[i][3]]
        if i == 0:
            playlist_name = playlist_data[0][2] + regular_gate
            dataVars.append([playlist_name, [url]])
        else:
            if playlist_data[i][2] == playlist_data[i-1][2]:
                dataVars[index_playlist][1].append(url)
            else:
                playlist_name = playlist_data[i][2] + regular_gate
                dataVars.append([playlist_name, [url]])
                index_playlist = index_playlist + 1        
    if len(dataVars) > 0:
        print("---------------- Register Play List -----------------")
        print(dataVars)
        print("--------------------- for testing --------------------")

        os.system('TASKKILL /F /IM chrome.exe')
        google_browser = Popen('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',show='maximize', priority=0)
        
        mouse = MController()
        keyboard = KController()

        # time.sleep(5)
        time.sleep(2*speed)

        readFile = open('data/data_03', 'rb')
        npp_values = pickle.load(readFile)
        readFile.close()
        print("original_data => ", npp_values)

        pos_location_bar    =   [npp_values[0][0], npp_values[0][1]]
        pos_new_playlist    =   [npp_values[1][0], npp_values[1][1]]
        pos_playlist_title  =   [npp_values[2][0], npp_values[2][1]]
        pos_create_btn      =   [npp_values[3][0], npp_values[3][1]]

        readFile = open('data/data_04', 'rb')
        nvp_values = pickle.load(readFile)
        readFile.close()
        print("original_data => ", nvp_values)

        pos_title_edit_btn  =   [nvp_values[0][0], nvp_values[0][1]]
        pos_share_btn       =   [nvp_values[1][0], nvp_values[1][1]]
        pos_more_btn        =   [nvp_values[2][0], nvp_values[2][1]]
        pos_drop_plus_btn   =   [nvp_values[3][0], nvp_values[3][1]]
        pos_url_tab         =   [nvp_values[4][0], nvp_values[4][1]]
        pos_paste_url       =   [nvp_values[5][0], nvp_values[5][1]]
        pos_add_videos      =   [nvp_values[6][0], nvp_values[6][1]]

        for pl in dataVars:
            #new playlist
            mouse.position = (pos_location_bar[0], pos_location_bar[1])
            mouse.click(MButton.left, 1)
            
            # time.sleep(random.randint(2, 5))
            time.sleep(random.randint(speed, 2*speed))

            with keyboard.pressed(Key.ctrl):
                keyboard.press('a')
                keyboard.release('a')
            # time.sleep(1)
            # time.sleep(random.randint(1, 5))
            time.sleep(speed)

            keyboard.type('https://youtube.com/view_all_playlists')
            keyboard.press(Key.enter)
            
            # time.sleep(random.randint(10, 15))
            time.sleep(random.randint(5*speed, 5*speed+3))

            mouse.position = (pos_new_playlist[0], pos_new_playlist[1])
            mouse.click(MButton.left, 1)
            
            # time.sleep(random.randint(2, 5))
            time.sleep(random.randint(speed, speed * 2))
            mouse.position = (pos_playlist_title[0], pos_playlist_title[1])
            mouse.click(MButton.left, 1)
            keyboard.type(pl[0][0:5])
            
            # time.sleep(random.randint(1, 5))
            time.sleep(random.randint(speed, speed * 2))
            mouse.move(20, -30)
            mouse.click(MButton.left, 1)
            
            # time.sleep(random.randint(2, 5))
            time.sleep(random.randint(speed*2, speed*2+3))
            mouse.position = (pos_create_btn[0], pos_create_btn[1])
            mouse.click(MButton.left, 1)                
            
            # time.sleep(4)
            time.sleep(speed*2)

            #new video
            for i in range(len(pl[1])):
                if i == 0:
                    space_x = 0
                else:
                    space_x = int(pos_more_btn[0]) - int(pos_share_btn[0])
                print("space_x => ", space_x)
                print("pos_more_btn_x => ", pos_more_btn[0])
                print("pos_more_btn_x + space_x => ", str(int(pos_more_btn[0]) + space_x))
                print("pos_more_btn_y => ", pos_more_btn[1])

                mouse.position = (str(int(pos_more_btn[0]) + space_x), pos_more_btn[1])
                # time.sleep(2)
                time.sleep(speed)
                mouse.click(MButton.left, 1)
                # time.sleep(2)
                time.sleep(speed)
                print(" ________________________________________________________________ ")
                print(str(int(pos_drop_plus_btn[0]) + space_x), pos_drop_plus_btn[1])
                mouse.position = (str(int(pos_drop_plus_btn[0]) + space_x), pos_drop_plus_btn[1])
                mouse.click(MButton.left, 1)
                print(" __________________________________________ mouse position => ", mouse.position)
                # time.sleep(random.randint(5, 6))
                # time.sleep(random.randint(9, 10))
                time.sleep(random.randint(speed*3, speed*3+1))

                mouse.position = (pos_url_tab[0], pos_url_tab[1])
                mouse.click(MButton.left, 1)
                # time.sleep(1)
                time.sleep(speed)

                mouse.position = (pos_paste_url[0], pos_paste_url[1])
                mouse.click(MButton.left, 1)


                with keyboard.pressed(Key.ctrl):
                    keyboard.press('a')
                    keyboard.release('a')
                time.sleep(1)


                keyboard.type("https://www.youtube.com/watch?v=" + pl[1][i])
                # time.sleep(3)
                time.sleep(speed)

                mouse.position = (pos_add_videos[0], pos_add_videos[1])
                mouse.click(MButton.left, 1)

                # time.sleep(4)
                time.sleep(speed*2)

            mouse.position = (pos_title_edit_btn[0], pos_title_edit_btn[1])
            mouse.click(MButton.left, 1)
            time.sleep(1)

            with keyboard.pressed(Key.ctrl):
                keyboard.press('a')
                keyboard.release('a')
            time.sleep(1)

            keyboard.type(pl[0])
            keyboard.press(Key.enter)

            # time.sleep(random.randint(4, 6))
            time.sleep(random.randint(speed*2, speed*2+2))
        # google_browser.terminate()

        # keyboard.type('https://youtube.com/view_all_playlists')
        # keyboard.press(Key.enter)
        mouse.position = (pos_location_bar[0], pos_location_bar[1])
        mouse.click(MButton.left, 1)
        
        # time.sleep(random.randint(2, 5))
        time.sleep(random.randint(speed+1, speed+3))

        with keyboard.pressed(Key.ctrl):
            keyboard.press('a')
            keyboard.release('a')
        time.sleep(1)
        # time.sleep(random.randint(1, 5))
        # time.sleep(random.randint(speed, speed+2))

        keyboard.type('https://youtube.com/view_all_playlists')
        keyboard.press(Key.enter)