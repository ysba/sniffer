import yaml
import time
import threading
import serial
import modbus


class Sniffer:
    def __init__(self, config_file):
        self.config_file = config_file
        self.threads = []

    
    def run(self):
        self.config_load() 
        self.run = True
        self.tick_last = int(time.time() * 1000)
        print("start")
        for thread in self.threads:
            thread.start()
        while self.run == True:
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("stop")
                self.run = False
        for thread in self.threads:
            thread.join()
        print("exit")


    def config_load(self):
        with open(self.config_file, "r") as file:
            config_data = yaml.safe_load(file)
        sniffers = config_data["sniffer"]
        for sniffer in sniffers:
            print(sniffer["protocol"], sniffer["uart"], sniffer["port"])
            baudrate, data_bits, parity, stop_bits = sniffer["uart"].split(",")
            com = serial.Serial()
            com.baudrate = int(baudrate)
            if parity == "N":
                com.parity = serial.PARITY_NONE
            elif parity == "E":
                com.parity = serial.PARITY_EVEN
            elif parity == "O":
                com.parity = serial.PARITY_ODD
            com.port = sniffer["port"]
            com.timeout = 1/com.baudrate*11*3.5
            if sniffer["protocol"] == "modbus":
                print("ok")
                self.threads.append(threading.Thread(target=self.rx_thread, args=(com, modbus.modbus_parser)))
            elif sniffer["protocol"] == "monitoring":
                print("ok")
                self.threads.append(threading.Thread(target=self.rx_thread, args=(com, None)))
            else:
                print("invalid")
            print("")
        
    
    def rx_thread(self, com, parser):
        print("rx thread enter", com.port)
        try:
            com.open()
        except:
            print("rx thread exit", com.port, " error opening port")
            return
        buffer = []
        while self.run == True:
            rx = com.read()
            if len(rx) > 0:
                buffer += rx
            elif len(rx) == 0:
                if len(buffer) > 0:
                    parser(buffer)
                    self.log()
                    buffer = []
        com.close()
        print("rx thread exit", com.port)


    def log(self):
        tick_current = int(time.time() * 1000)
        tick_diff = tick_current - self.tick_last
        self.tick_last = tick_current
        print("log", tick_diff)



