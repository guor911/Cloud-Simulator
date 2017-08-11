# -*- coding: utf-8 -*-
"""
User interface of Dialog layout.
"""
import wx


class ViewXmlDialog(wx.Dialog):
    """View Dialog layout
    """
    def __init__(self, parent, ID, title, size, text):
        wx.Dialog.__init__(self, parent, ID, title, size)
        self.text = text
        sizer = wx.BoxSizer(wx.VERTICAL)
        # URL Info
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'URL', (10, 20), size=(100, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[1], (130, 17), size=(300, 25), style=wx.TE_READONLY)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Report', (10, 70), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[2], (130, 67), size=(300, 110), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_WORDWRAP|wx.HSCROLL)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Request Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Request Report', (10, 185), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[3], (130, 185), size=(300, 110), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_WORDWRAP|wx.HSCROLL)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # button layout
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        # btn = wx.Button(self, wx.ID_CANCEL)
        # btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class EditXmlDialog(wx.Dialog):
    """Edit Dialog layout
    """
    def __init__(self, parent, ID, title, size, text):
        wx.Dialog.__init__(self, parent, ID, title, size)
        self.text = text
        sizer = wx.BoxSizer(wx.VERTICAL)
        # URL Info
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'URL', (10, 20), size=(100, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[1], (130, 17), size=(300, 25), style=wx.TE_READONLY)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 10)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Report', (10, 70), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        self.RespTextCtrl = wx.TextCtrl(self, -1, self.text[2], (130, 67), size=(300, 210), style=wx.TE_NOHIDESEL|wx.TE_MULTILINE|wx.TE_RICH2)
        self.RespTextCtrl.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        box.Add(self.RespTextCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # button layout
        btnsizer = wx.StdDialogButtonSizer()
        self.SaveBtn = wx.Button(self, wx.ID_OK, label="Save")
        self.SaveBtn.SetDefault()
        self.SaveBtn.Enable(False)
        btnsizer.AddButton(self.SaveBtn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def _EnableSaveBtn(self, evt):
        """Enable button
        """
        # Enable Save Button
        self.SaveBtn.Enable(True)

    def GetResponseText(self):
        """ Return the modify Response report text
        """
        return self.RespTextCtrl.GetValue()


class AddXmlDialog(wx.Dialog):
    """Add Dialog layout
    """
    def __init__(self, parent, ID, title, size):
        wx.Dialog.__init__(self, parent, ID, title, size)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # URL Info
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'URI', (10, 20), size=(100, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        # TextCtrl
        self.AddUrlTextCtrl = wx.TextCtrl(self, -1, "", pos=(130, 17), size=(300, 25), style=wx.TE_NOHIDESEL)
        self.AddUrlTextCtrl.Bind(wx.EVT_TEXT, self._EnableSaveBtn)

        box.Add(self.AddUrlTextCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Report', pos=(10, 70), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        self.AddRespTextCtrl = wx.TextCtrl(self, -1, value="", pos=(130, 67), size=(300, 110), style=wx.TE_NOHIDESEL | wx.TE_MULTILINE | wx.TE_RICH2)
        self.AddRespTextCtrl.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        box.Add(self.AddRespTextCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Request Report info text
        # box = wx.BoxSizer(wx.HORIZONTAL)
        # # StaticText
        # label = wx.StaticText(self, -1, 'Request Report', (10, 185), size=(115, 25))
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # # TextCtrl
        # self.AddReqTextCtrl = wx.TextCtrl(self, -1, "Request...", (135, 185), size=(300, 110), style=wx.TE_NOHIDESEL|wx.TE_MULTILINE)
        # self.AddReqTextCtrl.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        # box.Add(self.AddRespTextCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # button layout
        btnsizer = wx.StdDialogButtonSizer()
        self.SaveBtn = wx.Button(self, wx.ID_OK, label="Save")
        self.SaveBtn.SetDefault()
        self.SaveBtn.Enable(False)
        btnsizer.AddButton(self.SaveBtn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def _EnableSaveBtn(self, evt):
        """Enable button"""
        # Enable Save Button
        self.SaveBtn.Enable(True)

    def GetAddText(self):
        """ Return the add text"""
        # return [self.AddUrlTextCtrl.GetValue(), self.AddRespTextCtrl.GetValue(), self.AddReqTextCtrl.GetValue()]
        return [self.AddUrlTextCtrl.GetValue(), self.AddRespTextCtrl.GetValue()]


class ViewBinaryDialog(wx.Dialog):
    # View Binary Dialog layout
    def __init__(self, parent, ID, title, size, text):
        wx.Dialog.__init__(self, parent, ID, title, size)
        self.text = text
        sizer = wx.BoxSizer(wx.VERTICAL)
        # URL Info
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'URI', (10, 20), size=(100, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[1], (130, 19), size=(300, 25), style=wx.TE_READONLY)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 10)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Type', (10, 70), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # Radio layout
        RadioBox = wx.BoxSizer(wx.VERTICAL)
        PictureRadio = wx.RadioButton(self, 0, "Picture", style=wx.RB_GROUP)
        RadioBox.Add(PictureRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        VoiceRadio = wx.RadioButton(self, 1, "Voice")
        RadioBox.Add(VoiceRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        VideoRadio = wx.RadioButton(self, 2, "Video")
        RadioBox.Add(VideoRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        box.Add(RadioBox, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        # Set Radio layout statue
        if PictureRadio.GetId() != self.text[2]:
            PictureRadio.SetValue(False)
            PictureRadio.Enable(False)

        if VoiceRadio.GetId() != self.text[2]:
            VoiceRadio.SetValue(False)
            VoiceRadio.Enable(False)

        if VideoRadio.GetId() != self.text[2]:
            VideoRadio.SetValue(False)
            VideoRadio.Enable(False)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Respone prefix
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Prefix', (10, 60), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[3], (130, 70), size=(300, 80), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_WORDWRAP|wx.HSCROLL)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Respone suffix
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'Response Prefix', (10, 120), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[4], (130, 160), size=(300, 80), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_WORDWRAP|wx.HSCROLL)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # button layout
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        # btn = wx.Button(self, wx.ID_CANCEL)
        # btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class EditBinaryDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size, text):
        wx.Dialog.__init__(self, parent, ID, title, size)
        self.text = text
        sizer = wx.BoxSizer(wx.VERTICAL)
        # URL Info
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'URI', (10, 20), size=(100, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        # TextCtrl
        text = wx.TextCtrl(self, -1, self.text[1], (130, 19), size=(300, 25), style=wx.TE_READONLY)
        box.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, 10)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Type', (10, 60), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        # Radio layout
        RadioBox = wx.BoxSizer(wx.VERTICAL)
        self.PictureRadio = wx.RadioButton(self, 0, "Picture", style=wx.RB_GROUP)
        self.PictureRadio.Bind(wx.EVT_RADIOBUTTON, self._EnableSaveBtn)
        RadioBox.Add(self.PictureRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.VoiceRadio = wx.RadioButton(self, 1, "Voice")
        self.VoiceRadio.Bind(wx.EVT_RADIOBUTTON, self._EnableSaveBtn)
        RadioBox.Add(self.VoiceRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.VideoRadio = wx.RadioButton(self, 2, "Video")
        self.VideoRadio.Bind(wx.EVT_RADIOBUTTON, self._EnableSaveBtn)
        RadioBox.Add(self.VideoRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        if self.text[2] == self.PictureRadio.GetId():
            self.PictureRadio.SetValue(True)
        elif self.text[2] == self.VoiceRadio.GetId():
            self.VoiceRadio.SetValue(True)
        elif self.text[2] == self.VideoRadio.GetId():
            self.VideoRadio.SetValue(True)

        box.Add(RadioBox, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response prefix
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Prefix', (10, 180), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        self.prefixtext = wx.TextCtrl(self, -1, self.text[3], (130, 180), size=(300, 80), style=wx.TE_NOHIDESEL|wx.TE_MULTILINE|wx.TE_RICH2)
        self.prefixtext.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        box.Add(self.prefixtext, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # box.Add(self.prefixtext, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response suffix
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'Response Suffix', (10, 240), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        self.suffixtext = wx.TextCtrl(self, -1, self.text[4], (130, 240), size=(300, 80), style=wx.TE_NOHIDESEL|wx.TE_MULTILINE|wx.TE_RICH2)
        self.suffixtext.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        box.Add(self.suffixtext, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # box.Add(self.text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # button layout
        btnsizer = wx.StdDialogButtonSizer()
        self.SaveBtn = wx.Button(self, wx.ID_OK, label="Save")
        self.SaveBtn.SetDefault()
        self.SaveBtn.Enable(False)
        btnsizer.AddButton(self.SaveBtn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def _EnableSaveBtn(self, evt):
        """Enable button"""
        # Enable Save Button
        self.SaveBtn.Enable(True)

    def GetRadioboxSelect(self):
        """get selected radiobox
        0:PictureRadio
        1:VoiceRadio
        2:VideoRadio
        """
        radioboxgroup = {self.PictureRadio: 0, self.VoiceRadio: 1, self.VideoRadio: 2}
        for key in radioboxgroup.keys():
            if key.GetValue() is True:
                return str(radioboxgroup[key])

    def GetResponseText(self):
        """ Return the modify Response report text"""
        return [self.GetRadioboxSelect(), self.prefixtext.GetValue(), self.suffixtext.GetValue()]

class AddBinaryDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size):
        wx.Dialog.__init__(self, parent, ID, title, size)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # URL Info
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'URI', (10, 20), size=(100, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        # TextCtrl
        self.AddUrlTextCtrl = wx.TextCtrl(self, -1, "", pos=(130, 19), size=(300, 25), style=wx.TE_NOHIDESEL)
        self.AddUrlTextCtrl.Bind(wx.EVT_TEXT, self._EnableSaveBtn)

        box.Add(self.AddUrlTextCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 10)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Response Report info text
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Type', (10, 60), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        # Radio layout
        RadioBox = wx.BoxSizer(wx.VERTICAL)
        self.PictureRadio = wx.RadioButton(self, -1, "Picture", style=wx.RB_GROUP)
        self.PictureRadio.Bind(wx.EVT_RADIOBUTTON, self._EnableSaveBtn)
        RadioBox.Add(self.PictureRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.VoiceRadio = wx.RadioButton(self, -1, "Voice")
        self.VoiceRadio.Bind(wx.EVT_RADIOBUTTON, self._EnableSaveBtn)
        RadioBox.Add(self.VoiceRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.VideoRadio = wx.RadioButton(self, -1, "Video")
        self.VideoRadio.Bind(wx.EVT_RADIOBUTTON, self._EnableSaveBtn)
        RadioBox.Add(self.VideoRadio, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box.Add(RadioBox, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Respone prefix
        box = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText
        label = wx.StaticText(self, -1, 'Response Prefix', (10, 180), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        self.prefixtext = wx.TextCtrl(self, -1, "", (130, 180), size=(300, 80), style=wx.TE_NOHIDESEL|wx.TE_MULTILINE|wx.TE_RICH2)
        self.prefixtext.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        box.Add(self.prefixtext, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # box.Add(self.prefixtext, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Respone suffix
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, 'Response Suffix', (10, 240), size=(115, 25))
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # TextCtrl
        self.suffixtext = wx.TextCtrl(self, -1, "", (130, 240), size=(300, 80), style=wx.TE_NOHIDESEL|wx.TE_MULTILINE|wx.TE_RICH2)
        self.suffixtext.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        box.Add(self.suffixtext, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        # text.Bind(wx.EVT_TEXT, self._EnableSaveBtn)
        # box.Add(self.text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # button layout
        btnsizer = wx.StdDialogButtonSizer()
        self.SaveBtn = wx.Button(self, wx.ID_OK, label="Save")
        self.SaveBtn.SetDefault()
        self.SaveBtn.Enable(False)
        btnsizer.AddButton(self.SaveBtn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def _EnableSaveBtn(self, evt):
        """Enable button
        """
        self.SaveBtn.Enable(True)

    def GetRadioboxSelect(self):
        """
        get selected radiobox
            0:PictureRadio
            1:VoiceRadio
            2:VideoRadio
        """
        radioboxgroup = {self.PictureRadio: 0, self.VoiceRadio: 1, self.VideoRadio: 2}
        for key in radioboxgroup.keys():
            if key.GetValue() is True:
                return str(radioboxgroup[key])

    def GetAddText(self):
        """ Return the add text
        """
        return [self.AddUrlTextCtrl.GetValue(),
                self.GetRadioboxSelect(),
                self.prefixtext.GetValue(),
                self.suffixtext.GetValue()]
