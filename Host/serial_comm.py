import serial
import threading

class SerialManager:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.is_running = False
        
    def connect(self):
        # TODO: Initialize serial connection
        pass
        
    def start_threads(self):
        # TODO: Start Tx and Rx threads
        pass
