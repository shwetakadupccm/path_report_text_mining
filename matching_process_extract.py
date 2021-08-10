import pandas as pd
import os
import re
from fuzzywuzzy import process

def clean_names(file, folder, name_str):
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path)
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', '', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names


def find_matched_name(source_file, test_file, folder):
    source_name_file_num_path = os.path.join(folder, source_file)
    source_name_file_num = pd.read_excel(source_name_file_num_path)
    master_list = clean_names(source_file, folder, 'patient_name')
    test_list = clean_names(test_file, folder, 'Patient Name')
    matched_list = []

    for index, patient_name in enumerate(test_list):
        matched_name = process.extractOne(patient_name, master_list, score_cutoff=100)
        if matched_name is not None:
            row_no = index
            name_file_num = source_name_file_num.iloc[row_no]
            matched_list.append(name_file_num)
    return matched_list


