

from selenium import webdriver
import time
import random
import pandas as pd
from lxml import html 
import re
# parent = '//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div'
# all_links_in_parent = '//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div//@href'
# all_children_of_parent = '//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div/*'
# #itrate over childeren 


# url = 'http://web.mit.edu/physics/people/faculty/index.html'

# doc = open('MIT_Department_of_Physics.html', mode='r')
# page = doc.read()

# tree = html.fromstring(page)
# parent = tree.xpath('//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div')[0]

# children = parent.xpath('./*')
# for child in children:
#     print(child.xpath('*//text()'))
#     #print(child.xpath('*//@href'))

# # tree = html.fromstring(page)

# # children = tree.xpath('//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div/*')
# # for child in children:
# #     #print(child.xpath('*//text()'))
# #     print(child.xpath('*//@href'))

# doc.close()

#uni_file = open('Physics_departments.xlsx', mode = 'r')
unis_dataframe = pd.read_excel('Physics_departments.xlsx', na_values = 'None')
for index, row in unis_dataframe.iterrows():
    print(row['url'])






