import os
import pandas as pd
import argparse
from parser_validation import PathType

def list_dirs(args):

    subfolders = [ f.path for f in os.scandir(args.path) if f.is_dir() ]

    return subfolders

def concat_data(path):

    #os.chdir(path)
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

    all_filenames = []

    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            all_filenames.append(full_path)

    #all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]

    dfs = []
    for file_path in all_filenames:
        data = pd.read_csv(file_path, delimiter=';', iterator=True, chunksize=1000)
        df = pd.concat(data, ignore_index=True)
        dfs.append(df)
    
    newone = pd.concat(dfs, axis=1)
    newone.fillna(' ', inplace = True)
    perm = newone[fieldnames]
    
    return perm

def save_csv(args, x, perm):

    out_name = f'output_patient_{x}.csv'
    output_path = os.path.join(args.out, out_name)
    perm.to_csv(output_path, index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Conform data to a new csv.')
    parser.add_argument('--path', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all patients.')
    parser.add_argument('--out', type=PathType(exists=True, type='dir'), required=True, help='The path for your output csv file.')

    args = parser.parse_args()

    subfolders = list_dirs(args)
    comp = len(subfolders)

    for folder in subfolders:
        x = os.path.split(folder)[1]
        perm = concat_data(path=folder)
        save_csv(args, x, perm)