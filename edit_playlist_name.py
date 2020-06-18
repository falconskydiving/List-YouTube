try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import END, Checkbutton
from tkinter.ttk import Button, Entry, Combobox
import pickle

from regular_gate_list import RegularGateListWindow 

class EditPlaylistNameWindow:
    count = 0
    def __init__(self, parent):

        EditPlaylistNameWindow.count = EditPlaylistNameWindow.count + 1

        self.ckValue_apply_only_reguar_gate = tk.BooleanVar()
        self.ckValue_apply_only_reguar_gate.set(False)

        self.rbPlayListNameUpdateModeValue = tk.IntVar()
        self.rbPlayListNameUpdateModeValue.set(1)

        self.editPlaylistNameWindow = tk.Toplevel(parent)
        self.editPlaylistNameWindow.title("再生リスト名変更")
        self.editPlaylistNameWindow.resizable(0,0)

        self.editPlaylistNameWindow.protocol("WM_DELETE_WINDOW", self.close_window)
        # playlistWindow.wm_attributes("-disabled", True)

        width_of_window = 450
        height_of_window = 200
        screen_width = self.editPlaylistNameWindow.winfo_screenwidth()
        screen_height = self.editPlaylistNameWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.editPlaylistNameWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        # saveOwnUrlListWindow.wm_attributes("-topmost", 1)

        self.editPlaylistNameWindow.columnconfigure(0, weight=1)
        self.editPlaylistNameWindow.columnconfigure(1, weight=3)
        self.editPlaylistNameWindow.columnconfigure(2, weight=3)
        self.editPlaylistNameWindow.columnconfigure(3, weight=3)
        self.editPlaylistNameWindow.columnconfigure(4, weight=1)
        self.editPlaylistNameWindow.rowconfigure(0, weight=1)
        self.editPlaylistNameWindow.rowconfigure(1, weight=1)
        self.editPlaylistNameWindow.rowconfigure(2, weight=1)
        self.editPlaylistNameWindow.rowconfigure(3, weight=3)

    def _create_windowview(self, parent, playlistTable):
        label = tk.Label(self.editPlaylistNameWindow, text="リスト名 :")
        label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 10))

        self.entry_list_name = Entry(self.editPlaylistNameWindow)
        self.entry_list_name.grid( row=0, column=1, columnspan=3, sticky="we")        

        label = tk.Label(self.editPlaylistNameWindow, text="定型文 :")
        label.grid(row=1, column=0, sticky="w", padx=10)        
        
        self.cb_regular_gate = Combobox(self.editPlaylistNameWindow, state="readonly")
        self.refresh_cb_regular_gate()        
        self.cb_regular_gate.current(0)
        self.cb_regular_gate.grid( row=1, column=1, columnspan=3, sticky="wens")
        
        self.set_entry_list_name(playlistTable)

        settingBtnFrame = tk.Frame(self.editPlaylistNameWindow)
        settingBtnFrame.grid(row=0, column=4, rowspan=3, sticky='ens')
        
        btn_setting_playlist = Button(settingBtnFrame, text="設定", command=lambda: self.update_playlist_name(playlistTable))
        btn_setting_playlist.grid(sticky='wens', row=0, column=0, padx=5, pady=(10, 10), ipadx=5, ipady=3)

        btn_cancel = Button(settingBtnFrame, text="キャンセル", command=self.close_window)
        btn_cancel.grid(sticky='wens', row=1, column=0, padx=5, ipadx=5, ipady=3)

        regularGateFrame = tk.Frame(self.editPlaylistNameWindow)
        regularGateFrame.grid(row=2, column=0, sticky='wens')

        ck_apply_only_regular_gate = Checkbutton(regularGateFrame, variable=self.ckValue_apply_only_reguar_gate, text="定型文のみ変更", onvalue=True, offvalue=False)
        ck_apply_only_regular_gate.deselect()
        ck_apply_only_regular_gate.grid(row=0, column=0, padx=(6, 0), pady=(10, 0), sticky="")

        btn_update_regular_gates = Button(regularGateFrame, text = "定型文編集", command=lambda: self.regular_gate_list(parent, playlistTable))
        btn_update_regular_gates.grid(row=1, column=0, padx=(10, 0), pady=(5, 0), ipady=3, sticky='we')

        updateModeFrame = tk.LabelFrame(self.editPlaylistNameWindow, text='変更モード')
        updateModeFrame.grid(row=2, column=2, columnspan=2, rowspan=2, sticky='wens', padx=(10, 0), pady=10)
        
        rb_selection_update = tk.Radiobutton(updateModeFrame, text="選択行のみ", value=1, variable=self.rbPlayListNameUpdateModeValue)
        rb_samename_update = tk.Radiobutton(updateModeFrame, text="同ー名のみ", value=2, variable=self.rbPlayListNameUpdateModeValue)
        rb_all_update = tk.Radiobutton(updateModeFrame, text="全て", value=3, variable=self.rbPlayListNameUpdateModeValue)
        rb_selection_update.grid(row=0, column=0, sticky='w', padx=10, pady=(10, 0))
        rb_samename_update.grid(row=1, column=0, sticky='w', padx=10, pady=(5, 0))
        rb_all_update.grid(row=2, column=0, sticky='w', padx=10, pady=(5, 0))

    def set_entry_list_name(self, playlistTable):
        print(playlistTable.index_selection)
        if playlistTable.index_selection != -1:
            playlist_name = playlistTable.dataVars[playlistTable.index_selection][2]
            self.entry_list_name.delete(0, END)
            self.entry_list_name.insert(0, playlist_name)
            self.cb_regular_gate.current(playlistTable.dataVars[playlistTable.index_selection][3])    
    def update_playlist_name(self, playlistTable):
        print("self.ckValue_apply_only_reguar_gate", self.ckValue_apply_only_reguar_gate.get())
        if len(playlistTable.dataVars) > 0:
            if self.rbPlayListNameUpdateModeValue.get() == 1:
                if self.ckValue_apply_only_reguar_gate.get() == False:
                    playlistTable.dataVars[playlistTable.index_selection][2] = self.entry_list_name.get()
                playlistTable.dataVars[playlistTable.index_selection][3] = self.cb_regular_gate.current()
            elif self.rbPlayListNameUpdateModeValue.get() == 2:
                playlist_name_to_update = playlistTable.dataVars[playlistTable.index_selection][2]
                print("playlist_name_to_update => ", playlist_name_to_update)

                for i in range(len(playlistTable.dataVars)):
                    print("i => ", i)
                    print(i," th list name is =>", playlistTable.dataVars[i][2])
                    if playlist_name_to_update == playlistTable.dataVars[i][2]:
                        if self.ckValue_apply_only_reguar_gate.get() == False:
                            playlistTable.dataVars[i][2] = self.entry_list_name.get()
                        playlistTable.dataVars[i][3] = self.cb_regular_gate.current()
            elif self.rbPlayListNameUpdateModeValue.get() == 3:
                for i in range(len(playlistTable.dataVars)):
                    if self.ckValue_apply_only_reguar_gate.get() == False:
                        playlistTable.dataVars[i][2] = self.entry_list_name.get()
                    playlistTable.dataVars[i][3] = self.cb_regular_gate.current()
            playlistTable._load_data(playlistTable.dataVars)
            self.close_window()
        else:
            print("no playlist item!")
    def regular_gate_list(self, parent, playlist_table):
        if RegularGateListWindow.count == 0:
            regular_gate_list = RegularGateListWindow(self, parent, playlist_table)
    def refresh_cb_regular_gate(self):
        readFile = open('data/data_05', 'rb')
        self.cb_regular_gate['values'] = pickle.load(readFile)
        self.cb_regular_gate.current(0)
        readFile.close()
    def close_window(self):
        # playlistWindow.wm_attributes("-disabled", False)
        EditPlaylistNameWindow.count = EditPlaylistNameWindow.count - 1
        self.editPlaylistNameWindow.destroy()