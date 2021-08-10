import pandas as pd
from fuzzywuzzy import process
import numpy as np

ffpe_dat = pd.read_excel('D:\\Shweta\\ffpe_db_column_entries\\2021_01_25_PCCM_FFPE_1_672_values.xlsx')
defined_voc = pd.read_excel('D:\\Shweta\\ffpe_db_column_entries\\defined_vocab.xlsx')


ffpe_dat['all_values'] = ffpe_dat[ffpe_dat.columns[1:]].apply(
    lambda x: ','.join(x.dropna().astype(str)), axis = 1)


defined_voc['all_vocab'] = defined_voc[defined_voc.columns[1:]].apply(
    lambda x: ','.join(x.dropna().astype(str)), axis = 1)


ffpe_voc_dat = ffpe_dat[['col names', 'all_values']]
defined_voc_dat = defined_voc[['col names', 'all_vocab']]

ffpe_voc_dat = ffpe_voc_dat.rename(columns = {'col names' : 'ffpe_col_names',
                               'all_values' : 'ffpe_unique_values'})

defined_voc_dat = defined_voc_dat.rename(columns = {'col names' : 'vocab_col_names',
                                                'all_vocab': 'def_vocab_values'})

vocab = pd.concat([ffpe_voc_dat, defined_voc_dat], axis = 1)

 
def intersection(l1, l2):
    l3 = [value for value in l1 if value in l2]
    return l3
 
# def remove_voc_from_unique_entries(df, ffpe_col_name_str = 'ffpe_col_names', voc_col_name_str = 'vocab_col_names',
#                                    ffpe_val_str = 'ffpe_unique_values', voc_val_str = 'def_vocab_values'):
#     for col in df[ffpe_col_name_str]:
#         #print(col)
#         for col1 in df[voc_col_name_str]:
#             #print(col1)
#             if col == col1:
#                 for val1 in df[ffpe_val_str]:
#                     val1 = str(val1).split(',')
#                     for val2 in df[voc_val_str]:
#                         val2 = str(val2).split(',')
#
#                         int_sec = intersection(val1, val2)
#     return int_sec


def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        clean_name = str(name).lower()
        cleaned_names.append(clean_name)
    return cleaned_names


def split_the_column_entries(df, name_str):
    lst = []
    for value in df[name_str]:
        clean_value = str(value).split(',')
        lst.append(clean_value)
    return lst

def find_common_col(df, ffpe_col_name_str = 'ffpe_col_names', voc_col_name_str = 'vocab_col_names',
                    ffpe_val_str = 'ffpe_unique_values', voc_val_str = 'def_vocab_values'):
    ffpe_clean_names = clean_names(df, ffpe_col_name_str)
    voc_clean_names = clean_names(df, voc_col_name_str)
    common_col = []
    int_sec_lst = []
    for index, col in enumerate(ffpe_clean_names):
        #print(col)
        same_col = process.extractOne(query=col, choices=voc_clean_names, score_cutoff=100)
        #print(same_col)
        if same_col is not None:
            ffpe_values = df.iloc[index][[ffpe_val_str]]
            same_col_name = same_col[0]
            same_col_index = voc_clean_names.index(same_col_name)
            vocab_values = df.iloc[same_col_index][[voc_val_str]]
            for val1 in ffpe_values:
                val1 = str(val1).split(',')
                #print(val1)
                for val2 in vocab_values:
                    val2 = str(val2).split(',')
                    #print(val2)
                    int_sec = intersection(val1, val2)
                    final_list = list(set(ffpe_values) - set(int_sec))
                    print(final_list)
            output_list = np.append(col, same_col_name)
            common_col.append(output_list)
            common_df = pd.DataFrame(common_col, columns=['ffpe_col_names', 'vocab_col_names'])
    return int_sec, common_df

int_sec, com_col = find_common_col(vocab, ffpe_col_name_str = 'ffpe_col_names', voc_col_name_str = 'vocab_col_names',
                          ffpe_val_str = 'ffpe_unique_values', voc_val_str = 'def_vocab_values')



# for val1 in vocab['ffpe_unique_values']:
#     val1 = str(val1).split(',')
#     for val2 in vocab['def_vocab_values']:
#         val2 = str(val2).split(',')
#
#         int_sec = intersection(val1, val2)
#         print(int_sec)

# ffpe_col_entries = split_the_column_entries(vocab, 'ffpe_unique_values')
# voc_col_entries = split_the_column_entries(vocab, 'def_vocab_values')
#
# for val1 in ffpe_col_entries:
#     for val2 in voc_col_entries:
#         lst = list(set(val1)-set(val2))
#         print(lst)

# def find_same_col(df, ffpe_col_name_str = 'ffpe_col_names', voc_col_name_str = 'vocab_col_names'):
#     for col in df[ffpe_col_name_str]:
#         print(col)
#     for col1 in df[voc_col_name_str]:
#         print(col1)
#         if col == col1:
#             return col, col1
#
# names = find_same_col(vocab, ffpe_col_name_str = 'ffpe_col_names', voc_col_name_str = 'vocab_col_names')
