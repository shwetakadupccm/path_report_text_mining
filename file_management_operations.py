import os
import datetime
import shutil
import re
import pandas as pd

# SOURCE_FOLDER = r"D:\Shweta\Histopath_Reports 2019_05"
# REPORTS = pd.read_excel(r"D:\Shweta\Histopath_Reports 2019_05\reports_file_numbers.xlsx")


class FileManagement:

    def __init__(self, source_path, destination_path):
        self.source_path = source_path
        self.destination_path = destination_path

    ''' this function moves jpg files which have a date in the filename to a newly 
    created folder named with the date from filename. Files are moved from source_path to
    destinaion_path'''

    def create_date_dir_move_file(self, suffix='.jpg'):
        files = os.listdir(self.source_path)
        for file in files:
            if file.endswith(suffix):
                match = re.search('\d{4}-\d{2}-\d{2}', file)
                dt = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                dt_path = os.path.join(self.destination_path, str(dt))
                if not os.path.isdir(dt_path):
                    os.mkdir(dt_path)
                shutil.move(os.path.join(self.source_path, file), dt_path)


    '''this function renames a particular type of file with a name from a table of source file name and new file name.
    Table of source and new filenames is supplied as a two column csv (file_name, new_name). Adds an counter i if 
        '''
    def rename_file_name(self, suffix='.jpg'):
        i=0
        for file in os.listdir(self.source_path):
            if file.endswith(suffix):
                match = re.search('\d{4}-\d{2}-\d{2}', file)
                dt = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                source = os.path.join(self.source_path, file)
                test_name = os.path.join(self.source_path, "New_file_"+str(dt)+"_"+str(i)+".jpg")
                if os.path.exists(test_name):
                    i = i+1
                else:
                    i=0
                destination = os.path.join(self.source_path, "New_file_"+str(dt)+"_"+str(i)+".jpg")
                os.rename(source, destination)

########################

    '''this function renames the file from list. Provide the dataframe which have file_number and report name and in the 
    source path there is list of file names'''

class FileRenamingFromList:

    def __init__(self, source, reports, suffix=".pdf"):
        self.source = source
        self.reports = reports
        self.suffix = suffix

    @staticmethod
    def format_report_number(file_list):
        for file in file_list:
            x = file.replace("/", "_")
            return x

    @staticmethod
    def check_for_extension(report_name):
        for name in report_name:
            name_string = str(name).lower()
            if name_string.endswith('.pdf'):
                replaced_string = name_string[:-4]
                return replaced_string

    def rename_file(self):
        for file in os.listdir(self.source):
            if file.endswith(self.suffix):
                file = file[:-4]
                if file.isdigit():
                    file = str(file)
                    print(file)
        reports_str = self.reports.astype(str)
        reports = list(reports_str['ReportName'])
        if not os.path.isdir("renamed_reports"):
            os.mkdir(os.path.join(self.source, "renamed_reports"))

        for report in reports:
            query_stat = "ReportName == '" + report + "'"
            dat = reports_str.query(query_stat)
            new_name = self.format_report_number(dat["file_number"]) + "_Bx" + self.suffix
            print(new_name)
            newpath = os.path.join(self.source, "renamed_reports", new_name)
            print(newpath)
            report_path = os.path.join(self.source, report + self.suffix)
            shutil.move(report_path, newpath)
