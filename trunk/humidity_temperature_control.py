#!/usr/bin/env python

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import QThread, SIGNAL
#from PyQt4.QtGui import QColor
#from PyQt4.Qwt5 import QwtPlot, QwtPlotCurve
import gui
#from relayThread import RelayThread
#from festoThread import FestoThread
from DS18B20Thread import DS18B20Thread
from optidewThread import OptidewThread
from dg4Thread import DG4Thread
from bronkhorstThread import BronkhorstThread
from sht75Thread1 import Sht75Thread1
from sht75Thread2 import Sht75Thread2
from sht75Thread3 import Sht75Thread3
from sht75Thread4 import Sht75Thread4
import sys
import PyTango
#import csv
import time
import numpy as np
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from collections import deque
#import pyqtgraph as pg
#import matplotlib.pyplot as plt
#import PyQt4.Qwt5 as Qwt
#import pygame as pg
#import Raspberry_SHT7x
#import os
#mutex = QtCore.QMutex()


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class LabelBlinkThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.alive = True
        self.running = False
        print "LabelBlinkThread thread: Starting thread"
        
    def run(self):
        print "LabelBlinkThread thread: started"
        while self.alive:
            while self.running:
                self.emit(SIGNAL("blink(int)"), 0)
                time.sleep(0.75)
            self.emit(SIGNAL("blink(int)"), 1)
            time.sleep(1)
        print "LabelBlinkThread thread: died"
    def stop(self):
        print "LabelBlinkThread thread: Stopping thread"
        self.alive = False
        self.running = False
        self.wait()


class Humidity_Temperature_control(QtGui.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        self.numberOfImage1 = 0
        self.numberOfImage2 = 0
        
        self.firstTimeDS18B20Update1 = True
        self.firstTimeDS18B20ConnectionFailed1 = True
        self.firstTimeDS18B20Update2 = True
        self.firstTimeDS18B20ConnectionFailed2 = True
        self.firstTimeDS18B20Update3 = True
        self.firstTimeDS18B20ConnectionFailed3 = True
        self.firstTimeDS18B20Update4 = True
        self.firstTimeDS18B20ConnectionFailed4 = True
        self.firstTimeDS18B20Update5 = True
        self.firstTimeDS18B20ConnectionFailed5 = True
        self.firstTimeDS18B20Update6 = True
        self.firstTimeDS18B20ConnectionFailed6 = True
        self.firstTimeDS18B20Update7 = True
        self.firstTimeDS18B20ConnectionFailed7 = True
        self.firstTimeDS18B20Update8 = True
        self.firstTimeDS18B20ConnectionFailed8 = True
        
        self.firstTimeBronkhorstUpdate = True
        self.firstTimeBronkhorstConnectionFailed = True
        
        self.firstTimeDG4Update = True
        self.firstTimeDG4ConnectionFailed = True
        
        self.firstTimeOptidewUpdate = True
        self.firstTimeOptidewConnectionFailed = True
        
        self.firstTimeSHT75Update1 = True
        self.firstTimeSHT75ConnectionFailed1 = True
        self.firstTimeSHT75Update2 = True
        self.firstTimeSHT75ConnectionFailed2 = True
        self.firstTimeSHT75Update3 = True
        self.firstTimeSHT75ConnectionFailed3 = True
        self.firstTimeSHT75Update4 = True
        self.firstTimeSHT75ConnectionFailed4 = True
        
        self.firstTimeHumidityWarning = True
        self.firstTimeHumidityOk = True
        
        self.firstTimeFlowWarning = True
        self.firstTimeFlowOk = True
        
        """QtCore.QObject.connect(self.pushButton_heater,QtCore.SIGNAL("clicked()"), self.switchRelay)
        self.relay = RelayThread("192.168.39.41:10000/p11/raspberry/relay")
        self.connect(self.relay, SIGNAL("update()"), self.relay_update)
        self.connect(self.relay, SIGNAL("connectionFailed()"), self.relay_connectionFailed)
        self.relay.start()"""
        
        """QtCore.QObject.connect(self.doubleSpinBox_set_flowFesto,QtCore.SIGNAL("valueChanged(double)"), self.setFlow)
        self.festo = FestoThread("192.168.39.41:10000/p11/mcp3002_mcp4921/festo")
        self.connect(self.festo, SIGNAL("update()"), self.festo_update)
        self.connect(self.festo, SIGNAL("connectionFailed()"), self.festo_connectionFailed)
        self.festo.start()"""
        
        """self.sht75 = Sht75Thread(["192.168.39.52:10000/p11/raspberry/sht75.01", "192.168.39.52:10000/p11/raspberry/sht75.02", "192.168.39.52:10000/p11/raspberry/sht75.03", "192.168.39.52:10000/p11/raspberry/sht75.04"])
        self.connect(self.sht75, SIGNAL("update()"), self.sht75_update)
        self.connect(self.sht75, SIGNAL("connectionFailed()"), self.sht75_connectionFailed)
        self.sht75.start()"""
        
        self.DS18B20 = DS18B20Thread("192.168.39.77:10000/humidity/ds18b20/ds18b20.01")
        self.connect(self.DS18B20, SIGNAL("update()"), self.DS18B20_update)
        self.connect(self.DS18B20, SIGNAL("connectionFailed()"), self.DS18B20_connectionFailed)
        self.DS18B20.start()
        
        self.optidew = OptidewThread("192.168.39.77:10000/humidity/optidew/optidew.01")
        self.connect(self.optidew, SIGNAL("update()"), self.optidew_update)
        self.connect(self.optidew, SIGNAL("connectionFailed()"), self.optidew_connectionFailed)
        self.optidew.start()
                    
        QtCore.QObject.connect(self.doubleSpinBox_dg4_set_humidity,QtCore.SIGNAL("valueChanged(double)"), self.setHumidity)
        self.dg4 = DG4Thread("192.168.39.77:10000/humidity/dg4/dg4.01")
        self.connect(self.dg4, SIGNAL("update()"), self.dg4_update)
        self.connect(self.dg4, SIGNAL("connectionFailed()"), self.dg4_connectionFailed)
        self.dg4.start()
        
        QtCore.QObject.connect(self.doubleSpinBox_set_setpointBronkhorst,QtCore.SIGNAL("valueChanged(double)"), self.setSetpoint)
        self.bronkhorst = BronkhorstThread("192.168.39.77:10000/humidity/bronkhorst/bronkhorst.01")
        self.connect(self.bronkhorst, SIGNAL("update()"), self.bronkhorst_update)
        self.connect(self.bronkhorst, SIGNAL("connectionFailed()"), self.bronkhorst_connectionFailed)
        self.bronkhorst.start()

        self.sht75_1 = Sht75Thread1("192.168.39.77:10000/humidity/sht75/sht75.01")
        self.connect(self.sht75_1, SIGNAL("update()"), self.sht75_update1)
        self.connect(self.sht75_1, SIGNAL("connectionFailed()"), self.sht75_connectionFailed1)
        self.sht75_1.start()
        
        self.sht75_2 = Sht75Thread2("192.168.39.77:10000/humidity/sht75/sht75.02")
        self.connect(self.sht75_2, SIGNAL("update()"), self.sht75_update2)
        self.connect(self.sht75_2, SIGNAL("connectionFailed()"), self.sht75_connectionFailed2)
        self.sht75_2.start()

        self.sht75_3 = Sht75Thread3("192.168.39.77:10000/humidity/sht75/sht75.03")
        self.connect(self.sht75_3, SIGNAL("update()"), self.sht75_update3)
        self.connect(self.sht75_3, SIGNAL("connectionFailed()"), self.sht75_connectionFailed3)
        self.sht75_3.start()

        self.sht75_4 = Sht75Thread4("192.168.39.77:10000/humidity/sht75/sht75.04")
        self.connect(self.sht75_4, SIGNAL("update()"), self.sht75_update4)
        self.connect(self.sht75_4, SIGNAL("connectionFailed()"), self.sht75_connectionFailed4)
        self.sht75_4.start()

        #self.imageChangeThread = ImageChangeThread(self.label, self.bronkhorst)
        #self.imageChangeThread.start()
        QtCore.QObject.connect(self.doubleSpinBox_sht75_humidity_3,QtCore.SIGNAL("valueChanged(double)"), self.humidityWarning)
        QtCore.QObject.connect(self.doubleSpinBox_flowBronkhorst,QtCore.SIGNAL("valueChanged(double)"), self.flowWarning)
        
        self.humidityBlinkThread = LabelBlinkThread()
        self.connect(self.humidityBlinkThread, SIGNAL("blink(int)"), self.blinkHumidity)
        self.blinkStateHumidity = True
        self.humidityBlinkThread.start()
        
        self.flowBlinkThread = LabelBlinkThread()
        self.connect(self.flowBlinkThread, SIGNAL("blink(int)"), self.blinkFlow)
        self.blinkStateFlow = True
        self.flowBlinkThread.start()

                
    def DS18B20_update(self):
        temperature7 = self.DS18B20.temperature7
        if temperature7 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed1:
                self.firstTimeDS18B20ConnectionFailed1 = False
                self.firstTimeDS18B20Update1 = True
                self.doubleSpinBox_sensor1_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor1_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update1:
                self.firstTimeDS18B20Update1 = False
                self.firstTimeDS18B20ConnectionFailed1 = True
                self.doubleSpinBox_sensor1_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor1_temperature.setValue(temperature7)
        temperature1 = self.DS18B20.temperature1
        if temperature1 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed2:
                self.firstTimeDS18B20ConnectionFailed2 = False
                self.firstTimeDS18B20Update2 = True
                self.doubleSpinBox_sensor2_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor2_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update2:
                self.firstTimeDS18B20Update2 = False
                self.firstTimeDS18B20ConnectionFailed2 = True
                self.doubleSpinBox_sensor2_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor2_temperature.setValue(temperature1)
        temperature2 = self.DS18B20.temperature2
        if temperature2 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed3:
                self.firstTimeDS18B20ConnectionFailed3 = False
                self.firstTimeDS18B20Update3 = True
                self.doubleSpinBox_sensor3_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor3_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update3:
                self.firstTimeDS18B20Update3 = False
                self.firstTimeDS18B20ConnectionFailed3 = True
                self.doubleSpinBox_sensor3_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor3_temperature.setValue(temperature2)
        temperature3 = self.DS18B20.temperature3
        if temperature3 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed4:
                self.firstTimeDS18B20ConnectionFailed4 = False
                self.firstTimeDS18B20Update4 = True
                self.doubleSpinBox_sensor4_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor4_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update4:
                self.firstTimeDS18B20Update4 = False
                self.firstTimeDS18B20ConnectionFailed4 = True
                self.doubleSpinBox_sensor4_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor4_temperature.setValue(temperature3)
        temperature4 = self.DS18B20.temperature4
        if temperature4 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed5:
                self.firstTimeDS18B20ConnectionFailed5 = False
                self.firstTimeDS18B20Update5 = True
                self.doubleSpinBox_sensor5_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor5_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update5:
                self.firstTimeDS18B20Update5 = False
                self.firstTimeDS18B20ConnectionFailed5 = True
                self.doubleSpinBox_sensor5_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor5_temperature.setValue(temperature4)
        temperature5 = self.DS18B20.temperature5
        if temperature5 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed6:
                self.firstTimeDS18B20ConnectionFailed6 = False
                self.firstTimeDS18B20Update6 = True
                self.doubleSpinBox_sensor6_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor6_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update6:
                self.firstTimeDS18B20Update6 = False
                self.firstTimeDS18B20ConnectionFailed6 = True
                self.doubleSpinBox_sensor6_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor6_temperature.setValue(temperature5)
        temperature6 = self.DS18B20.temperature6
        if temperature6 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed7:
                self.firstTimeDS18B20ConnectionFailed7 = False
                self.firstTimeDS18B20Update7 = True
                self.doubleSpinBox_sensor7_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor7_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update7:
                self.firstTimeDS18B20Update7 = False
                self.firstTimeDS18B20ConnectionFailed7 = True
                self.doubleSpinBox_sensor7_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor7_temperature.setValue(temperature6)
        temperature8 = self.DS18B20.temperature8
        if temperature8 == -300.00:
            if self.firstTimeDS18B20ConnectionFailed8:
                self.firstTimeDS18B20ConnectionFailed8 = False
                self.firstTimeDS18B20Update8 = True
                self.doubleSpinBox_sensor8_temperature.setStyleSheet("background-color: rgb(153,0,0);")
                self.doubleSpinBox_sensor8_temperature.setValue(-300)
        else:
            if self.firstTimeDS18B20Update8:
                self.firstTimeDS18B20Update8 = False
                self.firstTimeDS18B20ConnectionFailed8 = True
                self.doubleSpinBox_sensor8_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor8_temperature.setValue(temperature8)
        
        self.firstTimeDS18B20ConnectionFailed = True
        """if self.firstTimeDS18B20:
            self.firstTimeDS18B20 = False
            self.firstTimeDS18B20ConnectionFailed = True
            self.doubleSpinBox_sensor1_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor2_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor3_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor4_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor5_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor6_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor7_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sensor8_temperature.setStyleSheet("background-color: rgb(255,255,255);")
        
        temperature1 = self.DS18B20.temperature1
        temperature2 = self.DS18B20.temperature2
        temperature3 = self.DS18B20.temperature3
        temperature4 = self.DS18B20.temperature4
        temperature5 = self.DS18B20.temperature5
        temperature6 = self.DS18B20.temperature6
        temperature7 = self.DS18B20.temperature7
        temperature8 = self.DS18B20.temperature8
        self.doubleSpinBox_sensor1_temperature.setValue(temperature7)
        self.doubleSpinBox_sensor2_temperature.setValue(temperature1)
        self.doubleSpinBox_sensor3_temperature.setValue(temperature2)
        self.doubleSpinBox_sensor4_temperature.setValue(temperature3)
        self.doubleSpinBox_sensor5_temperature.setValue(temperature4)
        self.doubleSpinBox_sensor6_temperature.setValue(temperature5)
        self.doubleSpinBox_sensor7_temperature.setValue(temperature6)
        self.doubleSpinBox_sensor8_temperature.setValue(temperature8)"""
    
    def DS18B20_connectionFailed(self):
        if self.firstTimeDS18B20ConnectionFailed:
            self.firstTimeDS18B20ConnectionFailed = False
            #self.firstTimeDS18B20 = True
            self.doubleSpinBox_sensor1_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor1_temperature.setValue(0.00)
            self.doubleSpinBox_sensor2_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor2_temperature.setValue(0.00)
            self.doubleSpinBox_sensor3_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor3_temperature.setValue(0.00)
            self.doubleSpinBox_sensor4_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor4_temperature.setValue(0.00)
            self.doubleSpinBox_sensor5_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor5_temperature.setValue(0.00)
            self.doubleSpinBox_sensor6_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor6_temperature.setValue(0.00)
            self.doubleSpinBox_sensor7_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor7_temperature.setValue(0.00)
            self.doubleSpinBox_sensor8_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sensor8_temperature.setValue(0.00)
        
    def optidew_update(self):
        if self.firstTimeOptidewUpdate:
            self.firstTimeOptidewUpdate = False
            self.firstTimeOptidewConnectionFailed = True
            self.doubleSpinBox_optidew_humidity.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_optidew_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_optidew_dewpoint.setStyleSheet("background-color: rgb(255,255,255);")
        humidity = self.optidew.humidity
        temperature = self.optidew.temperature
        dewpoint = self.optidew.dewpoint
        self.doubleSpinBox_optidew_humidity.setValue(humidity)
        self.doubleSpinBox_optidew_temperature.setValue(temperature)
        self.doubleSpinBox_optidew_dewpoint.setValue(dewpoint)
    
    def optidew_connectionFailed(self):
        if self.firstTimeOptidewConnectionFailed:
            self.firstTimeOptidewConnectionFailed = False
            self.firstTimeOptidewUpdate = True
            self.doubleSpinBox_optidew_humidity.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_optidew_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_optidew_dewpoint.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_optidew_humidity.setValue(0.00)
            self.doubleSpinBox_optidew_temperature.setValue(0.00)
            self.doubleSpinBox_optidew_dewpoint.setValue(0.00)
    
    def dg4_update(self):
        if self.firstTimeDG4Update:
            self.firstTimeDG4Update = False
            self.firstTimeDG4ConnectionFailed = True
            self.doubleSpinBox_dg4_humidity1.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_dg4_humidity2.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_dg4_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_dg4_set_humidity.setStyleSheet("background-color: rgb(255,255,255);")
        humidity1 = self.dg4.humidity1
        humidity1 = float(humidity1)
        humidity2 = self.dg4.humidity2
        temperature = self.dg4.temperature
        temperature = float(temperature)
        self.doubleSpinBox_dg4_humidity1.setValue(humidity1)
        self.doubleSpinBox_dg4_humidity2.setValue(humidity2)
        self.doubleSpinBox_dg4_temperature.setValue(temperature)
        
    def dg4_connectionFailed(self):
        if self.firstTimeDG4ConnectionFailed:
            self.firstTimeDG4ConnectionFailed = False
            self.firstTimeDG4Update = True
            self.doubleSpinBox_dg4_humidity1.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_dg4_humidity2.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_dg4_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_dg4_set_humidity.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_dg4_humidity1.setValue(0.00)
            self.doubleSpinBox_dg4_humidity2.setValue(0.00)
            self.doubleSpinBox_dg4_temperature.setValue(0.00)
        
    def setHumidity(self):
        humidity = self.doubleSpinBox_dg4_set_humidity.value()
        self.dg4.setHumidity(humidity)
        
    def bronkhorst_update(self):
        if self.firstTimeBronkhorstUpdate:
            self.firstTimeBronkhorstUpdate = False
            self.firstTimeBronkhorstConnectionFailed = True
            self.doubleSpinBox_flowBronkhorst.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_setpointBronkhorst.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_set_setpointBronkhorst.setStyleSheet("background-color: rgb(255,255,255);")
        flow = self.bronkhorst.flow
        setpoint = self.bronkhorst.setpoint
        self.doubleSpinBox_flowBronkhorst.setValue(flow)
        self.doubleSpinBox_setpointBronkhorst.setValue(setpoint)
        if flow >= 0 and flow < 0.5:
            self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild0.png")))
        elif flow >= 0.5 and flow < 5:
            if self.numberOfImage1 == 0:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild1_1.png")))
            if self.numberOfImage1 == 1:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild1_2.png")))
            if self.numberOfImage1 == 2:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild1_3.png")))
            if self.numberOfImage1 == 3 or self.numberOfImage1 > 3:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild1_4.png")))
                self.numberOfImage1 = 0
            self.numberOfImage1 += 1
        elif flow > 5 or flow == 5:
            if self.numberOfImage2 == 0:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild2_1.png")))
            if self.numberOfImage2 == 1:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild2_2.png")))
            if self.numberOfImage2 == 2:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild2_3.png")))
            if self.numberOfImage2 == 3 or self.numberOfImage2 > 3:
                self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild2_4.png")))
                self.numberOfImage2 = 0
            self.numberOfImage2 += 1
        
    def bronkhorst_connectionFailed(self):
        if self.firstTimeBronkhorstConnectionFailed:
            self.firstTimeBronkhorstConnectionFailed = False
            self.firstTimeBronkhorstUpdate = True
            self.doubleSpinBox_flowBronkhorst.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_setpointBronkhorst.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_set_setpointBronkhorst.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_flowBronkhorst.setValue(0.00)
            self.doubleSpinBox_setpointBronkhorst.setValue(0.00)
            self.label.setPixmap(QtGui.QPixmap(_fromUtf8("Bild0.png")))
                
    def setSetpoint(self):
        setpoint = self.doubleSpinBox_set_setpointBronkhorst.value()
        self.bronkhorst.setSetpoint(setpoint)

    def sht75_update1(self):
        if self.firstTimeSHT75Update1:
            self.firstTimeSHT75Update1 = False
            self.firstTimeSHT75ConnectionFailed1 = True
            self.doubleSpinBox_sht75_temperature.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sht75_humidity.setStyleSheet("background-color: rgb(255,255,255);") 
        temperature = self.sht75_1.temperature
        humidity = self.sht75_1.humidity 
        self.doubleSpinBox_sht75_temperature.setValue(temperature)
        self.doubleSpinBox_sht75_humidity.setValue(humidity)
        
    def sht75_connectionFailed1(self):
        if self.firstTimeSHT75ConnectionFailed1:
            self.firstTimeSHT75ConnectionFailed1 = False
            self.firstTimeSHT75Update1 = True
            self.doubleSpinBox_sht75_temperature.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_humidity.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_temperature.setValue(0.00)
            self.doubleSpinBox_sht75_humidity.setValue(0.00)

    def sht75_update2(self):
        if self.firstTimeSHT75Update2:
            self.firstTimeSHT75Update2 = False
            self.firstTimeSHT75ConnectionFailed2 = True
            self.doubleSpinBox_sht75_temperature_1.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sht75_humidity_1.setStyleSheet("background-color: rgb(255,255,255);")
        temperature = self.sht75_2.temperature
        humidity = self.sht75_2.humidity
        self.doubleSpinBox_sht75_temperature_1.setValue(temperature)
        self.doubleSpinBox_sht75_humidity_1.setValue(humidity)
        
    def sht75_connectionFailed2(self):
        if self.firstTimeSHT75ConnectionFailed2:
            self.firstTimeSHT75ConnectionFailed2 = False
            self.firstTimeSHT75Update2 = True
            self.doubleSpinBox_sht75_temperature_1.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_humidity_1.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_temperature_1.setValue(0.00)
            self.doubleSpinBox_sht75_humidity_1.setValue(0.00)

    def sht75_update3(self):
        if self.firstTimeSHT75Update3:
            self.firstTimeSHT75Update3 = False
            self.firstTimeSHT75ConnectionFailed3 = True
            self.doubleSpinBox_sht75_temperature_2.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sht75_humidity_2.setStyleSheet("background-color: rgb(255,255,255);")    
        temperature = self.sht75_3.temperature
        humidity = self.sht75_3.humidity     
        self.doubleSpinBox_sht75_temperature_2.setValue(temperature)
        self.doubleSpinBox_sht75_humidity_2.setValue(humidity)
        
    def sht75_connectionFailed3(self):
        if self.firstTimeSHT75ConnectionFailed3:
            self.firstTimeSHT75ConnectionFailed3 = False
            self.firstTimeSHT75Update3 = True
            self.doubleSpinBox_sht75_temperature_2.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_humidity_2.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_temperature_2.setValue(0.00)
            self.doubleSpinBox_sht75_humidity_2.setValue(0.00)

    def sht75_update4(self):
        if self.firstTimeSHT75Update4:
            self.firstTimeSHT75Update4 = False
            self.firstTimeSHT75ConnectionFailed4 = True
            self.doubleSpinBox_sht75_temperature_3.setStyleSheet("background-color: rgb(255,255,255);")
            self.doubleSpinBox_sht75_humidity_3.setStyleSheet("background-color: rgb(255,255,255);")  
        temperature = self.sht75_4.temperature
        humidity = self.sht75_4.humidity
        self.doubleSpinBox_sht75_temperature_3.setValue(temperature)
        self.doubleSpinBox_sht75_humidity_3.setValue(humidity)
        
    def sht75_connectionFailed4(self):
        if self.firstTimeSHT75ConnectionFailed4:
            self.firstTimeSHT75ConnectionFailed4 = False
            self.firstTimeSHT75Update4 = True
            self.doubleSpinBox_sht75_temperature_3.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_humidity_3.setStyleSheet("background-color: rgb(153,0,0);")
            self.doubleSpinBox_sht75_temperature_3.setValue(0.00)
            self.doubleSpinBox_sht75_humidity_3.setValue(0.00)
        
    """def sht75_update(self):
        self.doubleSpinBox_sht75_temperature.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_temperature_1.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_temperature_2.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_temperature_3.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_humidity.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_humidity_1.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_humidity_2.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_sht75_humidity_3.setStyleSheet("background-color: rgb(255,255,255);")
        
        temperature1 = self.sht75.temperature1
        temperature2 = self.sht75.temperature2
        temperature3 = self.sht75.temperature3
        temperature4 = self.sht75.temperature4
        humidity1 = self.sht75.humidity1
        humidity2 = self.sht75.humidity2
        humidity3 = self.sht75.humidity3
        humidity4 = self.sht75.humidity4
        
        self.doubleSpinBox_sht75_temperature.setValue(temperature4)
        self.doubleSpinBox_sht75_temperature_1.setValue(temperature2)
        self.doubleSpinBox_sht75_temperature_2.setValue(temperature3)
        self.doubleSpinBox_sht75_temperature_3.setValue(temperature1)
        self.doubleSpinBox_sht75_humidity.setValue(humidity4)
        self.doubleSpinBox_sht75_humidity_1.setValue(humidity2)
        self.doubleSpinBox_sht75_humidity_2.setValue(humidity3)
        self.doubleSpinBox_sht75_humidity_3.setValue(humidity1)
        
    def sht75_connectionFailed(self):
        self.doubleSpinBox_sht75_temperature.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_temperature_1.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_temperature_2.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_temperature_3.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_humidity.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_humidity_1.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_humidity_2.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_sht75_humidity_3.setStyleSheet("background-color: rgb(153,0,0);")

        self.doubleSpinBox_sht75_temperature.setValue(0.00)
        self.doubleSpinBox_sht75_temperature_1.setValue(0.00)
        self.doubleSpinBox_sht75_temperature_2.setValue(0.00)
        self.doubleSpinBox_sht75_temperature_3.setValue(0.00)
        self.doubleSpinBox_sht75_humidity.setValue(0.00)
        self.doubleSpinBox_sht75_humidity_1.setValue(0.00)
        self.doubleSpinBox_sht75_humidity_2.setValue(0.00)
        self.doubleSpinBox_sht75_humidity_3.setValue(0.00)"""
        
    """def relay_update(self):
        state = self.relay.relay1
        if state:
            self.pushButton_heater.setText("Heater ON")
            self.pushButton_heater.setStyleSheet("background-color: rgb(0,153,0);")
        else:
            self.pushButton_heater.setText("Heater OFF")
            self.pushButton_heater.setStyleSheet("background-color: rgb(255,255,255);")
    
    def relay_connectionFailed(self):
        self.pushButton_heater.setText("Connection failed")
        self.pushButton_heater.setStyleSheet("background-color: rgb(153,0,0);")
    
    def switchRelay(self):
        self.relay.switchRelay1()"""
        
    """def festo_update(self):
        self.doubleSpinBox_flowFesto.setStyleSheet("background-color: rgb(255,255,255);")
        self.doubleSpinBox_set_flowFesto.setStyleSheet("background-color: rgb(255,255,255);")
        #self.doubleSpinBox_flow3.setStyleSheet("background-color: rgb(255,255,255);")
        flow1 = self.festo.flow1
        #flow2 = self.festo.flow2
        self.doubleSpinBox_flowFesto.setValue(flow1)
        #self.doubleSpinBox_flow2.setValue(flow2)
    
    def festo_connectionFailed(self):
        self.doubleSpinBox_flowFesto.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_set_flowFesto.setStyleSheet("background-color: rgb(153,0,0);")
        #self.doubleSpinBox_flow3.setStyleSheet("background-color: rgb(153,0,0);")
        self.doubleSpinBox_flowFesto.setValue(0.00)
        self.doubleSpinBox_set_flowFesto.setValue(0.00)
    
    def setFlow(self):
        flow = self.doubleSpinBox_set_flowFesto.value()
        self.festo.setFlow(flow)"""
        
    def humidityWarning(self):
        humidity1 = self.doubleSpinBox_sht75_humidity.value()
        humidity2 = self.doubleSpinBox_sht75_humidity_1.value()
        humidity3 = self.doubleSpinBox_sht75_humidity_2.value()
        humidity4 = self.doubleSpinBox_sht75_humidity_3.value() 
        humidityArray = [humidity1, humidity2, humidity3, humidity4]
        minHumidity = np.min(humidityArray)
        if minHumidity >= 95:
            if self.firstTimeHumidityOk:
                self.firstTimeHumidityOk = False
                self.firstTimeHumidityWarning = True
                self.humidityBlinkThread.running = False
                self.label_warning_humidity.setStyleSheet("background-color: rgb(144,238,144);")
                self.label_warning_humidity.setText("Humidity is OK")
        else:
            if self.firstTimeHumidityWarning:
                self.firstTimeHumidityWarning = False
                self.firstTimeHumidityOk = True
                self.humidityBlinkThread.running = True
                self.label_warning_humidity.setStyleSheet("background-color: rgb(255,160,122);")
                self.label_warning_humidity.setText("Humidity is LOW!!!")
    
    def flowWarning(self):
        flow = self.doubleSpinBox_flowBronkhorst.value()
        if flow >= 6:
            if self.firstTimeFlowOk:
                self.firstTimeFlowOk = False
                self.firstTimeFlowWarning = True
                self.flowBlinkThread.running = False
                self.label_warning_flow.setStyleSheet("background-color: rgb(144,238,144);")
                self.label_warning_flow.setText("Flow is OK")
        else:
            if self.firstTimeFlowWarning:
                self.firstTimeFlowWarning = False
                self.firstTimeFlowOk = True
                self.flowBlinkThread.running = True
                self.label_warning_flow.setStyleSheet("background-color: rgb(255,160,122);")
                self.label_warning_flow.setText("Flow is LOW!!!")
            
    def blinkHumidity(self, finished):
        if not finished:
            if self.blinkStateHumidity:
                self.blinkStateHumidity = False
                self.label_warning_humidity.show()
            else:
                self.blinkStateHumidity = True
                self.label_warning_humidity.hide()
        else:
            self.label_warning_humidity.show()
            
    def blinkFlow(self, finished):
        if not finished:
            if self.blinkStateFlow:
                self.blinkStateFlow = False
                self.label_warning_flow.show()
            else:
                self.blinkStateFlow = True
                self.label_warning_flow.hide()
        else:
            self.label_warning_flow.show()
            
        
    def __del__(self):
        self.DS18B20.stop()
        #self.relay.stop()
        #self.festo.stop()
        self.optidew.stop()
        self.dg4.stop()
        self.bronkhorst.stop()
        self.humidityBlinkThread.stop()
        self.flowBlinkThread.stop()

def main():
    app = QtGui.QApplication(sys.argv)
    form = Humidity_Temperature_control()
    #form.showFullScreen()
    form.show()
    app.exec_()
    


if __name__ == '__main__':
    main()
