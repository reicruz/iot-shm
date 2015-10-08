import json
import datetime
import csv
import numpy as np
from sklearn import svm
from sklearn.externals import joblib

def makeFreqArray(fft_size,fs):
    freq_array=np.array(1*fs/fft_size)
    for i in range(2,int(fft_size/2)):
        freq_i=np.array(i*fs/fft_size)
        freq_array=np.vstack((freq_array,freq_i))
    return freq_array

def main():
    d={}
    with open('json_class3.csv', 'rU') as f:
        print('opening csv')
        reader=csv.reader(f)
        for row in reader:
            nprow=np.array(row)
            mags=nprow[5:len(nprow)]
            sensor_id=row[1].replace(' ','')
            reading_type=row[2].replace(' ', '')
            sampling_freq=nprow[0]
            fft_size=nprow[3]
            freq_array=makeFreqArray(int(fft_size),int(sampling_freq))
            mags.shape = (31,1)
            freq_mag_array=np.hstack((freq_array,mags))
            if sensor_id not in d:
                d[sensor_id]={}
                print(sensor_id)
            if reading_type not in d[sensor_id]:
                d[sensor_id][reading_type]=freq_mag_array
                print(reading_type)
            else:
                d[sensor_id][reading_type] = np.vstack((d[sensor_id][reading_type], freq_mag_array))
        for sensor in d:
            for axis in d[sensor]:
                classifier_array=d[sensor][axis]
                print(classifier_array)
                print(classifier_array.shape)
                print(sensor + "-" + axis)
                clf_axis=svm.OneClassSVM(gamma=0.001)
                clf_axis.fit(classifier_array)
                print('classifier made')
                joblib.dump(clf_axis, sensor + "-" + axis + ".pkl")
                print("saved " + sensor + "-" + axis)


if(__name__ == "__main__"):
    main()
