# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import configuration as conf
import sys
from MyException import *

reload(sys)
sys.setdefaultencoding("utf-8")


class Mysql():
    """connect db, execute sql, insert sql"""
    def __init__(self, m_host, m_port, m_user, m_password, m_dbname, m_cursorclass, LogPrint):

        self.logPrint = LogPrint
        self.err_text = "Error:in file MySQLconn.py of class Mysql(): method "
        try:
            self.conn = MySQLdb.connect(host=m_host, port=m_port, user=m_user, passwd=m_password, db=m_dbname, cursorclass=m_cursorclass)
            self.cur = self.conn.cursor()
        except TypeError as err:
            self.logPrint("TypeError:"+str(err))
            raise SQLconnError(self.err_text+"__init__ MySQLdb.connect :TypeError")
        except MySQLdb.Error as err:
            self.logPrint("Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise SQLconnError(self.err_text+"__init__ MySQLdb.connect")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"__init__ MySQLdb.connect")

    def query(self, sql):
        """
        query db func
        """
        try:
            data = self.cur.execute(sql)
        except UnicodeEncodeError as err:
            self.logPrint(self.err_text+"query sql execute error: %s" % err)
            raise SQLconnError(self.err_text+"query")
        except TypeError as err:
            self.logPrint(self.err_text+"query sql execute error: %s" % err)
            raise SQLconnError(self.err_text+"query")
        except Exception as err:
            self.logPrint(self.err_text+"query sql execute error: %s" % err)
            raise SQLconnError(self.err_text+"query")
        return data

    def queryall(self, sql):
        """queryall"""
        self.query(sql)
        return self.cur.fetchall()

    def insert(self, p_table_name, p_key, p_value):
        """insert"""
        # Exception Process
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            key = ",".join(p_key)
            for i in range(len(p_value)):
                if isinstance(p_value[i], unicode):
                    p_value[i] = p_value[i].replace("'", "\\'").encode('utf8')
            value = "'"+"','".join(p_value)+"'"
            real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
            query_result = self.query(real_sql)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"insert")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"insert")
        else:
            self.logPrint(real_sql, flag=False)
            self.logPrint("INSERT Success!")

        return query_result

    def delete(self, p_id,  p_table_name, p_key):
        """
        eg.
            DELETE FROM familie_test_guorui.`t_xml_conf` WHERE conf_id in (10,11)
        """
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            real_sql = "DELETE FROM " + table_name + " WHERE (" + p_key + ") IN (" + p_id + ")"
            query_result = self.query(real_sql)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"delete")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"delete")
        else:
            self.logPrint(real_sql, flag=False)
            self.logPrint("DELETE Success!")
        return query_result

    def alldelete(self, p_table_name):
        """
        eg.
            DELETE FROM familie_test_guorui.`t_xml_conf` WHERE conf_id in (10,11)
        """
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            real_sql = "DELETE FROM " + table_name
            # print real_sql
            query_result = self.query(real_sql)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"alldelete")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"alldelete")
        else:
            self.logPrint(real_sql, flag=False)
            self.logPrint("DELETE Success!")
        return query_result

    def update(self, listid, p_id, p_table_name, resp_val):
        """
        eg.
            UPDATE familie_test_guorui.`t_xml_conf` SET conf_response = 'guoup' WHERE conf_id = '22'
        """
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            if listid == 30:
                real_sql = "UPDATE " + table_name + " SET conf_response = \'" + str(resp_val).replace("'", "\\'").encode('utf-8') + "\' WHERE conf_id = \'" + p_id + "\'"
            else:
                # UPDATE `t_binary_conf` SET conf_before = 111, conf_after = 222  WHERE conf_id = 9
                real_sql = "UPDATE " + table_name + " SET conf_type = \'" + resp_val[0] + "\', conf_before = \'" + resp_val[1] + "\', conf_after = \'" + resp_val[2] + "\' WHERE conf_id = \'" + p_id + "\'"
                # print real_sql
            query_result = self.query(real_sql)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"update")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"update")
        else:
            self.logPrint(real_sql, flag=False)
            self.logPrint("UPDATE Success!")
        return query_result

    def getLastInsertId(self):
        return self.cur.lastrowid()

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class ExecSQL(object):
    """
        None
    """
    def __init__(self, LogPrint):
        self.logPrint = LogPrint
        self.err_text = "Error:in file MySQLconn.py of class ExecSQL():method "
        try:
            self.MySqlObj = Mysql(conf.DB_Address,conf.DB_Port,conf.DB_username,conf.DB_Passwd,conf.DB_Name, MySQLdb.cursors.DictCursor, LogPrint)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"__init__")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"__init__")

    def selectBut(self, list_id, url):
        """执行“Search”控件
            url: 传入textctr中过去的url值
            listid: 创建list的id [30=xml; 31=binary]
        """
        if list_id == 30:
            p_table_name = [conf.DB_Name,conf.Table_Name_XML]
        else:
            p_table_name = [conf.DB_Name,conf.Table_Name_Binary]

        # Exception process
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            sqlallrow = "SELECT * FROM " + table_name
            # 支持模糊查询
            sqlonerow = "SELECT * FROM " + table_name + " WHERE conf_url LIKE \'%" + url + "%\'"

            if url == "":
                QueryAllResult = self.MySqlObj.queryall(sqlallrow)
            else:
                QueryAllResult = self.MySqlObj.queryall(sqlonerow)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"selectBut")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"selectBut")
        finally:
            self.MySqlObj.close()
        return QueryAllResult

    def addSaveDataBut(self, listid, result):
        """add Save Data Button"""
        if listid == 30:
            p_table_name = [conf.DB_Name, conf.Table_Name_XML]
            table_key = ['conf_url', 'conf_response']
        else:
            p_table_name = [conf.DB_Name, conf.Table_Name_Binary]
            table_key = ['conf_url', 'conf_type', 'conf_before', 'conf_after']

        try:
            self.MySqlObj.insert(p_table_name, table_key, result)
            self.MySqlObj.commit()
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"addSaveDataBut")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"addSaveDataBut")
        finally:
            self.MySqlObj.close()

    def editSaveDataBut(self, listid, getlistitemid, result):
        if listid == 30:
            p_table_name = [conf.DB_Name,conf.Table_Name_XML]
        else:
            p_table_name = [conf.DB_Name,conf.Table_Name_Binary]
        try:
            self.MySqlObj.update(listid, getlistitemid, p_table_name, result)
            self.MySqlObj.commit()
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"editSaveDataBut")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"editSaveDataBut")
        finally:
            self.MySqlObj.close()

    def deleteBut(self, listid, getlistitemid):
        if listid == 30:
            p_table_name = [conf.DB_Name,conf.Table_Name_XML]
        else:
            p_table_name = [conf.DB_Name,conf.Table_Name_Binary]

        try:
            if getlistitemid == "":
                self.MySqlObj.alldelete(p_table_name)
            else:
                p_key = 'conf_id'
                conf_val = ",".join(getlistitemid)
                self.MySqlObj.delete(conf_val, p_table_name, p_key)
            self.MySqlObj.commit()
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"deleteBut")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"deleteBut")
        finally:
            self.MySqlObj.close()

    def getAll(self, listid, conf_id):
        """get url sql"""
        if listid == 30:
            p_table_name = [conf.DB_Name, conf.Table_Name_XML]
        else:
            p_table_name = [conf.DB_Name, conf.Table_Name_Binary]

        # Exception process
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            sqlonerow = "select * from " + table_name + " where conf_id = \'" + conf_id + "\'"
            QueryAllResult = self.MySqlObj.queryall(sqlonerow)
            # print QueryAllResult
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"geturlsql")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"geturlsql")
        finally:
            self.MySqlObj.close()
        return QueryAllResult

    def geturlsql(self, listid, url):
        """get url sql"""
        if listid == 30:
            p_table_name = [conf.DB_Name, conf.Table_Name_XML]
        else:
            p_table_name = [conf.DB_Name, conf.Table_Name_Binary]

        # Exception process
        try:
            table_name = "`"+"`.`".join(p_table_name) + "`"
            sqlonerow = "select conf_url from " + table_name + " where conf_url = \'" + url + "\'"
            QueryAllResult = self.MySqlObj.queryall(sqlonerow)
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"geturlsql")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"geturlsql")
        finally:
            self.MySqlObj.close()
        return QueryAllResult

    def insertXML2DB(self, p_url, p_data):
        """
            insert XML info to DB
        """
        try:
            p_table_name = [conf.DB_Name,conf.Table_Name_XML]
            table_name = "`"+"`.`".join(p_table_name) + "`"
            real_sql = "UPDATE " + table_name + " SET conf_request = \'" + p_data.replace("\'", "\\\'") + "\' WHERE conf_url = \'" + p_url + "\'"
            self.MySqlObj.query(str(real_sql))
            self.MySqlObj.commit()
            # else:
            #     self.logPrint("Request HTTP Body was exist")
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"insertXML2DB")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"insertXML2DB")
        finally:
            pass
            # self.MySqlObj.close()

    def getDataResp(self, url, xmldata):
        """
            get Data from Resp
        """
        try:
            p_table_name = [conf.DB_Name,conf.Table_Name_XML]
            table_name = "`"+"`.`".join(p_table_name) + "`"
            sql = "SELECT conf_response FROM " + table_name + " WHERE conf_url = '" + url + "'"
            url_result = self.MySqlObj.queryall(sql)
            self.MySqlObj.commit()
            if url_result == ():
                p_table_name = [conf.DB_Name,conf.Table_Name_Binary]
                table_name = "`"+"`.`".join(p_table_name) + "`"
                # SELECT conf_before,conf_after FROM t_binary_conf WHERE conf_url='123124'
                sql = "SELECT conf_before,conf_after FROM " + table_name + " WHERE conf_url = '" + url + "'"
                # url_result类型为元祖
                url_result = self.MySqlObj.queryall(sql)
                # ({'conf_after': '111', 'conf_before': '111'},)
                self.MySqlObj.commit()
                if url_result == ():
                    return "URL Not Found!"
                else:
                    # print url_result
                    # 将元祖解开后取出字典的value，以返回tuple
                    for i in url_result:
                        a = (i['conf_before'],i['conf_after'])
                        print a
                        return (i['conf_before'],i['conf_after'])
            else:
                # get方法xmldata值为None
                if xmldata != None:
                    self.insertXML2DB(url, xmldata)
                else:
                    pass
                # 将元祖解开后返回字典的value，返回值为str
                for i in url_result:
                    return i['conf_response']
        except SQLconnError as err:
            self.logPrint(err.arg)
            raise SQLconnError(self.err_text+"getDataResp")
        except Exception as err:
            self.logPrint(err)
            raise SQLconnError(self.err_text+"getDataResp")
        finally:
            self.MySqlObj.close()
