import Tkinter as tk
from Tkinter import BOTH, END, LEFT, ACTIVE
#import matplotlib
from matplotlib import pyplot as plt
#from matplotlib import style
#import Vocoder as vc
#import thinkdsp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import reldat
#import winsound

county_names = reldat.counties_names()

HEADER_FONT = ("Helvetica",24)
#MIN_HEIGHT = 600
#MIN_WIDTH  = 800
#style.use('ggplot')
  
def callback(val):
    print val
  

class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        county_list = []
        chem_list = []
        well_list = []
        global county_list
        global chem_list
        global well_list
        #Don't allow gui to be resized
        self.resizable(False,False)
        self.title('Geotracker GAMA Chemical Analyzer')
        #self.iconbitmap(self, 'Penguin.xbm')
        
        #Create frame for main window
        container = tk.Frame(self)
        container.pack(side=LEFT, fill="both", expand="True")
        
        #Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Create parameters frame
        self.parameters= tk.Frame(container)
        self.parameters.grid(row=0,column=0,sticky="NEWS",padx = 0)
    
        #Create plotarea frame
        self.plot_area = tk.Frame(container)
        self.plot_area.grid(row=0,column=1,sticky="NEWS",padx = 0)
        
        self.plot_select = tk.Frame(self.parameters)
        self.counties_select = tk.Frame(self.parameters)
        self.chem_select = tk.Frame(self.parameters)
        self.dates_select = tk.Frame(self.parameters)
        self.well_select = tk.Frame(self.parameters)

        self.plot_select.grid(row=0)
        self.counties_select.grid(row=1)
        self.chem_select.grid(row=2)
        self.dates_select.grid(row=3)
        self.well_select.grid(row=4)

        self.plot_var = tk.IntVar()
        self.plot_var.set(1)

        plot_select_label = tk.Label(self.plot_select, text="Analysis Type:",font=("Helvetica",16))
        plot_select_label.grid(row=0, column= 0, pady=5, sticky = "w")

        self.scatter_plot = tk.Radiobutton(self.plot_select,text="Scatter Plot",variable=self.plot_var,command=callback(self.plot_var.get()),value=1)#.pack()
        self.scatter_plot.grid(row=1, pady = 2,columnspan = 3, sticky = "w")

        self.tsa_plot = tk.Radiobutton(self.plot_select,text="Time Series Analysis",variable=self.plot_var,command=callback(self.plot_var.get()),value=2)#.pack()
        self.tsa_plot.grid(row=2, pady = 2,columnspan = 3, sticky = "w")

        self.geo_plot = tk.Radiobutton(self.plot_select,text="Geographic Display",variable=self.plot_var,command=callback(self.plot_var.get()),value=3)#.pack()
        self.geo_plot.grid(row=3, pady = 2,columnspan = 3, sticky = "w")

        #County Selection Menu
        county_select_label = tk.Label(self.counties_select, text="Select Counties:",font=("Helvetica",16))
        county_select_label.grid(row=0, column= 0, pady=2, sticky = "w")
        self.counties_search_var = tk.StringVar()
        self.counties_search_var.trace("w", lambda name, index, mode: self.counties_update_list())
        self.counties_entry = tk.Entry(self.counties_select, textvariable=self.counties_search_var, width=13)
        self.counties_lbox = tk.Listbox(self.counties_select, width=25, height=3)
        self.counties_nbox = tk.Listbox(self.counties_select, width=25, height=3)
        self.counties_lbox.bind("<Double-Button-1>", self.add_county)
        self.counties_nbox.bind("<Double-Button-1>", self.remove_county)

        self.counties_entry.grid(row=1, column=0, padx=2, pady=3)
        self.counties_lbox.grid(row=2, column=0, padx=2, pady=3)
        self.counties_nbox.grid(row=3, column=0, padx=2, pady=3)
        
        self.counties_update_list()

        #Chemicals Selection Menu
        chem_select_label = tk.Label(self.chem_select, text="Select Chemicals:",font=("Helvetica",16))
        chem_select_label.grid(row=0, column= 0, pady=2, sticky = "w")
        self.chem_search_var = tk.StringVar()
        self.chem_search_var.trace("w", lambda name, index, mode: self.chem_update_list())
        self.chem_entry = tk.Entry(self.chem_select, textvariable=self.chem_search_var, width=13)
        self.chem_lbox = tk.Listbox(self.chem_select, width=25, height=3)
        self.chem_nbox = tk.Listbox(self.chem_select, width=25, height=3)
        self.chem_lbox.bind("<Double-Button-1>", self.add_chem)
        self.chem_nbox.bind("<Double-Button-1>", self.remove_chem)

        self.chem_entry.grid(row=1, column=0, padx=2, pady=3)
        self.chem_lbox.grid(row=2, column=0, padx=2, pady=3)
        self.chem_nbox.grid(row=3, column=0, padx=2, pady=3)
        
        self.chem_update_list()

        # Dates Selection Menu
        date_select_label = tk.Label(self.dates_select, text="Select Start and End Dates:",font=("Helvetica",16))
        date_select_label.grid(row=0, column= 0, pady=2, sticky = "w")

        self.dates_search_var = tk.StringVar()
        self.dates_search_var.trace("w", lambda name, index, mode: self.dates_update_list())
        self.dates_entry = tk.Entry(self.dates_select, textvariable=self.dates_search_var, width=13)
        self.dates_lbox = tk.Listbox(self.dates_select, width=25, height=1)
        self.dates_sbox = tk.Listbox(self.dates_select, width=25, height=1)
        self.dates_ebox = tk.Listbox(self.dates_select, width=25, height=1)
        start_date_button = tk.Button(self.dates_select, height = 1, text="Start Date", command = lambda: self.set_start_date())
        end_date_button = tk.Button(self.dates_select, height = 1, text="End Date", command = lambda: self.set_end_date())
        start_date_button.grid(row=3, column=1, pady = 3)
        end_date_button.grid(row=4, column=1, pady = 3)
        self.dates_entry.grid(row=1, column=0, padx=2, pady=3)
        self.dates_lbox.grid(row=2, column=0, padx=2, pady=3)
        self.dates_sbox.grid(row=3, column=0, padx=2, pady=3)
        self.dates_ebox.grid(row=4, column=0, padx=2, pady=3)
        
        self.dates_update_list()

        # Wells Selection Menu
        well_select_label = tk.Label(self.well_select, text="Select Wells:",font=("Helvetica",16))
        well_select_label.grid(row=0, column= 0, pady=5, sticky = "w")
        self.well_search_var = tk.StringVar()
        self.well_search_var.trace("w", lambda name, index, mode: self.well_update_list())
        self.well_entry = tk.Entry(self.well_select, textvariable=self.well_search_var, width=13)
        self.well_lbox = tk.Listbox(self.well_select, width=25, height=3)
        self.well_nbox = tk.Listbox(self.well_select, width=25, height=3)
        self.well_lbox.bind("<Double-Button-1>", self.add_well)
        self.well_nbox.bind("<Double-Button-1>", self.remove_well)

        self.well_entry.grid(row=1, column=0, padx=2, pady=3)
        self.well_lbox.grid(row=2, column=0, padx=2, pady=3)
        self.well_nbox.grid(row=3, column=0, padx=2, pady=3)
        analyze_button = tk.Button(self.well_select, height = 1, text="ANALYZE", command = lambda: self.lawl())
        analyze_button.grid(row=4, column=0, padx=2, pady=3)
        self.well_update_list()

    def lawl(self):
        print (county_list,chem_list,well_list)

    def set_start_date(self):
        self.dates_sbox.delete(0, END)
        self.dates_sbox.insert(0,self.dates_lbox.get(ACTIVE))

    def set_end_date(self):
        self.dates_ebox.delete(0, END)
        self.dates_ebox.insert(0,self.dates_lbox.get(ACTIVE))

    def add_well(self,event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        if value not in well_list:
            well_list.append(value)
            self.well_nbox.insert(END,value)

    def remove_well(self,event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        self.well_nbox.delete(selection)
        well_list.remove(value)

    def add_chem(self,event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        if value not in chem_list:
            chem_list.append(value)
            self.chem_nbox.insert(END,value)

    def remove_chem(self,event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        self.chem_nbox.delete(selection)
        chem_list.remove(value)

    def add_county(self,event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        if value not in county_list:
            county_list.append(value)
            self.counties_nbox.insert(END,value)

    def remove_county(self,event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        self.counties_nbox.delete(selection)
        county_list.remove(value)

    def counties_update_list(self):

        search_term = self.counties_search_var.get()
     
        # Just a generic list to populate the listbox
        lbox_list = county_names

        self.counties_lbox.delete(0, END)
     
        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.counties_lbox.insert(END, item)

    def chem_update_list(self):

        search_term = self.chem_search_var.get()
     
        # Just a generic list to populate the listbox
        lbox_list = []
        for x in county_list:
            lbox_list = list(set(lbox_list) | set(reldat.county_chems(x)))

        self.chem_lbox.delete(0, END)
     
        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.chem_lbox.insert(END, item)

    def well_update_list(self):

        search_term = self.well_search_var.get()
     
        # Just a generic list to populate the listbox
        lbox_list = []
        for x in county_list:
            lbox_list = list(set(lbox_list) | set(reldat.county_wells(x)))

        self.well_lbox.delete(0, END)
     
        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.well_lbox.insert(END, item)

    def dates_update_list(self):

        search_term = self.dates_search_var.get()
     
        # Just a generic list to populate the listbox
        lbox_list = []
        for x in county_list:
            lbox_list = list(set(lbox_list) | set(reldat.county_dates(x)))

        self.dates_lbox.delete(0, END)
     
        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.dates_lbox.insert(END, item)








# class Interface(tk.Frame):
    
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self,parent, highlightthickness=0)
#         label = tk.Label(self, text="Interface",font=HEADER_FONT)
#         label.grid(row=0)
#         self.gui = controller
        
#         #INPUT STUFF
#         inputs = tk.Frame(self, height = 150, width = 150)
#         inputs.grid(row=1,pady=50)     

#         input_play = tk.BooleanVar()   
#         input_play.set(False)
        
#         play_input = tk.Button(inputs,height = 2, text="Press to Play",
#                                command = lambda: play_audio(self.gui.vocoder.input))
#         play_input.grid(row=0, pady = 15)
        
#         record_input = tk.Button(inputs,height = 2, text="Press to Record",
#                                  command = lambda: self.record_audio(rec_time.get()))
#         record_input.grid(row=2, pady = 15)
        
#         rec_time = tk.IntVar()
#         rec_time.set(6)        
        
#         input_label = tk.Label(inputs, text="Rec Time:")
#         input_label.grid(row=1, column= 0, pady=5, sticky = "w")
#         rec_timer = tk.Spinbox(inputs,width = 2,wrap = True, 
#                                from_ = 1,to=10,
#                                textvariable = rec_time,
#                                command = lambda: callback(rec_time.get()))
#         rec_timer.delete(0,tk.END)
#         rec_timer.insert(0,6)
#         rec_timer.grid(row=1,column = 1, pady=5, sticky = "w")
        
#         #OUTPUT STUFF
#         outputs = tk.Canvas(self, height = 150, width = 150)
#         outputs.grid(row=3,pady=70)
        
#         output_play = tk.BooleanVar()   
#         output_play.set(False)    
        
#         volume = tk.IntVar()   
#         volume.set(5)
        
#         play_output = tk.Button(outputs,height = 2, text="Press to Play",
#                                 command = lambda: play_audio(self.gui.vocoder.output))
#         play_output.grid(row=1, column=0, pady = 15)
        
#         vocode = tk.Button(outputs,height = 2, text="Press to Vocode",
#                                 command = lambda: self.vocodestuff())
#         vocode.grid(row=0, column=0, pady = 15)
        
# #        volume_output = tk.Scale(outputs,label = "Happiness Factor",variable = volume,
# #                                 from_ = 10,to=0, 
# #                                 command = lambda volume: callback(volume))
# #        volume_output.set(5)
# #        volume_output.grid(row=0, column=0, pady=15)
        
#         #Channel stuff
#         channels = tk.Frame(self, height = 450, width = 150)
#         channels.grid(row=2, pady=0)
#         channel_options = ('Sawtooth', 'Sin', 'Cos',
#                            'Square', 'Triangle', 'Parabolic') 
#         #Channel 1 Stuff
#         ch1 = tk.Canvas(channels,height = 150, width = 150)
#         ch1.grid(row=1, pady=55)
# #        
# #        ch1_var = tk.BooleanVar()
# #        ch1_var.set(False)
        
#         ch1_freq = tk.IntVar()
#         ch1_freq.set(440)
        
#         ch1_wave = tk.StringVar()
#         ch1_wave.set(channel_options[0])
          
#         ch1_dropdown = tk.OptionMenu(ch1,ch1_wave,*channel_options,
#                                      command = lambda ch1_wave: self.update_modulator(ch1_wave, ch1_freq.get()))
#         ch1_dropdown.grid(row=0, columnspan = 1, sticky = "w")
        
#         ch1_label = tk.Label(ch1, text="Pitch:")
#         ch1_label.grid(row=0, column= 1, pady=20, sticky = "w")
#         ch1_pitch = tk.Spinbox(ch1,width = 4,wrap = True, 
#                                from_ = 100,to=1000,
#                                textvariable = ch1_freq,
#                                command = lambda: self.update_modulator(ch1_wave.get(), ch1_freq.get()))
#         ch1_pitch.delete(0,tk.END)
#         ch1_pitch.insert(0,440)
#         ch1_pitch.grid(row=0, column =2, pady=5, sticky = "w")
        
#        # ch1_toggle = tk.Checkbutton(ch1,    
#        #                             text="Toggle Channel 1 Modulation",
#        #                             variable=ch1_var,
#        #                             command = lambda: callback(ch1_var.get()))
#        # ch1_toggle.grid(row=1, pady = 5,columnspan = 3, sticky = "w")
                
# class Waves(tk.Frame):
    
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self,parent, highlightthickness=0)
#         label = tk.Label(self, text="Waves",font=HEADER_FONT)
#         label.grid(row=0)
#         self.gui = controller
        
#         #INPUT STUFF
#         input_fig = plt.figure(figsize=(6.5,2.5), dpi=100)
#         input_fig.subplots_adjust(left=0.11, right=0.96,
#                                    top=0.95, bottom=0.11,
#                                    wspace = 0.2, hspace = 0.43)
        
#         self.input_wave = input_fig.add_subplot(211)        
#         self.input_spec = input_fig.add_subplot(212)
        
#         self.input_plot = FigureCanvasTkAgg(input_fig, master=self)
#         self.input_plot._tkcanvas.config(highlightthickness=0)
#         self.input_plot.show()
#         self.input_plot.get_tk_widget().grid(row=1)           
                
#         #CHANNEL STUFF
#         channel_fig = plt.figure(figsize=(6.5,2.5), dpi=100)
#         channel_fig.subplots_adjust(left=0.11, right=0.96,
#                                    top=0.95, bottom=0.11,
#                                    wspace = 0.2, hspace = 0.43)
        
#         self.channel_wave = channel_fig.add_subplot(211)
#         self.channel_spec = channel_fig.add_subplot(212)
        
#         self.channel_plot = FigureCanvasTkAgg(channel_fig, master=self)
#         self.channel_plot._tkcanvas.config(highlightthickness=0)
#         self.channel_plot.show()
#         self.channel_plot.get_tk_widget().grid(row=2)
        
#         #OUTPUT STUFF
#         output_fig = plt.figure(figsize=(6.5,2.5), dpi=100)
#         output_fig.subplots_adjust(left=0.11, right=0.96,
#                                    top=0.95, bottom=0.11,
#                                    wspace = 0.2, hspace = 0.43)        
        
#         self.output_wave = output_fig.add_subplot(211)
#         self.output_spec = output_fig.add_subplot(212)
        
#         self.output_plot = FigureCanvasTkAgg(output_fig, master=self)
#         self.output_plot._tkcanvas.config(highlightthickness=0)
#         self.output_plot.show()
#         self.output_plot.get_tk_widget().grid(row=3)
        
#         self.update()
# #        toolbar = NavigationToolbar2TkAgg( input_plot, self )
# #        toolbar.update()
# #        toolbar.grid(row=5,sticky='W')
    
#     def update(self):
#         self.input_wave.clear()
#         self.input_spec.clear()
#         self.input_wave.plot(self.gui.vocoder.input.ts,self.gui.vocoder.input.ys)
#         self.input_spec.plot(self.gui.vocoder.input_spec.fs,self.gui.vocoder.input_spec.amps)
#         self.input_plot.show()
        
#         self.channel_wave.clear()
#         self.channel_spec.clear()
#         channel_wave_seg = self.gui.vocoder.channel.segment(duration=(1.0/self.gui.vocoder.pitch)*5)
#         self.channel_wave.plot(channel_wave_seg.ts,channel_wave_seg.ys)
#         self.channel_spec.plot(self.gui.vocoder.channel_spec.fs,self.gui.vocoder.channel_spec.amps)   
#         self.channel_plot.show()
        
#         self.output_wave.clear()
#         self.output_spec.clear()
#         self.output_wave.plot(self.gui.vocoder.output.ts,self.gui.vocoder.output.ys)
#         self.output_spec.plot(self.gui.vocoder.output_spec.fs,self.gui.vocoder.output_spec.amps)
#         self.output_plot.show()
        
# if __name__ == "__main__":
#     #mod = C.Model()
#     #con = C.Controller(mod)
#     app = gui()
    
#     app.mainloop()

app = gui()
print reldat.counties
app.mainloop()