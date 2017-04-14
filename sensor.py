#!/usr/bin/python

from time import sleep
from sense_hat import SenseHat
from decimal import *
import traceback
import boto3
import datetime
import time
import sys
import os
from picamera import PiCamera
import threading
from botocore.exceptions import ClientError

s3_bucket = 'blackholegreenhouse'
photo_folder = 'photos'
log_interval = 300
log_file = './log.txt'
R = [255, 0, 0]
G = [0, 255, 0]
B = [0, 0, 255]
O = [0, 0, 0]  
success_pix = [
O, O, G, G, G, G, O, O,
O, G, O, O, O, O, G, O,
G, O, G, O, O, G, O, G,
G, O, O, O, O, O, O, G,
G, O, G, O, O, G, O, G,
G, O, O, G, G, O, O, G,
O, G, O, O, O, O, G, O,
O, O, G, G, G, G, O, O
]

s3 = boto3.client('s3')

dynamodb = boto3.resource('dynamodb')
sense = SenseHat()
camera = PiCamera()
table = dynamodb.Table('Greenhouse')
sense.low_light = True
sense.clear()

# get CPU temperature
def get_cpu_temp():
   res = os.popen("vcgencmd measure_temp").readline()
   t = float(res.replace("temp=","").replace("'C\n",""))
   return(t)

def get_gpu_temp():  
   res = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
   t = float(res)/1000
   return(t)

# convert float to a decimal string since dynamodb doesn't support floats
def floatToDec(float):
   return Decimal(str(float))

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

def display_error_led():
  sense.set_pixel(0, 0, 255, 0, 0)

def save_photo():
  now = str(datetime.datetime.utcnow())
  photo_file = '{}.jpg'.format(now)
  photo_path = '{}/{}'.format(photo_folder, photo_file)
  camera.capture(photo_path)
  try:
    s3.upload_file(photo_path, 
      s3_bucket, 
      photo_file, 
      Callback=ProgressPercentage(photo_path))
  except ClientError as e:
    print('error saving photo' + e.response['Error']['Code'])
    display_error_led()
     
  print('saved photo to s3')
  return (now, photo_file, photo_path)

def log_sensor():
  try:
    now, photo_file, photo_path = save_photo()
  except:
    print('error saving photo')
    display_error_led()
    return
  Item={
    'log': now,
    'date': int(time.time()), 
    'humidity': str(sense.get_humidity()),
    'pressure': str(sense.get_pressure()),
    'compass': str(sense.get_compass()),
    'temperature': str(sense.get_temperature()),
    'cpu_temp': str(get_cpu_temp()), 
    'gpu_temp': str(get_gpu_temp()),
    'temperature_from_humidity': str(sense.get_temperature_from_humidity()),
    'temperature_from_pressure': str(sense.get_temperature_from_pressure()),
    'photo': photo_file,
  }
  table.put_item(Item = Item)
  logitem = str(Item).replace("'", "").replace('{', '').replace('}', '')
  log = open(log_file, 'a')
  log.write(logitem + "\n")
  log.close()
  sense.set_pixels(success_pix)
  sleep(5)
  sense.clear()
  sense.set_pixel(0, 0, 0, 240, 0) 
  print(logitem)
  print('log saved to database')


def main():
  try:
    while True:
      log_sensor()
      sleep(log_interval)
  except KeyboardInterrupt:
    sense.clear()
    print "Exiting sensor logger"
  except Exception:
    display_error_led()    
    traceback.print_exc(file=sys.stdout)
  sys.exit(0)

if __name__ == "__main__":
    main()

