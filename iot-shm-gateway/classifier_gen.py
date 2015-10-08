__author__ = 'iot-shm'
import numpy as np
from sklearn import svm
from sklearn.externals import joblib

#Create X-Classifer
clf_x=svm.OneClassSVM(gamma=0.001)
print('x classifier made')
clf_x.fit(x_magfreq, sample_weight=None)
print('fitted x data')
joblib.dump(clf_x, 'xClf.pkl')
print('saved x data')

# Create Y-Classifier
clf_y=svm.OneClassSVM(gamma=0.001)
print('y classifier made')
clf_y.fit(y_magfreq, sample_weight=None)
print('fitted x data')
joblib.dump(clf_y, 'yClf.pkl')
print('saved y data')

# Create Z-Classifier
clf_z=svm.OneClassSVM(gamma=0.001)
print('z classifier made')
clf_z.fit(z_magfreq, sample_weight=None)
print('fitted z data')
joblib.dump(clf_z, 'yClf.pkl')
print('saved z data')