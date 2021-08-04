import tensorflow as tf
import numpy as np
import os
import pandas as pd
import argparse

from parser_validation import PathType
from tensorflow import keras

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


def input_data(args):

  test_list = os.listdir(args.test_folder)
  
  test_batch = []

  for filename in test_list:
    file_path = os.path.join(args.test_folder, filename)
    data = pd.read_csv(file_path, sep=',', header = None)
    data.drop(index=data.index[0], 
              axis=0, 
              inplace=True)
    data.replace(' ', 0, inplace=True)
    data = data.apply(pd.to_numeric)
    arr = data.to_numpy()
    np.reshape(arr,(1, 18001, 15))
    test_batch.append(arr)

  test_batch = np.array(test_batch)

  return test_batch

def predictions(args):

    test_batch = input_data(args)

    model_path = args.model_path

    model = keras.models.load_model(model_path)
    
    model.predict_on_batch(test_batch)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Train the model.')
  parser.add_argument('--test_folder', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing your test data.')
  parser.add_argument('--model_path', type=PathType(exists=True, type='file'), required=True, help='The path for your folder containing your h5 keras model.')

  args = parser.parse_args()

  exports()
  preds = predictions(args)
  print(preds)