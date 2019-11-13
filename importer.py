import wx
import os
import sys
from urllib.request import urlopen
import io
# Custom modules below
import search_youtube as sy

urls = sy.youtube_search_keyword("Maroon 5", 20)

class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()
        self.Ctrls()
        self.makeButtons()

    def makeButtons(self):
        i = 0

        for url in urls:
            f = urlopen(url)
            data = f.read()

            i += 1
            print(f" url = {url}, {i}")
            stream = io.BytesIO(data)
            bmp = wx.Bitmap( (wx.Image( stream ).Rescale(width=20, height=20)) )
            # bmp = wx.Bitmap( wx.Image( stream ), width=20, height=20 )
            button = wx.Button(self.panel, -1, "Singer covers", style=wx.ALIGN_CENTER, size=wx.Size(100, 100))
            button.SetToolTip("Tooltip for Singer Covers")
            button.SetBitmap(bmp, wx.TOP)
            button.SetBitmapMargins((10,10))
            button.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False))
            self.wrapSizer.Add(button, 1, wx.EXPAND)
        self.Show(True)
        self.panel.Layout()     # Not sure

    def InitUI(self):
        self.SetSize((800, 400))
        self.SetTitle("Dynamically flow buttons to next row on window resize")
        self.Centre()

    def Sizers(self):
        self.wrapSizer = wx.WrapSizer()
        self.panel.SetSizer(self.wrapSizer)

    def Ctrls(self):
        self.panel = wx.Panel(parent=self, pos=wx.Point(0, 0), size=wx.Size(750, 550), style=wx.TAB_TRAVERSAL)
        self.Sizers()       # Not sure

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()



# m1 = importlib.import_module('sender.sender')
# m1.calculate()


# calculate = input('calculate')
# importlib.import_module(Calculate)

# result = calculate()
# print(result)
