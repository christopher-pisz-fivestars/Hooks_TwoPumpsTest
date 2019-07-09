import wx


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.CreateStatusBar()

        menu_file = wx.Menu()
        menu_item_exit = menu_file.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        menu_help = wx.Menu()
        menu_item_about = menu_help.Append(wx.ID_ABOUT, "&About", " Information about this program")

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_file, "&File")
        menu_bar.Append(menu_help, "&Help")
        self.SetMenuBar(menu_bar)

        self.panel = MainPanel(self)

        self.Bind(wx.EVT_MENU, self.on_about, menu_item_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_item_exit)
        self.Connect(-1, -1, windows_hooks.WX_EVT_MOUSE_LEFT_BUTTON_DOWN_ID,
                     self.on_hooked_left_button_down)

        self.Show(True)

    def on_about(self, e):
        dlg = wx.MessageDialog(self, "A window to test stuff", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def on_exit(self, e):
        self.Close(True)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        self.consuming = False

        wx.Panel.__init__(self, parent)
        self.textbox = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.button_task = wx.Button(self, label="Long Task")
        self.button_consume = wx.Button(self, label="Start Consuming")

        self.horizontal = wx.BoxSizer()
        self.horizontal.Add(self.textbox, proportion=1, flag=wx.EXPAND)

        self.horizontal2 = wx.BoxSizer()
        self.horizontal2.Add(self.button_consume)
        self.horizontal2.Add(self.button_task)

        self.sizer_vertical = wx.BoxSizer(wx.VERTICAL)
        self.sizer_vertical.Add(self.horizontal, proportion=1, flag=wx.EXPAND)
        self.sizer_vertical.Add(self.horizontal2, proportion=1, flag=wx.CENTER)
        self.SetSizerAndFit(self.sizer_vertical)

        self.Bind(wx.EVT_BUTTON, self.on_click_task, self.button_task)
        self.Bind(wx.EVT_BUTTON, self.on_click_consume, self.button_consume)

    def on_click_task(self, event):
        self.textbox.AppendText('Starting a long task...\n')
        self.textbox.AppendText('MessageName: {}\n'.format(10))
        self.textbox.AppendText('Message: {}\n'.format(50))

    def on_click_consume(self, event):
        if not self.consuming:
            self.button_consume.SetLabel('Stop Consuming')
            self.consuming = True

        else:
            self.button_consume.SetLabel('Start Consuming')
            self.consuming = False
