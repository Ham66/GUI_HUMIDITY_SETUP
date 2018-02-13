# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class DG4Thread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,dg4_server):
        QThread.__init__(self)
        print "DG4 thread: Starting thread"
        self.alive = True
        self.humidity1 = 0.00
        self.humidity2 = 0.00
        self.temperature = 0.00
        self.dg4_server = DeviceProxy(dg4_server)
        #if self.dg4_server.state() != DevState.ON:
        #    self.dg4_server.On()

    def stop(self):
        print "DG4 thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        print "DG4 thread: started"
        while self.alive:
            try:
                self.readAttributes()
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
                #time.sleep(0.5)
            time.sleep(0.3)       
        print "DG4 thread: died"

    def readAttributes(self):
        self.humidity1 = self.dg4_server.humidity
        self.humidity2 = self.dg4_server.set_humidity_attribute
        self.temperature = self.dg4_server.temperature
            
    def setHumidity(self, humidity):
        try:
            self.dg4_server.set_humidity_attribute = humidity
        except:
            self.emit(SIGNAL('connectionFailed()'))