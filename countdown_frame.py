# Frame to track countdown timer
class CountdownFrame(wx.Frame):
    # def __init__(self, duration):
    def __init__(self, values):
        # Variables that determine if time values are zero
        self.second_zero = False
        self.minute_zero = False
        self.hour_zero = False
        
        # Time values
        self.hours = int(values["hours"])
        self.minutes = int(values["minutes"])
        self.seconds = int(values["seconds"])
    
        super().__init__(parent=None, title='Countdown Frame')
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.create_labels()
        
        # Creating a button to start playing audio. https://stackoverflow.com/questions/34266964/how-can-i-prevent-gui-freezing-in-wxpython
        self.addButton = wx.Button(self.panel, -1, "Start", style=wx.BU_EXACTFIT)
        self.main_sizer.Add(self.addButton, 0, wx.ALL | wx.CENTER, 5)
        # self.addButton.Bind(wx.EVT_BUTTON, self.song_thread)
        
        self.countdown_timer()
        self.panel.SetSizer(self.main_sizer)
        self.Show()
        
    # Creating the time labels
    # Currently labels are overlapping each other
    def create_labels(self):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Hours label
        self.hours_label = wx.StaticText(self.panel, label=str(self.hours), size=(50, -1))
        row_sizer.Add(self.hours_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Minutes label
        self.minutes_label = wx.StaticText(self.panel, label=str(self.minutes), size=(50, -1))
        row_sizer.Add(self.minutes_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Seconds label
        self.seconds_label = wx.StaticText(self.panel, label=str(self.seconds), size=(50, -1))
        row_sizer.Add(self.seconds_label, 0, wx.ALL | wx.CENTER, 5)
        
        self.main_sizer.Add(row_sizer)
        
    # Creating countdown timer
    def countdown_timer(self):
        self.seconds_update()
    
    def seconds_update(self):
        print(f'Seconds: {self.seconds}')
        self.seconds_label.SetLabel(str(self.seconds))
        # This constant if else check may not be very efficient. Take a look whether it can be optimized or not
        # Its possible that calling like this without initialising a time.sleep(1000) may cause the program to be 1 second faster. Check it out
        if self.seconds == 0:
            self.second_zero = True
            if (self.timer_end()):
                self.song_thread()
                return
        else:
            self.second_zero = False
            self.seconds -= 1
        self.minutes_update()
        # Calls itself one second later
        wx.CallLater(1000, self.seconds_update)
    
    def minutes_update(self):
        # Temporary lazy method of fixing. Updating it regardless if the value changes or not. 17:06, 21/10/2019
        print(f'Minutes: {self.minutes}')
        self.minutes_label.SetLabel(str(self.minutes))
        if self.minutes > 0 and self.second_zero:
            self.minutes -= 1
            self.seconds = 59
            
        if self.minutes == 0:
            self.minute_zero = True
        else:
            self.minute_zero = False
        self.hours_update()
            
    def hours_update(self):
        # Temporary lazy method of fixing. Updating it regardless if the value changes or not. 17:06, 21/10/2019
        print(f'Hours: {self.hours}')
        self.hours_label.SetLabel(str(self.hours))
        if self.hours > 0 and self.minute_zero:
            self.hours -= 1
            self.minutes = 59
            
        if self.hours == 0:
            self.hour_zero = True
        # This else statement may not be necessary
        else:
            self.hour_zero = False
    
    def timer_end(self):
        # Check the value of hours, minutes, and seconds. If all 0, means timer end.
        if self.hour_zero and self.minute_zero and self.second_zero:
            return True
    
    def song_thread(self):
        th = threading.Thread(target=self.play_audio)
        th.start()
    
    def play_audio(self):
        # Assign a static song path. Temp
        # Decide to use pydub after research. Alternative that may consider in the future is pyaudio(low level manipulation) or pythonsounddevice
        song_path = 'song.mp3'
        audio = AudioSegment.from_mp3(song_path)
        play(audio)