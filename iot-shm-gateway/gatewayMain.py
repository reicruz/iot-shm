__author__ = 'rasha'
import csv, numpy as np, datetime, uuid, threading, serial, time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from collections import deque
from xbee import ZigBee
import json
import serial
import struct
import time

sensor_mac_addresses = []
data_queue = deque([])
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

TIME_SIZE = 4
TYPE_SIZE = 1
SAMPLING_FREQ_SIZE = 4
FFT_SIZE_SIZE = 4

class SensorPacket:
    def __init__(self, sensorId, time, readingType, samplingFreq, fftSize, fftMags):
        self.sensorId = sensorId
        self.time = time
        self.readingType = readingType
        self.samplingFreq = samplingFreq
        self.fftSize = fftSize
        self.fftMags = fftMags
    def __str__(self):
        return "sensorId="+self.sensorId + ", time=" + str(self.time) + ", readingType=" + str(self.readingType) + ", samplingFreq="+str(self.samplingFreq) + ", fftSize=" + str(self.fftSize) + ", fftMags=" + str(self.fftMags)

    def toJson(self):
        data = {"sensorId":self.sensorId, "time":self.time, "readingType":self.readingType, "samplingFreq":self.samplingFreq, "fftSize":self.fftSize, "fftMags":self.fftMags}
        return json.dumps(data).encode('utf-8')

class XBeeReceiver(threading.Thread):
    daemon = True

    def bytesToInt(self, arr):
        return int.from_bytes(arr, byteorder='little', signed=False)

    def parse(self, response):
        try:
            payload = response["rf_data"]
            sensorId = (''.join('{:02x}-'.format(x) for x in response["source_addr_long"]))[:-1]
            data_length = len(payload)
            currTime = int(time.time())

            type_start = 0
            readingTypeArr = payload[type_start : type_start + TYPE_SIZE]
            readingType = self.bytesToInt(readingTypeArr)       
            
            sampling_freq_start = type_start + TYPE_SIZE
            samplingFreqArr = payload[sampling_freq_start : sampling_freq_start + SAMPLING_FREQ_SIZE]
            samplingFreq = self.bytesToInt(samplingFreqArr) 

            fft_size_start = sampling_freq_start + SAMPLING_FREQ_SIZE
            fftSizeArr = payload[fft_size_start : fft_size_start + FFT_SIZE_SIZE]
            fftSize = self.bytesToInt(fftSizeArr)

            fft_start = fft_size_start + FFT_SIZE_SIZE        
            fftMags = [x for x in payload[fft_start:fft_start + int(fftSize/2)]]
            return SensorPacket(sensorId, currTime, readingType, samplingFreq, fftSize, fftMags)
        except Exception:
            print("null")
            return None


    def run(self):
        stop = False
        ser = serial.Serial(PORT, BAUD_RATE)
        xbee = ZigBee(ser)
        i = 0
        count = 0
        while(True):
            response = xbee.wait_read_frame()
            parsed = self.parse(response)
            if(self.parse(response) != None):
                if(len([x for x in parsed.fftMags if(x == 0)]) == len(parsed.fftMags)):
                    count+= 1
                    print("TOTAL NONZEROS THUS FAR: " + str(count))
                else:
                    data_queue.append(parsed)
        ser.close

#format data and send to Kafka
class KafkaProducer(threading.Thread):
    daemon = True

    def run(self):
        client = KafkaClient('ip-172-31-28-55.ec2.internal:6667')
        producer = SimpleProducer(client)        
        x = 0
        while True:
            if len(data_queue)!=0:
                data = data_queue.popleft()
                json = data.toJson()
                #if(x%30 == 0 or x%30 == 1 or x%30 == 2):
                print(json)
                x+=1
                if True: # for when we send to storm topic
                    producer.send_messages('shm', json)
                else: # for when we send to create the classifier
                    producer.send_messages('classifier_topic',data)

#check if building needs to be classified or analyzed
#class KafkaConsumer(threading.Thread):
#    daemon = True
#
#    def run(self):
#        client = KafkaClient('ip-72-131-4-78-ec2.internal:6667')
#        consumer = SimpleConsumer(client, 'building_status_topic')
#
#        for message in consumer:
#            print(message)

def main():    
    threads = [
        KafkaProducer(),
        #KafkaConsumer(), #for classifying feature
	XBeeReceiver()
    ]

    for t in threads:
        t.start()
    time.sleep(5)
    while(True):
        print

if __name__ == '__main__':
    main()

