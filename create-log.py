# 17:18, 22/10/2019: TODO: Trigger some kind of message or sound when the countdown timer reachest zero
# Modules for time scheduler
import schedule             # pip install schedule
import time
# GUI
import wx                   # pip install wxPython / pip install -U wxPython
import wx.richtext
# Get current date
import datetime
from datetime import date

  
# def create_prompt():

# Frame to enter task details
class CountdownFrame(wx.Frame):
    def __init__(self, duration):
        # Temp variables. Check if it works
        self.second_zero = False
        self.minute_zero = False
        self.hour_zero = False
    
    
        super().__init__(parent=None, title='Countdown Frame')
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.create_labels(duration)
        
        self.countdown_timer()
        self.panel.SetSizer(self.main_sizer)
        self.Show()
    
    # Creating the time labels
    # Currently labels are overlapping each other
    def create_labels(self, duration):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        
        if (duration == 0):
            self.minutes = 30
        elif (duration == 1):
            self.hours = 1
        
        
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

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Enter description")
        panel = wx.Panel(self)
        
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Creating OnClose frame event handler
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.text_area = wx.TextCtrl(panel, style = wx.TE_MULTILINE)
        my_sizer.Add(self.text_area, 0, wx.ALL | wx.EXPAND, 5)
        
        self.submit = wx.Button(panel, label="Submit")
        self.submit.Bind(wx.EVT_BUTTON, self.submit_click)
        my_sizer.Add(self.submit, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(my_sizer)
        self.Show()
    
    # Temp code
    def submit_click(self, event):
        print(self.text_area.GetValue())
        
    def on_close(self, event):
        print('Closed')

# Frame for setting due time and starting the countdown timer
class StartFrame(wx.Frame):
    def __init__(self):
        self.selected_item = ''
        cur_datetime = datetime.datetime.today()
        # Filters cur_datetime into [hours, minutes, seconds]
        cur_time = [cur_datetime.hour, cur_datetime.minute, cur_datetime.second]
        
        # Variables that hold current time values
        self.hours = cur_time[0];
        self.minutes = cur_time[1];
        self.seconds = cur_time[2];
        
        
        
        # Sizers for widget placements
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        super().__init__(parent=None, title="Start timer")
        start_panel = wx.Panel(self)
        
        self.Bind(wx.EVT_CHOICE, self.update_choice)
        
        # Current Time label
        self.current_label = wx.StaticText(start_panel, label='Current Time:')
        main_sizer.Add(self.current_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Seconds label
        # seconds_string = wx.String.Format(wxT("%i"), cur_time[2])
        self.seconds_label = wx.StaticText(start_panel, label=str(cur_time[0]), size=(50, -1))
        row_sizer.Add(self.seconds_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Minutes label
        self.minutes_label = wx.StaticText(start_panel, label=str(cur_time[1]), size=(50, -1))
        row_sizer.Add(self.minutes_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Hours label
        self.hours_label = wx.StaticText(start_panel, label=str(cur_time[0]), size=(50, -1))
        # self.hours_label.SetForegroundColour(wx.Colour(255, 0, 0))    # Changing text colour
        row_sizer.Add(self.hours_label, 0, wx.ALL | wx.CENTER, 5)
        
        main_sizer.Add(row_sizer)
        
        # Set due label
        self.set_label = wx.StaticText(start_panel, label="Set due:")
        main_sizer.Add(self.set_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Create drop down list
        self.choices = wx.Choice(start_panel, choices=["30 minutes", "1 hour"])
        main_sizer.Add(self.choices, 0, wx.ALL | wx.CENTER, 5)
      
        
        self.start_button = wx.Button(start_panel, label="Start")
        self.start_button.Bind(wx.EVT_BUTTON, self.start_click)
        main_sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)
        
        start_panel.SetSizer(main_sizer)
        self.Show()
        
    def update_choice(self, event):
        self.selected_item = (self.choices.GetString(self.choices.GetCurrentSelection()))
        print(f"Current value of selected_item: {self.selected_item}")
        
    def start_click(self, event):
        # Opening another frame
        # Returns the choice index
        countdown_frame_instance = CountdownFrame(self.choices.GetCurrentSelection())

# Frame for showing current time and how long more to due deadline
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
        
        # Creating custom TextAttr for labels
        text_colour = wx.Colour(255, 87, 51)    # Shade of red
        background_colour = wx.Colour(63, 255, 51)  # Shade of green
        font_styling = wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)  # Font styling
        style = wx.TextAttr(text_colour, background_colour, font_styling, wx.TEXT_ALIGNMENT_DEFAULT)
        
        super().__init__(parent=None, title="Timer")
        # Bind close event to Frame
        self.Bind(wx.EVT_CLOSE, self.when_closed)
        
        main_panel = wx.Panel(self)
        
        # Seconds label
        # seconds_string = wx.String.Format(wxT("%i"), cur_time[2])
        self.seconds_label = wx.StaticText(self, label=str(cur_time[0]), size=(50, -1))
        row_sizer.Add(self.seconds_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Minutes label
        self.minutes_label = wx.StaticText(self, label=str(cur_time[1]), size=(50, -1))
        row_sizer.Add(self.minutes_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Hours label
        self.hours_label = wx.StaticText(self, label=str(cur_time[0]), size=(50, -1))
        # self.hours_label.SetForegroundColour(wx.Colour(255, 0, 0))    # Changing text colour
        row_sizer.Add(self.hours_label, 0, wx.ALL | wx.CENTER, 5)
        
        # Try using RichTextCtrl
        # Need to set the size for rich_text
        self.rich_text = wx.richtext.RichTextCtrl(self, value='2928392', size=(500, 30), style=wx.richtext.RE_READONLY)
        self.rich_text.SetStyle(0, len(self.rich_text.GetValue()), style)
        row_sizer.Add(self.rich_text, 0, wx.ALL | wx.CENTER, 5)
        
        
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
    
    '''
    def file_creation():
        static_path = "one_log.txt"
        static_text = "Temp string to write to file"
        try:
            f = open(static_path, 'w+')
            f.write(static_text)
            f.close()
            print("Text written to file")
        except OSError:
            print('File already exists')
    '''
            
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
            

'''
def file_creation():
    static_path = "one_log.txt"
    static_text = "Temp string to write to file"
    try:
        f = open(static_path, 'w+')
        f.write(static_text)
        f.close()
        print("Text written to file")
    except OSError:
        print('File already exists')
'''
            
if __name__ == '__main__':
    app = wx.App(False)
    frame = StartFrame()
    app.MainLoop()
    

    
    
    

# Not working at the moment. Maybe while True block into app.MainLoop()

'''        
schedule.every().day.at("17:15").do(create_file)
schedule.every().day.at("17:15").do(create_prompt)
'''

# Keeps the script running. Might want to change the code to just check every minute instead of evey second

