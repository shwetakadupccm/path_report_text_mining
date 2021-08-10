import pandas as pd
import re
import os
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import datetime
import numpy as np

folder = 'D:\\Shweta\\file_num_not_available\\'
master_file_name = '2010_2018_name_file_number_whole.xlsx'
file_num_not_available_file = 'file_number_not_availablewithnameandsxdate_RB_02_03_2021_updated.xlsx'
surgery_data_file = '1179 Breast Sx Cases 2010 Till 2020  - Updated 19-01-2021   Sheet.xlsx'
master_file_path = os.path.join(folder, master_file_name)
file_num_not_available_file_path = os.path.join(folder, file_num_not_available_file)
surgery_data_file_path = os.path.join(folder, surgery_data_file)
master_file = pd.read_excel(master_file_path)
test_file = pd.read_excel(file_num_not_available_file_path)
surgery_data = pd.read_excel(surgery_data_file_path)

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names


def find_date(sx_df, dt_str):
    dts = []
    for sx_dt in sx_df[dt_str]:
        match = re.search('\d{4}-\d{2}-\d{2}', str(sx_dt))
        if match is not None:
            dt = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            dts.append(str(dt))
        else:
            dts.append(sx_dt)
    return dts


# def find_file_num_from_surgery_list(surgery_df, test_file, surgery_name_str ='Name ', surgery_dt_str = 'Sx Date', surgery_file_str = 'File_number',
#                                     test_name_str='736 Breast surgery by Dr. koppiker 2010-2018', test_dt_str = 'Surgery Date'):
#     surgery_clean_names = clean_names(surgery_df, surgery_name_str)
#     surgery_clean_date = find_date(surgery_df, surgery_dt_str)
#     test_clean_names = clean_names(test_file, test_name_str)
#     test_clean_date = find_date(test_file, test_dt_str)
#     matched_list = []
#     for index, name in enumerate(test_clean_names):
#         matched_name = process.extractOne(query=name, choices=surgery_clean_names,
#                                           score_cutoff=100, scorer=fuzz.token_set_ratio)
#         if matched_name is not None:
#             test_cols = [test_name_str, test_dt_str]
#             test_dat = test_file.iloc[index][test_cols]
#             surgery_cols = [surgery_name_str, surgery_dt_str, surgery_file_str]
#             surgery_index = surgery_clean_names.index(matched_name[0])
#             surgery_dat = surgery_df.iloc[surgery_index][surgery_cols]
#             score = matched_name[1]
#             output_dat = np.append(test_dat, surgery_dat)
#             final_output_list = np.append(output_dat, score)
#             matched_list.append(final_output_list)
#             matched_df = pd.DataFrame(matched_list, columns=[test_name_str, test_dt_str, surgery_name_str,
#                                                              surgery_dt_str, surgery_file_str, 'score'])
#             matched_df['comparison'] = np.where(matched_df[test_dt_str] == matched_df[surgery_dt_str], True, False)
#     return matched_df


# matched_df = find_file_num_from_surgery_list(surgery_data, test_file, surgery_name_str ='Name ', surgery_dt_str = 'Sx Date',
#                                              surgery_file_str = 'File_number',test_name_str='736 Breast surgery by Dr. koppiker 2010-2018',
#                                              test_dt_str = 'Surgery Date')


def find_file_num_from_master_list(source_file, test_file, source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='736 Breast surgery by Dr. koppiker 2010-2018'):
    source_clean_names = clean_names(source_file, source_name_str)
    test_clean_names = clean_names(test_file, test_name_str)
    matched_list = []
    for index, name in enumerate(test_clean_names):
        matched_name = process.extractOne(query=name, choices=source_clean_names,
                                           scorer=fuzz.token_set_ratio)
        if matched_name is not None:
            test_cols = [test_name_str]
            test_dat = test_file.iloc[index][test_cols]
            source_cols = [source_name_str, source_file_str]
            source_index = source_clean_names.index(matched_name[0])
            source_dat = source_file.iloc[source_index][source_cols]
            score = matched_name[1]
            output_dat = np.append(test_dat, source_dat)
            final_output_list = np.append(output_dat, score)
            matched_list.append(final_output_list)
            matched_df = pd.DataFrame(matched_list, columns=[test_name_str, source_name_str,
                                                             source_file_str, 'score'])
            #matched_df['comparison'] = np.where(matched_df[test_dt_str] == matched_df[surgery_dt_str], True, False)
    return matched_df


matched_names_file_num = find_file_num_from_master_list(master_file,test_file,source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='736 Breast surgery by Dr. koppiker 2010-2018')

matched_names_file_num.to_excel(os.path.join(folder, '2021_02_03_matched_names_file_number_all_sk.xlsx'))