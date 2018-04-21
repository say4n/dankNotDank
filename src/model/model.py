#!/usr/bin/env python3

import numpy as np
import keras


NUM_CHANNELS = 3

def classifier(num_channels):
    # Channels last : (height, width, num_channels)
    
    # Input layer
    input_layer = keras.layers.Input(shape=(None, None, num_channels),
                                     name="dankNet_input_layer")
    
    # single stride 4x4 filter for 16 maps
    x = keras.layers.Conv2D(16,(4,4), activation = 'elu')(input_layer)

    # single stride 4x4 filter for 32 maps
    x = keras.layers.Conv2D(32,(4,4), activation = 'elu')(x)
    x = keras.layers.Dropout(0.5)(x)

    # single stride 4x4 filter for 64 maps
    x = keras.layers.Conv2D(64,(4,4), activation = 'elu')(x)
    x = keras.layers.Dropout(0.5)(x)

    # finally 128 maps for global average-pool
    x = keras.layers.Conv2D(128, (1,1))(x)

    # pseudo-dense 128 layer
    x = keras.layers.GlobalMaxPooling2D()(x)

    # Output
    output_layer = keras.layers.Dense(10, activation = "softmax")(x)


    model = keras.Model(inputs=input_layer, outputs=output_layer)

    return model
    

if __name__ == "__main__":
    dankNet_model = classifier(NUM_CHANNELS)
    
    dankNet_model.compile(optimizer = "adam",
                          loss = "mse",
                          metrics=["accuracy"])

    print(dankNet_model.summary())