import pandas as pd
import re
import fuzzywuzzy
from fuzzywuzzy import fuzz
import Levenshtein

patient_name_mater = pd.read_excel('D:\\Shweta\\Patient_name_matching\\2010_2018_names_file_number.xlsx')
ffpe_db = pd.read_excel('D:\\Shweta\\Patient_name_matching\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx')

# clean the name and make it lower case, removes unnecessary characters
def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', '', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names


def get_best_match(source_file, test_file):
    best_score = 0
    best_match = None
    patient_name_from_master = clean_names(df=source_file, name_str='patient_name')
    patient_name_to_match = clean_names(df=test_file, name_str='Patient Name')

    for index, row in source_file.iterrows():
        patient_name = row['patient_name']
        file_number = row['file_number']
    for name in patient_name_to_match:
        score = fuzz.WRatio(name, patient_name)
        if score > best_score:
            best_match = name
            best_score = score
            file_number = file_number
            output_df = pd.DataFrame(name, best_match, best_score, file_number)
    return output_df

matched_list = get_best_match(patient_name_mater, ffpe_db)
