import os
import sys
import numpy as np
from PIL import Image
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

if os.path.exists('mnist_model'):
    print ('[+]Loading trained model...')
    model = keras.models.load_model('mnist_model')
    model.summary()
    print (f'[*]Predicting "{sys.argv[1]}"...')
    image = keras.preprocessing.image.load_img(sys.argv[1])
    image_arr = np.array([keras.preprocessing.image.img_to_array(image)])
    prediction = model.predict(image_arr)
    print ('[*]Results:')
    for i in prediction:
        print (i)
else:
    train_dir = "archive\\trainingSet\\trainingSet"
    train_dataset = keras.preprocessing.image.ImageDataGenerator(rescale=1./255, validation_split=0.1)
    train_dataset_generator = train_dataset.flow_from_directory(train_dir, target_size=(28, 28), batch_size=64, subset='training')
    validate_dataset_generator = train_dataset.flow_from_directory(train_dir, target_size=(28, 28), batch_size=64, subset='validation')
    print ("[+]Initialized training generator and validation generator")

    input_shape = (28,28,3) # shape  of input without batch size
    num_classes = 10
    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )
    model.summary()
    epochs = 15
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(train_dataset_generator, validation_data=validate_dataset_generator, epochs=epochs)
    model.save("mnist_model")
