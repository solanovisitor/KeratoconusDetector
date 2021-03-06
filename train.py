import tensorflow as tf
import numpy as np
import os
import pandas as pd
import argparse
import sys

from tqdm import tqdm
from parser_validation import PathType
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

def exports():

  # Set CUDA and CUPTI paths
  os.environ['CUDA_HOME'] = '/usr/local/cuda'
  os.environ['PATH']= '/usr/local/cuda/bin:$PATH'
  os.environ['CPATH'] = '/usr/local/cuda/include:$CPATH'
  os.environ['LIBRARY_PATH'] = '/usr/local/cuda/lib64:$LIBRARY_PATH'
  os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH'
  os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/lib64:$LD_LIBRARY_PATH'

  # Set CUDA optimizer flags

  # Permitindo o caching na compilação do modelo. (if 1: disabled; if 0: enabled)
  os.environ['CUDA_CACHE_DISABLE'] = '0'
  # Alocação dinâmica de memória.
  os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
  # Dedicando os threads da GPU para seu uso exclusivo. 
  # Por default, ela dividiria threads com a CPU.
  os.environ['TF_GPU_THREAD_MODE'] = 'gpu_private'
  # Faz cuDNN realizar etapa de normalização com uma operação por batch. 
  # Por default, ela quebraria essa operação em vários subprocessos.
  os.environ['TF_USE_CUDNN_BATCHNORM_SPATIAL_PERSISTENT'] = '1'
  # Permite o uso do algoritmo de convolução de Winograd de forma non-fused.
  os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'
  os.environ['TF_SYNC_ON_FINISH'] = '0'
  # Delimita o uso da função experimental AUTOTUNE
  # usada para realizar o pipeline de input.
  os.environ['TF_AUTOTUNE_THRESHOLD'] = '2'

  # fast math - permitem a realização de multiplicações
  # entre matrizes utilizando float32.
  os.environ['TF_ENABLE_CUBLAS_TENSOR_OP_MATH_FP32'] = '1'
  os.environ['TF_ENABLE_CUDNN_TENSOR_OP_MATH_FP32'] = '1'
  os.environ['TF_ENABLE_CUDNN_RNN_TENSOR_OP_MATH_FP32'] = '1'

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

  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

  return X_train, X_test, y_train, y_test

def lstm():

  model = keras.Sequential(
    [
      tf.keras.layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'),
      tf.keras.layers.MaxPooling1D(pool_size=2),
      tf.keras.layers.LSTM(100),
      tf.keras.layers.Dense(1, activation='sigmoid')
    ]
  )

  return model


def train_model(args):

  exports()

  X, Y = input_fn(args)

  model = lstm()
  
  X_train, X_test, y_train, y_test = split(X, Y)

  optimizer = tf.keras.optimizers.RMSprop(learning_rate=10e-5)

  model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=[[tf.keras.metrics.BinaryAccuracy()], [tf.keras.metrics.AUC()]])

  callback_list = []

  model_name = 'keras_model.h5'
  model_name_local = os.path.join('/tmp', model_name)
  callback_checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=model_name_local,
            save_best_only=False,
            save_weights_only=False,
            save_freq='epoch'
          )

  callback_list.append(callback_checkpoint)

  callback_tboard = tf.keras.callbacks.TensorBoard(log_dir=os.path.join(args.job_dir, 'tensorboard_3'))

  callback_list.append(callback_tboard)

  model.fit(X_train, y_train, epochs=600, batch_size=32, verbose=1, validation_data=(X_test, y_test), callbacks=callback_list)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Train the model.')
  parser.add_argument('--pos_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all positive class.')
  parser.add_argument('--neg_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all negative class.')
  parser.add_argument('--job_dir', type=PathType(exists=True, type='dir'), required=True, help='The path for saving the model.')

  args = parser.parse_args()

  with tqdm(total=1, file=sys.stdout) as pgbar:
    train_model(args)
