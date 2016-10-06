#!/usr/bin/python
from Form import *
from client import Client
from stream_manager import StreamReader
import sys
import threading
import Reminder
from PyQt4 import QtCore, QtGui
import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as figurecanvas
from time import sleep

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionReminder.triggered.connect(self.onreminder)
        self.ui.livroom_on.clicked.connect(self.livroom)
        self.ui.livroom_off.clicked.connect(self.livroom)
        self.ui.bathroom_on.clicked.connect(self.bathroom)
        self.ui.bathroom_off.clicked.connect(self.bathroom)
        self.ui.kitchen_on.clicked.connect(self.kitchen)
        self.ui.kitchen_off.clicked.connect(self.kitchen)
        self.ui.hall_on.clicked.connect(self.hall)
        self.ui.hall_off.clicked.connect(self.hall)
        self.my_stream_reader = StreamReader(url="http://10.42.0.98:8081")
        self.myclient = Client(('10.42.0.98',5000))
        self.myclient.connect()
        self.get_played()
        self.Harray = [0] * 20
        self.Tarray = [0]* 20
        self.X =  xrange(20)
        self.addplot()

        self.weather_thread = threading.Thread(target=self.updateWeather)
        self.weather_thread.setDaemon(True)
        self.weather_thread.start()

        self.plot_thread = threading.Thread(target=self.update_plot)
        self.plot_thread.setDaemon(True)
        self.plot_thread.start()

        #self.timer = QtCore.QBasicTimer()

        #self.timer.start(500,self)
    def addplot(self):

        self.fig1 = Figure()
        self.axf1 = self.fig1.add_subplot(111)
        self.axf1.grid()
        self.canvas = figurecanvas(self.fig1)
        self.ui.verticalLayout_3.addWidget(self.canvas)

        self.canvas.draw()

    """" def timerEvent(self,e):
        self.axf1.clear()
        self.axf1.grid()
        self.axf1.set_ylim([0, 100])
        self.axf1.set_ylim([0, 100])
        self.Harray.append(int(self.h))
        self.Tarray.append(int(self.t))
        del self.Harray[0]
        del self.Tarray[0]
        self.axf1.plot(self.X, self.Harray,lw=2,color="blue",label="Humidity(%)")
        self.axf1.plot(self.X, self.Tarray,lw=2,color="red",label="Temperature(*C)")
        self.canvas.draw()"""

    def onreminder(self):
        self.dial = Reminder.Dialog(self)
        self.dial.show()


    def livroom(self):
        if self.sender().text() == 'ON':
            self.myclient.send(message='living room on')
            self.ui.label.setPixmap(QtGui.QPixmap('icons/lighton.png'))
        if self.sender().text() == 'OFF':
            self.myclient.send(message='living room off')
            self.ui.label.setPixmap(QtGui.QPixmap('icons/lightoff.png'))

    def bathroom(self):
        if self.sender().text() == 'ON':
            self.myclient.send(message='bathroom on')
            self.ui.label_14.setPixmap(QtGui.QPixmap('icons/lighton.png'))
        if self.sender().text() == 'OFF':
            self.myclient.send(message='bathroom off')
            self.ui.label_14.setPixmap(QtGui.QPixmap('icons/lightoff.png'))

    def kitchen(self):
        if self.sender().text() == 'ON':
            self.myclient.send(message='kitchen on')
        if self.sender().text() == 'OFF':
            self.myclient.send(message='kitchen off')

    def hall(self):
        if self.sender().text() == 'ON':
            self.myclient.send(message='hall on')
        if self.sender().text() == 'OFF':
            self.myclient.send(message='hall off')

    def get_played(self):
        self.my_stream_reader.MultiplatformSupport(frame_obj=self.ui.video_frame)
        self.my_stream_reader.player.play()

    def updateWeather(self):
        while True:
            # noinspection PyBroadException
            try:
                #self.myclient.send(message='weather')
                self.h, self.t = self.myclient.receive().split(";")
                #self.ui.indoor_temp.setValue(float(self.t))
                #self.ui.indoor_hum.setValue(float(self.h))
                self.ui.lcdNumber.display(self.t)
                self.ui.lcdNumber_2.display(self.h)
            except:
                break


    def update_plot(self):
        while self.weather_thread.isAlive():

            try:
                self.axf1.clear()
                self.axf1.grid()
                self.axf1.set_ylim([0, 100])
                self.axf1.set_ylim([0, 100])

                self.Harray.append(int(self.h))
                self.Tarray.append(int(self.t))
                del self.Harray[0]
                del self.Tarray[0]

                while len(self.Harray) != len(self.Tarray):
                    self.Harray.append(int(self.h))
                    self.Tarray.append(int(self.t))
                    del self.Harray[0]
                    del self.Tarray[0]

                self.axf1.plot(self.X, self.Harray, lw=2, color="blue", label="Humidity(%)")
                self.axf1.plot(self.X, self.Tarray, lw=2, color="red", label="Temperature(*C)")
                self.canvas.draw()
                sleep(1)
            except:
                break

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    try:
        myapp = MainWindow()
        myapp.show()

    except:
        box = QtGui.QMessageBox().warning(w,"warning","Could not connect to the server\n Double check your connections and try again." )
        w.show()
        sys.exit()

    sys.exit(app.exec_())
