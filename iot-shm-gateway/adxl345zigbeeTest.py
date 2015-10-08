import serial
import time

def adxl345Test():
	startTime = time.time()
	currTime = startTime
	print(startTime)
	print(currTime)
	ser = serial.Serial('/dev/tty.usbserial-DA013M0S', 9600)
	print("connected")
	while(True == True):
		currTime = time.time()
		print("about to read")
		reading = ser.readline()
		print(reading)
		#print(reading[:len(reading)-2] + "," + str(currTime) + "\n")
	ser.close()
if(__name__ == "__main__"):
	adxl345Test()
