import pandas as pd

from course.model import Section


def select_all_sections(subject_code,
                        course_number,
                        year='2018W',
                        term='1',
                        campus='UBC'):
    data = pd.read_csv(f'./data/user_{year}T{term}_{campus}_reqs_filled.csv')

    course = []
    for idx, row in data.iterrows():
        if row['SUBJECT_CODE'] == subject_code and row['COURSE_NUMBER'] == course_number:
            course.append(Section(row))
    return course
