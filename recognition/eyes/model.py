import os
from PIL import Image
import numpy as np

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import AveragePooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator

from imageio import imread
from cv2 import resize as imresize
from imageio import imwrite as imsave
from .config import EyeConfig


def collect():
    train_datagen = ImageDataGenerator(**EyeConfig.IMAGE_GENERATOR_ARGS)
    val_datagen = ImageDataGenerator(**EyeConfig.IMAGE_GENERATOR_ARGS)
    train_generator = train_datagen.flow_from_directory(directory=EyeConfig.FOLDER + "dataset/train", **EyeConfig.DATASETS_INFO)
    val_generator = val_datagen.flow_from_directory(directory=EyeConfig.FOLDER + "dataset/val", **EyeConfig.DATASETS_INFO)
    return train_generator, val_generator


def save_model(model):
    model_json = model.to_json()
    with open(EyeConfig.FOLDER + "model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights(EyeConfig.FOLDER + "model.h5")


def load_model():
    json_file = open(EyeConfig.FOLDER + 'model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(EyeConfig.FOLDER + "model.h5")
    loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return loaded_model


def train(train_generator, val_generator):
    STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
    STEP_SIZE_VALID = val_generator.n // val_generator.batch_size

    print('[LOG] Intialize Neural Network')

    model = Sequential()

    model.add(Conv2D(filters=6, kernel_size=(3, 3), activation='relu', input_shape=(EyeConfig.IMG_SIZE, EyeConfig.IMG_SIZE, 1)))
    model.add(AveragePooling2D())

    model.add(Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
    model.add(AveragePooling2D())

    model.add(Flatten())

    model.add(Dense(units=120, activation='relu'))

    model.add(Dense(units=84, activation='relu'))

    model.add(Dense(units=1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit_generator(generator=train_generator,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=val_generator,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=20
                        )
    save_model(model)


def predict(img, model):
    img = Image.fromarray(img, 'RGB').convert('L')
    img = img.resize((EyeConfig.IMG_SIZE, EyeConfig.IMG_SIZE))
    img = np.array(img.getdata()).astype('float32')
    img /= 255
    img = img.reshape(1, EyeConfig.IMG_SIZE, EyeConfig.IMG_SIZE, 1)
    prediction = model.predict(img)
    if prediction < 0.1:
        prediction = 'closed'
    elif prediction > 0.9:
        prediction = 'open'
    else:
        prediction = 'idk'
    return prediction


def evaluate(X_test, y_test):
    model = load_model()
    print('Evaluate model')
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(acc * 100)


if __name__ == '__main__':
    train_generator, val_generator = collect()
    train(train_generator, val_generator)
