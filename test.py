from selenium import webdriver
import time
import random
import pandas as pd
from lxml import html 
import re 
import os
import csv 

class UniScrappedDataStat:
    def __init__(self, name = None, url_count = None, 
                faculty_count = None, image_count = None, fail_reason=None):
                if name is None:
                    name = ''
                self.name = name
                if url_count is None:
                    url_count = 0
                self.url_count= url_count
                if faculty_count is None:
                    faculty_count = 0
                self.faculty_count = faculty_count
                if image_count is None:
                    image_count = 0
                self.image_count = image_count
                if fail_reason is None:
                    fail_reason = 'None'
                self.fail_reason = fail_reason
    
    def csv_heading_list(self):
        return ['University name','faculty count','personal images count','scrapped urls count','fail reason']

    def stat(self):
        return [self.name, self.faculty_count ,self.image_count, self.url_count, self.fail_reason]