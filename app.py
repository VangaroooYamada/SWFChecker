import wx


SCR_size = wx.Size(500, 400)
MB_size = wx.Size(32, 32)           # MenuButton size
PI_size = wx.Size(64, 64)           # ProfileIcon size


def scale_bmp(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    return wx.BitmapFromImage(image)


# class PlayersViewer():


class MenuPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.set_buttons()

    def set_buttons(self):
        config_btn = wx.BitmapButton(self, wx.ID_ANY,
                                     wx.Bitmap('./images/config.png'),
                                     style=0)
        clear_btn = wx.BitmapButton(self, wx.ID_ANY,
                                    wx.Bitmap('./images/clear.png'),
                                    style=0)

        self.layout = wx.BoxSizer(wx.HORIZONTAL)
        self.layout.Add(config_btn, flag=wx.GROW, border=0)
        self.layout.Add(clear_btn, flag=wx.GROW, border=0)

        self.SetSizer(self.layout)


class MainPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, wx.ID_ANY, *args, **kw)
        self.init_ui()

    def init_ui(self):
        pl_1 = wx.BitmapButton(self, wx.ID_ANY,
                               scale_bmp(wx.Bitmap('./images/person.png'),
                                         PI_size.x, PI_size.y), style=0)
        pl_2 = wx.BitmapButton(self, wx.ID_ANY,
                               scale_bmp(wx.Bitmap('./images/person.png'),
                                         PI_size.x, PI_size.y), style=0)
        pl_3 = wx.BitmapButton(self, wx.ID_ANY,
                               scale_bmp(wx.Bitmap('./images/person.png'),
                                         PI_size.x, PI_size.y), style=0)
        pl_4 = wx.BitmapButton(self, wx.ID_ANY,
                               scale_bmp(wx.Bitmap('./images/person.png'),
                                         PI_size.x, PI_size.y), style=0)

        pl_box = wx.GridSizer(rows=2, cols=2, gap=(0, 0))
        pl_box.Add(pl_1)
        pl_box.Add(pl_2)
        pl_box.Add(pl_3)
        pl_box.Add(pl_4)

        self.SetSizer(pl_box)


class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)
        self.init_ui()

    def init_ui(self):
        self.SetTitle('SWFChecker')
        self.SetSize(SCR_size)
        self.SetTransparent(128)

        self.main_layout = wx.BoxSizer(wx.VERTICAL)

        menu_panel = MenuPanel(self, size=(SCR_size.width, MB_size.height))
        menu_panel.SetBackgroundColour('GRAY')

        main_panel = MainPanel(self, size=(SCR_size.width,
                                           SCR_size.height - MB_size.height))
        main_panel.SetBackgroundColour('RED')

        self.main_layout.Add(menu_panel)
        self.main_layout.Add(main_panel)
        self.SetSizer(self.main_layout)


if __name__ == '__main__':
    app = wx.App()

    frame = MyApp(None, wx.ID_ANY,
                  style=wx.DEFAULT_FRAME_STYLE &
                  ~(wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU |
                    wx.RESIZE_BORDER))

    frame.Center()
    frame.Show()

    app.MainLoop()
