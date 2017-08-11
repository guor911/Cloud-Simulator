# -*- coding: utf-8 -*-
"""
Used when use want to execute the camera test harness using command line
"""

# Function to set global value for supported camera API
# Do not make any changes in below method


# def generateSupportedCameraAPI():
#     global supportedCameraAPI
#     supportedCameraAPI = None
import os

curpath=os.getcwd()

# Currently supported routers are Netgear WNR1000 and WNR2000 
# supportedRouters = ['WNR1000', 'WNR2000']

# URL to get attached device information for different routers
# statusURLWNR1000 = 'http://{0}/RST_status.htm'
# deviceInfoURLWNR1000 = 'http://{0}/DEV_show_device.htm'
# fetchDeviceInfoRegexWNR1000 = 'var deviceIP_name\d+=\"(.*)\";'
# statusURLWNR2000 = 'http://{0}/RST_status.htm'
# deviceInfoURLWNR2000 = 'http://{0}/DEV_show_device.htm'
# fetchDeviceInfoRegexWNR2000 = 'var access_control_device\d+=\"Allowed\*(.*)\";'

# My Local DB
DB_Address = '192.168.139.206'
DB_Port = 3306
DB_username = 'root'
DB_Passwd = '12345678'
DB_Name = 'familie_test_guorui'
Table_Name_XML = 't_xml_conf'
Table_Name_Binary = 't_binary_conf'

# Testing Mysql DB Info
# DB_Address = '192.168.139.206'
# DB_Port = 3306
# DB_username = 'root'
# DB_Passwd = '123456'
# DB_Name = 'familie_test_guorui'
# Table_Name_XML = 't_xml_conf'
# Table_Name_Binary = 't_binary_conf'

# WebServer Port
Web_Port = 8080

# Camera Test Harness version
version = '0.6.00.000'

# failedOnXSD = True
