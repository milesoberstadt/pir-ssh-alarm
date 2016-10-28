import RPi.GPIO as GPIO
import time
from subprocess import call

inputPin = 11

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inputPin, GPIO.IN)

sshAddress = "username@hostname"

lastAlarm = 0
# This defines the frequency in seconds that the alarm can go off
alarmFrequency = 10

def alarm():
	global lastAlarm
	# Get the current unix timestamp...
	timestamp = int(time.time())
	if (timestamp > lastAlarm+alarmFrequency):
		lastAlarm = timestamp
		print("I'm not alone...")
		call(["ssh", sshAddress, "~/scripts/serverPIR.sh"])
	return

print("Script started, monitoring for monsters...")
while True:
        i=GPIO.input(inputPin)
        #print i
        if (i==1):
        	alarm()
        time.sleep(0.1)
