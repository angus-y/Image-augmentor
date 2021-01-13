import numpy
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing


train_dataset = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
train_dataset_generator = train_dataset.flow_from_directory("C:\\Users\\angus\\Desktop\\python\\generic_scripts\\tensorflow_stuff\\archive\\trainingSet\\trainingSet",
                                                    target_size=(28, 28), batch_size=64)
print ("[+]Initialized dataset generator")

input_shape = (28,28,3)
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
model.fit(train_dataset_generator, steps_per_epoch=650,epochs=epochs)
print ('[+]Trained kerase model, evaluating accuracy...')

results = model.evaluate()
print ('[*]Evaluated')


# scaler = preprocessing.Rescaling(scale=1.0/255)
# normalized_dataset = scaler(dataset)
#
# for i, j in normalized_dataset:
#     print (i)

#
# input_shape = (28,28,3)
# num_classes = 10
#
#
#
# inputs = keras.Input(shape=input_shape)
# x = normalize_images(inputs)
#
# model = keras.Sequential(
#     [
#         keras.Input(shape=input_shape),
#         layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dropout(0.5),
#         layers.Dense(num_classes, activation="softmax"),
#     ]
# )
# model.summary()
# batch_size = 128
# epochs = 15
# model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# model.fit(dataset, epochs=epochs, validation_split=0.1)


























# train_datagen = ImageDataGenerator(rescale=1./255)
# train_generator = train_datagen.flow_from_directory("C:\\Users\\angus\\Desktop\\python\\generic_scripts\\tensorflow_stuff\\archive\\trainingSet\\trainingSet",
#                                                     target_size=(28, 28), batch_size=64)
# print ('[+]Created generator')
#
#
# input_shape = (28,28,3)
# num_classes = 10
# model = keras.Sequential(
#     [
#         keras.Input(shape=input_shape),
#         layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dropout(0.5),
#         layers.Dense(num_classes, activation="softmax"),
#     ]
# )
# model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# history = model.fit_generator(train_generator, steps_per_epoch=100, epochs=15)
#
#
# x_test = numpy.asarray(Image.open("C:\\Users\\angus\\Desktop\\python\\generic_scripts\\tensorflow_stuff\\archive\\trainingSet\\trainingSet\\0\\img_1.jpg"))
# y_test = [0]
#
# score = model.evaluate(x_test, y_test, verbose=0)
# print("Test loss:", score[0])
# print("Test accuracy:", score[1])























#
#
#
#
# num_classes = 10
# input_shape = (28, 28, 1)
#
# # the data, split between train and test sets
# (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
#
# # Scale images to the [0, 1] range
# x_train = x_train.astype("float32") / 255
# x_test = x_test.astype("float32") / 255
# # Make sure images have shape (28, 28, 1)
# x_train = np.expand_dims(x_train, -1)
# x_test = np.expand_dims(x_test, -1)
# print("x_train shape:", x_train.shape)
# print(x_train.shape[0], "train samples")
# print(x_test.shape[0], "test samples")
#
#
# # convert class vectors to binary class matrices
# y_train = keras.utils.to_categorical(y_train, num_classes)
# y_test = keras.utils.to_categorical(y_test, num_classes)
#
# model = keras.Sequential(
#     [
#         keras.Input(shape=input_shape),
#         layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dropout(0.5),
#         layers.Dense(num_classes, activation="softmax"),
#     ]
# )
#
# model.summary()
#
#
# batch_size = 128
# epochs = 15
#
# model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
#
# model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
#
# score = model.evaluate(x_test, y_test, verbose=0)
# print("Test loss:", score[0])
# print("Test accuracy:", score[1])
