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

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

active = False
fade = 10000
pos = 0
last = 0
new = 0
msg = ''
trigs = [b'ACTUALIZA\r\n',b'ACTIVO\r\n']
shuts = [b'PASIVO\r\n',b'MANUAL\r\n',b'ALTO\r\n']

tracks = ['/home/pi/Desktop/ManzoArt/audio/2mov.mp3','/home/pi/Desktop/ManzoArt/audio/4mov.mp3']
ntr = len(tracks)-1

btSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=1 )

sleep(2)

last = randint(0,ntr)
pygame.mixer.music.load(tracks[last])
new = randint(0,ntr)

while new == last:
    new = randint(0,ntr)

pygame.mixer.music.queue(tracks[new])
pygame.mixer.music.set_endevent ( pygame.USEREVENT )
last=new


def deactiv():
        global active
        global pos
        print("Stopping")
        active = False
        pos = pygame.mixer.music.get_pos()/1000
        pygame.mixer.music.fadeout(fade)

def start():
        global pos
        global active
        print("Playing ")
        active = True
        pygame.mixer.music.play(loops=0,start=pos,fade_ms=fade)


def read_bt():
        global msg
        global active
        print('Received: ' + msg.decode('utf-8'))
        if msg in trigs and not active:
            start()
        elif msg in shuts and active:
            deactiv()



while True:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:    # A track has ended
            new = randint(0,ntr)
            while new == last:
                new = randint(0,ntr)
            pygame.mixer.music.queue(tracks[new])
            last=new
    msg = btSerial.readline()
    if len(msg) > 1:
        read_bt()
