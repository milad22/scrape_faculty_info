from selenium import webdriver
import time
import random
import pandas as pd
from lxml import html 
import re 
import os
import csv
from scholarly import scholarly

# class UniScrappedDataStat:
#     def __init__(self, name = None, url_count = None, 
#                 faculty_count = None, image_count = None, fail_reason=None):
#                 if name is None:
#                     name = ''
#                 self.name = name
#                 if url_count is None:
#                     url_count = 0
#                 self.url_count= url_count
#                 if faculty_count is None:
#                     faculty_count = 0
#                 self.faculty_count = faculty_count
#                 if image_count is None:
#                     image_count = 0
#                 self.image_count = image_count
#                 if fail_reason is None:
#                     fail_reason = 'None'
#                 self.fail_reason = fail_reason
    
#     def csv_heading_list(self):
#         return ['University name','faculty count','personal images count','scrapped urls count','fail reason']

#     def stat(self):
#         return [self.name, self.faculty_count ,self.image_count, self.url_count, self.fail_reason]


# # import csv
# # with open('demo007.csv') as input, open('demo008.csv', 'w', newline='') as output:
# #     writer = csv.writer(output)
# #     for row in csv.reader(input):
# #         if any(field.strip() for field in row):
# #             writer.writerow(row)

# fac_info_df = pd.read_csv('demo008.csv',skip_blank_lines=True,
#                  keep_default_na=False, usecols = [0,1,2,3,4,5,6,7,8,9])
# #drop duplicate rows
# fac_info_df_dup = fac_info_df.drop_duplicates(subset=['Affiliation', 'Name'])
# fac_info_df_dup.to_csv('faculty_info_for_google_scholar.csv')



import json
import numpy as np 
search_query = scholarly.search_author('Matthew D Duez')
author = scholarly.fill(next(search_query))
scholar_id = author['scholar_id']
ind = np.arange(12)
author_dict = {    
    "scholar_id": author['scholar_id'],
    "name": author['name'],
    "affiliation": author['affiliation'],
    "email_domain": author['email_domain'],
    "url_picture": author['url_picture'],
    "citedby": author['citedby'],
    "interests": author['interests'],
    "citedby5y": author['citedby5y'],
    "hindex": author['hindex'],
    "hindex5y": author['hindex5y'],
    "i10index": author['i10index'],
    "i10index5y": author['i10index5y'],
    "coauthors": author['coauthors']
    }
author_df = pd.DataFrame([author_dict])
file_name = scholar_id + '.json'
file_path = './google_scholar_data/'
with open(file_path+file_name, mode='w') as f:
    author_df.to_json(file_path+file_name, orient = 'split')

author_pubs = []
for i in range(5):
    pub = scholarly.fill(author['publications'][i])
    pub_dict = {
    "abstract": pub['bib']['abstract'],
    "title": pub['bib']['title'],
    "author": pub['bib']['author'],
    "pub_year": pub['bib']['pub_year'],
    "author_pub_id": pub['author_pub_id'],
    "num_citations": pub['num_citations'],
    "pub_url": pub['pub_url'],
    "cites_id": pub['cites_id'],
    "citedby_url": pub['citedby_url'],
    "cites_per_year": pub['cites_per_year']
    }
    author_pubs.append(pub_dict)

pubs_df = pd.DataFrame(author_pubs)
file_name = scholar_id + '_pubs' + '.json'
with open(file_path+file_name, mode='w') as f:
    pubs_df.to_json(file_path+file_name, orient = 'split')

# df = pd.read_json('oEAz5kUAAAAJ_pubs.json', orient='split')
# print(df.columns)
# for index, row in df.iterrows():
#     print(row['abstract'])