import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class DQN:
    def __init__(self, env):
        self.env = env
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01
        self.model = self.create_model()

    def create_model(self):
        model = keras.Sequential()
        state_shape = self.env.observation_space.shape
        model.add(layers.Dense(14, input_dim=state_shape[0],
                               activation="relu"))
        model.add(layers.Dense(28, activation="relu"))
        model.add(layers.Dense(14, activation="relu"))
        model.add(layers.Dense(self.env.action_space.shape[0]))
        model.compile(loss="mean_squared_error", optimizer=(tf.keras.optimizers.Adam(learning_rate=self.learning_rate)))
        return model
