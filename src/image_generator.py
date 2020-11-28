import tensorflow as tf
from tensorflow import keras
import numpy as np
import PIL
from tensorflow_addons.layers import InstanceNormalization
import io


def normalize_img(img):
    img = tf.cast(img, dtype=tf.float32)
    # Map values in the range [-1, 1]
    return (img / 127.5) - 1.0


def pil_2_bio(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="jpeg")
    img_byte_arr.seek(0)
    return img_byte_arr


def gen_monet(file_path):
    model = keras.models.load_model('../models/monet_generator.h5',
                                    custom_objects={'InstanceNormalization': InstanceNormalization},
                                    compile=True)
    img = PIL.Image.open(file_path)
    resized_img = img.resize((256, 256))
    img_array = keras.preprocessing.image.img_to_array(resized_img)
    img_array = normalize_img(img_array)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    prediction = model.predict(img_array)[0]  # make prediction
    prediction = (prediction * 127.5 + 127.5).astype(np.uint8)  # re-scale
    out_img = PIL.Image.fromarray(prediction).resize(img.size)
    return pil_2_bio(out_img)


if __name__ == "__main__":
    gen_monet('./data/input_img.jpg')
