import pystray
from PIL import Image, ImageDraw

import os
import sys

def recurso(nombre):
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)

    return os.path.join(base, nombre)

class TrayIcon:

    def __init__(self, listener, cerrar_event):
        self.listener = listener
        self.cerrar_event = cerrar_event
        # Crear un icono simple
        image = Image.open(recurso("imagen.png"))

        draw = ImageDraw.Draw(image)
        draw.text(
            (20, 20),
            "S",
            fill="white"
        )

        self.icon = pystray.Icon(
            "Spotify Controller",
            image,
            "Spotify Controller",
            menu=pystray.Menu(
                pystray.MenuItem(
                    "Salir",
                    self.exit
                )
            )
        )





    def exit(self, icon, item):
        icon.stop()
        self.cerrar_event.set()


    def start(self):
        self.icon.run()
