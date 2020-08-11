from keras.datasets import mnist
from keras import models, layers
from keras.utils import to_categorical
from keras import optimizers


(train_image, train_label), (test_image, test_label) = mnist.load_data()
networks = models.Sequential()
networks.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
networks.add(layers.Dense(10, activation='softmax'))
networks.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
train_image = train_image.reshape((train_image.shape[0], train_image.shape[1]*train_image.shape[2]))
train_image = train_image.astype('float32')/255
test_image = test_image.reshape((test_image.shape[0], test_image.shape[1]*test_image.shape[2]))
test_image = test_image.astype('float32')/255
train_label = to_categorical(train_label)
test_label = to_categorical(test_label)
networks.fit(train_image, train_label, epochs=5, batch_size=128)

test_loss, test_acc = networks.evaluate(test_image, test_label)
print(test_loss, test_acc)

