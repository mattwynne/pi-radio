#!/usr/bin/env python
# Bare bones simple internet radio
# www.suppertime.co.uk/blogmywiki

import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

CURRENT_STATION = '/home/pi/pi-radio/current-station'

def num_stations():
    return len(filter(lambda x: len(x) > 0, subprocess.check_output(["mpc", "playlist"]).split("\n")))

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

def play_next_station():
    station = get_current_station() + 1
    if station > num_stations():
        station = 1
    play(station)
    save_current_station(station)

play(get_current_station())
while True:
    channel = GPIO.wait_for_edge(23, GPIO.RISING)
    if channel is not None:
        play_next_station()
