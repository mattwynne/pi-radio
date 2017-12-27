#!/usr/bin/env python
# Bare bones simple internet radio
# www.suppertime.co.uk/blogmywiki

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

CURRENT_STATION = '/home/pi/pi-radio/current-station'
NUM_STATIONS = 3

def get_current_station():
    os.system("touch %s" % CURRENT_STATION)
    f = open(CURRENT_STATION, 'r')
    station = int(f.read() or 1)
    f.close
    return station

def save_current_station(station):
    f = open(CURRENT_STATION, 'w')
    f.write('%d' % station)
    f.close

def play(station):
    os.system("mpc play " + str(station))

def play_next_station(channel):
    station = get_current_station() + 1
    if station > NUM_STATIONS:
        station = 1
    print(str(station))
    play(station)
    save_current_station(station)

GPIO.add_event_detect(23, GPIO.RISING, play_next_station)
while True:
  # slight pause to debounce
  time.sleep(0.05)
