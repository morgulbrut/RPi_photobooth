#!/usr/bin/python3

import RPi.GPIO as GPIO, time, os, subprocess

import http.server
import socketserver
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN)
RESET = 25
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23


def start_webserver(directory):
    PORT = 8000

    pwd = os.curdir
    os.chdir('/home/pi/PB_archive')

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()

    os.chdir(pwd)


def setup_io():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SWITCH, GPIO.IN)
    GPIO.setup(RESET, GPIO.IN)
    GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

while True:
  if (GPIO.input(SWITCH)):
    snap = 0
    while snap < 4:
      print("pose!")
      GPIO.output(BUTTON_LED, False)
      GPIO.output(POSE_LED, True)
      time.sleep(1.5)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED, True)
        time.sleep(0.4)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      GPIO.output(POSE_LED, False)
      print("SNAP")
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      if "ERROR" not in gpout: 
        snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(0.5)
def wait_for_camera():
    cam_ready = False
    print("Waiting for camera")
    while cam_ready == False:
        GPIO.output(PRINT_LED, False)
        time.sleep(0.2)
        try: 
            gpout = subprocess.check_output("gphoto2 -l", stderr=subprocess.STDOUT, shell=True)
            print(gpout)
            cam_ready = True
        except:
            print("...")
        GPIO.output(PRINT_LED, True)
        time.sleep(0.2)
            wait_for_camera()
    print("please wait while your photos print...")
    GPIO.output(PRINT_LED, True)
    # build image and send to printer
    subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    time.sleep(110)
    print("ready for next round")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
