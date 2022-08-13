import os
import warnings

from keras.backend import set_session
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image

sess = tf.Session()
graph = tf.get_default_graph()

warnings.filterwarnings('ignore', category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)


def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)


mobile = tf.keras.applications.mobilenet.MobileNet()
x = mobile.layers[-6].output
x = Dropout(0.25)(x)
predictions = Dense(4, activation='softmax')(x)
model = Model(inputs=mobile.input, outputs=predictions)
for layer in model.layers[:-23]:
    layer.trainable = False

model.compile(Adam(lr=0.01), loss='categorical_crossentropy',
              metrics=[categorical_accuracy, top_2_accuracy, top_3_accuracy])
set_session(sess)
model.load_weights('base/static/adminResources/model/model.h5')
class_labels = ["psoriasis", "measles", "melanoma", "ringworm"]


def loadImages(path):
    img = image.load_img(path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = tf.keras.applications.mobilenet.preprocess_input(img_data)
    global sess
    global graph
    with graph.as_default():
        set_session(sess)
        features = np.array(model.predict(img_data))
    y_classes = features.argmax(axis=-1)
    tf.keras.backend.clear_session()
    return y_classes


def pridictor(inputfile):
    print(inputfile)
    x = loadImages(inputfile)
    return class_labels[x[0]]
