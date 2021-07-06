import csv
import pandas as pd
import os
import argparse
import sys
from tqdm import tqdm
from parser_script import PathType


def input_fn(args):
    dir = f'patient_{args.patient}'
    full_path = os.path.join(args.path, dir)
    lista = os.listdir(full_path)
    
    dfs = []
    for filename in lista:
        final_path = os.path.join(full_path, filename)
        data = pd.read_csv(final_path, delimiter=';', iterator=True, chunksize=1000)
        df = pd.concat(data, ignore_index=True)
        dfs.append(df)
        
    return dfs


def preprocess(dfs):
    newone = pd.concat(dfs, axis=1)
    newone.fillna(' ', inplace = True)
    perm = newone[fieldnames]
    
    return perm

def generate_data(args):
    dfs = input_fn(args)
    perm = preprocess(dfs)
    out_path = f'output_patient_{args.patient}.csv'
    output_path = os.path.join(args.out, out_path)
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
    parser.add_argument('--patient', required=True, help='The ID number of the patient.')
    parser.add_argument('--path', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all patients.')
    parser.add_argument('--out', type=PathType(exists=True, type='dir'), required=True, help='The path for your output csv file.')

    args = parser.parse_args()

    with tqdm(total=100, file=sys.stdout) as pgbar:
        generate_data(args)
