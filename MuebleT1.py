#Script base para pruebas con mueble 01/2021
#sudo rfcomm bind 0 A3:3A:11:08:96:8E 1
#@reboot /home/pi/on_reboot.sh
#t = Timer(300, deactiv)
#t.start()

from time import sleep
from threading import Timer
from random import randint
import serial
import pygame
import os


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.init()

active = False
fade = 25000
pos = 0
last = 0
new = 0
msg = ''
trigs = [b'ACTUALIZA\r\n',b'ACTIVO\r\n']
shuts = [b'PASIVO\r\n',b'MANUAL\r\n',b'ALTO\r\n']

tracks = ['/home/pi/Desktop/ManzoArt/audio/2mov1.wav','/home/pi/Desktop/ManzoArt/audio/2mov2.wav','/home/pi/Desktop/ManzoArt/audio/2mov3.wav','/home/pi/Desktop/ManzoArt/audio/2mov4.wav','/home/pi/Desktop/ManzoArt/audio/4mov1.wav','/home/pi/Desktop/ManzoArt/audio/4mov2.wav']
ntr = len(tracks)-1

btSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=1 )

sleep(2)

pygame.mixer.music.set_endevent ( pygame.USEREVENT )

def deactiv():
        global active
        global pos
        print("Stopping")
        active = False
        pygame.mixer.music.fadeout(fade)

def start():
        global pos
        global active
        global last
        global new
        print("Playing ")
        active = True
        last = randint(0,ntr)
        pygame.mixer.music.load(tracks[last])
        new = randint(0,ntr)
        while new == last:
            new = randint(0,ntr)

        last = new
        pygame.mixer.music.queue(tracks[new])
        pygame.mixer.music.play(loops=0,start=pos,fade_ms=fade)

def read_bt():
        global msg
        global active
        print('Received: ' + msg.decode('utf-8'))
        if msg in trigs and not active:
            start()
        elif msg in shuts and active:
            deactiv()

def send_bt(pump_com):
        print('Sending: '+pump_com)
        btSerial.write(pump_com.encode())

send_bt('READY')
while True:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:    # A track has ended
            print('NEW QUEUE')
            new = randint(0,ntr)
            while new == last:
                new = randint(0,ntr)
            pygame.mixer.music.queue(tracks[new])
            last=new
    try:
        msg = btSerial.readline()
        if len(msg) > 1:
            read_bt()
    except:
        print("Error con controlador. Reiniciando..")
       # os.system("sudo reboot")
