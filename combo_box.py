import wx
import wx.grid as gridlib
# 16:52, 7/11/2019: Try using OwnerDrawnComboBox instead of Grid
# 16:21, 7/11/2019, For resizing image: https://stackoverflow.com/questions/2504143/how-to-resize-and-draw-an-image-using-wxpython/8466013#8466013
# 17:02, 6/11/2019: How do I edit how many columns and rows the image spans
# Temporarily try using wx.grid.Grid
# Reference code: http://www.blog.pythonlibrary.org/2010/03/18/wxpython-an-introduction-to-grids/
# Creating custom GridCell editor: https://github.com/wxWidgets/wxPython/blob/master/demo/GridCustEditor.py
# Inserting image into wx.grid.Grid cells: https://stackoverflow.com/questions/56204181/wx-grid-grid-doesnt-load-image
# wxPython Examples: https://extras.wxpython.org/wxPython4/extras/4.0.4/wxPython-docs-4.0.4.tar.gz
class ComboBox(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Grid List")
        self.main_panel = wx.Panel(self)
        
        # Create grid
        grid = gridlib.Grid(self.main_panel)
        grid.CreateGrid(5, 5)
        
        # img = wx.Bitmap("wxpython.png", wx.BITMAP_TYPE_ANY)
        
        # Resizing the image 
        img = wx.Image('wxpython.png', wx.BITMAP_TYPE_ANY)
        img = img.Rescale(width=259, height=122)
        img = img.ConvertToBitmap()
        
        imageRenderer = MyImageRenderer(img)
        grid.SetCellRenderer(0, 0, imageRenderer)
        grid.SetCellSize(0, 0, 4, 4)
        
        # Added
        grid.SetCellAlignment(0, 0, 1, 1)
        # grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        # Center content
        '''
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(hAlign=wx.ALIGN_CENTRE, vAlign=wx.ALIGN_CENTRE)
        # attr.SetReadOnly(True)
        grid.SetAttr(0, 0, attr)
        '''
        
        grid.SetColSize(0, img.GetWidth()/2)
        grid.SetColSize(1, img.GetWidth()/2)
        grid.SetRowSize(0, img.GetHeight()*2)
        grid.SetRowSize(1, img.GetHeight()/2)
        
        
        
        '''
        detail_grid.SetCellValue(0, 0, "Hello")
        detail_grid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        print(detail_grid.GetCellValue(0, 0))
        
        detail_grid.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1, 1000))
        detail_grid.SetCellValue(5, 0, '123')
        detail_grid.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        detail_grid.SetCellValue(6, 0, '123.34')
        detail_grid.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        
        detail_grid.SetCellSize(11, 1, 3, 3)
        detail_grid.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        detail_grid.SetCellValue(11, 1, "This cell is set to span up to 3 rows and 3 columns")
        
        detail_grid.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        detail_grid.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        '''
        
        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND)
        self.main_panel.SetSizer(sizer)

        
        self.Show()
    
    '''
    def OnLabelLeftClick(self, evt):
        print(f'OnLabelLeftClick {evt.GetRow()} {evt.GetCol()} {evt.GetPosition}')
        evt.Skip()
        
    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print(f'OnRangeSelect: {msg} top-left {evt.GetTopLeftCoords()} bottom-right {evt.GetBottomRightCoords()}')
        evt.Skip()
    '''
    
class MyImageRenderer(wx.grid.GridCellRenderer):
    def __init__(self, img):
        wx.grid.GridCellRenderer.__init__(self)
        self.img = img
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        image = wx.MemoryDC()
        image.SelectObject(self.img)
        dc.SetBackgroundMode(wx.SOLID)
        if isSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangle(rect)
        width, height = self.img.GetWidth(), self.img.GetHeight()
        
        print(f"Width: {width}, Height: {height}")  
        print(f"Rect width: {rect.width}, rect height: {rect.height}")  
        if width > rect.width - 2:
            width = rect.width - 2
        if height > rect.height - 2:
            height = rect.height - 2
        print(f"After Width: {width}, After Height: {height}")  
        dc.Blit(rect.x+1, rect.y+1, width, height, image, 0, 0, wx.COPY, True)
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = ComboBox()
    app.MainLoop()