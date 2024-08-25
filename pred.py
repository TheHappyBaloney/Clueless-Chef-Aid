import tensorflow as tf
import numpy as np


def model_prediction(image):
    model = tf.keras.models.load_model("trained_model.h5")
    image = tf.keras.preprocessing.image.load_img(image, target_size=[64,64])
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model.predict(input_arr)
    return np.argmax(predictions[0])


