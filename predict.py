import tensorflow as tf
import numpy as np
import os
import pandas as pd
import argparse

from parser_validation import PathType
from tensorflow import keras

def input_data(args):

  test_list = os.listdir(args.test_folder)
  
  test_batch = []

  for filename in test_list:
    file_path = os.path.join(args.test_folder, filename)
    data = pd.read_csv(file_path, sep=',', header = None)
    data.drop(index=data.index[0], 
              axis=0, 
              inplace=True)
    data = data.apply(pd.to_numeric)
    arr = data.to_numpy()
    np.reshape(arr,(1, 18001, 15))
    test_batch.append(arr)

  test_batch = np.array(test_batch)

  return test_batch

def predictions(args):

    test_batch = input_data()

    model_path = args.model_path

    model = keras.models.load_model(model_path)
    
    model.predict_on_batch(test_batch)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Train the model.')
  parser.add_argument('--test_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing your test data.')
  parser.add_argument('--model_path', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing your h5 keras model.')

  args = parser.parse_args()

  predictions(args)