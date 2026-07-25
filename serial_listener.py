from threading import Thread
import serial


class SerialListener:

    def __init__(self, puerto, baudrate, callback):
        self.callback = callback

        self.ser = serial.Serial(
            puerto,
            baudrate,
            timeout=None
        )

    def start(self):
        Thread(
            target=self.run,
            daemon=True
        ).start()

    def run(self):
        while True:
            linea = self.ser.readline()

            if linea:
                self.callback(linea)