#you should run this code on the Raspberry Pi
import socket
import RPi.GPIO as gpio
from threading import Thread
import dht11

class GPIOHandler(object):

        def __init__(self,output_list):
                gpio.setmode(gpio.BCM)
                gpio.setwarnings(False)
                gpio.setup(output_list,gpio.OUT)

        def setLow(self,pins):
                gpio.output(pins,gpio.LOW)

        def setHigh(self,pins):
                gpio.output(pins,gpio.HIGH)

        def shutdown(self,pins):
                gpio.cleanup(pins)

class WeatherThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sensor = dht11.DHT11(pin=12)

    def run(self):
        while True:
            try:
                result = self.sensor.read()
                if result.is_valid():
                    self.m = "%d;%d" % (result.humidity, result.temperature)
                    conn.send(self.m)
            except:
                break

if __name__ == '__main__':

    TCP_IP = '10.42.1.98'
    TCP_PORT = 5000
    BUFFER_SIZE = 100

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(2)
    conn, addr = s.accept()
    rooms = {'living_room': 21, 'bathroom': 26, 'kitchen': 23, 'hall': 13}
    gpiohandler = GPIOHandler(rooms.values())
    if conn:
        wthread = WeatherThread()
        wthread.start()

    def setgpio(m):
        if len(data) > 0:
            if m == 'living room on':
                gpiohandler.setHigh(rooms['living_room'])
            if m == 'living room off':
                gpiohandler.setLow(rooms['living_room'])
            if m == 'bathroom on':
                gpiohandler.setHigh(rooms['bathroom'])
            if m == 'bathroom off':
                gpiohandler.setLow(rooms['bathroom'])
            if m == 'kitchen on':
                gpiohandler.setHigh(rooms['kitchen'])
            if m == 'kitchen off':
                gpiohandler.setLow(rooms['kitchen'])
            if m == 'hall on':
                gpiohandler.setHigh(rooms['hall'])
            if m == 'hall off':
                gpiohandler.setLow(rooms['hall'])
            if m == 'clean':
                gpiohandler.setLow(rooms.values())
            if m == 'all on':
                gpiohandler.setHigh(rooms.values())


    print "got connection from %r" % conn
    while True:

        try:
            data = conn.recv(BUFFER_SIZE)
            if len(data) > 0:
                setgpio(data)

            else:
                s.listen(2)
                conn, addr = s.accept()
                data = conn.recv(BUFFER_SIZE)
                if conn:
                    wthread = WeatherThread()
                    wthread.start()
                    setgpio(data)
        except:
            continue
