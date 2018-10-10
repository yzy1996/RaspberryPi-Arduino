from tensorflow.python.keras.applications.inception_v3 import InceptionV3
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.models import Model, load_model
from tensorflow.python.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.python.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.optimizers import RMSprop, SGD
import os

model_file = 'cat.hd5'
num_classes = 4
FC_SIZE = 1024


def create_model(num_hidden, num_classes):

    base_model = InceptionV3(include_top=False, weights='imagenet')
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(num_hidden, activation='relu')(x)

    predictions = Dense(num_classes, activation='softmax')(x)

    for layer in base_model.layers:
        layer.trainable = False

    model = Model(inputs=base_model.input, outputs=predictions)

    return model

#load an existing model then set the last 3 layers to be trainable


def load_existing_model(model_file):
    model = load_model(model_file)

    for layer in model.layers[:-3]:
        layer.trainable = False

    for layer in model.layers[-3:]:
        layer.trainable = True

    return model


def train(model_file, train_path, validation_path,
          num_hidden=FC_SIZE, num_classes=num_classes,
          steps=32, epochs=20, save_preiod=1):

    if os.path.exists(model_file):
        print("\n***Existing model found at {}.Loading***\n\n".format(model_file))
        model = load_existing_model(model_file)
    else:
        print("\n***Creating New Model***\n")
        model = create_model(num_hidden, num_classes)

    model.compile(optimizer=RMSprop(lr=0.001, decay=0.000001), loss='categorical_crossentropy')

    #create a checkpoint

    checkpoint = ModelCheckpoint(model_file, period=save_preiod)
    tbCallBack = TensorBoard(log_dir='./graph', histogram_freq=0,
                             write_graph=True, write_images=True)
    train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2,
                                       zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_datagen.flow_from_directory(train_path, target_size=(249, 249),
                                                        batch_size=32,
                                                        class_mode="categorical")
    validation_generator = test_datagen.flow_from_directory(validation_path,
                                                            target_size=(249, 249),
                                                            batch_size=32,
                                                            class_mode='categorical')
    model.fit_generator(train_generator,
                        steps_per_epoch=steps, epochs=epochs,
                        callbacks=[checkpoint, tbCallBack],
                        validation_data=validation_generator,
                        validation_steps=50)
    for layer in model.layers[:249]:
        layer.trainable = False
    for layer in model.layers[249:]:
        layer.trainable = True

    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')
    model.fit_generator(train_generator, steps_per_epoch=steps,
                        epochs=epochs, callbacks=[checkpoint, tbCallBack],
                        validation_data=validation_generator, validation_steps=50)



def main():
    train(model_file, train_path="Cat_photos/Training", validation_path="Cat_photos/Testing", steps=120, epochs=10)


if __name__ == '__main__':
    main()
