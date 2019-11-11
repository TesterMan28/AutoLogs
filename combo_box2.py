import wx
import wx.adv
import wx.grid as gridlib
import search_youtube
# 16:52, 7/11/2019: Try using OwnerDrawnComboBox instead of Grid
# 16:21, 7/11/2019, For resizing image: https://stackoverflow.com/questions/2504143/how-to-resize-and-draw-an-image-using-wxpython/8466013#8466013
# 17:02, 6/11/2019: How do I edit how many columns and rows the image spans

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


class DrawComboBox(wx.adv.OwnerDrawnComboBox):
    # def __init__(self, parent, list):
    #    super().__init__(parent, choices=list, style=wx.CB_READONLY, pos=(20,40), size=(250, -1))

    # Override this method to draw each item in the list
    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            # painting the control, but there is no valid item selected
            return

        r = wx.Rect(*rect)
        r.Deflate(3, 5)     # Not sure how this works. Comment out later

        # Define fixed size for rectanglar thumbnail
        thumbWidth = 5
        thumbHeight = 5

        penStyle = wx.PENSTYLE_SOLID
        '''
        if item == 1:
            penStyle = wx.PENSTYLE_DOT_DASH
        elif item == 2:
            penStyle: wx.PENSTYLE_CROSS_HATCH
        elif item == 3:
            penStyle = wx.PENSTYLE_LONG_DASH
        elif item == 4:
            penStyle = wx.PENSTYLE_SHORT_DASH
        elif item == 5:
            penStyle = wx.PENSTYLE_DOT_DASH
        elif item == 6:
            penStyle = wx.PENSTYLE_BDIAGONAL_HATCH
        '''

        pen = wx.Pen(dc.GetTextForeground(), 3, penStyle)
        dc.SetPen(pen)

        if flags & wx.adv.ODCB_PAINTING_CONTROL:
            # For painting the control itself
            dc.DrawLine( r.x+5, r.y+r.height/2, r.x+r.width - 5, r.y+r.height/2)

        else:
            # Draw image
            img = wx.Bitmap()

            # For painting the items in the popup
            dc.DrawText( self.GetString( item ),
                        r.x + 100,
                        (r.y + 0) + ( (r.height/2) - dc.GetCharHeight() ) /2 )
            # dc.DrawLine( r.x + 5, r.y+((r.height/4)*3)+1, r.x+r.width - 5, r.y+((r.height/4)*3)+1 )
            dc.SetPen(wx.Pen(wx.GREEN))
            dc.SetBrush(wx.Brush(wx.GREEN))
            # dc.DrawRectangle(r.width / 5 * 1 + 1, r.y + ((r.height / 2)) + 1, r.x+3, r.y+3)
            dc.DrawRectangle(r.x + 3, r.y+(r.height / 2) - thumbHeight, thumbWidth, thumbHeight)
            '''
            dc.DrawText( self.GetString( item ),
                        r.x + 100,
                        (r.y + 0) + ( (r.height/2) + (dc.GetCharHeight() / 2 + 3) ) /2 )
            '''

    # Overridden from OwnerDrawnComboBox, called for drawing the
    # background area of each item
    def OnDrawBackground(self, dc, rect, item, flags):
        # If the item is selected, or its item # iseven, or we are painting the
        # combo control itself, then use the default rendering
        if (item & 1 == 0 or flags & (wx.adv.ODCB_PAINTING_CONTROL |
                                      wx.adv.ODCB_PAINTING_SELECTED)):
            wx.adv.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

            # Otherwise draw every other background with different colour
            bgCol = wx.Colour(240, 240, 250)
            dc.SetBrush(wx.Brush(bgCol))
            dc.SetPen(wx.Pen(bgCol))
            dc.DrawRectangle(rect);

    # Overridden from OwnerDrawnComboBox, should return the height
    # needed to display an item in the popup, or -1 for default
    def OnMeasureItem(self, item):
        # Simply demonstrate the ability to have variable-height items
        if item & 1:
            return 36
        else:
            return 24

    # Overridden from OwnerDrawnComboBox.  Callback for item width, or
    # -1 for default/undetermined
    def OnMeasureItemWidth(self, item):
        return -1; # default - will be measured from text width


class TestPanel(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="OwnerDrawnComboBox Test")
        self.main_panel = wx.Panel(self)

        # Temporary items
        # items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6']
        # self.items = []

        # Create instance of OwnerDrawnComboBox
        # odcb = DrawComboBox(self, items)
        # odcb = DrawComboBox(self, choices=self.items, style=wx.CB_READONLY, pos=(20, 40), size=(250, -1))

        # Button to trigger wx.EVT_PAINT
        generate = wx.Button(self, label="Search")
        self.Bind(wx.EVT_BUTTON, lambda event: self.searchResults(event, self), generate)

        # generate.Bind(wx.EVT_BUTTON, self.CallPaint)

        # Set temporary static image
        img = wx.Bitmap('wxpython.png', wx.BITMAP_TYPE_ANY)

        # self.InitUI()
        self.Show()

    def searchResults(self, event, parent):
        # results = search_youtube.youtube_search_keyword("Maroon 5", 10)
        # self.items.extend(results)
        results = search_youtube.youtube_search_keyword("Maroon 5", 10)
        # self.items.extend(results)
        odcb = DrawComboBox(parent, choices=results, style=wx.CB_READONLY, pos=(20, 40), size=(250, -1))

    def InitUI(self):
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.Show(True)

    # def CallPaint(self, e, list)

    '''
    def CallPaint(self, e):
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.Show(True)
    '''

    '''
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

        dc.DrawBitmap(wx.Bitmap("wxpython.png"), 10, 10, True)  # 10, 10 are the coordinates to paint
    '''


if __name__ == '__main__':
    app = wx.App(False)
    frame = TestPanel()
    app.MainLoop()
