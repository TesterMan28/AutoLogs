# Use multiple panels to show each result

import wx
import io
from urllib.request import urlopen
import search_youtube as sy

# Playing audio
import requests
import vlc
from time import sleep

class InitUI(wx.Frame):
    def __init__(self):
        self.results = sy.youtube_search_keyword("Maroon 5", 8)

        super().__init__(parent=None, title="Using panels to display the results")

        self.main_panel = wx.Panel(self, style=wx.SUNKEN_BORDER);
        self.main_sizer = wx.GridBagSizer(0,0)

        self.query = wx.TextCtrl(self.main_panel, size=(50, 20))
        self.main_sizer.Add(self.query, pos=(1, 0), span=(1,1), flag=wx.EXPAND|wx.ALL, border=5)

        self.search = wx.Button(self.main_panel, label="Search")
        self.main_sizer.Add(self.search, pos=(2, 0), span=(1,1), flag=wx.EXPAND|wx.ALL, border=5)
        self.search.Bind(wx.EVT_BUTTON, self.Search)

        # Temp assign sizer to main_panel
        self.main_panel.SetSizer(self.main_sizer)

        # self.SetSizer(self.main_sizer)
        self.Show()

    def Search(self, event):
        self.ResultPanel(self.results)
        self.main_panel.SetSizerAndFit(self.main_sizer)

    def ResultPanel(self, results):
        gridy = 8
        gridx = 0

        # Readd components to the main_sizer?
        #self.main_sizer.Add(self.query, pos=(1, 2), span=(1,3), flag=wx.EXPAND|wx.ALL, border=5)
        #self.main_sizer.Add(self.search, pos=(2, 2), span=(1,3), flag=wx.EXPAND|wx.ALL, border=5)

        for i in results:
            self.side_panel = wx.Panel(self.main_panel, style=wx.SIMPLE_BORDER)

            # Add styling for each result panel
            #panel_size = self.side_panel.GetSize
            self.side_panel.SetBackgroundColour("#ECEAE9")

            self.side_panel.SetFont(wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, True))
            self.side_panel.SetForegroundColour("#191817")
            # self.side_panel.SetBackgroundStyle(wx.BG_STYLE_TRANSPARENT)


            self.side_panel.Bind(wx.EVT_LEFT_DCLICK, self.PanelClick)
            self.side_sizer = wx.GridBagSizer(5, 5)

            bit = self.ImageURL(i["thumbnail"])
            img = wx.StaticBitmap(self.side_panel, bitmap=bit)

            #self.main_sizer.Add(img, pos=(4, 0), span=(5, 2), flag=wx.EXPAND|wx.ALL, border=5) # 0,0 : 2, 2
            # self.main_sizer.Add(img, pos=(gridy, gridx), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=5)
            self.side_sizer.Add(img, pos=(0 , 0), span=(2, 2), flag=wx.EXPAND|wx.ALL, border=5)
            #self.side_sizer.Add(img, pos=(gridy, gridx), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=5)

            title = wx.StaticText(self.side_panel, label=i["title"])
            #self.main_sizer.Add(title, pos=(3, 3), span=(3, 5), flag=wx.ALL, border=5)    # 1,3 : 1, 5
            # self.main_sizer.Add(title, pos=(gridy - 1, gridx + 3), span=(1, 2), flag=wx.ALL, border=5)
            self.side_sizer.Add(title, pos=(0, 3), span=(1, 2), flag=wx.ALL, border=5)
            #self.side_sizer.Add(title, pos=(gridy - 1, gridx + 3), span=(1, 2), flag=wx.ALL, border=5)

            description = wx.StaticText(self.side_panel, label=i["description"])
            #self.main_sizer.Add(description, pos=(5, 3), span=(5, 5), flag=wx.ALL, border=5)  # 2,3 : 2, 5
            # self.main_sizer.Add(description, pos=(gridy + 1, gridx + 3), span=(1, 2), flag=wx.ALL, border=5)
            self.side_sizer.Add(description, pos=(1, 3), span=(1, 2), flag=wx.ALL, border=5)
            #self.side_sizer.Add(description, pos=(gridy + 1, gridx + 3), span=(1, 2), flag=wx.ALL, border=5)

            self.side_panel.SetSizer(self.side_sizer)

            self.main_sizer.Add(self.side_panel, pos=(gridy, gridx), span=(1, 2),flag=wx.EXPAND|wx.ALL, border=5)

            print(f'Value of gridy: {gridy}')
            gridy = gridy + 4

            # panel.SetSizerAndFit(sizer)
            # self.results_sizer.Add(panel, 0, wx.ALL | wx.CENTER, 5)
            # self.main_panel.Add(panel)

    def PanelClick(self, event):
        #wx.MessageDialog(self, message="Song added!", caption="Success Caption", style=OK|CENTRE)
        video_ids = []
        '''
        for video in self.results:
            video_ids.append('https://www.youtube.com/watch?v=' + video['video_id'])
        '''
        #video_ids.append('http://www.hochmuth.com/mp3/Haydn_Cello_Concerto_D-1.mp3')
        #video_ids.append('http://www.hochmuth.com/mp3/Tchaikovsky_Rococo_Var_orch.mp3')
        self.AddStream(video_ids)


    def AddStream(self, video_url):
        playlists = set(['pls', 'm3u'])

        Instance = vlc.Instance()

        for url in video_url:
            ext = (url.rpartition(".")[2])[:3]
            test_pass = False
            try:
                if url[:4] == 'file':
                    test_pass = True
                else:
                    r = requests.get(url, stream=True)
                    test_pass = r.ok
            except Exception as e:
                print('Failed to get stream: {e}'.format(e=e))
                test_pass = False
            else:
                if test_pass:
                    print('Sampling for 15 seconds')
                    player = Instance.media_player_new()
                    Media = Instance.media_new(url)
                    Media_list = Instance.media_list_new([url])
                    Media.get_mrl()
                    player.set_media(Media)
                    if ext in playlists:
                        list_player = Instance.media_list_player_new()
                        list_player.set_media_list(Media_list)
                        if list_player.play() == -1:
                            print("Error playing playlist")
                    else:
                        if player.play() == -1:
                            print("Error playing Stream")
                    sleep(15)
                    if ext in playlists:
                        list_player.stop()
                    else:
                        player.stop()

                else:
                    print('Error getting the audio')

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
