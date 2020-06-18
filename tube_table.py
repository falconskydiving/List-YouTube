try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter.ttk import Frame, Scrollbar, Combobox
from tkinter import Checkbutton, TOP, BOTH, Y
import pickle

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 300   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class ScrollableTableWidget(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frameTHeader = Frame(self)
        frameTHeader.pack(side=TOP, fill="x")

        frameTBody = Frame(self)
        frameTBody.pack(fill="both", expand=True)

        canvas_table_header = tk.Canvas(frameTHeader, height=20)
        self.scrollable_theader = Frame(canvas_table_header)
        
        self.scrollable_theader.bind(
            "<Configure>",
            lambda e: canvas_table_header.configure(
                scrollregion=canvas_table_header.bbox("all")
            )
        )

        canvas_table_body = tk.Canvas(frameTBody)
        def multiple_xview(*args):
            canvas_table_header.xview(*args)
            canvas_table_body.xview(*args)
        scrollbar_horizontal = Scrollbar(frameTBody, orient="horizontal", command=multiple_xview)
        scrollbar_vertical = Scrollbar(frameTBody, orient="vertical", command=canvas_table_body.yview)

        self.scrollable_frame = Frame(canvas_table_body)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_table_body.configure(
                scrollregion=canvas_table_body.bbox("all")
            )
        )

        canvas_table_header.create_window((0, 0), window=self.scrollable_theader, anchor="nw")
        canvas_table_header.configure(xscrollcommand=scrollbar_horizontal.set)
        canvas_table_body.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas_table_body.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)        
        
        scrollbar_vertical.pack(side="right", fill="y")
        scrollbar_horizontal.pack(side="bottom", fill="x")
        canvas_table_header.pack(fill="x", expand=True)
        canvas_table_body.pack( fill="both", expand=True)

class TubeTable(tk.Frame):
    def __init__(self, parent=None, row=0, column=0, rowspan=1, columnspan=1, padx1=0, padx2=0, pady1=0, pady2=0):
        tk.Frame.__init__(self)
        self.f = tk.Frame(parent, borderwidth=1, relief="solid",)
        self.f.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='wnes', padx=(padx1, padx2), pady=(pady1, pady2))
    def _create_tableview(self, dataColummns, index_position, is_selection_mode=False):
        # create the table and scrollbars
        self.datatbl = ScrollableTableWidget(self.f)
        self.datatbl.pack(side=TOP, fill=BOTH, expand=Y)
        self.dataColummns = dataColummns
        self.index_position = index_position
        self.widgets = []
        
        self.dataVars = []
        self.is_selection_mode = is_selection_mode
        self.index_selection = -1

        self.comboRegularGates = []

        for column in range(len(self.dataColummns)):
            label = tk.Label(self.datatbl.scrollable_theader, text=self.dataColummns[column][0])
            label.config(font=('Arial', 11), bg="#73b0fb", width=self.dataColummns[column][2])
            if self.dataColummns[column][1] == 'Label' or self.dataColummns[column][1] == 'Combobox':
                label.config(anchor="w")
            label.grid(row=0, column=column, sticky="nsew", padx=0, pady=1)
    def callBackFunc(self):
        print("+++++++++++-- handleCheckbuttonChange before +++++++++++")
        print(self.dataVars[0][0].get())
        print("+++++++++++ handleCheckbuttonChange after +++++++++++")
    def select_row(self, row):
        self.index_selection = row
        columns_cnt = len(self.dataColummns)
        
        print("~ clicked a row! ~", "-row index is ", row)
        index = 0
        for widget in self.datatbl.scrollable_frame.winfo_children():
            if self.dataColummns[index % columns_cnt][1] == 'Label':
                if (index >= row * columns_cnt) and (index < (row + 1) * columns_cnt):
                    for label in widget.winfo_children():
                        label.config(bg="#0080ff", fg="#ffffff")
                    # widget.config(bg="#0080ff", fg="#ffffff")
                else:
                    if (index//columns_cnt) % 2 == 1:
                        bg_color = "#e5e9e0"
                        for label in widget.winfo_children():
                            label.config(bg="#e5e9e0", fg="#000000")
                        # widget.config(bg="#e5e9e0", fg="#000000")
                    else:
                        bg_color = "#a8c9f2"
                        for label in widget.winfo_children():
                            label.config(bg="#a8c9f2", fg="#000000")
                        # widget.config(bg="#a8c9f2", fg="#000000")
            index = index + 1
    def refresh(self, dataVars):
        self.dataVars = dataVars
        print("--------------- len of datavars --------------------------------------------------> ", len(self.dataVars))
        if len(self.dataVars) == 0:
            self.index_selection = -1

        label_frame_arr = []

        for row in range(len(self.dataVars)):
            if row % 2 == 1:
                bg_color = "#e5e9e0"
            else:
                bg_color = "#a8c9f2"    
            print("--------------- dataColumns --------------- > ", self.dataColummns)
            for column in range(len(self.dataColummns)):
                column_var = column
                if column > self.index_position and self.index_position != -1:
                    column_var = column - 1
                print("--------------- column_var --------------- > ", column_var)
                print("--------------- index_position --------------- > ", self.index_position)
                if self.index_position == column:
                    label = tk.Label(self.datatbl.scrollable_frame, text=str(row+1), bg=bg_color, width=self.dataColummns[column][2], )                                    # borderwidth=2, relief="groove",
                    label.config(font=('Arial', 11))
                    label.grid(row=row, column=column, sticky="nsew", padx=0, pady=0)
                else:                    
                    if self.dataColummns[column][1] == 'Label':
                        label_frame_arr.append(  Frame(self.datatbl.scrollable_frame)  )
                        label_frame_arr[len(label_frame_arr)-1].grid(row=row, column=column, sticky="nsew")

                        label_frame_arr[len(label_frame_arr)-1].rowconfigure(0, weight=1)

                        label=tk.Label(label_frame_arr[len(label_frame_arr)-1], text=self.dataVars[row][column_var] , width=self.dataColummns[column][2]-1, bg=bg_color, fg="#000000", anchor="w")
                        label.config(font=('Arial', 11))
                        label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
                        
                        label_ttp = CreateToolTip(label, \
                        self.dataVars[row][column_var])

                        if self.is_selection_mode == True:
                            label.bind("<Button-1>",lambda e, row=row:self.select_row(row))
                        label=tk.Label(label_frame_arr[len(label_frame_arr)-1], text="" , width=1, bg=bg_color, fg="#000000", anchor="w")
                        label.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

                        # label_content = self.dataVars[row][column_var]
                        # label=tk.Label(label_frame_arr[len(label_frame_arr)-1], text=label_content , width=self.dataColummns[column][2], bg=bg_color, fg="#000000", anchor="w")
                        # label.config(font=('Arial', 11))
                        # label.grid(row=row, column=column, sticky="nsew", padx=0, pady=0)
                        # if self.is_selection_mode == True:
                        #     label.bind("<Button-1>",lambda e, row=row:self.select_row(row))
                    elif self.dataColummns[column][1] == 'CheckButton':
                        print(" ----------------- check button ---------------- ")
                        checkBtn = Checkbutton(self.datatbl.scrollable_frame, bg=bg_color, width=self.dataColummns[column][2]-2, var=self.dataVars[row][column_var], command=self.callBackFunc)
                        checkBtn.grid(row=row, column=column, sticky="")
                    elif self.dataColummns[column][1] == 'Combobox':
                        self.comboRegularGates.append(Combobox(self.datatbl.scrollable_frame, state="readonly",  width=self.dataColummns[column][2]))
                        k = len(self.comboRegularGates) - 1

                        readFile = open('data/data_05', 'rb')
                        self.comboRegularGates[k]['values'] = pickle.load(readFile)
                        readFile.close()
                        
                        self.comboRegularGates[k].current(self.dataVars[row][column_var])
                        self.comboRegularGates[k].grid(row=row, column=column)
                        self.comboRegularGates[k].bind("<<ComboboxSelected>>", lambda e, obj=self.comboRegularGates[k], row=row, column=column_var: self.updateCombobox(e, obj, row, column))
                    else:
                        pass
        print("when updating regular gates => ", self.index_selection)
        if self.index_selection > -1:
            self.select_row(self.index_selection)
    def _load_data(self, dataVars):
        self.clear_body()
        self.refresh(dataVars)
    def get_datacolumns(self):
        return self.dataColummns
    def get_data_vars(self):
        return self.dataVars
    def get_selected_data_vars(self):
        selectedDataVars = []
        column_var = -1
        for column in range(len(self.dataColummns)):
            if self.dataColummns[column][1] == 'CheckButton':
                if column > self.index_position and self.index_position != -1:
                    column_var = column - 1
                else:
                    column_var = column
                break        
        for row in self.dataVars:
            if row[column_var].get() == True:
                selectedDataVars.append(row)
        return selectedDataVars
    def delete_selected_data_vars(self):
        column_var = -1
        for column in range(len(self.dataColummns)):
            if self.dataColummns[column][1] == 'CheckButton':
                if column > self.index_position and self.index_position != -1:
                    column_var = column - 1
                else:
                    column_var = column
                break
        print("column_var", column_var)
        I = []
        for i in range(len(self.dataVars)):
            print("i=>", i)
            print(self.dataVars[i][column_var].get())

            if self.dataVars[i][column_var].get() == True:
                I.append(i)
        print(I)
        for i in sorted(I, reverse=True):
            del self.dataVars[i]

        self._load_data(self.dataVars)
    def select_all(self):
        print("Select all")    
        column_var = -1
        for column in range(len(self.dataColummns)):
            if self.dataColummns[column][1] == 'CheckButton':
                if column > self.index_position and self.index_position != -1:
                    column_var = column - 1
                else:
                    column_var = column
                break
        for i in range(len(self.dataVars)):
            print(i)
            self.dataVars[i][column_var].set(True)
    def unselect_all(self):
        print("Unselect all")    
        column_var = -1
        for column in range(len(self.dataColummns)):
            if self.dataColummns[column][1] == 'CheckButton':
                if column > self.index_position and self.index_position != -1:
                    column_var = column - 1
                else:
                    column_var = column
                break
        for i in range(len(self.dataVars)):
            print(i)
            self.dataVars[i][column_var].set(False)
    def clear_body(self):
        print("---------------- clear body -------------")
        self.dataVars = []
        self.comboRegularGates = []
        
        for widget in self.datatbl.scrollable_frame.winfo_children():
            widget.destroy()
    def move_up_selection(self):
        print("++++++++++++++++++ move_up_selection +++++++++++++++++++++++")
        print("BEFORE=>", self.dataVars)
        if self.index_selection > 0:
            self.dataVars[self.index_selection], self.dataVars[self.index_selection-1] = self.dataVars[self.index_selection-1], self.dataVars[self.index_selection]
            self._load_data(self.dataVars)
            self.select_row(self.index_selection - 1)
        print("AFTER=>", self.dataVars)
    def move_down_selection(self):
        if self.index_selection >= 0 and self.index_selection < len(self.dataVars)-1:
            self.dataVars[self.index_selection], self.dataVars[self.index_selection+1] = self.dataVars[self.index_selection+1], self.dataVars[self.index_selection]
            self._load_data(self.dataVars)
            self.select_row(self.index_selection + 1)
    def updateCombobox(self, event, combo_obj, row, column_var):
        self.dataVars[row][column_var] = combo_obj.current()
    def delete_selection(self):
        if self.index_selection >= 0:
            del self.dataVars[self.index_selection]
            self.index_selection = -1
            self._load_data(self.dataVars)