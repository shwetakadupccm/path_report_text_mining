import os
import re


def clean_path_report_names(path):
    path_reports = os.listdir(path)
    cleaned_path_report_names = []
    for path_report in path_reports:
        cleaned_path_report = re.sub('[^a-zA-Z_0-9]', '_', path_report)
        cleaned_path_report = cleaned_path_report.lower()
        cleaned_path_report = cleaned_path_report.split('_')
        cleaned_path_report = '_'.join(cleaned_path_report)
        cleaned_path_report = cleaned_path_report.replace("__", "_")
        cleaned_path_report = cleaned_path_report.replace("___", "_")
        cleaned_path_report = cleaned_path_report.replace("_pdf", '.pdf')
        source = os.path.join(path, path_report)
        destination = os.path.join(path, cleaned_path_report)
        os.rename(source, destination)
        cleaned_path_report_names.append(cleaned_path_report)
    return cleaned_path_report_names

clean_path_report_names('D:\\Shweta\\Surgery\\Jehangir_Surgery_Path_Reports\\')
