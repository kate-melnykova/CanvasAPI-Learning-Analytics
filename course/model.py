import json

class Section:
    def __init__(self, data):
        self.session_year = data['SESSION_YEAR']
        self.course_title = data['COURSE_TITLE']
        self.course_description = data['COURSE_DESCRIPTION']
        self.faculty = data['FACULTY']
        self.subject_code = data['SUBJECT_CODE']
        self.course_number = data['COURSE_NUMBER']
        self.section_number = data['SECTION_NUMBER']
        self.section_type = data['SECTION_TYPE']
        self.credits = data['CREDITS']
        self.pre_requisitive_descriptions = data['PRE_REQUISITE_DESCRIPTIONS']
        self.co_prerequisitive_descriptions = data['CO_PRE_REQUISITE_DESCRIPTIONS']
        self.term = data['TERM']
        self.daysmet = data['DAYSMET']
        self.start_time = data['START_TIME']
        self.end_time = data['END_TIME']
        self.campus = data['CAMPUS']
        self.building = data['BUILDING']
        self.room_number = data['ROOM_NUMBER']
        self.instructors = data['INSTRUCTORS']
        self.total_seats_remaining = data['TOTAL_SEATS_REMAINING']
        self.currently_registered = data['CURRENTLY_REGISTERED']
        self.general_seats_remaining = data['GENERAL_SEATS_REMAINING']
        self.restricted_seats_remaining = data['RESTRICTED_SEATS_REMAINING']
        self.prereq_list = json.loads(data['PREREQ_LIST'])
        self.prereq_cond = data['PREREQ_COND']
        self.prereq_grade = data['PREREQ_GRADE']
        self.prereq_titles = json.loads(data['PREREQ_TITLES'])
        self.prereq_satisfied = json.loads(data['PRE_REQ_SATISFIED'])