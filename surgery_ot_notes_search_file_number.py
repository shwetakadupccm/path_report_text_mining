import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz, process

ot_notes_df = pd.read_excel('D:\\Shweta\\surgery_ot_notes\\PCCM_Surgery_OT notes_10-03-2021_RB_RU_DA.xlsx')
master_file = pd.read_excel('D:\\Shweta\\Patient_name_matching\\master_list\\2010_2018_name_file_number_whole.xlsx')


ot_notes_df['full_name'] = ot_notes_df[ot_notes_df.columns[1:4]].apply(
    lambda x: ' '.join(x.dropna().astype(str)), axis = 1)


# def create_full_name(df, first_name_str, middle_name_str, last_name_str):
#     full_names = []
#     for i in range(len(df)):
#         full_name = df[i][first_name_str, middle_name_str, last_name_str].apply(
#             lambda x: ' '.join(x.dropna().astype(str)), axis = 1)
#         full_names.append(full_name)
#     return full_names

# names = create_full_name(ot_notes_df, first_name_str = 'First Name', middle_name_str = 'Middle Name', last_name_str = 'Last Name')

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        clean_name = re.sub('[^a-zA-Z]', ' ', str(name))
        clean_name = clean_name.lower()
        cleaned_names.append(clean_name)
    return cleaned_names

def find_file_number_from_master_list(master_df, ot_notes_df, master_name_str='patient_name',
                                      master_file_num_str='file_number', ot_notes_name_str='full_name'):
    master_cleaned_names = clean_names(master_df, master_name_str)
    ot_notes_clean_names = clean_names(ot_notes_df, ot_notes_name_str)
    matched_names = []

    for name in ot_notes_clean_names:
        matched_name = process.extractOne(query=name, choices=master_cleaned_names, scorer=fuzz.token_set_ratio)
        if matched_name is not None:
            master_name_index = master_cleaned_names.index(matched_name[0])
            master_cols = [master_name_str, master_file_num_str]
            master_dat = master_df.iloc[master_name_index][master_cols]
            lst = np.append(name, master_dat)
            matched_names.append(lst)
            output_df = pd.DataFrame(matched_names, columns= ['patient_name_from_ot_list', 'patient_name_from_master', 'file_number'])
    return output_df

df = find_file_number_from_master_list(master_file, ot_notes_df, master_name_str='patient_name',
                                      master_file_num_str='file_number', ot_notes_name_str='full_name')

df.to_excel('D:\\Shweta\\surgery_ot_notes\\master_ot_patient_names_file_nums.xlsx', index=False)




