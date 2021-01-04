from selenium import webdriver
import time
import random
import pandas as pd
from lxml import html 
import re 

def make_xpath(string,n,sep):
    strs = string.split(sep)
    joined_str = ''
    for i in range(1,len(strs)):
        joined_str = str(n) + strs[i]
    joined_str = strs[0] + joined_str

    return joined_str

def format_name(name):
    name = name.replace('-',' ')
    name = name.replace('–',' ')
    name = name.replace(',',' ')
    name = '_'.join(name.split())
    #name = re.sub(r"\s+", '_', name)
    return name

#Here the physics prgrams information is scrapped from us news website
url = 'https://www.usnews.com/best-graduate-schools/top-science-schools/physics-rankings'
unis_data = []
driver = webdriver.Firefox()
driver.get(url)
time.sleep(80)
#Since the page loads as we scroll down. We need to scroll the webpage by hand in this interval
page_source = None
try:
    page_source = driver.page_source
except:
    print("Couldn't save page source")
    driver.close()
source_tree = html.fromstring(page_source)

name_general_xpath = '//*[@id="app"]/div/div[1]/div[4]/div/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/table/tbody/tr[?]/td[1]/span/div/h3/a/text()'
location_general_xpath='//*[@id="app"]/div/div[1]/div[4]/div/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/table/tbody/tr[?]/td[1]/span/div/p[1]/text()'
rank_general_xpath='//*[@id="app"]/div/div[1]/div[4]/div/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/table/tbody/tr[?]/td[1]/span/div/p[2]/a/strong[1]/text()[2]'


for i in range(2,220):
    uni_data = []
    name = ''
    location = ''
    rank = 0
    name_xpath = make_xpath(name_general_xpath, i,'?')
    rank_xpath = make_xpath(rank_general_xpath, i,'?')
    location_xpath = make_xpath(location_general_xpath, i,'?')
    
    try:
        name = source_tree.xpath(name_xpath)[0]
        print(name)
    except:
        name = 'None'
        print("Didn't find name")
 
    try:
        rank = source_tree.xpath(rank_xpath)[0]
        print(rank)
    except:
        rank = 'None'
        print("Didn't find rank")
    try:
        loc = source_tree.xpath(location_xpath)
        location = ''.join(loc)
        print(location)
    except:
        location = None
        print("Didn't find location")

    uni_data.append(format_name(name))
    uni_data.append(rank)
    uni_data.append(location)

    unis_data.append(uni_data)
df = pd.DataFrame(unis_data)
df.to_csv("US_new_top_schools.csv", index=False, header=['name','rank','location'])
driver.close()
