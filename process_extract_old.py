import pandas as pd
import re
from fuzzywuzzy import process
import numpy as np
import os

def get_file_df(file_name, folder):
    file_path = os.path.join(folder, file_name)
    df = pd.read_excel(file_path)
    return df

def clean_names(file, folder, name_str):
    df = get_file_df(file, folder)
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', '', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names

def find_matched_name(source_file_name, test_file_name, folder, source_name_str, test_name_str):
    master_list = clean_names(source_file_name, folder, source_name_str)
    test_list = clean_names(test_file_name, folder, test_name_str)
    matched_list = []

    for row_no, patient_name in enumerate(test_list):
        matched_name = process.extractOne(patient_name, master_list)
        if matched_name is not None:
            cols = ['Patient Name', 'File_Number']
            name_file_num = test_file_name.iloc[row_no][cols]
            output_list = np.append(name_file_num, matched_name)
            matched_list.append(output_list)
            matched_df = pd.DataFrame(matched_list, columns=['patient_name_from_ffpe', 'file_number_from_ffpe', 'patient_name_from_master', 'score'])
    return matched_df


def get_file_number(source_file, test_file, folder, source_name_str, test_name_str):
    matched_names = find_matched_name(source_file, test_file, folder, source_name_str, test_name_str)
    matched_names = pd.DataFrame(matched_names)
    source_df_path = os.path.join(folder, source_file)
    source_df = os.read_excel(source_df_path)
    source_df['cleaned_patient_names'] = clean_names(source_file, folder, source_name_str)

    for index, row in source_df.iterrows():
        cleaned_patient_name = row['cleaned_patient_names']
        patient_name = row['patient_name']
        file_number = row['file_number']

        if matched_names['patient_name_from_master'].str.contains(cleaned_patient_name).any():
            matched_names['patient_name_from_master'] = patient_name
            matched_names['file_number_from_master'] = file_number

    return matched_names

master_file = pd.ExcelFile('D:\\Shweta\\Patient_name_matching\\2010_2018_names_file_number.xlsx')
patients_10_16 = pd.read_excel(master_file, sheet_name='2010_2016')
patients_17 = pd.read_excel(master_file, sheet_name='2017')
patients_18 = pd.read_excel(master_file, sheet_name='2018')

patient_master_file = pd.concat([patients_10_16, patients_17, patients_18])
ffpe_db = pd.read_excel("D:\\Shweta\\Patient_name_matching\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx")

names_file_nums = get_file_number(patient_master_file, ffpe_db)

matched_names.to_excel('D:\\Shweta\\Patient_name_matching\\18_02_2021_matched_names_file_number.xlsx')

#####################################################################################################################################################

def find_matched_name(source_file, test_file):
    master_list = clean_names(source_file, 'patient_name')
    test_list = clean_names(test_file, 'Patient Name')
    matched_list = []

    for row_no, patient_name in enumerate(test_list):
        matched_name = process.extractOne(patient_name, master_list)
        if matched_name is not None:
            cols = ['Patient Name', 'File_Number']
            name_file_num = test_file.iloc[row_no][cols]
            output_list = np.append(name_file_num, matched_name)
            matched_list.append(output_list)
            matched_df = pd.DataFrame(matched_list, columns=['patient_name_from_ffpe', 'file_number_from_ffpe', 'patient_name_from_master', 'score'])
    return matched_df

##
def get_file_number(source_df, test_df):
    matched_names = find_matched_name(source_df, test_df)
    matched_names = pd.DataFrame(matched_names)
    source_df['cleaned_patient_names'] = clean_names(source_df, 'patient_name')

    for index, row in source_df.iterrows():
        cleaned_patient_name = row['cleaned_patient_names']
        patient_name = row['patient_name']
        file_number = row['file_number']

        if cleaned_patient_name in matched_names['patient_name_from_master']:
            matched_patient_name = patient_name
            matched_file_num = file_number
            matched_names[['patient_name_from_master', 'file_number_from_master']] = pd.DataFrame([[matched_patient_name, matched_file_num]], index = matched_names.index)

    return matched_names

