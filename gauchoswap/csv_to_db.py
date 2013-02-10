from gauchoswap import db
from gauchoswap.models import Lecture, Section, Lab
from course_abrev import course_abrv_to_department

import csv
import datetime
import os


def scrape_csv():

    schedule_file = os.path.join(os.path.dirname(__file__), 'Spring_13_Schedule.csv')
    with open(schedule_file, 'rb') as f:
        course_rows = csv.reader(f)
        columns = course_rows.next()
        col_name_to_index = {col: index for index, col in enumerate(columns)}

        is_section = lambda section_code: not section_code.endswith('00')
        is_lab = lambda name: name.endswith('L')
        is_lecture = lambda section_code: section_code.endswith('00')
        current_lecture = None
        for course in course_rows:
            init_dict = {}
            init_dict['name'] = ' '.join(course[col_name_to_index['Course']].strip().split())
            init_dict['title'] = course[col_name_to_index['TITLE']]
            init_dict['department'] = course_abrv_to_department[' '.join(init_dict['name'].split()[:-1])]
            init_dict['location'] = course[col_name_to_index['Room_1']].strip()
            init_dict['days'] = course[col_name_to_index['Days_1']].strip()
            start_time = course[col_name_to_index['Begin_1']]
            end_time = course[col_name_to_index['End_1']]
            init_dict['time'] = ' - '.join(military_to_standard(start_time, end_time))
            init_dict['max_spots'] = course[col_name_to_index['MAX']].strip()
            init_dict['space'] = course[col_name_to_index['Seats']].strip()
            init_dict['teacher'] = course[col_name_to_index['INSTR_1']].strip()

            section_code = course[col_name_to_index['Section']]
            if is_lab(init_dict['name']):
                print 'adding: %s' % init_dict['name'] + ' lab'
                create_lab(**init_dict)
            elif is_lecture(section_code):
                print 'adding: %s' % init_dict['name'] + ' lecture'
                current_lecture = create_lecture(**init_dict)
            elif is_section(section_code):
                print 'adding: %s' % init_dict['name'] + ' section'
                create_section(current_lecture, **init_dict)

        print 'commiting errtang'
        db.session.commit()


def military_to_standard(start, end):
    def format_time_string(time, am=True, noon=False):
        time_period = 'AM' if am else 'PM'
        hour_indicies = (0, 1) if len(time) == 3 else (0, 2)
        minute_indicies = (1, 3) if len(time) == 3 else (2, 4)
        time_obj = datetime.time(hour=int(time.__getslice__(*hour_indicies)), minute=int(time.__getslice__(*minute_indicies)))

        return time_obj.isoformat()[:-3] + time_period

    def convert_time(time):
        if int(time) < 1200:
            converted_time = format_time_string(time)
        elif int(time) in range(1200, 1260):
            converted_time = format_time_string(time, am=False, noon=True)
        else:
            time = str(int(time) - 1200)
            converted_time = format_time_string(time, am=False)

        return converted_time

    converted_start = convert_time(start) if len(start.strip()) else ''
    converted_end = convert_time(end) if len(end.strip()) else ''

    return converted_start, converted_end


def create_lecture(**kwargs):
    professor = kwargs['teacher']
    del kwargs['teacher']
    l = Lecture(professor, **kwargs)
    db.session.add(l)
    return l


def create_section(lecture, **kwargs):
    ta = kwargs['teacher']
    del kwargs['teacher']
    s = Section(ta, lecture, **kwargs)
    db.session.add(s)


def create_lab(**kwargs):
    instructor = kwargs['teacher']
    del kwargs['teacher']
    l = Lab(instructor, **kwargs)
    db.session.add(l)

if __name__ == '__main__':
    try:
        scrape_csv()
    except:
        db.session.rollback()
        raise
