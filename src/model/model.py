#!/usr/bin/env python3

from decouple import config
import keras
import numpy as np
import pandas as pd
from tinydb import TinyDB

# Constants
NUM_CHANNELS = 3
DATABASE_PATH = config("DATABASE_PATH")

# Lambdas
LEGROOM = lambda num_lines: print("\n" * num_lines)


def load_data():
    """Load database"""
    db = TinyDB(DATABASE_PATH)
    data = db.all()

    return pd.DataFrame(data)


def process_dataset(df, train_validation_ratio = 0.8):
    """Given a dataset, perform train-validation split"""
    x_train, y_train, x_val, y_val = None, None, None, None

    # image data
    xS = None
    # dankness score
    yS = df.dankness

    return (x_train, y_train, x_val, y_val)


def classifier(num_channels):
    """dankNet Classifier"""
    # Channels last : (height, width, num_channels)
    
    # Input layer
    input_layer = keras.layers.Input(shape=(None, None, num_channels),
                                     name="dankNet_input_layer")
    
    # single stride 4x4 filter for 16 maps
    x = keras.layers.Conv2D(16, (4, 4), activation='elu')(input_layer)

    # single stride 4x4 filter for 32 maps
    x = keras.layers.Conv2D(32, (4, 4), activation='elu')(x)
    x = keras.layers.Dropout(0.5)(x)

    # single stride 4x4 filter for 64 maps
    x = keras.layers.Conv2D(64, (4, 4), activation='elu')(x)
    x = keras.layers.Dropout(0.5)(x)

    # finally 128 maps for global average-pool
    x = keras.layers.Conv2D(128, (1, 1))(x)

    # pseudo-dense 128 layer
    x = keras.layers.GlobalMaxPooling2D()(x)

    # dense layers
    x = keras.layers.Dense(64, activation="elu")(x)
    x = keras.layers.Dense(16, activation="elu")(x)

    # Output
    output_layer = keras.layers.Dense(1, activation="softmax")(x)


    model = keras.Model(inputs=input_layer, outputs=output_layer)

    return model


if __name__ == "__main__":
    # Model
    dankNet_model = classifier(NUM_CHANNELS)
    dankNet_model.compile(optimizer = "adam",
                          loss = "mse",
                          metrics=["accuracy"])
    dankNet_model.summary()
    LEGROOM(5)

    # Prelim data
    all_data = load_data()
    all_data["dankness"] = all_data.ups / (all_data.ups + all_data.downs)

    all_data.info()
    LEGROOM(5)
