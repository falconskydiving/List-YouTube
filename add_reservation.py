try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from tkinter.ttk import Button, Entry
from tkcalendar import DateEntry
from babel.numbers import *
from timepicker import TimePicker
import pickle

class AddReservationWindow:
    count = 0
    def __init__(self, parent):
        AddReservationWindow.count = AddReservationWindow.count + 1

        self.addReservationWindow = tk.Toplevel(parent)
        self.addReservationWindow.title("予約リストに追加")
        self.addReservationWindow.resizable(0,0)
        self.addReservationWindow.protocol("WM_DELETE_WINDOW", self.close_window)
        # playlistWindow.wm_attributes("-disabled", True)

        width_of_window = 450
        height_of_window = 150
        screen_width = self.addReservationWindow.winfo_screenwidth()
        screen_height = self.addReservationWindow.winfo_screenheight()
        x_coordinate = (screen_width/2) - (width_of_window/2)
        y_coordinate = (screen_height/2) - (height_of_window/2)

        self.addReservationWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        
        self.addReservationWindow.columnconfigure(0, weight=3)
        self.addReservationWindow.columnconfigure(1, weight=1)
        self.addReservationWindow.columnconfigure(2, weight=3)
        self.addReservationWindow.columnconfigure(3, weight=3)
        self.addReservationWindow.columnconfigure(4, weight=3)
        self.addReservationWindow.rowconfigure(0, weight=1)
        self.addReservationWindow.rowconfigure(1, weight=1)
        self.addReservationWindow.rowconfigure(2, weight=1)
        self.addReservationWindow.rowconfigure(3, weight=3)

    def _create_windowview(self, dataVars):
        self.dataVars = dataVars
        label =  tk.Label(self.addReservationWindow, text="予約名:")
        label.grid(row=0, column=0, sticky="wn", padx=10, pady=(12, 0))

        self.entry_reservation_name =  Entry(self.addReservationWindow)
        self.entry_reservation_name.grid( row=0, column=1, columnspan=3, sticky="wne", pady=(12, 0))        

        label =  tk.Label(self.addReservationWindow, text="予約日時:")
        label.grid(row=1, column=0, sticky="wn", padx=10)
        
        self.cal_reservation_date = DateEntry(self.addReservationWindow, width=12, background='darkblue', foreground='white', borderwidth=2, year=2020)
        self.cal_reservation_date.grid( row=1, column=1, sticky="wne")

        self.tp_reservation_time = TimePicker(self.addReservationWindow, )
        self.tp_reservation_time.grid( row=1, column=2, columnspan=3, sticky="wns")
        
        addBtnFrame =  tk.Frame(self.addReservationWindow)
        addBtnFrame.grid(row=0, column=4, rowspan=3, sticky='ens',)

        btn_add_reservation = Button(addBtnFrame, text="登録", command=self.add_reservation)
        btn_add_reservation.grid(sticky='wens', row=0, column=0, padx=5, pady=(10, 10), ipadx=5, ipady=3)

        btn_cancel_ar = Button(addBtnFrame, text="キャンセル", command=self.close_window)
        btn_cancel_ar.grid(sticky='wens', row=1, column=0, padx=5, ipadx=5, ipady=3)    
    def add_reservation(self):
        # playlistWindow.wm_attributes("-disabled", False)
        if len(self.dataVars) > 0:
            readFile = open('data/data_06', 'rb')
            values_reservation = pickle.load(readFile)
            readFile.close()

            reservation_name = self.entry_reservation_name.get()
            reservation_date = self.cal_reservation_date.get_date()
            reservation_hour = self.tp_reservation_time.hour.get()
            reservation_min = self.tp_reservation_time.min.get()
            reservation_data = self.dataVars
            print("reservation_name", reservation_name)
            new_reservation = [reservation_name, reservation_date, reservation_hour, reservation_min, reservation_data]

            values_reservation.append(new_reservation)
            writeFile = open('data/data_06', 'wb')

            pickle.dump(values_reservation, writeFile)
            writeFile.close()

            self.close_window()
        else:
            print("No playlist")
            tk.messagebox.showwarning("List Tube", "再生リストテーブルにデータがありません。")
    def close_window(self):
        # playlistWindow.wm_attributes("-disabled", False)
        AddReservationWindow.count = AddReservationWindow.count - 1
        self.addReservationWindow.destroy()