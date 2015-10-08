from kafka.client import KafkaClient
from kafka.consumer import KafkaConsumer
from kafka.producer import SimpleProducer

import numpy as np
from sklearn import svm
from sklearn.externals import joblib

import mysql.connector
from datetime import datetime

import json


client = KafkaClient("ip-172-31-28-55.ec2.internal:6667")
consumer = KafkaConsumer("shm", metadata_broker_list=['ip-172-31-28-55.ec2.internal:6667'])
#consumer = KafkaConsumer("shm", metadata_broker_list=['ip-172-31-28-55.ec2.internal:6667'])

conn = mysql.connector.connect(user='iotshm', password='pa$$word',
                              host='iotshm-data.ck3sx5qm0blx.us-west-2.rds.amazonaws.com',
                              database='iotshm')

cursor = conn.cursor()

#add_health = ("""INSERT IGNORE INTO iotshm.Health (sensor_id, timestamp, reading_type, healthy) VALUES (%s, %s, %s, %s)""")
add_magnitude = ("""INSERT IGNORE INTO iotshm.Magnitude (frequency, sensor_id, magnitude, reading_type, timestamp, healthy) VALUES(%s, %s, %s, %s, %s, %s)""")


# TODO add new classifier files and change file names
x_clf = joblib.load('xClf.pkl')
y_clf = joblib.load('xClf.pkl')
z_clf = joblib.load('xClf.pkl')


def getData():	
	data = consumer.next().value
	return data

def analyzeData(data):

	json_data = json.loads(data)

	sampling_freq = json_data['samplingFreq']
	sensor_id = json_data['sensorId']
	reading_type = json_data['readingType']
	time = datetime.fromtimestamp(int(json_data['time'])).strftime('%Y-%m-%d %H:%M:%S')

	mags = json_data['fftMags']
	fft_size = json_data['fftSize']
	freq_array = np.array((1 * sampling_freq / fft_size))
   	
	mags.pop(0)
    	mags_array = np.array(mags)[np.newaxis]
	mags_array = mags_array.transpose()

   	for i in range(2, int(fft_size/2)):
    		freq_i = np.array((i * sampling_freq / fft_size))
       		freq_array = np.vstack((freq_array, freq_i))

#	print(freq_array)
#	print(mags_array)
	
	if reading_type == 0:
		pred = x_clf.predict(np.hstack((freq_array, mags_array)))
	elif reading_type == 1:
		pred = y_clf.predict(np.hstack((freq_array, mags_array)))
	elif reading_type == 2:
		pred = z_clf.predict(np.hstack((freq_array, mags_array)))

	
	unhealthy = -1 in pred.tolist()

	mags_list = [x[0] for x in mags_array.tolist()]
	freq_list = [x[0] for x in freq_array.tolist()]

	#for i in range(0, len(mags_list)):
	
	data_magnitude = (str(freq_list)[1:-1], sensor_id, str(mags_list)[1:-1], reading_type, time, not unhealthy)
    	cursor.execute(add_magnitude, data_magnitude)

        #data_health = (sensor_id, time, reading_type, not unhealthy)
        #cursor.execute(add_health, data_health)
    
   	conn.commit()
	
    	return "sensor_id: " + str(sensor_id) + "\ntime: " + str(time) + "\nreading_type: " + str(reading_type) + "\nmags:  " + str(mags_list) + "\n"



while (True):
	data = getData()
    	print(analyzeData(data))


conn.close()



