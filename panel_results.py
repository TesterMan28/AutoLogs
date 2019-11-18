import wx
import io
from urllib.request import urlopen
import search_youtube as sy

class InitUI(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Using panels to display the results")

        self.main_panel = wx.Panel(self, style=wx.SIMPLE_BORDER);
        self.main_sizer = wx.GridBagSizer(0,0)

        self.query = wx.TextCtrl(self.main_panel, size=(50, 20))
        self.main_sizer.Add(self.query, pos=(1, 2), span=(1,3), flag=wx.EXPAND|wx.ALL, border=5)

        self.search = wx.Button(self.main_panel, label="Search")
        self.main_sizer.Add(self.search, pos=(2, 2), span=(1,3), flag=wx.EXPAND|wx.ALL, border=5)
        self.search.Bind(wx.EVT_BUTTON, self.Search)

        # Temp assign sizer to main_panel
        self.main_panel.SetSizer(self.main_sizer)

        # self.SetSizer(self.main_sizer)
        self.Show()

    def Search(self, event):
        results = sy.youtube_search_keyword("Maroon 5", 8)
        self.ResultPanel(results)
        self.main_panel.SetSizerAndFit(self.main_sizer)

    def ResultPanel(self, results):
        gridy = 6
        gridx = 0
        for i in results:
            # panel = wx.Panel(self.main_panel)
            # sizer = wx.GridBagSizer(0, 0)

            bit = self.ImageURL(i["thumbnail"])
            img = wx.StaticBitmap(self.main_panel, bitmap=bit)

            #self.main_sizer.Add(img, pos=(4, 0), span=(5, 2), flag=wx.EXPAND|wx.ALL, border=5) # 0,0 : 2, 2
            self.main_sizer.Add(img, pos=(gridy, gridx), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=5)

            title = wx.StaticText(self.main_panel, label=i["title"])
            #self.main_sizer.Add(title, pos=(3, 3), span=(3, 5), flag=wx.ALL, border=5)    # 1,3 : 1, 5
            self.main_sizer.Add(title, pos=(gridy - 1, gridx + 3), span=(1, 2), flag=wx.ALL, border=5)

            description = wx.StaticText(self.main_panel, label=i["description"])
            #self.main_sizer.Add(description, pos=(5, 3), span=(5, 5), flag=wx.ALL, border=5)  # 2,3 : 2, 5
            self.main_sizer.Add(description, pos=(gridy + 1, gridx + 3), span=(1, 2), flag=wx.ALL, border=5)

            print(f'Value of gridy: {gridy}')
            gridy = gridy + 4

            # panel.SetSizerAndFit(sizer)
            # self.results_sizer.Add(panel, 0, wx.ALL | wx.CENTER, 5)
            # self.main_panel.Add(panel)

    def ImageURL(self, url):
        f = urlopen(url)
        data = f.read()

        stream = io.BytesIO(data)
        #bmp = wx.Bitmap( ( wx.Image( stream ) ).Rescale(width = 20, height = 20) )
        bmp = wx.Bitmap( ( wx.Image( stream ) ) )

        return bmp

app = wx.App()
InitUI()
app.MainLoop()
