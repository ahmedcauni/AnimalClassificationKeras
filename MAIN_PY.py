
import numpy as np
import os
import random
import cv2

folder= 'Imgs' # creating my directory
classes = ['cane', 'cavallo', 'elefante', 'farfalla', 'gallina'] # defining my classes
dataset = []
for cl in classes:
    cls_num = classes.index(cl)
    path = os.path.join(folder, cl)
    for img in os.listdir(path):
        try:
            img = cv2.imread(os.path.join(path, img)) # getting the images
            resized_img = cv2.resize(img, (200,200)) # resizing them into 200*200 pixels
            dataset.append([resized_img, cls_num])   #adding the resized image with the class asscoiated with it
        except Exception as e:
            pass

len(dataset)     #checking my data set size

random.shuffle(dataset) #shuffling data set to avoid overfitting
for i in dataset[:1000]:
    print(classes[i[1]])

x = []
y = []
for pic, label in dataset:
    x.append(pic)#adding the pictures my data
    y.append(label)#adding the labels for each picture

x = np.array(x)
y = np.array(y)

print(type(x),x.shape)
print(type(y),y.shape)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization, Dropout, Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.constraints import max_norm
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#creating my Multi-Layer Network and intializing it
model = Sequential([
    Conv2D(filters=128, kernel_size=(3, 3), activation='relu', input_shape=(200,200, 3)),
    BatchNormalization(),
    Dropout(0.2),
    Conv2D(filters=128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    BatchNormalization(),
    Flatten(),
    Dense(128, kernel_constraint=max_norm(3), activation='relu'),
    BatchNormalization(),
    Dropout(0.2),
    Dense(5, activation='softmax')
])

from keras import optimizers #compiling my model
model.compile(optimizer=optimizers.Adam(lr=1e-3),loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=15, batch_size=64,verbose=1,validation_split=0.2)#training the data
model.evaluate(x_test,y_test,verbose=1) #testing it

