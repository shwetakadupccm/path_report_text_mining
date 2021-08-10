import pandas as pd
import numpy as np
import uuid
import os

TABLE_DICT = {'block_information': 'primary',
                'fnac': ['site', 'type'],
                'biopsy': ['site', 'type'],
                'biopsy_ihc': ['site', 'type'],
                'surgery': 'type',
                'surgery_ihc': 'type'}


table_types_site = {'type': ['primary', 'review'],
                    'site': ['breast', 'node','other']}


# reasons = ['Reason_for_Biopsy', 'Reason for Surgery', 'Reason for Review_Surgery']

def generate_pk(df):
    pks = []
    for i in range(0, len(df)):
        pk = uuid.uuid4().hex
        pks.append(pk)
    return pks


def get_table_map(mapping, table):
    dat = mapping[['old_names', table]]
    filtered_df = dat[dat[table].notnull()]
    filtered_df = filtered_df.rename(columns = {table : 'table_tbd'})
    return filtered_df


def get_old_col(filtered_df, new_col):
    new_col = (filtered_df[filtered_df.table_tbd == new_col])
    old_col = new_col['old_names']
    return old_col

    
def add_fk(df, key_col_name):
    df[key_col_name] = generate_pk(df)
    return df


def get_input_data():
    folder = 'D:\\Shweta\\Blocks_updated_data'
    ffpe_file = '2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx'
    mapping_file = '2021_02_15_column_names_mapping_sk.xlsx'
    ffpe_db_path = os.path.join(folder, ffpe_file)
    mapping_path = os.path.join(folder, mapping_file)
    ffpe_db = pd.read_excel(ffpe_db_path)
    mapping = pd.read_excel(mapping_path)
    ffpe_db = add_fk(ffpe_db, 'pk')
    return (ffpe_db, mapping)


def add_old_data_new_cols():
    # df = add_pk(df)
    ffpe_db, mapping = get_input_data()    
    tables = TABLE_DICT.keys()
    table_type_site = table_types_site.keys()
    writer = pd.ExcelWriter('mapped_ffpe.xlsx', engine = 'xlsxwriter')
    for table in tables:
        reasons = '?'
        # create pk/reason table
        for reason in reasons:
            for site in table_type_site:
                for type in table_type_site:
                    col_maps = get_table_map(mapping, table)
                    df_all = pd.DataFrame(ffpe_db['pk'])
                    col_list = list(col_maps['table_tbd'])
                for col in col_list:
                    old_col = get_old_col(col_maps, col)
                    print(col, old_col)
                    # old_col_dat = ffpe_db_reason[old_col]
                    # dat = df_all['pk'], old_col_dat]
                    df_col = df_all
                    try:
                        df_col[col] = ffpe_db[old_col]
                    except:
                        df_col[col] = [None]*len(ffpe_db)
                    print(df_all.head())
                    df_table = pd.merge(df_all, df_col, on='pk')
                    df_table['fk'] = add_fk(df_table, key_col_name='fk')
                df_table.to_excel(writer, sheet_name=table, index=False)
                print(table, 'done')
    writer.save()


def get_mapped_df(df, mapping, table):
    col_maps = get_table_map(mapping, table)
    new_df = add_old_data_new_cols(df, col_maps)
    return new_df


if '__name__' == '__main__':
    add_old_data_new_cols()
    # filt_df = get_table_map(ffpe_db, mapping)