from ..model import Model
from sklearn.linear_model import LogisticRegression


class LogRegModel(Model):
    def __init__(self):
        super().__init__()
        self.recognizer = LogisticRegression(random_state=0,  max_iter=1000)

    def train(self, x, y):
        self.recognizer.fit(x, y)

    def predict(self, img):
        return self.recognizer.predict(img)

    def predict_proba(self, img):
        return self.recognizer.predict_proba(img)

    def read(self, face):
        pass

    def write(self, face):
        pass

    def compare(self, frame, boxes, font):
        pass


'''
from recognition.logreg import LogRegModel
from recognition import Detector
import numpy as np


input_folder = 'recognition/logreg/data/'
output_folder = 'recognition/logreg/out/'
model = LogRegModel()
val = list(Detector().get_data(input_folder, output_folder))
val[0] = np.array(val[0])
nsamples, nx, ny = val[0].shape
val[0] = val[0].reshape((nsamples,nx*ny))

input_folder = 'recognition/logreg/train/'
output_folder = 'recognition/logreg/out-2/'
now = list(Detector().get_data(input_folder, output_folder))
now[0] = np.array(now[0])
nsamples, nx, ny = now[0].shape
now[0] = now[0].reshape((nsamples, nx*ny))
now[1] += 1

data = [[], []]
for x in val[0]:
    data[0].append(x)
for x in val[1]:
    data[1].append(x)
for x in now[0]:
    data[0].append(x)
for x in now[1]:
    data[1].append(x)

model.train(*data)
test_folder = 'recognition/logreg/test/'
output_folder = 'recognition/logreg/out-3/'
test = Detector().get_data(test_folder, output_folder)[0]
test = np.array(test)

nsamples, nx, ny = test.shape
test = test.reshape((nsamples, nx*ny))
ans = model.predict_proba(test)
print(ans)
'''
