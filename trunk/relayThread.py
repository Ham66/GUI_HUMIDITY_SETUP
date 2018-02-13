# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class RelayThread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,relay_server):
        QThread.__init__(self)
        print "Relay thread: Starting thread"
        self.alive = True
        self.relay1 = False
        self.relay2 = False
        self.relay3 = False
        self.relay4 = False
        self.relay_server = DeviceProxy(relay_server)        
               
        print "Relay thread: started"

    def stop(self):
        print "Relay thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        while self.alive:
            try:
                self.readAttributes()
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
            time.sleep(0.3)            
        print "Relay thread: died"

    def readAttributes(self):
        self.relay1 = self.relay_server.relay1
        self.relay2 = self.relay_server.relay2
        self.relay3 = self.relay_server.relay3
        self.relay4 = self.relay_server.relay4
    
    def switchRelay1(self):
        try:
            state = self.relay_server.relay1
            state = not state
            self.relay_server.relay1 = state
        except:
            self.emit(SIGNAL('connectionFailed()'))