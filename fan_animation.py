#!/usr/bin/python

from time import sleep
from sense_hat import SenseHat
import thread

sense = SenseHat()

image = 0
is_playing = False

def spin():
  global is_playing
  global image
  while is_playing:
    sense.load_image("led/fan{}.PNG".format(image))
    sleep(.05)
    image = image + 1
    if image > 4:
      image = 0
  sense.clear()

def play():
  global is_playing
  is_playing = True
  thread.start_new_thread(spin, ())

def stop():
  global is_playing
  is_playing = False

