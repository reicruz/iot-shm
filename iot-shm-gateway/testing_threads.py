__author__ = 'rasha'
import time, threading
from collections import deque
import csv, numpy as np, datetime, uuid, threading, serial, time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from collections import deque
#import XBee
import json
import numpy as np
#from sklearn import svm
#from sklearn.externals import joblib
fft_size = 64
sensor_mac_addresses = []
mags = []
data_queue = deque([])

data_queue = deque([])
count = 0

#from sensor:
#unix time
#sensor/xbee id
#freq, xmag, ymag, zmag
#...

#initialize Kafka producer - send data to storm and to classifier node
class ZigbeeReceiver(threading.Thread):
    daemon = True

    def run(self):
        while True:
            global count
            data_queue.append(count)
            count += 1

class KafkaProducer(threading.Thread):
    daemon = True
   
    def run(self):
        while True:
             if len(data_queue)!=0:
                 print(data_queue.popleft())

def main():    
    global freq_array 
    client = KafkaClient('ip-172-31-28-55.ec2.internal:6667')
    producer = SimpleProducer(client)    
    
    fft_size=1000
    fs=92
    freq_array=np.array((1*fs/fft_size))
    for i in range(2,int(fft_size/2)):
        freq_i=np.array((i*fs/fft_size))
        freq_array=np.vstack((freq_array,freq_i))

    with open('xfourmag.csv', 'rt') as f:
        print('opening csv')
        reader=csv.reader(f)
        row = next(reader)
        #global mags
        mags = np.array(row)
        for row in reader:
            #mags += row
            mags = np.vstack((mags,row))
    #print(mags)
    #print(freq_array)	
    
    json_data = {'time': int(time.time()), 'fft': np.hstack((freq_array[0:31],mags[0:31])).tolist(), 'sensor_id': '1', 'reading_type': '0'}
    print('sending data...')
    producer.send_messages('shm', (json.dumps(json_data)).encode('utf-8')) 
    print('data sent! :)')

    #n = np.hstack((freq_array[0:31],mags[0:31]))
    #clf_x=svm.OneClassSVM(gamma=0.001)
    #print('x classifier made')
    #clf_x.fit(x_magfreq, sample_weight=None)
    #print('fitted x data')
    #joblib.dump(clf_x, 'xClf.pkl')
    #print('saved x data')   

    #threads = [
    #    KafkaProducer(),
        #KafkaConsumer(), #for classifying feature
    #	ZigbeeReceiver()
    #]

    #for t in threads:
    #    t.start()
    #time.sleep(5)

if __name__ == '__main__':
    main()


