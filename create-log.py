# Stopped, 16:37, 18/10/2019

# Modules for time scheduler
import schedule             # pip install schedule
import time
# GUI
import wx                   # pip install wxPython / pip install -U wxPython
# Get current date
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
            
if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
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