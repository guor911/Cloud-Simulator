# -*- coding: utf-8 -*-

import urllib2
import sys

class FamilieSimulatorCommonFunctions():

    def __init__(self):
        # Intialize urllib for camera verification
        handler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)


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