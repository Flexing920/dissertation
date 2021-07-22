import tensorflow as tf
from tensorflow import keras
import numpy as np

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model


class TrainModel:
    def __init__(self, n_layers, n_nodes, batch_size, learning_rate, input_dims, output_dims):

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.input_dims = input_dims
        self.output_dims = output_dims
        self.model = self.build_model(n_layers, n_nodes)

    def build_model(self, n_layers, n_nodes):
        inputs = keras.Input(shape=(self.input_dims, ))
        x = keras.layers.Dense(n_nodes, activation="relu")(inputs)
        for _ in range(n_layers):
            x = keras.layers.Dense(n_nodes, activation="relu")(x)

        # no activation for the output layer
        outputs = keras.layers.Dense(self.output_dims, activation=None)
        model = keras.Model(inputs=inputs, outputs=outputs, name="dqn_model")
        model.compile(optimizer=Adam(lr=self.learning_rate), loss=keras.losses.mean_squared_error)

        return model

    def predict_one(self, state):
        state = np.reshape(state, [1, self.input_dims])
        return self.model.predict(state)

    def predict_batch(self, states):
        return self.model.predict(states)

    def train_batch(self, states, q_table):
        self.model.fit(states, q_table, epochs=1, verbose=0)

    def model_save(self, path):
        self.model.save(os.path.join(path, "model_train.h5"))
        plot_model(self.model, to_file=os.path.join(path, "model_structure.jpg"), show_shapes=True, show_layer_names=True)