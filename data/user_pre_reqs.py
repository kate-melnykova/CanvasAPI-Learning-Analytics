from typing import List
import json

import pandas as pd
import numpy as np

url = 'https://docs.google.com/spreadsheets/d/1kPzVTGq_dqic6YZbQvnE9WvRWbbdxm69U5ro9Wdd-HU/edit#gid=1364618903'
url = url.replace('/edit#gid=', '/export?format=csv&gid=')

user_data = pd.read_csv(url, dtype=str)
user_data['subject_code'] = user_data['subject_code'].apply(lambda x: x.strip())
user_data['course_number'] = user_data['course_number'].apply(lambda x: x.strip())

course_data = pd.read_csv('2018WT1_processed.csv')


def is_course_taken(course: str) -> bool:
    subject_code = course[0]
    course_number = course[-1]
    mask1 = user_data['subject_code'] == subject_code
    mask2 = user_data['course_number'] == course_number
    matched_courses = user_data[mask1 & mask2]
    return matched_courses.shape[0] > 0


def is_course_list_taken(course_list: List) -> List[bool]:
    course_list = json.loads(course_list)
    # print(type(course_list), course_list)
    if not isinstance(course_list, list):
        return np.nan
    return json.dumps([is_course_taken(course) for course in course_list])


course_data['PRE_REQ_SATISFIED'] = course_data['PREREQ_LIST'].apply(is_course_list_taken)

course_data.to_csv('user_pre_reqs_filled.csv')
