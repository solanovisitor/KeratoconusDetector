import os
import pandas as pd
import argparse
from parser_validation import PathType

def list_dirs(args):

    ''' 
        This function will list all the directories containing the examination folders.
        Finally, will return the folders' paths as a list.
    '''

    subfolders = [ f.path for f in os.scandir(args.path) if f.is_dir() ]

    return subfolders

def concat_data(path):

    ''' 
        This is the main function.
        It takes the path of a folder, opens every .csv file and concatenate in a single .csv.
        Then, we drop all the coordinates and remain with the measurements' columns in a DataFrame
    '''

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

    dfs = []
    for file_path in all_filenames:
        # print(file_path)
        data = pd.read_csv(file_path, delimiter=';')# iterator=True)#, chunksize=1000)
        # print(data)
        data.round(4)
        data.replace(' ', 0, inplace=True)
        df = data.iloc[:,-1]
        # 
        dfs.append(df)
    try:
        df = pd.concat(dfs, axis=1, ignore_index=True)
    except:
        pass

    return df

def save_csv(args, file_name, perm):

    '''
        This function takes the DataFrame and saves this final format in a .csv file.
    '''
    out_name = f'output_patient_{file_name}.csv'
    output_path = os.path.join(args.out, out_name)
    perm.to_csv(output_path, index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Conform data to a new csv.')
    parser.add_argument('--path', type=PathType(exists=True, type='dir'), required=True, help='The path for your folder containing all patients.')
    parser.add_argument('--out', type=PathType(exists=True, type='dir'), required=True, help='The path for your output csv file.')

    args = parser.parse_args()

    subfolders = list_dirs(args)
    # print(subfolders)
    comp = len(subfolders)
    print(comp)

    for folder in subfolders:
        file_name = os.path.split(folder)[1]
        print(folder)
        perm = concat_data(path=folder)
        save_csv(args, file_name, perm)