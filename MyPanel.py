# -*- coding: utf-8 -*-
"""
User interface of Cloud Simulator.
"""

"""
Contains common method for user interface and command line execution
"""

import os
import sys
import time
import traceback
import imghdr
import binascii
import base64
import configuration as conf

from SelectResultReport import AutoWidthListCtrl
from MySQLconn import ExecSQL
from MyDialog import *
from MyThreading import MyThread
from MyException import *
from WebServer.WebpyServer import GetBinaryData

# sys.stdout.flush()


class FamilieCloudHarness(wx.Panel):
    def __init__(self, parent, windows, log, retMyThreadObj):
        wx.Panel.__init__(self, parent, -1)
        self.isWindows = windows
        self.ListCtrlObj = None   # 防止多处调用变量不存在（使用时先判断是否为None）
        self.mythread = None
        self.XmlListCtrlId = 30
        self.BinaryListCtrlId = 31
        self.log_obj = log
        self.retMyThreadObj = retMyThreadObj
        self.err_text = "Error:in file MyPanel.py of class CloudSimulatorHarness(): method "
        self.SetBackgroundColour(wx.WHITE)
        self.renderGUI()    # Display GUI

    def renderGUI(self):
        """ Generate and display GUI based on OS
        :Parameters
            none
        :Return
            none
        """
        # sizer = wx.BoxSizer(wx.VERTICAL)
        self.setAppHeader()
        self.setRespConf()
        self.setStreamMsg()
        self.setSelectResult()
        self.setListCtrl()
        self.setEventLog()
        self.setRunButton()
        self.setCloseButton()

    def setAppHeader(self):
        """ Display application header with logo and app name"""
        wx.StaticBitmap(self, pos=(60, 15)).SetBitmap(wx.Bitmap(os.getcwd() + '/images/logo.png'))
        if self.isWindows:
            statictext = wx.StaticText(self, -1, 'Cloud Simulator', (260, 12), size=(100, 25))
        else:
            statictext = wx.StaticText(self, -1, 'Cloud Simulator', (260, 17), size=(100, 25))

        font = statictext.GetFont()
        font.SetPointSize(25)
        statictext.SetFont(font)
        statictext.SetForegroundColour((128, 128, 128))

        wx.StaticText(self, -1, 'Date: ' + time.strftime('%b %d, %Y'), (700, 15), size=(150, 20))
        wx.StaticText(self, -1, 'Version: ' + conf.version, (700, 35), size=(120, 20))

    def setRespConf(self):
        """ Url Configuraton
        """
        # Panel
        wx.StaticBox(self, -1, 'Response Configuration', (8, 80), size=(360, 140))
        wx.StaticText(self, -1, 'URI:', (20, 113), size=(30, 25))
        # TextCtrl
        self.texturl = wx.TextCtrl(self, -1, '', (60, 110), size=(300, 25), style=wx.TE_PROCESS_ENTER)
        self.texturl.Bind(wx.EVT_TEXT_ENTER, self.searchUrlInfo)
        # Button
        self.searchBtn = wx.Button(self, -1, 'Search', (280, 180), size=(80, 25))
        self.searchBtnEvn =self.searchBtn.Bind(wx.EVT_BUTTON, self.searchUrlInfo)

    def setStreamMsg(self):
        """ Stream Configuration
        """
        wx.StaticBox(self, -1, 'Stream Configuration', (380, 80), size=(437, 140))

        wx.StaticText(self, -1, 'Picture:', (395, 113), size=(50, 25))
        self.picPath = wx.TextCtrl(self, -1, '', (455, 110), size=(240, 25), style=wx.TE_READONLY)

        wx.StaticText(self, -1, 'Audio:', (395, 148), size=(50, 25))
        self.vocPath = wx.TextCtrl(self, -1, '', (455, 145), size=(240, 25), style = wx.TE_READONLY)

        wx.StaticText(self, -1, 'Video:', (395, 183), size=(50, 25))
        self.vdoPath = wx.TextCtrl(self, -1, '', (455, 180), size=(240, 25), style = wx.TE_READONLY)

        self.PicBtn = wx.Button(self, -1, 'Browse', pos=(715, 110), size=(80, 25), style = wx.BU_EXACTFIT)
        self.VocBtn = wx.Button(self, -1, 'Browse', pos=(715, 145), size=(80, 25), style = wx.BU_EXACTFIT)
        self.VdoBtn = wx.Button(self, -1, 'Browse', pos=(715, 180), size=(80, 25), style = wx.BU_EXACTFIT)
        self.PicBtn.Bind(wx.EVT_BUTTON, self.PicBtnInfo)
        self.VocBtn.Bind(wx.EVT_BUTTON, self.VocBtnInfo)
        self.VdoBtn.Bind(wx.EVT_BUTTON, self.VdoBtnInfo)
        # set Stream Msg disable
        self.setStreamMsgStatue(False)

    def setStreamMsgStatue(self, value):
        """ set Stream button statue
        """
        self.picPath.Clear()
        self.vdoPath.Clear()
        self.vocPath.Clear()
        self.PicBtn.Enable(value)
        self.VocBtn.Enable(value)
        self.VdoBtn.Enable(value)

    def setSelectResult(self):
        """Display Url result
        """
        wx.StaticBox(self, -1, 'Select Result', (8, 230), size=(810, 240))
        # CheckBox
        self.allcheck = wx.CheckBox(self, -1, 'Select all', (27, 255), size=(100, -1))
        self.allcheck.Enable(False)
        self.allcheck.Bind(wx.EVT_CHECKBOX, self.selectAllList)

        self.addBtn = wx.Button(self, 1, 'Add', (460, 251), size=(80, 25))
        self.deleteBtn = wx.Button(self, 1, 'Delete', (700, 251), size=(80, 25))
        self.deleteBtn.Enable(False)
        self.editBtn = wx.Button(self, 1, 'Edit', (580, 251), size=(80, 25))
        self.editBtn.Enable(False)

        self.addBtn.Bind(wx.EVT_BUTTON, self.addUrlInfo)
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.deleteUrlInfo)
        self.editBtn.Bind(wx.EVT_BUTTON, self.EditResponseInfo)

    def setListCtrl(self, ID=30):
        """ set list ctrl
        """
        if self.XmlListCtrlId == ID:
            # layout ListCtrl
            self.creatListCtrlObj(self.XmlListCtrlId)
            self.ListCtrlObj.insertXmlListHead()
        else:
            self.creatListCtrlObj(self.BinaryListCtrlId)
            self.ListCtrlObj.insertBinaryListHead()

    def creatListCtrlObj(self, ID):
        """ Create and bind function
            ID：创建的ListCtr的ID
        """
        self.ListCtrlObj = AutoWidthListCtrl(self, 785, ID)
        self.ListCtrlObj.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick)
        self.ListCtrlObj.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.ListCtrlObj.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)

    def insert2List(self, result):
        """ result: 数据库查询结果\
            30:XML LIST ID
            30:Binary LIST ID
        """
        if self.ListCtrlObj is None:
            self.PrintEventLog(self.err_text+"insert2List self.ListCtrlObj is None")
            return
        # Exception result return
        if result is None:
            self.PrintEventLog(self.err_text+"insert2List result is None")
            return

        list_id = self.ListCtrlObj.GetId()
        if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
            self.PrintEventLog(self.err_text+"insert2List self.ListCtrlObj.GetId() is not 30 or 31")
            return

        # if resutl is not list Type Exception process
        try:
            if list_id == self.XmlListCtrlId:
                for index in result:
                    pos = self.ListCtrlObj.InsertStringItem(sys.maxint, str(index['conf_id']))
                    self.ListCtrlObj.SetStringItem(pos, 1, index['conf_url'])
                    self.ListCtrlObj.SetStringItem(pos, 2, str(index['conf_response']).decode('utf-8'))
                    self.ListCtrlObj.SetStringItem(pos, 3, str(index['conf_request']).decode('utf-8'))
                for i in range(self.ListCtrlObj.GetItemCount()):
                    if self.ListCtrlObj.GetItem(i, 2).GetText() == 'Fail':
                        self.ListCtrlObj.SetItemTextColour(i, wx.Colour(204, 0, 0))
                    # else:
                    #     self.ListCtrlObj.SetItemTextColour(i, wx.Colour(0, 0, 0))
            else:
                for index in result:
                    pos = self.ListCtrlObj.InsertStringItem(sys.maxint, str(index['conf_id']))
                    self.ListCtrlObj.SetStringItem(pos, 1, index['conf_url'])
                    if str(index['conf_type']) == '0':
                        self.ListCtrlObj.SetStringItem(pos, 2, 'Picture')
                    elif str(index['conf_type']) == '1':
                        self.ListCtrlObj.SetStringItem(pos, 2, 'Voice')
                    elif str(index['conf_type']) == '2':
                        self.ListCtrlObj.SetStringItem(pos, 2, 'Video')
                    else:
                        self.ListCtrlObj.SetStringItem(pos, 2, 'None')
                        self.PrintEventLog(self.err_text+"insert2List ListCtrlObj.SetStringItem is None")
                    self.ListCtrlObj.SetStringItem(pos, 3, index['conf_before'])
                    self.ListCtrlObj.SetStringItem(pos, 4, index['conf_after'])

                for i in range(self.ListCtrlObj.GetItemCount()):
                    if self.ListCtrlObj.GetItem(i, 2).GetText() == 'Fail':
                        self.ListCtrlObj.SetItemTextColour(i, wx.Colour(204, 0, 0))
                    # else:
                    #     self.ListCtrlObj.SetItemTextColour(i, wx.Colour(0, 102, 0))

        except (TypeError, KeyError, AttributeError) as err:
            self.PrintEventLog(self.err_text+"insert2List "+str(err))
        except Exception as err:
            self.PrintEventLog(self.err_text+"insert2List "+str(err))

    def destoryListCtrl(self):
        """ destory list ctrl obj
        """
        self.ListCtrlObj.Destroy()

    def swapListCtrlLayout(self, ID):
        """ swap list ctrl layout
        """
        if self.ListCtrlObj.GetId() is ID:
            self.PrintEventLog(self.err_text+"swapListCtrlLayout self.ListCtrlObj.GetId() is not 30 or 31")
            return

        if self.ListCtrlObj.GetId() is self.XmlListCtrlId:
            self.destoryListCtrl()
            self.setListCtrl(self.BinaryListCtrlId)
        else:
            self.destoryListCtrl()
            self.setListCtrl(self.XmlListCtrlId)

    def setEventLog(self):
        """Display EventLog result
        """
        wx.StaticBox(self, -1, "Event Log", (8, 480), size=(810, 140))
        # Create TextCtrl for Event log
        self.eventlogprint = wx.TextCtrl(self, -1, 'Test event log Ouput:', (20, 505), size=(785, 100), style=wx.TE_READONLY | wx.TE_MULTILINE)

    def searchUrlInfo(self, event):
        """Display selected Url information
        """
        if self.ListCtrlObj is None:
            self.PrintEventLog(self.err_text+"searchUrlInfo self.ListCtrlObj is None")
            return

        # delete all list
        self.ListCtrlObj.DeleteAllItems()
        # get url value
        urlpath = self.texturl.GetValue()

        # self.ListCtrlObj.GetId() Exception Process(Not is 30 or 31 )
        list_id = self.ListCtrlObj.GetId()
        if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
            self.PrintEventLog(self.err_text+"searchUrlInfo self.ListCtrlObj.GetId() is not 30 or 31")
            return

        # traceback flag
        flag = True
        execsql = None
        # Xml执行DB查询
        # add SQL Connect Exception Process
        try:
            execsql = ExecSQL(self.PrintEventLog)
            result = execsql.selectBut(list_id, urlpath)
        # My define SQL Connect Exception trap and return
        except (TypeError, AttributeError) as err:
            self.PrintEventLog(err)
            return
        except SQLconnError as err:
            self.PrintEventLog(err.arg)
            return
        # BaseException trap and return
        except BaseException as err:
            self.PrintEventLog(self.err_text+str(err))
            return
        else:
            flag = False
            # self.PrintEventLog("SQL Connection OK")
        finally:
            self.tracebackOutput(flag)
            # release value
            del execsql

        # 将DB结果插入list表单
        self.insert2List(result)
        # set button state(Enable or Disable)
        self.SetButtonState()

    def PicBtnInfo(self, event):
        """Open a file
        """
        self.vdoPath.Clear()
        self.vocPath.Clear()
        dirname = ""
        openPicBtnInfo = wx.FileDialog(self, "Choose a picture file...",dirname,"","*.*", wx.OPEN)

        if openPicBtnInfo.ShowModal() == wx.ID_OK:
            filename= openPicBtnInfo.GetFilename()
            dirname = openPicBtnInfo.GetDirectory()
            imgtype = imghdr.what(os.path.join(dirname, filename))
            if imgtype:
                f = open(os.path.join(dirname, filename), 'rb')
                # base64位编码
                # fbase64 = base64.b64encode(f.read())
                fbase64 = base64.encodestring(f.read())
                # hexstring = binascii.b2a_hex(fbyte)
                # binnum = bin(int(hexstring, 16))[2:]
                GetBinaryData(fbase64)
                self.picPath.AppendText(os.path.join(dirname, filename))
                self.PrintEventLog(imgtype)
                f.close()
            else:
                self.PrintEventLog(filename + " is not picture.")
        openPicBtnInfo.Destroy()

    def VocBtnInfo(self, event):
        """Open a file
        """
        self.vdoPath.Clear()
        self.picPath.Clear()
        dirname = ""
        openVocBtnInfo = wx.FileDialog(self, "Choose a voice file...",dirname,"","*.*", wx.OPEN)
        if openVocBtnInfo.ShowModal() == wx.ID_OK:
            filename= openVocBtnInfo.GetFilename()
            dirname = openVocBtnInfo.GetDirectory()
            f = open(os.path.join(dirname, filename), 'rb')
            # base64位编码
            # fbase64 = base64.b64encode(f.read())
            # hexstring = binascii.b2a_hex(fbyte)
            # binnum = bin(int(hexstring, 16))[2:]
            try:
                GetBinaryData(f.read())
            except IOError as e:
                self.PrintEventLog("IO ERROR: %s" %e)
            self.vocPath.AppendText(os.path.join(dirname, filename))
            print f.read()

            f.close()
        openVocBtnInfo.Destroy()

    def VdoBtnInfo(self, event):
        """OPen a file
        """
        self.vocPath.Clear()
        self.picPath.Clear()
        dirname = ""
        openVdoBtnInfo = wx.FileDialog(self, "Choose a video file...",dirname,"","*.*", wx.OPEN)
        if openVdoBtnInfo.ShowModal() == wx.ID_OK:
            filename= openVdoBtnInfo.GetFilename()
            dirname = openVdoBtnInfo.GetDirectory()
            f = open(os.path.join(dirname, filename), 'rb')
            fbase64 = base64.b64encode(f.read())
            # hexstring = binascii.b2a_hex(fbyte)
            # binnum = bin(int(hexstring, 16))[2:]
            GetBinaryData(fbase64)

            self.vdoPath.AppendText(os.path.join(dirname, filename))
            f.close()
        openVdoBtnInfo.Destroy()

    def selectAllList(self, event):
        """ Check/Uncheck all iterm
        :Parameters
            event - event bounded to check box
        :Return
            none
        """
        if self.ListCtrlObj is None:
            self.PrintEventLog(self.err_text+"selectAllList self.ListCtrlObj is None")
            return

        # deleteBtn Enable
        if self.allcheck.GetValue():
            self.ListCtrlObj.SelectAllItem(1)
        else:
            self.ListCtrlObj.SelectAllItem(0)
        self.SetButtonState()

    def SetButtonState(self):
        """ Set Button State
        :Parameters
            call function
        :Return
            none
        """
        if self.ListCtrlObj is None:
            self.PrintEventLog(self.err_text+"SetButtonState self.ListCtrlObj is None")
            return

        # set delete button state
        if not self.ListCtrlObj.GetSelectedItemCount():
            self.deleteBtn.Enable(False)
        else:
            self.deleteBtn.Enable(True)

        # set select all button state
        if not self.ListCtrlObj.GetItemCount():
            self.allcheck.SetValue(False)
            self.allcheck.Enable(False)
        else:
            self.allcheck.Enable(True)
            if self.ListCtrlObj.GetItemCount() == self.ListCtrlObj.GetSelectedItemCount():
                self.allcheck.SetValue(True)
            else:
                self.allcheck.SetValue(False)

        # set edit button state
        if self.ListCtrlObj.GetSelectedItemCount() is 1:
            self.editBtn.Enable(True)
        else:
            self.editBtn.Enable(False)

    def addUrlInfo(self, event):
        """Create a new Url information
        """
        if self.ListCtrlObj is None:
            self.PrintEventLog(self.err_text+"addUrlInfo self.ListCtrlObj is None")
            return

        if self.ListCtrlObj.GetId() == self.XmlListCtrlId:
            self.addXmlDialog()
        else:
            self.addBinaryDialog()

    def addXmlDialog(self):
        """ add xml dialog
        """
        execsql = None
        # Show Information Dialog
        adddialog = AddXmlDialog(self, -1, "Add Config", (450, 400))
        adddialog.CenterOnScreen()
        # this does not return until the dialog is closed.
        val = adddialog.ShowModal()

        flag = True
        # add SQL Connect Exception Process
        try:
            if val == wx.ID_OK:
                # print "You pressed OK"
                # 获取add的值
                getresult = adddialog.GetAddText()
                # [u'111', u'2222', u'33333']
                # Analyzing the encoding type
                list_id = self.ListCtrlObj.GetId()
                if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
                    self.PrintEventLog(self.err_text+"addXmlDialog self.ListCtrlObj.GetId() is not 30 or 31")
                    return
                # 查询url是否唯一
                execsql = ExecSQL(self.PrintEventLog)
                url = execsql.geturlsql(list_id, getresult[0])
                # 判断url是否唯一
                if getresult[0] == '':
                    self.PrintEventLog("Please enter URL.")
                elif not len(url):
                    # insert db
                    execsql = ExecSQL(self.PrintEventLog)
                    execsql.addSaveDataBut(list_id, getresult)
                    # refresh db
                else:
                    # print("The URL address is existing. ")
                    self.PrintEventLog("The URL address is existing. URL: %s" % getresult[0])
                # refresh listctrl
                self.searchUrlInfo(self.searchBtnEvn)

            else:
                # print "You pressed CANCEL"
                pass

        # My define SQL Connect Exception trap and return
        except (TypeError, AttributeError) as err:
            self.PrintEventLog(err)
            return
        except SQLconnError as err:
            self.PrintEventLog(err.arg)
            return
        # BaseException trap and return
        except BaseException as err:
            self.PrintEventLog(self.err_text+str(err))
            return
        else:
            flag = False
            # self.PrintEventLog("SQL Connection OK")
        finally:
            self.tracebackOutput(flag)
            # release value
            del execsql
            adddialog.Destroy()

    def addBinaryDialog(self):
        """ add binary dialog
        """

        execsql = None
        # Show Information Dialog
        adddialog = AddBinaryDialog(self, -1, "Add Config", (450, 400))
        adddialog.CenterOnScreen()
        # this does not return until the dialog is closed.
        val = adddialog.ShowModal()

        flag = True
        # add SQL Connect Exception Process
        try:
            if val == wx.ID_OK:
                # print "You pressed OK"
                # 获取add的值
                getresult = adddialog.GetAddText()
                # [u'111', u'2222', u'33333']
                # print getresult[0], type(getresult[0])
                # print getresult
                # print type(getresult[0]), getresult[1]

                # Analyzing the encoding type
                list_id = self.ListCtrlObj.GetId()
                if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
                    self.PrintEventLog(self.err_text+"addXmlDialog self.ListCtrlObj.GetId() is not 30 or 31")
                    return

                # 查询url是否唯一
                execsql = ExecSQL(self.PrintEventLog)
                url = execsql.geturlsql(list_id, getresult[0])
                # url为空是不允许insert
                if getresult[0] == '':
                    self.PrintEventLog("Please enter URL.")
                # 判断url是否唯一
                elif not len(url):
                    # insert db
                    execsql = ExecSQL(self.PrintEventLog)
                    execsql.addSaveDataBut(list_id, getresult)
                    # refresh db
                else:
                    # print("The URL address is existing. ")
                    self.PrintEventLog("The URL address is existing. URL: %s" % getresult[0])
                # refresh listctrl
                self.searchUrlInfo(self.searchBtnEvn)

            else:
                # print "You pressed CANCEL"
                pass

        # My define SQL Connect Exception trap and return
        except (TypeError, AttributeError) as err:
            self.PrintEventLog(err)
            return
        except SQLconnError as err:
            self.PrintEventLog(err.arg)
            return
        # BaseException trap and return
        except BaseException as err:
            self.PrintEventLog(self.err_text+str(err))
            return
        else:
            flag = False
            # self.PrintEventLog("SQL Connection OK")
        finally:
            self.tracebackOutput(flag)
            # release value
            del execsql
            adddialog.Destroy()

    def deleteUrlInfo(self, event):
        """Delete a selected Url information """
        execsql = None
        flag = True
        try:
            # eg. listitemselected, getlistitemid = [1, 0] [u'22', u'23']
            listitemselected, getlistitemid = self.ListCtrlObj.GetSelectListItem()
            # print listitemselected, getlistitemid
            execsql = ExecSQL(self.PrintEventLog)

            list_id = self.ListCtrlObj.GetId()
            if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
                self.PrintEventLog(self.err_text+"deleteUrlInfo self.ListCtrlObj.GetId() is not 30 or 31")
                return
            if self.ListCtrlObj.GetItemCount() == self.ListCtrlObj.GetSelectedItemCount():
                self.ListCtrlObj.DeleteAllItems()
                execsql.deleteBut(list_id, "")
            else:
                for item in listitemselected:
                    self.ListCtrlObj.DeleteItem(item)
                # 删除选中项（多选和单选）
                execsql.deleteBut(list_id, getlistitemid)
        # My define SQL Connect Exception trap and return
        except (TypeError, AttributeError) as err:
            self.PrintEventLog(err)
            return
        except SQLconnError as err:
            self.PrintEventLog(err.arg)
            return
        # BaseException trap and return
        except BaseException as err:
            self.PrintEventLog(self.err_text+str(err))
            return
        else:
            flag = False
            # self.PrintEventLog("SQL Connection OK")
        finally:
            self.tracebackOutput(flag)
            # release value
            del execsql
        # set button state(Enable or Disable)
        self.SetButtonState()

    def EditResponseInfo(self, event):
        """ Edit Response info
        """
        conf_id = self.ListCtrlObj.GetSelectedSingleItemInfo(self.ListCtrlObj.GetSelectListItem()[0][0],self.ListCtrlObj.GetId())
        execsql = ExecSQL(self.PrintEventLog)

        if self.ListCtrlObj.GetId() == self.XmlListCtrlId:
            querydata = execsql.getAll(self.ListCtrlObj.GetId(), conf_id)
            for index in querydata:
                self.resultall = (index['conf_id'], index['conf_url'], str(index['conf_response']).decode('utf-8'), str(index['conf_request']).decode('utf-8'))
                self.editXmlDialog(self.resultall)
        else:
            querydata = execsql.getAll(self.ListCtrlObj.GetId(), conf_id)
            for index in querydata:
                self.resultall = (index['conf_id'], index['conf_url'], index['conf_type'], index['conf_before'], index['conf_after'])
                self.editBinaryDialog(self.resultall)

    def editXmlDialog(self, text):
        """ edit xml dialog
        """
        flag = True
        execsql = None
        # Show Information Dialog
        editdialog = EditXmlDialog(self, -1, "Edit Config", (450, 400), text)
        editdialog.CenterOnScreen()
        # this does not return until the dialog is closed.
        val = editdialog.ShowModal()
        try:
            if val == wx.ID_OK:
                getresult = editdialog.GetResponseText()

                list_id = self.ListCtrlObj.GetId()
                if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
                    self.PrintEventLog(self.err_text+"editXmlDialog self.ListCtrlObj.GetId() is not 30 or 31")
                    return

                # 执行查询插入操作
                execsql = ExecSQL(self.PrintEventLog)
                listitemselected, getlistitemid = self.ListCtrlObj.GetSelectListItem()
                execsql.editSaveDataBut(list_id, str(getlistitemid[0]), getresult)
                # refresh ListCtrl layout result
                self.searchUrlInfo(self.searchBtnEvn)
            else:
                # print "You pressed CANCEL"
                pass
        # My define SQL Connect Exception trap and return
        except (TypeError, AttributeError) as err:
            self.PrintEventLog(err)
            return
        except SQLconnError as err:
            self.PrintEventLog(err.arg)
            return
        # BaseException trap and return
        except BaseException as err:
            self.PrintEventLog(self.err_text+str(err))
            return
        else:
            flag = False
            # self.PrintEventLog("SQL Connection OK")
        finally:
            self.tracebackOutput(flag)
            # release value
            del execsql
            editdialog.Destroy()

    def editBinaryDialog(self, text):
        """ edit binary dialog
        """
        # self.PrintEventLog("edit binary dialog is not Achieve")
        # self.searchUrlInfo(self.searchBtnEvn)
        """ edit Binary dialog """
        flag = True
        execsql = None
        # Show Information Dialog
        editdialog = EditBinaryDialog(self, -1, "Edit Config", (450, 400), text)
        editdialog.CenterOnScreen()
        # print editdialog.GetResponseText()
        #[1, u'wfrwaef', u'wfrwaef']
        # this does not return until the dialog is closed.
        val = editdialog.ShowModal()
        try:
            if val == wx.ID_OK:
                getresult = editdialog.GetResponseText()

                list_id = self.ListCtrlObj.GetId()
                if list_id not in [self.XmlListCtrlId, self.BinaryListCtrlId]:
                    self.PrintEventLog(self.err_text+"editXmlDialog self.ListCtrlObj.GetId() is not 30 or 31")
                    return

                # 执行查询插入操作
                execsql = ExecSQL(self.PrintEventLog)
                listitemselected, getlistitemid = self.ListCtrlObj.GetSelectListItem()
                execsql.editSaveDataBut(list_id, str(getlistitemid[0]), getresult)
                # refresh ListCtrl layout result
                self.searchUrlInfo(self.searchBtnEvn)
            else:
                # print "You pressed CANCEL"
                pass
        # My define SQL Connect Exception trap and return
        except (TypeError, AttributeError) as err:
            self.PrintEventLog(err)
            return
        except SQLconnError as err:
            self.PrintEventLog(err.arg)
            return
        # BaseException trap and return
        except BaseException as err:
            self.PrintEventLog(self.err_text+str(err))
            return
        else:
            flag = False
            # self.PrintEventLog("SQL Connection OK")
        finally:
            self.tracebackOutput(flag)
            # release value
            del execsql
            editdialog.Destroy()

    def OnDoubleClick(self, event):
        """double click to show this iterm information
        """
        conf_id = self.ListCtrlObj.GetSelectedSingleItemInfo(event.m_itemIndex,self.ListCtrlObj.GetId())
        execsql = ExecSQL(self.PrintEventLog)

        if self.ListCtrlObj.GetId() == self.XmlListCtrlId:
            querydata = execsql.getAll(self.ListCtrlObj.GetId(), conf_id)
            for index in querydata:
                self.resultall = (index['conf_id'], index['conf_url'], str(index['conf_response']).decode('utf-8'), str(index['conf_request']).decode('utf-8'))

            # Show Information Dialog
            viewdialog = ViewXmlDialog(self, -1, "Show Information", (450, 400), self.resultall)
            viewdialog.CenterOnScreen()
            # this does not return until the dialog is closed.
            val = viewdialog.ShowModal()
            if val == wx.ID_OK:
                pass
                # print "You pressed OK"
            viewdialog.Destroy()
        else:
            querydata = execsql.getAll(self.ListCtrlObj.GetId(),conf_id)
            for index in querydata:
                self.resultall = (index['conf_id'], index['conf_url'], index['conf_type'], index['conf_before'], index['conf_after'])
            # Show Information Dialog
            viewbinarydialog = ViewBinaryDialog(self, -1, "Show Information", (450, 400), self.resultall)
            viewbinarydialog.CenterOnScreen()
            # this does not return until the dialog is closed.
            val = viewbinarydialog.ShowModal()
            if val == wx.ID_OK:
                # print "You pressed OK"
                pass
            viewbinarydialog.Destroy()

    def OnItemSelected(self, evt):
        # self.PrintEventLog('@item selected: %s' % evt.m_itemIndex)
        self.ListCtrlObj.CheckItem(evt.m_itemIndex, True)
        self.SetButtonState()

    def OnItemDeselected(self, evt):
        # self.PrintEventLog('@item deselected: %s' % evt.m_itemIndex)
        self.ListCtrlObj.CheckItem(evt.m_itemIndex, False)
        self.SetButtonState()

    def PrintEventLog(self, log, flag=True):
        """Print Event Log Func
        """
        # self.eventlogprint.Clear()
        # output to log file
        str_log = '\n' + time.strftime(' %Y-%m-%d %X', time.localtime()) + ':  %s' % str(log)
        self.log_obj.write(str_log)

        if flag:
            self.eventlogprint.write(str_log)
        self.eventlogprint.SetOwnForegroundColour(wx.RED)


    def tracebackOutput(self, flag=True):
        """tracebackOutput
        """
        if flag:
            traceback.print_exc(file=self.log_obj)

    def run(self, event):
        """Run WebServer Func
        """
        try:
            # Avoid duplication create objects self.mythread
            self.mythread = MyThread(self.PrintEventLog)

            if "RunServer" == self.runButton.GetLabelText():
                self.runButton.SetLabelText("StopServer")
                self.eventlogprint.Clear()
                self.mythread.start()
                self.PrintEventLog("Web Server Started.")
            else:
                # self.mythread.stop()
                self.ErrorDialog(self.mythread, "Are You Sure Stop Web Server!")
                self.PrintEventLog("Web Server Stoped.")

            self.getThreadObj()
        except RuntimeError as err:
            self.PrintEventLog(err)
        except Exception as err:
            self.PrintEventLog(err)

    def getThreadObj(self):
        """get My thread Obj
        """
        if "RunServer" != self.runButton.GetLabelText():
            self.retMyThreadObj(self.mythread, True)
        else:
            self.retMyThreadObj(self.mythread, False)

    def setRunButton(self):
        """ set run button label
        """
        self.runButton = wx.Button(self, -1, "RunServer", (580, 630), size=(80, 25))
        self.runButton.Bind(wx.EVT_BUTTON, self.run)

    def ErrorDialog(self, obj, msg):
        dlg = wx.MessageDialog(self, msg, "Warning", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            obj.stop()
            self.runButton.SetLabelText("RunServer")
        else:
            self.runButton.SetLabelText("StopServer")
        dlg.Destroy()

    def setCloseButton(self):
        """ Display Save and Run button

        :Parameters
            none
        :Return
            none
        """
        if not self.isWindows:
            self.closeButton = wx.Button(self, -1, 'Close', (680, 605), size=(80, 25))
        else:
            self.closeButton = wx.Button(self, -1, 'Close', (700, 630), size=(80, 25))
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)

    def close(self, event):
        """ Kill the thread if it is running
        :Parameters
            event - event bounded to frame
        :Return
            none
        """
        self.Close()
