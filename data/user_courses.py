import dotenv
import os
import canvasapi

import pandas as pd

dotenv.load_dotenv(dotenv.find_dotenv())

# TOKEN = os.environ.get('CANVAS_API_TOKEN')
TOKEN = '11224~cIKr3JVQ4jrnetydawaWK74SbLHijg8f8aytW9HTtyh1vhuKzVbQdMYRfkX6gc1C'
BASEURL = 'https://ubc.instructure.com'

canvas_api = canvasapi.Canvas(BASEURL, TOKEN)

result = canvas_api.get_user('self')
print(result)
# print(dir(result))
print('_________')
data = pd.DataFrame(columns=['course_id', 'subject_code', 'course_number', 'state'])
for course in result.get_courses(enrollment_state='completed'):
    try:
        z = course.course_code.split(' ')
        subject_code = z[0]
        course_number = z[1]
        int(course_number[:3])
    except:
        print(f'Course is not in traditional encoding: {course.course_code}')
    else:
        data.loc[data.shape[0]] = [course.id, subject_code, course_number, 'completed']

print(data)
data.to_csv('courses_taken.csv')