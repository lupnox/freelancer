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


pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

state = False
active = False
fade = 6500
pos = 0
last = 0
new = 0
msg = ''

tracks = ['./audio/2mov.mp3','./audio/4mov.mp3']
ntr = tracks.count()-1

btSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=1 )

sleep(2)

last = random.randint(0,ntr)
pygame.mixer.music.load(tracks[last])
new = random.randint(0,ntr)

while new == last:
    new = random.randint(0,ntr)

pygame.mixer.music.queue(tracks[new])
pygame.mixer.music.set_endevent ( pygame.USEREVENT )
last=new


def deactiv():
        global active
        global pos
        active = False
        pos = pygame.mixer.music.get_pos()
        pygame.mixer.music.fadeout(fade)
        

def start():
        global active
        global pos
        active = True
        pygame.mixer.music.play(0,pos,fade)


def read_bt():
        global msg
        print('Received: ' + msg)
        if "ACTIVO" in msg and not active:
            start()
        elif "PASIVO" in msg and active:
            deactiv()
        elif "ALTO" in msg and active:
            deactiv()
        elif "MANUAL" in msg and active:
            deactiv()



while True:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:    # A track has ended
            new = random.randint(0,ntr)
            while new == last:
                new = random.randint(0,ntr)
            pygame.mixer.music.queue(tracks[new])
            last=new
    msg = btSerial.readline()
    if len(msg) > 1:
        read_bt()
