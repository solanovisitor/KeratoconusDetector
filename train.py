import tensorflow as tf
import numpy as np
import os
import csv
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def input_fn(args):

  pos_class = os.listdir(args.pos_folder)
  neg_class = os.listdir(args.neg_folder)
  pos_dfs = []
  neg_dfs = []

  for filename in pos_class:
    file_path = os.path.join(args.pos_folder, filename)
    data = pd.read_csv(file_path, delimiter=';', iterator=True, chunksize=1000)
    data.drop(index=df.index[0], 
              axis=0, 
              inplace=True)
    pos_dfs.append(data)

  for filename in neg_class:
    file_path = os.path.join(args.neg_folder, filename)
    data = pd.read_csv(file_path, delimiter=';', iterator=True, chunksize=1000)
    data.drop(index=df.index[0], 
              axis=0, 
              inplace=True)
    neg_dfs.append(data)

  return pos_dfs, neg_dfs

def preprocess(pos_dfs, neg_dfs):

  X = []
  Y = []

  for df in pos_dfs:
    arr = df.to_numpy()
    X.append(arr)
    Y.append(1)

  for df in neg_dfs:
    arr = df.to_numpy()
    X.append(arr)
    Y.append(0)

  return X, Y


def split(X, Y):

  tam = len(Y)

  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)

  X_train = np.reshape(X_train,(1, 18001, 15))
  X_test = np.reshape(X_test,(1, 18001, 15))
  y_train = np.reshape(y_train,(1, tam, 15))
  y_test = np.reshape(y_test,(1, tam, 15))


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

  pos_dfs, neg_dfs = input_fn(args)
  X, Y = preprocess(pos_dfs=pos_dfs, neg_dfs=neg_dfs)
  
  model, X_train, X_test, y_train, y_test = split(X, Y)

  model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1, loss='binary_crossentropy')

  model.compile(optimizer="rmsprop", loss='mse', metrics=['accuracy'])

  results = model.evaluate(X_test, y_test, batch_size=128)

  return results


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Conform data to a new csv.')
  parser.add_argument('--pos_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all positive class.')
  parser.add_argument('--neg_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all negative class.')

  args = parser.parse_args()

  with tqdm(total=1, file=sys.stdout) as pgbar:
    train_model(args)
