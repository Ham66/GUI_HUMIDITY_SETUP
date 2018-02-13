# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class BronkhorstThread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,bronkhorst_server):
        QThread.__init__(self)
        print "Bronkhorst thread: Starting thread"
        self.alive = True
        self.flow = 0.00
        self.setpoint = 0.00
        self.bronkhorst_server = DeviceProxy(bronkhorst_server)
        print "Bronkhorst thread: started"

    def stop(self):
        print "Bronkhorst thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        while self.alive:
            try:
                self.readAttributes()
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
                #time.sleep(0.5)
            time.sleep(0.5)
        print "Bronkhorst thread: died"

    def readAttributes(self):
        self.flow = self.bronkhorst_server.Flow
        self.setpoint = self.bronkhorst_server.Setpoint
                    
    def setSetpoint(self, setpoint):
        try:
            self.bronkhorst_server.Set_setpoint = setpoint
        except:
            self.emit(SIGNAL('connectionFailed()'))
