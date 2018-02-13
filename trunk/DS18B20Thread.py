# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class DS18B20Thread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,DS18B20_server):
        QThread.__init__(self)
        print "DS18B20 thread: Starting thread"
        self.alive = True
                
        self.temperature1 = 0
        self.temperature2 = 0
        self.temperature3 = 0
        self.temperature4 = 0
        self.temperature5 = 0
        self.temperature6 = 0
        self.temperature7 = 0
        self.temperature8 = 0
        
        self.states = [0, 0, 0, 0, 0, 0, 0, 0]
        
        self.DS18B20_server = DeviceProxy(DS18B20_server)
        """if self.DS18B20_server.state() == DevState.OFF:
            self.emit(SIGNAL('connectionFailed()'))
            self.alive == False"""

    def stop(self):
        print "DS18B20 thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        print "DS18B20 thread: started"
        while self.alive:
            try:
                self.readAttributes()
                """if self.temperature1 == -300.00:
                    self.states[0] = 1
                if self.temperature2 == -300.00:
                    self.states[1] = 1
                if self.temperature3 == -300.00:
                    self.states[2] = 1
                if self.temperature4 == -300.00:
                    self.states[3] = 1
                if self.temperature5 == -300.00:
                    self.states[4] = 1
                if self.temperature6 == -300.00:
                    self.states[5] = 1
                if self.temperature7 == -300.00:
                    self.states[6] = 1
                if self.temperature8 == -300.00:
                    self.states[7] = 1
                if (self.temperature1 != -300.00 and self.temperature2 != -300.00 and self.temperature3 != -300.00 
                    and self.temperature4 != -300.00 and self.temperature5 != -300.00 and self.temperature6 != -300.00 
                    and self.temperature7 != -300.00 and self.temperature8 != -300.00):
                    self.emit(SIGNAL("update()"))
                else:
                    self.emit(SIGNAL('connectionFailed()'), self.states)"""
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
            time.sleep(0.5)            
        print "DS18B20 thread: died"

    def readAttributes(self):
        self.temperature1 = self.DS18B20_server.temperature1
        self.temperature2 = self.DS18B20_server.temperature2
        self.temperature3 = self.DS18B20_server.temperature3
        self.temperature4 = self.DS18B20_server.temperature4
        self.temperature5 = self.DS18B20_server.temperature5
        self.temperature6 = self.DS18B20_server.temperature6
        self.temperature7 = self.DS18B20_server.temperature7
        self.temperature8 = self.DS18B20_server.temperature8