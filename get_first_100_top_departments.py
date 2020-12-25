from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd

def MakeFacultyXpath(string,n,sep):
    strs = string.split(sep)
    joined_str = ''
    for i in range(1,len(strs)):
        joined_str = str(n) + strs[i]
    joined_str = strs[0] + joined_str

    return joined_str

urls = ['https://www.niche.com/graduate-schools/search/best-physics-graduate-programs/']
#make pages urls
for i in range(2,11):
    urls.append(urls[0]+'?page='+str(i))

general_xpath = '/html/body/div[1]/div/section/main/div/div/section/div[2]/ol//li/section/div/a/div[2]/ul[1]/li[1]'
name_xpath = '/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li[?]/section/div/a/div[2]/ul[1]/li[1]'


f = open('Deparments_list.txt', mode='w')
driver = webdriver.Firefox()
for url in urls:
    driver.get(url)
    time.sleep(random.randint(5,15))
    uni_number = len(driver.find_elements_by_xpath(general_xpath)) # number of the faculties
    print(uni_number)
    for i in range(1,uni_number+1):
        filled_name_xpath = MakeFacultyXpath(name_xpath,i,'?')
        try:
            time.sleep(random.randint(3,9))
            uni_name = driver.find_element_by_xpath(filled_name_xpath).text
        except:
            uni_name = 'None'
            uni_number +=1
        print("faculty number is: {}".format(uni_number))
        print("university name is: {}".format(uni_name))
        f.write(uni_name)
        f.write('\n')
driver.close()  
f.close()  










#/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li[10]
#/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li[9]/section/div/a/div[2]/h2
#/html/body/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr[9]/td[1]/p[1]/strong
#/html/body/div[2]/div/div[2]/div[2]/div[2]/table/tbody
#/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li[2]/section/div/a/div[2]/h2
#/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li[1]/section/div/a/div[2]/ul[1]/li[1]/text()
#/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li[3]/section/div/a/div[2]/ul[1]/li[1]/text()


