# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class Sht75Thread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,sht75_server):
        QThread.__init__(self)
        print "DG4 thread: Starting thread"
        self.alive = True
        self.temperature1 = 0.00
        self.temperature2 = 0.00
        self.temperature3 = 0.00
        self.temperature4 = 0.00
        self.humidity1 = 0.00
        self.humidity2 = 0.00
        self.humidity3 = 0.00
        self.humidity4 = 0.00
        self.sht75_server1 = DeviceProxy(sht75_server[0])
        self.sht75_server2 = DeviceProxy(sht75_server[1])
        self.sht75_server3 = DeviceProxy(sht75_server[2])
        self.sht75_server4 = DeviceProxy(sht75_server[3])

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
                time.sleep(0.5)
            time.sleep(0.5)       
        print "sht75 thread: died"

    def readAttributes(self):
        self.temperature1 = self.sht75_server1.Temperature
        self.temperature2 = self.sht75_server2.Temperature
        self.temperature3 = self.sht75_server3.Temperature
        self.temperature4 = self.sht75_server4.Temperature
        self.humidity1 = self.sht75_server1.Humidity
        self.humidity2 = self.sht75_server2.Humidity
        self.humidity3 = self.sht75_server3.Humidity
        self.humidity4 = self.sht75_server4.Humidity
    
