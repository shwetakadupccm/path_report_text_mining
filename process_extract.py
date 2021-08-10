import pandas as pd
import re
import os
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import numpy as np

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names


def find_matched_name_file_num(source_file, test_file, source_name_str='patient_name', test_name_str='Patient Name',
                      source_file_str='file_number', test_file_str='File_Number'):
    clean_source = 'clean_' + source_name_str
    clean_test = 'clean_' + test_name_str
    source_clean_names = clean_names(source_file, source_name_str)
    source_file[clean_source] = source_clean_names
    test_clean_names = clean_names(test_file, test_name_str)
    test_file[clean_test] = test_clean_names
    matched_list = []

    for test_index, test_clean_name in enumerate(test_clean_names):
        matched_name = process.extractOne(query=test_clean_name, choices=source_clean_names, scorer = fuzz.token_sort_ratio)
        if matched_name is not None:
            test_cols = [test_name_str, test_file_str, clean_test]
            source_col = [source_name_str, source_file_str, clean_source]
            source_index = source_clean_names.index(matched_name[0])
            # find index of matched_name in source_clean_names (is pulled from best match in source).
            #  use that to pull out source data like done for test data.
            test_dat = test_file.iloc[test_index][test_cols]
            source_dat = source_file.iloc[source_index][source_col]
            score = matched_name[1]
            output_list = np.append(test_dat, source_dat)
            final_output_list = np.append(output_list, score)
            matched_list.append(final_output_list)
            col_list = ['test_'+test_name_str, 'test_'+test_file_str, 'clean_test',  'source_'+source_name_str,
                        'source_'+source_file_str, 'clean_source', 'matched_score']
            matched_df = pd.DataFrame(matched_list, columns=col_list)
            matched_df['comparison'] = np.where(matched_df['test_' + test_file_str] == matched_df['source_' + source_file_str],
                True, False)
    return matched_df, source_clean_names, test_clean_names


source_file_name = "2010_2018_name_file_number_whole.xlsx"
test_file_name = "2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx"
folder = 'D:\\Shweta\\Patient_name_matching'
source_path = os.path.join(folder, source_file_name)
test_path = os.path.join(folder, test_file_name)
source_file = pd.read_excel(source_path)
test_file = pd.read_excel(test_path)

matched_names, source_clean_names, test_clean_names =find_matched_name_file_num(source_file, test_file, source_name_str='patient_name',
                  test_name_str='Patient Name', source_file_str='file_number', test_file_str='File_Number')
matched_names.to_excel(os.path.join(folder, '20_02_2021_names_file_number_score.xlsx'))

sum(matched_names['comparison']==True)
sum(matched_names['comparison']==False)

