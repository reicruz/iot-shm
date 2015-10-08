from kafka.client import KafkaClient
from kafka.consumer import KafkaConsumer
from kafka.producer import SimpleProducer
import json
import datetime


client = KafkaClient("ip-172-31-28-55.ec2.internal:6667")
consumer = KafkaConsumer("shm", metadata_broker_list=['ip-172-31-28-55.ec2.internal:6667'])
#consumer = KafkaConsumer("shm", metadata_broker_list=['ip-172-31-28-55.ec2.internal:6667'])

def getData():	
	data = consumer.next().value
	return data

def parseData(data):
    json_data=json.loads(data)
    sampling_freq = json_data['samplingFreq']
    sensor_id = json_data['sensorId']
    reading_type = json_data['readingType']
    mags = json_data['fftMags']
    fft_size = json_data['fftSize']
    output = str(sampling_freq) + ", " + str(sensor_id) + ", " + str(reading_type) + ", " + str(fft_size) + ", "
    for x in mags:
        output += str(x) + ", "
    return output[:-2]

def writeData(outfile, parsed):
    outfile.write(parsed + "\n")
        
def main():
    f = open('json_class3.csv', 'w')
    start = datetime.datetime.now().time()
    x = 0
    while (x < 32400):
        data = getData()
        #print(data)
        parsed=parseData(data)
        #print(parsed)
        writeData(f, parsed)
        #print(parsed)
        x+=1
        if x%30==0:
            print(x)
            print(parsed)
    f.close()

if(__name__ == "__main__"):
    main()
