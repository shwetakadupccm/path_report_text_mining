import pandas as pd

patient_master_file = pd.read_excel("D:\\Shweta\\Patient_name_matching\\2010_2018_names_file_number.xlsx")
ffpe_db = pd.read_excel("D:\\Shweta\\Patient_name_matching\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx")

df1 = patient_master_file
df2 = ffpe_db[['Patient Name', 'File_Number']]

df = df1.merge(df2, how= 'inner', left_on= 'file_number', right_on='File_Number')
df.columns = ['patient_name_from_master', 'file_number_from_master', 'patient_name_from_ffpe', 'file_number-from_ffpe']
df.to_excel('D:\\Shweta\\Patient_name_matching\\18_02_2021_matched_file_number_names.xlsx')
###################################################################################################################################

import pandas as pd
import re
from fuzzywuzzy import process
import numpy as np

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', '', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names


def find_matched_name(source_file, test_file):
    master_list = clean_names(source_file, 'patient_name')
    test_list = clean_names(test_file, 'Patient Name')
    matched_list = []

    for row_no, patient_name in enumerate(master_list):
        matched_name = process.extractOne(patient_name, test_list)
        if matched_name is not None:
            cols = ['patient_name', 'file_number']
            name_file_num = source_file.iloc[row_no][cols]
            output_list = np.append(name_file_num, matched_name)
            matched_list.append(output_list)
            matched_df = pd.DataFrame(matched_list, columns=['patient_name_master', 'file_number_master', 'name_from_ffpe', 'score'])
    return matched_df


patient_master_file = pd.read_excel("D:\\Shweta\\Patient_name_matching\\2010_2018_names_file_number.xlsx")
ffpe_db = pd.read_excel("D:\\Shweta\\Patient_name_matching\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx")

matched_names = find_matched_name(patient_master_file, ffpe_db)
matched_names = pd.DataFrame(matched_names)
matched_names.to_excel('D:\\Shweta\\Patient_name_matching\\18_02_2021_matched_names_file_number-reverse.xlsx')

def get_file_number(source_df, test_df):
    matched_names = find_matched_name(source_df, test_df)
    matched_names = pd.DataFrame(matched_names)
    source_df['cleaned_patient_names'] = clean_names(source_df, 'patient_name')

    for index, row in source_df.iterrows():
        cleaned_patient_name = row['cleaned_patient_names']
        patient_name = row['patient_name']
        file_number = row['file_number']
        for name in matched_names['name_from_master']:
            if name == cleaned_patient_name:
            matched_patient_name = patient_name
            matched_file_num = file_number
            matched_names['patient_name_from_master', 'file_number_from_master'] = matched_patient_name, matched_file_num
    return matched_names

get_file_number(patient_master_file, ffpe_db)
#################################################################################################

def get_file_number(source_df, test_df):
    matched_names = find_matched_name(source_df, test_df)
    matched_names = pd.DataFrame(matched_names)
    source_df['cleaned_patient_names'] = clean_names(source_df, 'patient_name')

    for index, cleaned_name in enumerate(source_df):
        if matched_names['patient_name_from_master'].str.contains(cleaned_name):
            name_file_num_master = source_df[index][['patient_name', 'file_number']]
            #op_list = np.append(matched_names, name_file_num_master)
    return name_file_num_master

enu_op = get_file_number(patient_master_file, ffpe_db)