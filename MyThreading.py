# -*- coding: utf-8 -*-

import threading
import configuration as conf
from WebServer.WebpyServer import MyWebServer


class MyThread(threading.Thread):
    def __init__(self, log):
        """The timer class is derived from the class threading.Thread
        """
        threading.Thread.__init__(self)
        self.log = log
        self.MyWeb = MyWebServer(self.log)

    def run(self):
        """
        # Overwrite run() method, put what you want the thread do here
        """
        if conf.Web_Port is None or conf.Web_Port is '':
            self.MyWeb.StartWeb()
        else:
            self.MyWeb.StartWeb(conf.Web_Port)

    def stop(self):
        self.MyWeb.StopWeb()

