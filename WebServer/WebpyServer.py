# -*- coding: utf-8 -*-

import os, web
from MySQLconn import ExecSQL


LOG_OBJ = None
BinaryData = None


class index(object):

    def GET(self):
        referer = web.ctx.fullpath
        LOG_OBJ("URL: "+str(referer))
        web.header('content-type','application/xml;chartset=UTF-8')
        # get resp xml from db and resp to sender
        self.execsql = ExecSQL(LOG_OBJ)
        result = self.execsql.getDataResp(referer, None)
        if type(result) is str:
            return result
        elif type(result) is tuple:
            return result[0] + str(BinaryData) + result[1]
        if "URL Not Found!" == result:
            LOG_OBJ("RESPONSE: " + result)
        else:
            LOG_OBJ("RESPONSE: Success!")

    def POST(self):
        # Add header
        web.header('content-type','application/xml;chartset=UTF-8')
        web.header('Server','Apache-Coyote/1.1')
        web.header('Content-Language','zh-CN')
        web.header('Pragram','no-cache')
        web.header('Expires','Thu, 01 Jan 1970 00:00:00 GMT')
        web.header('Cache-Control','no-cache, no-store, max-age=0')
        # get xml body
        xmldata = web.data()
        referer = web.ctx.fullpath
        LOG_OBJ("URL: "+str(referer))
        LOG_OBJ("REQUEST: "+str(xmldata))
        # get resp xml from db and resp to sender
        self.execsql = ExecSQL(LOG_OBJ)
        result = self.execsql.getDataResp(referer,xmldata)
        if type(result) is str:
            return result
        elif type(result) is tuple:
            # result = result[0] + str(BinaryData) + result[1]
            # print result
            return result[0] + str(BinaryData) + result[1]
        if "URL Not Found!" == result:
            LOG_OBJ("RESPONSE: " + result)
        else:
            LOG_OBJ("RESPONSE: Success!")
        # insert request xml data to db
        # self.execsql = ExecSQL(LOG_OBJ)
        # self.execsql.insertXML2DB(referer, xmldata)
        return result

    def PUT(self):
        return self.POST()

    def DELETE(self):
        return self.POST()


class GetBinaryData(object):
    def __init__(self, binarydata):
        global BinaryData
        self.binarydata = binarydata
        BinaryData = self.binarydata


class MyWebServer(object):
    def __init__(self, log):
        global LOG_OBJ
        self.log = log
        LOG_OBJ = self.log
        self.urls = ('/.*', 'index')
        self.app = web.application(self.urls, globals())
        self.execsql = ExecSQL(self.log)

    def StartWeb(self, port=None):
        if port is None:
            self.app.run()
        else:
            os.environ['PORT'] = str(port)
            self.app.run()

    def StopWeb(self):
        self.app.stop()
