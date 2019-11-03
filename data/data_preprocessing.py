import pandas as pd

df = pd.read_csv('ubc_course_calendar_data.csv')


def select_data(year='2018W', term='1', campus='UBC', data=df):
    mask1 = data['SESSION_YEAR'] == year
    mask2 = data['CAMPUS'] == campus
    mask3 = data['TERM'] == term
    data = data[mask1 & mask2 & mask3]

    # print(f'Current number of courses: {data.shape[0]}')
    data.to_csv(f'{year}T{term}_{campus}.csv')
