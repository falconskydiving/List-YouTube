try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from tkinter.ttk import Button, Entry
from tkcalendar import DateEntry
from timepicker import TimePicker
import pickle

from tube_table import TubeTable

class ReservationListWindow:
    count = 0
    def __init__(self, parent):
        ReservationListWindow.count = ReservationListWindow.count + 1

        self.reservationsListWindow =  tk.Toplevel(parent)
        self.reservationsListWindow.title("予約リスト")
        self.reservationsListWindow.protocol("WM_DELETE_WINDOW", self.close_window)

        width_of_window = 500
        height_of_window = 350
        screen_width = self.reservationsListWindow.winfo_screenwidth()
        screen_height = self.reservationsListWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.reservationsListWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.reservationsListWindow.columnconfigure(0, weight=1)
        self.reservationsListWindow.columnconfigure(1, weight=1)
        self.reservationsListWindow.rowconfigure(0, weight=1)

        readFile = open('data/data_06', 'rb')
        values_reservation = pickle.load(readFile)
        readFile.close()

        self.dataVars = []
        for row in values_reservation:
            # print("row =========================== > ", row)
            ckValue =  tk.BooleanVar()
            ckValue.set(False)
            self.dataVars.append([ckValue, str(row[1]) + " " + str(row[2]) + ":" + str(row[3]), row[0]])
        
    def _create_windowview(self):
        self.reservationsListTable = TubeTable(self.reservationsListWindow, 0, 0, 3, 1)
        dataColummns = [['選択', 'CheckButton', 8], ['実行日時', 'Label', 15], ['予約名', 'Label', 20]]
        self.reservationsListTable._create_tableview(dataColummns, -1, True)
        self.reservationsListTable._load_data(self.dataVars)

        btnRLFrame =  tk.Frame(self.reservationsListWindow)
        btnRLFrame.grid(row=0, column=1, sticky='wn')

        btn_del_seleced_reservations = Button(btnRLFrame, text = "選択行削除",  command = self.del_selection_reservations)
        btn_del_seleced_reservations.grid(row=0, column=0, padx=5, pady=(5, 0), ipady=3, sticky='we')
        
        btn_del_all_reservations = Button(btnRLFrame, text = "全削除", command = self.del_all_reservations)
        btn_del_all_reservations.grid(row=1, column=0, pady=(10, 30), padx=5, ipady=3, sticky='we')

        btn_close_rl = Button(btnRLFrame, text = "戻る", command = self.close_window)
        btn_close_rl.grid(row=2, column=0, sticky='we', padx=5)

    def del_selection_reservations(self):
        readFile = open('data/data_06', 'rb')
        values_reservation = pickle.load(readFile)
        readFile.close()

        self.dataVars = []
        for i in range(len(self.reservationsListTable.dataVars)):
            if self.reservationsListTable.dataVars[i][0].get() == False:
                self.dataVars.append(values_reservation[i])

        writeFile = open('data/data_06', 'wb')
        pickle.dump(self.dataVars, writeFile)
        writeFile.close()
        
        self.reservationsListTable.delete_selected_data_vars()
    def del_all_reservations(self):
        self.reservationsListTable.clear_body()
        self.dataVars = []
        writeFile = open('data/data_06', 'wb')
        pickle.dump(self.dataVars, writeFile)
        writeFile.close()
    def close_window(self):
        ReservationListWindow.count = ReservationListWindow.count - 1
        self.reservationsListWindow.destroy()