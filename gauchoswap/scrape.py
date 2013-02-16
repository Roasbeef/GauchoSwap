from gauchoswap import db
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyquery import PyQuery as pq

from gauchoswap.models import Lecture, Section, Lab

import os


class GoldBot(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
        self.lecture_selector = ""
        self.section_selection = ""

    def authenticate(self):
        self.bot.get('https://my.sa.ucsb.edu/gold/login.aspx')

        user_field = self.bot.find_element_by_css_selector('#ctl00_pageContent_userNameText')
        user_field.send_keys(self.username)

        password_field = self.bot.find_element_by_css_selector('#ctl00_pageContent_passwordText')
        password_field.send_keys(self.password)

        box = self.bot.find_element_by_css_selector('#ctl00_pageContent_CredentialCheckBox')
        box.click()

        submit_button = self.bot.find_element_by_css_selector('#ctl00_pageContent_loginButton')
        submit_button.click()

    def navigate_to_courses(self):
        course_button = self.bot.find_element_by_css_selector('#ctl00_ctl05')
        course_button.click()

    def get_course_drop_down(self):
        course_drop_down = Select(self.bot.find_element_by_css_selector('#ctl00_pageContent_subjectAreaDropDown'))
        return course_drop_down

    def create_course_dict(self):
        """ returns a mapping of course abrev to actual name """
        drop_down = self.get_course_drop_down()
        course_dict = {course.get_attribute("value"): course.text.split('-')[0].strip()
                       for course in drop_down.options if course.get_attribute("value")}
        return course_dict

    def scrape(self):
        self.authenticate()
        self.navigate_to_courses()

        course_dict = self.create_course_dict()
        for department, course_html in self.iter_departments(course_dict):
            for lecture_dict_list, section_dict_list in self.iter_classes(department, course_html):
                l = Lecture(**lecture_dict)
                for section_dict in section_dict_list:
                    s = Section(lecture=l, **section_dict)

    def iter_departments(self, course_dict):
        for abbrev, department in course_dict.items():
            drop_down = self.get_course_drop_down()
            drop_down.select_by_value(abbrev)

            self.bot.find_element_by_css_selector('#ctl00_pageContent_searchButton').click()
            yield department, self.bot.page_source

            self.navigate_to_courses()

    def iter_classes(self, department, course_html):
        #parse html
        d = pq(course_html)
        main_course_table = d.find('#ctl00_pageContent_CourseList')

        for class_table in main_course_table.children().children():
            class_table = pq(class_table)
            course_name = self._get_class_name(class_table)
            #classes_container = class_table.children().children().children().children().children()
            classes_conteiner = class_table.find('#ctl00_pageContent_CourseList_ctl00_PrimarySections').children().children()
            for c in classes_container:
                class_dict = self._get_lecture_dict(c)
                class_dict.update(name=course_name)




        #flag true somewhere if lab
        #get lecture and section dict
        #yield both
        pass

    @staticmethod
    def _get_lecture_dict(class_container):
        lecture_info = class_container.children().eq(0).children()
        lecture_info = lecture_info[1:-2]
        return {'days': lecture_info[0],
                'time': lecture_info[1],
                'professor': lecture_info[2],
                'location': lecture_info[3],
                'max_spots': lecture_info[4],
                'space': lecture_info[5]
                }

    @staticmethod
    def _get_class_name(class_table):
        #x = class_table.find('#ctl00_pageContent_CourseList_ctl00_PermNbr')
        x = class_table.children().children().children().children().eq(0).children().children().children().children().eq(0).children()
        course_name = x.children().children().children().children().children().eq(0).children().text()
        course_name = ' '.join(course_name.split())
        return course_name

if __name__ == '__main__':
    username = os.environ['GOLD_USER']
    password = os.environ['GOLD_PASS']
    g = GoldBot(username, password)
    #g.scrape()
