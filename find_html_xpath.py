from typing import Text
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
from lxml import html 
import re


url = 'http://web.mit.edu/physics/people/faculty/index.html'

driver = webdriver.Firefox()
driver.get(url)
#html = driver.find_element_by_xpath('/*').text
# print(driver.page_source.encode("utf-8"))
f = open('page_source.txt', mode='w')
page = driver.page_source
f.write(page)
tree = html.fromstring(page)
faculty = tree.xpath('/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[1]//*/a/@href')
contents = tree.xpath('/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[1]//*/text()')
filtered_contents = []

for content in contents:
    result = (re.search(r"[a-z]|[A-Z]|[0-9]", content))
    if result != None:
        filtered_contents.append(content)
    # if content is not '':
    #     filtered_contents = filtered_contents.append(content)
print(filtered_contents)
f.close()
driver.close()

                     #/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[3]