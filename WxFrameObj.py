# -*- coding: utf-8 -*-
"""
User Create New New Feame object.
"""
import wx

class TestDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size, pos, style):
        wx.Dialog.__init__(self, parent, ID, title, size, pos, style)

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal constru ction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
        # wx.StaticText(self.NewFrame.panel, -1, 'URL', (10, 20), size=(100, 25))
        label = wx.StaticText(self, -1, 'URL', (10, 20), size=(100, 25))
        label.SetHelpText("This is the help text for the label")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Field #1:")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #1")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Field #2:")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #2")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

class WxFrameObj(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450, 400), style=wx.MINIMIZE_BOX|wx.CAPTION|wx.CLOSE_BOX)

        # Initialize common variables
        #self.initializeVariables()

        # Set panel into frame
        self.panel = wx.Panel(self, -1, (0, 0), (450, 400))
        self.panel.SetFocusIgnoringChildren()
        self.panel.SetBackgroundColour(wx.WHITE)

        # Set Save and Run button
        #self.setExecuteButton()

        # Make the frame visible in center of screen
        self.Centre()

        self.Bind(wx.EVT_CLOSE, self.close)


    def close(self, event):
        """ Kill the thread if it is running

        :Parameters
            event - event bounded to frame
        :Return
            none
        """
        event.Skip()

