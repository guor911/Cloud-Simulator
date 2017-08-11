# -*- coding: utf-8 -*-

import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin

"""
List control with auto scroll
"""


class AutoWidthListCtrl(wx.ListCtrl, CheckListCtrlMixin):
    """继承类，重写ListCtrl
    """
    def __init__(self, parent, width, id):
        self.XmlListCtrlId = 30
        self.BinaryListCtrlId = 31
        wx.ListCtrl.__init__(self, parent, id, pos=(20, 280), size=(width, 180), style=wx.LC_REPORT)
        # surpport sort style:wx.LC_SORT_ASCENDING
        CheckListCtrlMixin.__init__(self)

    def OnCheckItem(self, index, flag):
        """
        this is called by the base class when an item is checked/unchecked
        """
        # data = self.GetItemData(index)
        # title = self.GetItem(data, 1)
        # title = listdata[data][1]
        if flag:
            # what = "checked"
            self.Select(index, on=1)
        else:
            # what = "unchecked"
            self.Select(index, on=0)
        # print '@item at index %d was %s\n' % (index, what)

    # def ToggleItem(self, index):
    #     # self.CheckItem(index, not self.IsChecked(index))
    #     pass

    def GetSelectedSingleItemInfo(self, itemid, listid):
        # # list Single text info
        # get Row value

        if listid == self.XmlListCtrlId:
            conf_id = self.GetItem(itemid, 0).Text
            return conf_id
        else:
            conf_id = self.GetItem(itemid, 0).Text
            return conf_id

    def SelectAllItem(self, switch):
        """ Select All Item"""
        count = self.GetItemCount()
        for item in range(0, count):
            self.Select(item, on=switch)

    def GetSelectListItem(self):
        """Get Select ListItem"""
        listitemselected = []
        getlistitemid = []
        itemid = self.GetFirstSelected()
        while itemid != -1:
            #Do something
            if self.IsSelected(itemid):
                listitemselected.append(itemid)
                getitemid = self.GetItemText(itemid)
                getlistitemid.append(getitemid)
            itemid = self.GetNextSelected(itemid)
        listitemselected.reverse()
        return listitemselected, getlistitemid

    def insertXmlListHead(self):
        #Column name of list
        self.InsertColumn(0, 'ID', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=40)
        self.InsertColumn(1, 'URI', width=260)
        self.InsertColumn(2, 'Response', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=180)
        self.InsertColumn(3, 'Request', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=180)

    def insertBinaryListHead(self):
        #Column name of list
        self.InsertColumn(0, 'ID', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=40)
        self.InsertColumn(1, 'URI', width=260)
        self.InsertColumn(2, 'Type', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=55)
        self.InsertColumn(3, 'Response Prefix', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=160)
        self.InsertColumn(4, 'Response Suffix', wx.LIST_FORMAT_CENTRE | wx.LIST_ALIGN_LEFT, width=160)

