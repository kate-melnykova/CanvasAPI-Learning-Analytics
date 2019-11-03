from typing import List, Tuple
import json
import os.path

import numpy as np
import pandas as pd

df = pd.read_csv('./data/ubc_course_calendar_data.csv')


def select_data(year='2018W', term='1', campus='UBC', data=df):
    mask1 = data['SESSION_YEAR'] == year
    mask2 = data['CAMPUS'] == campus
    mask3 = data['TERM'] == term
    data = data[mask1 & mask2 & mask3]

    # print(f'Current number of courses: {data.shape[0]}')
    data.to_csv(f'./data/{year}T{term}_{campus}.csv')
    return data


# data engineering: add column with course names
def add_prereq_titles(pre_reqs: str or None) -> List[Tuple[str]]:
    if isinstance(pre_reqs, float):
        return [json.dumps([]), '', '']

    if '.' not in pre_reqs:
        return [json.dumps([]), '', '']
    pre_reqs = pre_reqs.split('.')[:-1]
    course_r = pre_reqs[0].replace('and', ' ')
    course_r = course_r.replace('or', ' ')
    if course_r.startswith('All of '):
        condition = 'all of'
        course_r = course_r[7:]
    elif course_r.startswith('One of '):
        condition = 'one of'
        course_r = course_r[7:]
    else:
        condition = ''
    course_r = course_r.split(',')
    for i, course in enumerate(course_r):
        course = course.strip()
        course = course.split(' ')
        course_r[i] = (course[0], course[-1])
    course_r = json.dumps(course_r)
    if len(pre_reqs) > 1:
        return [course_r, condition, pre_reqs[1]]
    else:
        return [course_r, condition, '']


def add_prereqs(year='2018W', term='1', campus='UBC'):
    if not os.path.exists(f'./data/{year}T{term}_{campus}.csv'):
        select_data(year, term, campus)

    data = pd.read_csv(f'./data/{year}T{term}_{campus}.csv')
    data = data.drop(['Unnamed: 0'], axis=1)

    course_req = []
    cond = []
    grade_req = []
    for idx, val in data['PRE_REQUISITE_DESCRIPTIONS'].items():
        [val1, val2, val3] = add_prereq_titles(val)
        course_req.append(val1)
        cond.append(val2)
        grade_req.append(val3)

    data['PREREQ_LIST'] = course_req
    data['PREREQ_COND'] = cond

    def find_course_title(course_list):
        course_list = json.loads(course_list)
        if not isinstance(course_list, list):
            return []
        lst = []
        for subject_code, course_number in course_list:
            mask = (data['SUBJECT_CODE'] == subject_code) & (data['COURSE_NUMBER'] == course_number)
            course_description = data[mask]['COURSE_DESCRIPTION']
            try:
                lst.append(course_description.iloc[0])
            except:
                lst.append('')
        return json.dumps(lst)

    data['PREREQ_GRADE'] = grade_req

    data['PREREQ_TITLES'] = data['PREREQ_LIST'].apply(find_course_title)
    data.to_csv(f'./data/{year}T{term}_{campus}_processed.csv')
