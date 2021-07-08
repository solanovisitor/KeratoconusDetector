import tensorflow as tf
import numpy as np
import os
import csv
import pandas as pd
import argparse
import sys

from tqdm import tqdm
from parser_script import PathType
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

def input_fn(args):

  pos_class = os.listdir(args.pos_folder)
  neg_class = os.listdir(args.neg_folder)
  
  X = []
  Y = []

  for filename in pos_class:
    file_path = os.path.join(args.pos_folder, filename)
    data = pd.read_csv(file_path, sep=',', header = None)
    data.drop(index=data.index[0], 
              axis=0, 
              inplace=True)
    data = data.apply(pd.to_numeric)
    arr = data.to_numpy()
    np.reshape(arr,(1, 18001, 15))
    X.append(arr)
    Y.append(1)

  for filename in neg_class:
    file_path = os.path.join(args.neg_folder, filename)
    data = pd.read_csv(file_path, sep=',', header = None)
    data.drop(index=data.index[0], 
              axis=0, 
              inplace=True)
    data = data.apply(pd.to_numeric)
    arr = data.to_numpy()
    np.reshape(arr,(1, 18001, 15))
    X.append(arr)
    Y.append(0)

  X = np.array(X)
  Y = np.array(Y)

  tam = len(Y)
  np.reshape(Y,(1, 1, tam))

  return X, Y


def split(X, Y):

  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)

  model = keras.Sequential(
    [
      tf.keras.layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'),
      tf.keras.layers.MaxPooling1D(pool_size=2),
      tf.keras.layers.LSTM(15),
      tf.keras.layers.Dense(1, activation='sigmoid')
    ]
  )

  return model, X_train, X_test, y_train, y_test


def train_model(args):

  X, Y = input_fn(args)
  
  model, X_train, X_test, y_train, y_test = split(X, Y)

  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=[[tf.keras.metrics.BinaryAccuracy()], [tf.keras.metrics.AUC()]])

  callback_list = []

  model_name = 'keras_model.h5'
  model_name_local = os.path.join('/tmp', model_name)
  callback_checkpoint_path = os.path.join(args.job_dir, 'model', model_name)
  callback_checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=model_name_local,
            save_best_only=False,
            save_weights_only=False,  # https://github.com/tensorflow/tensorflow/issues/38745
            save_freq='epoch'
          )

  callback_list.append(callback_checkpoint)

  callback_tboard = tf.keras.callbacks.TensorBoard(log_dir=os.path.join(args.job_dir, 'tensorboard'))

  callback_list.append(callback_tboard)

  model.fit(X_train, y_train, epochs=40, batch_size=32, verbose=1, validation_data=(X_test, y_test), callbacks=callback_list)

  results = model.evaluate(X_test, y_test, batch_size=1)

  return results


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Train the model.')
  parser.add_argument('--pos_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all positive class.')
  parser.add_argument('--neg_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all negative class.')
  parser.add_argument('--job_dir', type=PathType(exists=True, type='dir'), required=True, help='The path for saving the model.')

  args = parser.parse_args()

  with tqdm(total=1, file=sys.stdout) as pgbar:
    train_model(args)
