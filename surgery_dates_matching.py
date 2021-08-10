import pandas as pd
import os
from fuzzywuzzy import process
import datetime
import dateparser
import re


def find_date(sx_df, dt_str = 'Sx Date'):
    dts = []
    for sx_dt in sx_df[dt_str]:
        match = re.search('\d{4}-\d{2}-\d{2}', str(sx_dt))
        if match is not None:
            dt = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            dts.append(str(dt))
        else:
            dts.append(sx_dt)
    return dts


def convert_all_dates_into_one_format(dates):
    dts = []
    for date in dates:
        dt_find = dateparser.parse(str(date))
        match = re.search('\d{4}-\d{2}-\d{2}', str(dt_find))
        if match is not None:
            dts.append(match[0])
        else:
            dts.append(date)
    return dts


def match_the_dates(path, sx_df, sx_images_dts, dt_str = 'Sx Date', sx_name_str = 'Name '):
    sx_dates = find_date(sx_df, dt_str)
    all_dates = convert_all_dates_into_one_format(sx_dates)
    sx_df['cleaned_sx_dates'] = all_dates
    for sx_image_dt in sx_images_dts:
        matched_dates = process.extractBests(query=sx_image_dt, choices=all_dates, score_cutoff=100)
        print(matched_dates)
        if matched_dates is not None:
            dt_gr = sx_df.groupby('cleaned_sx_dates')
            if len(matched_dates) == 1:
                matched_dt_gr = dt_gr.get_group(matched_dates[0][0])
                names = matched_dt_gr[sx_name_str]
                new_name = sx_image_dt + '_' + names.iloc[0]
                source = os.path.join(path, sx_image_dt)
                destination = os.path.join(path, new_name)
                os.rename(source, destination)
            if len(matched_dates) == 2:
                matched_dt_gr = dt_gr.get_group(matched_dates[0][0])
                names = matched_dt_gr[sx_name_str]
                new_name = sx_image_dt + '_' + names.iloc[0] + '_' + names.iloc[1]
                source = os.path.join(path, sx_image_dt)
                destination = os.path.join(path, new_name)
                os.rename(source, destination)
            if len(matched_dates) == 3:
                matched_dt_gr = dt_gr.get_group(matched_dates[0][0])
                names = matched_dt_gr[sx_name_str]
                new_name = sx_image_dt + '_' + names.iloc[0] + '_' + names.iloc[1] + '_' + names.iloc[2]
                source = os.path.join(path, sx_image_dt)
                destination = os.path.join(path, new_name)
                os.rename(source, destination)
            if len(matched_dates) == 4:
                matched_dt_gr = dt_gr.get_group(matched_dates[0][0])
                names = matched_dt_gr[sx_name_str]
                new_name = sx_image_dt + '_' + names.iloc[0] + '_' + names.iloc[1] + '_' + names.iloc[2] + '_' + names.iloc[3]
                source = os.path.join(path, sx_image_dt)
                destination = os.path.join(path, new_name)
                os.rename(source, destination)

sx_data = pd.read_excel('D:\\Shweta\\Surgery\\surgery_list.xlsx')
sx_images_dt = os.listdir('D:\\Shweta\\Surgery\\Date_Wise_Files\\')
matched_dates_and_names = match_the_dates('D:\\Shweta\\Surgery\\Date_Wise_Files\\', sx_data, sx_images_dt, dt_str = 'Sx Date', sx_name_str = 'Name ')

