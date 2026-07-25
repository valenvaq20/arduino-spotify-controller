from spotify_listener import SpotifyListener
from tray import TrayIcon
from serial_listener import SerialListener

from threading import Thread, Event
import time

import os

abierto = False
cerrar_programa = Event()


# ==============================
# EVENTOS DE SPOTIFY
# ==============================

def spotify_event(event, data):
    global abierto

    if event == "OPEN":
        abierto = True
        print("Spotify abierto")

    elif event == "CLOSE":
        abierto = False
        print("---------------")
        print("Spotify cerrado")


# ==============================
# CONTROL DE SPOTIFY
# ==============================

listener = SpotifyListener(spotify_event)
listener.start()


def pausar_reanudar():
    listener.toggle_play_pause()


def siguiente_cancion():
    listener.next()


def anterior_cancion():
    listener.previous()


# ==============================
# EVENTOS DEL PUERTO SERIE
# ==============================

def serial_event(datos):
    global abierto

    #if not abierto:
     #
     #    return

    comando = datos.decode(errors="ignore").strip()

    print("Serie:", comando)

    if comando == "12":
        pausar_reanudar()

    elif comando == "13":
        siguiente_cancion()

    elif comando == "11":
        anterior_cancion()

    elif comando == "10":
        os.startfile("spotify.exe")


serial_listener = SerialListener(
    "COM5",      # Cambiar por tu puerto
    9600,
    serial_event
)

serial_listener.start()


# ==============================
# ICONO EN BANDEJA
# ==============================

tray = TrayIcon(
    listener,
    cerrar_programa
)

Thread(
    target=tray.start,
    daemon=True
).start()


# ==============================
# BUCLE PRINCIPAL
# ==============================

while not cerrar_programa.is_set():
    time.sleep(1)
