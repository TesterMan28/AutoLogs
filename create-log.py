# 16:36, 21/10/2019, After experimenting with: wx.Timer, schedule, time.sleep(x), wx.CallLater, decided to use wx.CallLater
# 17:00, 21/10/2019, For the update functions, we can start disabling the hours_update when it becomes 0 since its the top one and continue with minutes update
# 17:15, 21/10/2019, Take a look at wx.StaticBox and wx.StaticBoxSizer
# Modules for time scheduler
import schedule             # pip install schedule
import time
# GUI
import wx                   # pip install wxPython / pip install -U wxPython
# Get current date
import datetime
from datetime import date
# At the moment this function will create file at a fixed path
# TODO: Create a file and send it to a server as JSON maybe? 

''' Try declaring this method inside the MyFrame class
def create_file():
    # Defines a fixed path to create file
    dir_path = 'C:/Users/Zohl/Desktop/Internship Documents'
    cur_date = date.today()
    # Defining format for filename
    filename = 'day' + cur_date.day + '_' + 'month' + cur_date.month + 'year' + cur_date.year
    try:
        with open(f'{filename}.txt', w) as writer:
            # Declare string to right to the text file. Need to change to some variable or another file which contains the 
            writer.write("Temp string")
    catch OSError:
        print('Temp error message. OSError occured.')
''' 
  
# def create_prompt():


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Enter description")
        panel = wx.Panel(self)
        
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text_area = wx.TextCtrl(panel, style = wx.TE_MULTILINE)
        my_sizer.Add(self.text_area, 0, wx.ALL | wx.EXPAND, 5)
        
        self.submit = wx.Button(panel, label="Submit")
        self.submit.Bind(wx.EVT_BUTTON, self.submit_click)
        my_sizer.Add(self.submit, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(my_sizer)
        self.Show()
    
    def submit_click(self, event):
        print(self.text_area.GetValue())
        
class StartFrame(wx.Frame):
    def __init__(self):
        cur_time = datetime.today()
        super().__init__(parent=None, title="Start timer")
        start_panel = wx.Panel(self)
        
        start_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Set temporary label for StaticText
        self.time_label = wx.StaticText(start_panel, cur_time, size=(50, -1))
        start_sizer.Add(self.time_label, 0, wx.ALL | wx.CENTER, 5)
        
        self.start_button = wx.Button(start_panel, label="Start")
        self.start_button.Bind(wx.EVT_BUTTON, self.start_click)
        start_sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)
        
        start_panel.SetSizer(start_sizer)
        self.Show()
        
    def start_click(self, event):
        # TODO: Create a countdown timer when click button started for one hour OR create drop down boxes to select hour, minute, second
        # wx.ComboBox or wx.TextCtrl
        print('Start click')
        
class TimerFrame(wx.Frame):
    def __init__(self):
        self.value_changed = False
        cur_datetime = datetime.datetime.today()
        # Filters cur_datetime into [hours, minutes, seconds]
        cur_time = [cur_datetime.hour, cur_datetime.minute, cur_datetime.second]
        
        # Variables that hold current time values
        self.hours = cur_time[0];
        self.minutes = cur_time[1];
        self.seconds = cur_time[2];
        
        # Variables that determine if time values are zero
        self.second_zero = False
        self.minute_zero = False
        self.hour_zero = False
        
        # Sizers for widget placement
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        super().__init__(parent=None, title="Timer")
        # Bind close event to Frame
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        
        main_panel = wx.Panel(self)
        
        # Seconds label
        # seconds_string = wx.String.Format(wxT("%i"), cur_time[2])
        self.seconds_label = wx.StaticText(main_panel, label=str(cur_time[0]), size=(50, -1))
        row_sizer.Add(self.seconds_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Minutes label
        self.minutes_label = wx.StaticText(main_panel, label=str(cur_time[1]), size=(50, -1))
        row_sizer.Add(self.minutes_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Hours label
        self.hours_label = wx.StaticText(main_panel, label=str(cur_time[0]), size=(50, -1))
        row_sizer.Add(self.hours_label, 0, wx.ALL | wx.CENTER, 5)
        
        main_sizer.Add(row_sizer)
        
        main_panel.SetSizer(main_sizer)
        self.Show()
        self.zero_checker()
        
        # Define schedule tasks
        # schedule.every(10).seconds.do(self.seconds_update)
        '''
        self.changeAlpha_timer = wx.Timer(main_panel, 1)
        self.Bind(wx.EVT_TIMER, self.seconds_update)
        self.changeAlpha_timer.Start(1000)  # 1 second interval
        '''
        self.seconds_update()
        
        # Run the timer
        # while True:
            # Its possible by using this method that the function is synchronous and will cause the program to freeze and crash
            # self.seconds_update()
            # schedule.run_pending()
            # time.sleep(1)
            
    def when_closed(self, event):
        # Temporary code to create close event. Change later
        if event.CanVeto():
            event.Veto()
            print('Destruction incoming')
            self.Destroy()
            return
        
        
        
    def seconds_update(self):
        print(f'Seconds: {self.seconds}')
        self.seconds_label.SetLabel(str(self.seconds))
        # This constant if else check may not be very efficient. Take a look whether it can be optimized or not
        # Its possible that calling like this without initialising a time.sleep(1000) may cause the program to be 1 second faster. Check it out
        if self.seconds == 0:
            self.second_zero = True
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
            
    def zero_checker(self):
        if (self.value_changed):
            print('Value changed')
        else:  
            print('Not changed')
            
    # def time_timer(self):
        
            
        
            
if __name__ == '__main__':
    app = wx.App(False)
    frame = TimerFrame()
    app.MainLoop()

'''        
schedule.every().day.at("17:15").do(create_file)
schedule.every().day.at("17:15").do(create_prompt)
'''

# Keeps the script running. Might want to change the code to just check every minute instead of evey second
'''
while True:
    schedule.run_pending()
    time.sleep(1)
'''