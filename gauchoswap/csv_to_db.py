from gauchoswap import db
from gauchoswap.models import Class, Lecuture, Section, Lab

import csv
import datetime


def scrape_csv():

    course_abrv_to_department = {
        "ANTH": "Anthropology",
        "ART CS": "Art (Creative Studies)",
        "ARTHI": "Art History",
        "ARTST": "Art Studio",
        "AS AM": "Asian American Studies",
        "ASTRO": "Astronomy",
        "BIOL CS": "Biology (Creative Studies)",
        "BMSE": "Biomolecular Science and Engineering",
        "BL ST": "Black Studies",
        "CH E": "Chemical Engineering",
        "CHEM": "Chemistry and Biochemistry",
        "CH ST": "Chicano Studies",
        "CHIN": "Chinese",
        "CLASS": "Classics",
        "COMM": "Communication",
        "C LIT": "Comparative Literature",
        "CMPSC": "Computer Science",
        "CNCSP": "Counseling, Clinical, School Psychology",
        "DANCE": "Dance",
        "EARTH": "Earth Science",
        "EACS": "East Asian Cultural Studies",
        "EEMB": "Ecology, Evolution & Marine Biology",
        "ECON": "Economics",
        "ED": "Education",
        "ECE": "Electrical Computer Engineering",
        "ENGR": "Engineering Sciences",
        "ENGL": "English",
        "ESM": "Environmental Science & Management",
        "ENV S": "Environmental Studies",
        "ESS": "Exercise & Sport Studies",
        "ES": "Exercise Sport",
        "FEMST": "Feminist Studies",
        "FLMST": "Film Studies",
        "FR": "French",
        "GEN S CS": "General Studies (Creative Studies)",
        "GEOG": "Geography",
        "GER": "German",
        "GPS": "Global Peace and Security",
        "GLOBL": "Global Studies",
        "GREEK": "Greek",
        "HEB": "Hebrew",
        "HIST": "History",
        "INT": "Interdisciplinary",
        "ITAL": "Italian",
        "JAPAN": "Japanese",
        "KOR": "Korean",
        "LATIN": "Latin",
        "LAIS": "Latin American and Iberian Studies",
        "LING": "Linguistics",
        "LIT CS": "Literature (Creative Studies)",
        "MARSC": "Marine Science",
        "MATRL": "Materials",
        "MATH": "Mathematics",
        "ME": "Mechanical Engineering",
        "MAT": "Media Arts and Technology",
        "ME ST": "Medieval Studies",
        "MES": "Middle East Studies",
        "MS": "Military Science",
        "MCDB": "Molecular, Cellular & Develop. Biology",
        "MUS": "Music",
        "MUS A": "Music Performance Laboratories",
        "PHIL": "Philosophy",
        "PHYS": "Physics",
        "POL S": "Political Science",
        "PORT": "Portuguese",
        "PSY": "Psychology",
        "RG ST": "Religious Studies",
        "RENST": "Renaissance Studies",
        "SLAV": "Slavic",
        "SOC": "Sociology",
        "SPAN": "Spanish",
        "SHS": "Speech & Hearing Sciences",
        "PSTAT": "Statistics & Applied Probability",
        "TMP": "Technology Management",
        "THTR": "Theater",
        "WRIT": "Writing",
    }

    with open('Spring_13_Schedule.csv', 'rb') as f:
        course_rows = csv.reader(f)
        columns = course_rows.next()
        col_name_to_index = {col: index for index, col in enumerate(columns)}

        is_section = lambda section_code: not section_code.endswith('0')
        is_lab = lambda name: name.endswith('L')
        is_lecture = lambda section_code: section_code.endswith('0')
        for course in course_rows:
            init_dict = {}
            init_dict['name'] = course[col_name_to_index['Course']]
            init_dict['department'] = course_abrv_to_department[init_dict['name'].split()[:-1]]
            init_dict['location'] = course[col_name_to_index['Room1']]
            init_dict['days'] = course[col_name_to_index['Days_1']]
            start_time = course[col_name_to_index['Begin_1']]
            end_time = course[col_name_to_index['End_1']]
            init_dict['time'] = military_to_standard(start_time, end_time)
            init_dict['max_spots'] = course[col_name_to_index['MAX']]
            init_dict['space'] = course[col_name_to_index['Seats']]
            init_dict['teacher'] = course[col_name_to_index['INSTR_1']]

            section_code = course[col_name_to_index['Section']]
            if is_lecture(section_code):
                create_lecture(init_dict)
            elif is_section(section_code):
                create_section(init_dict)
            elif is_lab(name):
                create_lab(init_dict)


def military_to_standard(start, end):
    converted_start = ''
    converted_end = ''

    if len(start) > 3:
        converted_start = datetime.time(hours=int(start[0:2]), minute=int(start[2:4]))
    if len(end) > 3:
        converted_end = datetime.time(hours=int(end[0:2]), minute=int(end[2:4]))


def create_lecture(**kwargs):
    pass


def create_section(**kwargs):
    pass


def create_lab(**kwargs):
    pass

if __name__ == '__main__':
    scrape_csv()
