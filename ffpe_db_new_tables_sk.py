import pandas as pd
import uuid
import os

# ffpe_db = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx')
# # # mapping  = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\Final_R_code_excel_files\\2021_02_15_column_names_mapping_sk.xlsx')

TABLE_DICT = {'block_information': 'primary',
                'fnac': ['site', 'type'],
                'biopsy': ['site', 'type'],
                'biopsy_ihc': ['site', 'type'],
                'surgery': 'type',
                'surgery_ihc': 'type'}


table_types_site = {'type': ['primary', 'review'],
                    'site': ['breast', 'node']}


def generate_pk(df):
    pks = []
    for i in range(0, len(df)):
        pk = uuid.uuid4().hex
        pks.append(pk)
    return pks


def add_fk(df, key_col_name):
    df[key_col_name] = generate_pk(df)
    return df


def get_input_data():
    folder = 'D:\Shweta\Blocks_updated_data\input_files'
    ffpe_file = '2021_01_25_PCCM_FFPE_1_672.xlsx'
    mapping_file = '2021_02_13FFPE_column_names_mapping_sk.xlsx'
    ffpe_db_path = os.path.join(folder, ffpe_file)
    mapping_path = os.path.join(folder, mapping_file)
    ffpe_db = pd.read_excel(ffpe_db_path)
    mapping = pd.read_excel(mapping_path)
    ffpe_db = add_fk(ffpe_db, 'pk')
    return (ffpe_db, mapping)


def get_table_map(mapping, table):
    dat = mapping[['old_names', table]]
    map_df = dat[dat[table].notnull()]
    map_df = map_df.rename(columns = {table: 'table_tbd'})
    new_cols = list(map_df['table_tbd'])
    return map_df, new_cols


def get_old_col(map_df, new_col):
    new_col = (map_df[map_df.table_tbd == new_col])
    old_col = new_col['old_names'].to_list()[0]
    return old_col


def add_old_data_new_cols(df, map_df, new_cols):
    df_all = pd.DataFrame(df['pk'])
    for col in new_cols:
        old_col = get_old_col(map_df, col)
        df_col = pd.DataFrame(df_all['pk'])
        try:
            df_col[col] = df[old_col]
        except KeyError:
            df_col[col] = ['data_not_curated'] * len(df)
        df_all = pd.merge(df_all, df_col, on='pk')
    return df_all


def get_mapped_df():
    df, mapping = get_input_data()
    tables = list(TABLE_DICT.keys())
    table_values = TABLE_DICT.values()
    types = table_types_site.get('type')
    sites = table_types_site.get('site')
    writer = pd.ExcelWriter('D:\\Shweta\\Blocks_updated_data\\output_files\\ffpe_new_tables_type_site.xlsx', engine = 'xlsxwriter')
    for table in tables:
        table_df = pd.DataFrame()
        for type in types:
            for site in sites:
                if type in table_values:
                    map_df, new_cols = get_table_map(mapping, table)
                    df_mapped = add_old_data_new_cols(df, map_df, new_cols)
                    df_mapped['type'] = type
                    df_mapped['site'] = site
                    df_mapped['fk'] = add_fk(df_mapped, 'fk')
                    table_df = table_df.append(df_mapped, ignore_index=True)
        table_df.to_excel(writer, sheet_name=table, index=False)
        print(table)
        print(table_df.columns)
    writer.save()


if '__name__' == '__main__':
    new_df = get_mapped_df()

# def add_old_data_new_cols(df, map_df):
#     df_all = pd.DataFrame(df['pk'])
#     for col in map_df['table_tbd']:
#         old_col = get_old_col(map_df, col)
#         df_col = pd.DataFrame(df_all['pk'], columns=['pk'])
#         df_col[old_col] = [None]*len(df)
#         #df_col = df_col.rename(columns={col: old_col})
#         if old_col is not None:
#             df_col[old_col] = df[[old_col]]
#         df_all = pd.merge(df_col, df_all, on='pk')
#         df_all = df_all.rename(columns= {old_col: col})
#     return df_all

# def add_old_data_new_cols():
#     ffpe_db, mapping = get_input_data()
#     tables = TABLE_DICT.keys()
#     types =
