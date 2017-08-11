# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# Name:         run.py
# Purpose:      run demos
#
# Author:       xxx
#
# Created:      2015-10-30
# RCS-ID:       xxx
# Copyright:    (c) 2015 by Total Control Software
# Licence:      wxWindows license
# ----------------------------------------------------------------------------

"""
This program will load and run one of the individual demos in this
file within its own frame window.
"""

import wx
import os
import sys
import time
import traceback
from MyPanel import FamilieCloudHarness

WEBSVC_AND_STATE = [None, False]


class RunDemoApp(wx.App):
    """
    Display menubar with required option
    :Parameters
        ID,title,Size
    :Return
        none
    """
    def __init__(self, parent, ID, title, Size, log):
        self.parent = parent
        self.ID = ID
        self.title = title
        self.size = Size
        self.log = log
        self.frame = None
        self.isMacOS = None
        self.isWindows = None
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        """
        Init Parameters func
        :Parameters
            ID,title,Size
        :Return
        none
        """
        self.frame = wx.Frame(self.parent, self.ID, self.title, wx.DefaultPosition, self.size,
                              style=wx.MINIMIZE_BOX|wx.CAPTION|wx.CLOSE_BOX)
        self.isWindows, self.isMacOS = self.identifyOperatingSystem()

        # Display menu bar
        self.setMenubar()
        # Display GUI
        self.FrameObject = FamilieCloudHarness(self.frame, self.isWindows, self.log, getPanelThreadObj)
        self.FrameObject.Bind(wx.EVT_CLOSE, self.OnExitApp)
        # self.FrameObject.Bind(wx.CloseEvent, self.OnExitApp)
        # Make the frame visible in center of screen
        self.frame.Centre()
        self.frame.Show(True)
        return True

    def setMenubar(self):
        """
        Display menubar with required option
        :Parameters
            none
        :Return
            none
        """
        # Identify OS for GUI
        if self.isWindows:
            self.frame.SetSize((830, 715))
        # MenuBar Create
        menubar = wx.MenuBar()
        File = wx.Menu()
        File.Append(11, '&Import', 'ImportUrllist')
        File.AppendSeparator()
        File.Append(12, '&Export', 'ExportUrllist')
        File.AppendSeparator()
        File.Append(13, '&Exit', 'Exit')
        menubar.Append(File, '&File')
        Option = wx.Menu()
        Option.Append(22, 'XMLConfig')
        Option.AppendSeparator()
        Option.Append(23, 'BinaryConfig')
        menubar.Append(Option, '&Option')
        self.frame.SetMenuBar(menubar)

        # Bind Event
        self.Bind(wx.EVT_MENU, self.ImportUrllist, id=11)
        self.Bind(wx.EVT_MENU, self.ExportUrllist, id=12)
        self.Bind(wx.EVT_MENU, self.OnExitApp, id=13)
        self.Bind(wx.EVT_MENU, self.XMLConfig, id=22)
        self.Bind(wx.EVT_MENU, self.BinaryConfig, id=23)

    def identifyOperatingSystem(self):
        """ Identify operating system to make GUI
        :Parameters
            none
        :Return
            none
        """
        isWindows = False
        isMacOS = False
        platform = sys.platform
        if platform == 'win32':
            isWindows = True
        elif platform == 'darwin':
                isMacOS = True
        elif platform == 'linux2':
                isMacOS = False

        return isWindows, isMacOS

    def ImportUrllist(self, event):
        """
        """
        pass

    def ExportUrllist(self, event):
        """
        """
        pass

    def XMLConfig(self, event):
        """"""
        self.FrameObject.setStreamMsgStatue(False)
        self.FrameObject.swapListCtrlLayout(self.FrameObject.XmlListCtrlId)

    def BinaryConfig(self, event):
        """"""
        self.FrameObject.setStreamMsgStatue(True)
        self.FrameObject.swapListCtrlLayout(self.FrameObject.BinaryListCtrlId)

    def OnExitApp(self, event):
        self.frame.Close(True)


# log output
def logfile():
    """ print traceback error to log.txt
    :log
        log/log.txt
    """
    log_dir = "./log"
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    time_str = time.strftime("%Y%m%d", time.localtime())
    file_name = log_dir + "/errorlog_" + time_str + ".txt"
    log_obj = open(file_name, "a+")
    time_str = time.strftime(" %Y-%m-%d %H:%M:%S START ", time.localtime())
    time_str = time_str.center(80, '*')
    log_obj.write(time_str + '\n')
    return log_obj


def closefile(logobj, Flag):
    """ close file """
    if Flag:
        traceback.print_exc(file=logobj)
    # end file
    logobj.write('\n' + " END ".center(80, '*') + '\n')
    logobj.close()


def getPanelThreadObj(obj, state):
    """get Panel Thread Obj"""
    global WEBSVC_AND_STATE
    WEBSVC_AND_STATE = [obj, state]


def webSvcStop():
    """ webSvcStop """
    obj = WEBSVC_AND_STATE[0]
    state = WEBSVC_AND_STATE[1]
    # webserver stop
    if state:
        obj.stop()


def main(log):
    app = RunDemoApp(None, -1, "Cloud Simulator", (830, 715), log)
    app.MainLoop()

if __name__ == "__main__":
    log_obj = None
    # 标志flag 标识异常traceback.print_exc日志打印（flag = True打印 False不打印traceback信息）
    flag = True
    try:
        log_obj = logfile()
        main(log_obj)
    except Exception as e:
        print e
    except BaseException as e:
        print e
    else:
        flag = False
    finally:
        # BaseException Process and Release external resources(Web Server or Network Connections)
        webSvcStop()
        # Close log file
        closefile(log_obj, flag)
