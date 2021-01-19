import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

BATCH_SIZE = 5
train_dir = r"C:\Users\Admin\Desktop\Python\imeg\train_dataset"
train_dataset = keras.preprocessing.image.ImageDataGenerator(rescale=1./255, validation_split=0.1)
train_dataset_generator = train_dataset.flow_from_directory(train_dir, target_size=(512, 512), batch_size=BATCH_SIZE, subset='training')
validate_dataset_generator = train_dataset.flow_from_directory(train_dir, target_size=(512, 512), batch_size=BATCH_SIZE, subset='validation')
print ("[+]Initialized training generator and validation generator")

input_shape = (512,512,3) # shape  of input without batch size

# input_shape = (28,28,3) # shape  of input without batch size
# num_classes = 10
num_classes = 26

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(5, 5), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(32, kernel_size=(7, 7), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)
model.summary()

epochs = 5

training_steps = max(train_dataset_generator.samples // BATCH_SIZE, 1)
validation_steps = max(validate_dataset_generator.samples // BATCH_SIZE, 1)

train_dataset_generator.reset()  # Reset the training generator to start from the beginning

with tf.device("/GPU:0"):
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    # Train the model
    model.fit(
        train_dataset_generator,
        steps_per_epoch = training_steps,
        epochs = epochs,
        validation_data = validate_dataset_generator,
        validation_steps = validation_steps,
        verbose=1)
    history.save("ocr_model")
