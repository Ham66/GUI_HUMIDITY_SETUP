# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class Sht75Thread1(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,sht75_server):
        QThread.__init__(self)
        print "DG4 thread: Starting thread"
        self.alive = True
        self.temperature = 0.00
        self.humidity = 0.00
        self.sht75_server1 = DeviceProxy(sht75_server)

    def stop(self):
        print "sht75 thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        print "sht75 thread: started"
        while self.alive:
            try:
                self.readAttributes()
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
                #time.sleep(0.5)
            time.sleep(0.3)       
        print "sht75 thread: died"

    def readAttributes(self):
        self.temperature = self.sht75_server1.Temperature
        self.humidity = self.sht75_server1.Humidity
        
