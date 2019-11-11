import wx
import io
from urllib.request import urlopen
import search_youtube as sy
# Getting image stream from URL: https://stackoverflow.com/questions/41218148/wxpython-fetch-remote-image-and-threading

class Mywin(wx.Frame):

   def __init__(self, parent, title):
      super(Mywin, self).__init__(parent, title = title,size = (500,300))
      self.InitUI()

   def InitUI(self):
      self.Bind(wx.EVT_PAINT, self.OnPaint)
      self.Centre()
      self.Show(True)

   def OnPaint(self, e):
      dc = wx.PaintDC(self)
      brush = wx.Brush("white")
      dc.SetBackground(brush)
      dc.Clear()

      # List of thumbnail urls
      results = sy.youtube_search_keyword("Maroon 5", 10)

      # Copying function code
      i = 0

      for url in results:
          f = urlopen(url)
          data = f.read()

          i += 1
          print(f" url = {url} {i}")
          stream = io.StringIO(data)
          bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ) )


      # Getting the stream for thumbnail url
      stream = io.StringIO()

      dc.DrawBitmap(wx.Bitmap("https://i.ytimg.com/vi/SlPhMPnQ58k/default.jpg"),10,10,True)
      color = wx.Colour(255,0,0)
      b = wx.Brush(color)

      dc.SetBrush(b)
      dc.DrawCircle(300,125,50)
      dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
      dc.DrawCircle(300,125,30)

      font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
      dc.SetFont(font)
      dc.DrawText("Hello wxPython",200,10)

      pen = wx.Pen(wx.Colour(0,0,255))
      dc.SetPen(pen)
      dc.DrawLine(200,50,350,50)
      dc.SetBrush(wx.Brush(wx.Colour(0,255,0), wx.CROSS_HATCH))
      dc.DrawRectangle(380, 15, 90, 60)

if __name__ == '__main__':
    ex = wx.App()
    Mywin(None,'Drawing demo')
    ex.MainLoop()
