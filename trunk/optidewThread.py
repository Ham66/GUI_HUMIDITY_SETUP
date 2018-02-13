# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class OptidewThread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,optidew_server):
        QThread.__init__(self)
        print "Optidew thread: Starting thread"
        self.alive = True
        self.humidity = 0.00
        self.temperature = 0.00
        self.dewpoint = 0.00
        self.optidew_server = DeviceProxy(optidew_server)
        #if self.optidew_server.state() != DevState.ON:
        #    self.optidew_server.On()

    def stop(self):
        print "Optidew thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        print "Optidew thread: started"
        while self.alive:
            try:
                self.readAttributes()
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
                #time.sleep(0.5)
            time.sleep(0.3)       
        print "Optidew thread: died"

    def readAttributes(self):
        self.humidity = self.optidew_server.rh
        self.temperature = self.optidew_server.temperature
        self.dewpoint = self.optidew_server.dewpoint
    
