# 16:27, 24/10/2019: TODO: Change update_values to check for any changes in TextCtrl instead of on EVT_KILL_FOCUS
# 17:03, 23/10/2019: TODO: Complete horizontal_adding() as a helper method to add widgets in a horizontal row
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
# Playing audio
from pydub import AudioSegment
from pydub.playback import play
# Threading
import threading

  
# def create_prompt():

# Frame to enter task details
class CountdownFrame(wx.Frame):
    def __init__(self, duration):
        # Variables that determine if time values are zero
        self.second_zero = False
        self.minute_zero = False
        self.hour_zero = False
        
        # Time values
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
    
        super().__init__(parent=None, title='Countdown Frame')
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.create_labels(duration)
        
        # Creating a button to start playing audio. https://stackoverflow.com/questions/34266964/how-can-i-prevent-gui-freezing-in-wxpython
        self.addButton = wx.Button(self.panel, -1, "Start", style=wx.BU_EXACTFIT)
        self.main_sizer.Add(self.addButton, 0, wx.ALL | wx.CENTER, 5)
        # self.addButton.Bind(wx.EVT_BUTTON, self.song_thread)
        
        self.countdown_timer()
        self.panel.SetSizer(self.main_sizer)
        self.Show()
        
    @classmethod
    def user_values(cls, value_dict):
        self.seconds = value_dict["seconds"]
        self.minutes = value_dict["minutes"]
        self.hours = value_dict["hours"]
        
    @classmethod
    def dropdown_values(cls, duration):
        # TODO: Get values if user chooses from the dropdown menu
        if (duration == 0):
            self.minutes = 30
        elif (duration == 1):
            self.hours = 1
        elif (duration == 2):
            self.seconds = 10
    
    # Creating the time labels
    # Currently labels are overlapping each other
    def create_labels(self, duration):
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
        if (self.hour_zero, self.minute_zero, self.second_zero):
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
        
        # Temp dictionary variable to hold variables
        self.time_values = {
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds
        }
        
        
        
        # Sizers for widget placements
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
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
        self.choices = wx.Choice(start_panel, choices=["30 minutes", "1 hour", "10 seconds"])
        main_sizer.Add(self.choices, 0, wx.ALL | wx.CENTER, 5)
      
        
        # Start the countdown timer. Creates an instance of CountdownFrame
        self.start_button = wx.Button(start_panel, label="Start")
        self.start_button.Bind(wx.EVT_BUTTON, self.start_click)
        # self.start_button.Bind(wx.EVT_BUTTON, self.verify_values)
        main_sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)
        
        
        # Create initial styling for TextCtrl
        text_colour = wx.Colour(245, 245, 245)
        background_colour = wx.Colour(255, 255, 255)
        font_styling = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT, True)
        initial_style = wx.TextAttr(text_colour, background_colour, font_styling, wx.TEXT_ALIGNMENT_DEFAULT)
        
        # Creates TextCtrl boxes to enter time details
        self.hour_textctrl = wx.TextCtrl(start_panel, value="hh", style=wx.TE_PROCESS_ENTER, name="hours")
        self.hour_textctrl.SetStyle(0, len(self.hour_textctrl.GetValue()) - 1, initial_style)
        row_sizer2.Add(self.hour_textctrl, 0, wx.ALL | wx.CENTER, 5)
        self.hour_textctrl.Bind(wx.EVT_SET_FOCUS, self.empty_text)      # On obtain focus
        self.hour_textctrl.Bind(wx.EVT_KILL_FOCUS, self.update_values)
        
        
        self.colon1 = wx.TextCtrl(start_panel, value=":", size=(10, 20), style=wx.TE_READONLY)
        row_sizer2.Add(self.colon1, 0, wx.ALL | wx.CENTER, 5)
        
        self.minute_textctrl = wx.TextCtrl(start_panel, value="mm",  style=wx.TE_PROCESS_ENTER, name="minutes")
        self.minute_textctrl.SetStyle(0, len(self.minute_textctrl.GetValue()) - 1, initial_style)
        row_sizer2.Add(self.minute_textctrl, 0, wx.ALL | wx.CENTER, 5)
        self.minute_textctrl.Bind(wx.EVT_SET_FOCUS, self.empty_text)
        self.minute_textctrl.Bind(wx.EVT_KILL_FOCUS, self.update_values)
        
        self.colon2 = wx.TextCtrl(start_panel, value=":", style=wx.TE_READONLY)
        row_sizer2.Add(self.colon2, 0, wx.ALL | wx.CENTER, 5)
        
        self.second_textctrl = wx.TextCtrl(start_panel, value="ss",  style=wx.TE_PROCESS_ENTER, name="seconds")
        self.second_textctrl.SetStyle(0, len(self.second_textctrl.GetValue() ) - 1, initial_style)
        row_sizer2.Add(self.second_textctrl, 0, wx.ALL | wx.CENTER, 5)
        self.second_textctrl.Bind(wx.EVT_SET_FOCUS, self.empty_text)
        self.second_textctrl.Bind(wx.EVT_KILL_FOCUS, self.update_values)
        # End TextCtrl
        
        main_sizer.Add(row_sizer2)
        
        start_panel.SetSizer(main_sizer)
        self.Show()
        
    # OnFocus TextCtrl handler
    def empty_text(self, event):
        widget = event.GetEventObject() # Get widget that triggered this event
        
        if widget.IsModified(): # If user has edited the field, do not remove the user entered text
            widget.Enable(True)
            widget.SetFocus()
            # event.Skip()
        else:
            widget.MarkDirty()  # Mark widget as edited
            # Remove initial placeholder of TextCtrl
            widget.Enable(True)
            widget.SetFocus()
            widget.SetValue("")
            # event.Skip()
        
        
        print(f'Window name: {widget.GetName()}')
        
        event.Skip()    # Allows default handling to take place. The insertion point is inserted
        # widget.Bind(wx.EVT_KILL_FOCUS, self.update_values)        # Causes update_values to be called more and more times. Not sure why
        
    
    # Printing statement repeats more and more times
    def update_values(self, event):
        # TODO: Update values on kill focus TextCtrl
        widget = event.GetEventObject()
        if widget.GetName() in self.time_values:
            self.time_values[widget.GetName()] = widget.GetValue()
            print(f'New value assigned to {widget.GetName()}: {widget.GetValue()}')
        else:
            print('Error in update_values method')
        event.Skip()
        
    
    # Passes values in TextCtrl to CountdownFrame
    def timer_set(self):
        set_hours = self.hour_textctrl.GetValue()
        set_minutes = self.minute_textctrl.GetValue()
        set_seconds = self.second_textctrl.GetValue()
        
        time_values = {
            "hours": set_hours,
            "minutes": set_minutes,
            "seconds": set_seconds
        }
        
        
    
        
    # TODO: Helper method to add multiple widgets in a row. Not completed yet.
    def horizontal_adding(self, *args):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
    def update_choice(self, event):
        self.selected_item = (self.choices.GetString(self.choices.GetCurrentSelection()))
        print(f"Current value of selected_item: {self.selected_item}")
        
    def start_click(self, event):
        # Opening another frame
        # Determine which CountdownFrame constructor to call
        
        # Set TextCtrl as priority
        # if ()
        
        
        # countdown_frame_instance = CountdownFrame(self.choices.GetCurrentSelection())
        print(f'Current hours: {self.hours}')
        print(f'Current minutes: {self.minutes}')
        print(f'Current seconds: {self.seconds}')
        
    def verify_values(self, event):
        ValueValidator(self.event, self.hours, self.minutes, self.seconds)

class ValueValidator(wx.Validator):
    def __init__ (self, event, hours, minutes, seconds):
        if (self.Validate(event.GetEventObject()) and self.TransferFromWindow()):
            print(f'Window that called: {self.GetWindow()}')

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

