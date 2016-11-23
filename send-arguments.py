#!/usr/bin/env python

"""send-joystick.py: Reads a command device using pygame and sends the information via UDP."""

__original_author__ = "Aldo Vargas"
__author__ = "Hussain Alamood"

__version__ = "0.1"
__maintainer__ = "Hussain Alamood"
__email__ = "hualamood@gmail.com"
__status__ = "Development"

import time
import datetime
import socket, struct
from modules.utils import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="The action you want to take", type=str)
parser.add_argument("-t", "--time",help="The duration you want the action to be done in seconds", type=str)
parser.add_argument("-i", "--intensity",help="The intensity of the action (between 0.1 - 0.999)", type=float)
args = vars(parser.parse_args())

if args.get("action", None) is None:
    print "Please set the -a parameter"
    exit()
else:
    command = args["action"]

if args.get("time", None) is None:
    print "Please set the -t parameter"
    exit()
else:
    duration = args["time"]

if args.get("intensity", None) is None:
    print "Please set the -i parameter"
    exit()
else:
    intensity = args["intensity"]



def addtime(duration, currentTime):
    wantedTime = currentTime + (int(duration))
    return wantedTime

def getIntensity(command, intensity, givenVar):
    # print command
    # print givenVar
    if givenVar == command:
        return intensity
    else:
        return 0

# Main configuration
UDP_IP = "127.0.0.1" # Localhost (for testing)
#UDP_IP = "10.42.0.54" # Ip address for raspberry pi connected via ethernet
UDP_PORT = 51001 # This port match the ones using on other scripts

update_rate = 0.01 # 100 hz loop cycle
# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Break = True
used = 0

while True:
    if Break == False:
        currentTime = int(str(time.time()).split(".")[0])
        #print command
        #print intensity
        print datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
        #print currentTime
        print datetime.datetime.fromtimestamp(wantedTime).strftime('%Y-%m-%d %H:%M:%S')
        #print wantedTime
        current = time.time()
        elapsed = 0

        # Joystick reading
        #pygame.event.pump()
        roll     = mapping(getIntensity(command, intensity, "roll"),-1.0,1.0,1000,2000)
        pitch    = mapping(getIntensity(command, intensity, "pitch"),1.0,-1.0,1000,2000)
        yaw      = mapping(getIntensity(command, intensity, "yaw"),-1.0,1.0,1000,2000)
        throttle = mapping(getIntensity(command, intensity, "throttle"),1.0,-1.0,1000,2000)
        #mode     = joystick.get_button(24)

        # Be sure to always send the data as floats
        # The extra zeros on the message are there in order for the other scripts to do not complain about missing information
        message = [roll, pitch, yaw, throttle, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        buf = struct.pack('>' + 'd' * len(message), *message)
        sock.sendto(buf, (UDP_IP, UDP_PORT))

        print message

        # Make this loop work at update_rate
        while elapsed < update_rate:
            elapsed = time.time() - current
        if wantedTime == currentTime:
            Break = True
    elif Break == True:
        currentTime = int(str(time.time()).split(".")[0])
        wantedTime = addtime(duration, currentTime)
        if used >= 1:
            exit()
        else:
            used += 1
            Break = False

    time.sleep(1)
