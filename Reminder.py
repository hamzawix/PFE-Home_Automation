from Reminder_ui import *
from PyQt4 import QtGui,QtCore
import multiprocessing
import time
from gi.repository import Notify
from time import sleep
from sys import exit

class Dialog(QtGui.QDialog):
    def __init__(self,p):
        QtGui.QDialog.__init__(self,p)
        self.dial_ui = Ui_Dialog()
        self.dial_ui.setupUi(self)
        self.dial_timer = QtCore.QBasicTimer()
        self.dial_timer.start(1000,self)
        QtCore.QObject.connect(self.dial_ui.buttonBox,QtCore.SIGNAL('accepted()'),self.onaccept)

    def timerEvent(self,e):
        self.dial_ui.lcdNumber.display(QtCore.QTime.currentTime().toString(QtCore.QString("hh:mm:ss")))

    def onaccept(self):
        self.title = self.dial_ui.title.text()
        self.com = self.dial_ui.comment.text()
        self.time = self.dial_ui.timeEdit.text()
        process = multiprocessing.Process(target=self.startreminder)
        process.start()

    def startreminder(self):
        Notify.init("reminder")
        summary = self.title
        body = self.com
        t = list(str(self.time))
        current_time = list(str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min))
        if len(current_time) == 5:
            del t[0]
        notification = Notify.Notification.new(str(summary),str(body),)
        while True:
            current_time = list(str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min))
            if current_time == t:
                notification.show()
                break
