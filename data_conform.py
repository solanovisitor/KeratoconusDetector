import pandas as pd
import os
import argparse
import sys
from tqdm import tqdm
from parser_validation import PathType


def input_fn(args):
    mother_dirs = os.listdir(args.path)
    lista = []
    for dir in mother_dirs:
        folder_path = os.path.join(args.path, dir)
        lista.append(folder_path)
    
    dfs = []
    for folder in lista:
        final_list = os.listdir(folder)
    
    for filename in final_list:
        file_path = os.path.join(folder, filename)
        data = pd.read_csv(file_path, delimiter=';', iterator=True, chunksize=1000)
        df = pd.concat(data, ignore_index=True)
        dfs.append(df)
  
    return dfs, mother_dirs


def preprocess(dfs):
    newone = pd.concat(dfs, axis=1)
    newone.fillna(' ', inplace = True)
    perm = newone[fieldnames]
    
    return perm

def generate_data(args):
    dfs, mother_dirs = input_fn(args)
    perm = preprocess(dfs)
    comp = len(mother_dirs)
    for x in range(comp):
        out_name = f'output_patient_{x}.csv'
        output_path = os.path.join(args.out, out_name)
        output_csv = perm.to_csv(output_path, index=False)

    return output_csv

if __name__ == '__main__':

    fieldnames = ['Ant. Elevation BFA_[um]',
                    'Ant. Elevation BFS_[um]',
                    'Ant. Elevation BFTA_[um]',
                    'Axial-CURV-ant_ [D]',
                    'Axial-CURV-post_ [D]',
                    'HEIGHT-ant_ [mm]',
                    'HEIGHT-post_ [mm]',
                    'Inst-CURV-ant_ [D]',
                    'Inst-CURV-post_ [D]',
                    'PACHY_[um]',
                    'Post. Elevation BFA_[um]',
                    'Post. Elevation BFS_[um]',
                    'Post. Elevation BFTA_[um]',
                    'Refractive Power_ [D]',
                    'Total-POWER_ [D]']

    parser = argparse.ArgumentParser(description='Conform data to a new csv.')
    parser.add_argument('--path', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all patients.')
    parser.add_argument('--out', type=PathType(exists=True, type='dir'), required=True, help='The path for your output csv file.')

    args = parser.parse_args()

    with tqdm(total=1, file=sys.stdout) as pgbar:
        generate_data(args)
