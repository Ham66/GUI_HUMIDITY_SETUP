# -*- coding: utf-8 -*-
#import sys
from PyTango import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import thread
from PyQt4.QtCore import SIGNAL, QThread


class FestoThread(QThread):
    # A thread is started by calling QThread.start() never by calling run() directly!
    def __init__(self,festo_server):
        QThread.__init__(self)
        print "Festo thread: Starting thread"
        self.alive = True
        self.flow1 = 0.00
        self.flow2 = 0.00
        self.festo_server = DeviceProxy(festo_server)        
               
        print "Festo thread: started"

    def stop(self):
        print "Festo thread: Stopping thread"
        self.alive = False
        self.wait() # waits until run stops on his own

    def run(self):
        while self.alive:
            try:
                self.readAttributes()
                self.emit(SIGNAL("update()"))
            except:
                self.emit(SIGNAL('connectionFailed()'))
                time.sleep(0.5)
            time.sleep(0.5)       
        print "Festo thread: died"

    def readAttributes(self):
        self.flow1 = self.festo_server.actual_value1
        self.flow2 = self.festo_server.actual_value2
            
    def setFlow(self, flow):
        try:
            self.festo_server.set_flow = flow            
        except:
            self.emit(SIGNAL('connectionFailed()'))
