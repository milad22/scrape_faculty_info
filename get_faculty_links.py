from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
from lxml import html 
import re 

def MakeFacultyXpath(string,n,sep):
    strs = string.split(sep)
    joined_str = ''
    for i in range(1,len(strs)):
        joined_str = str(n) + strs[i]
    joined_str = strs[0] + joined_str

    return joined_str

def IsUrl(string):
    if ('http' in string) or ('https' in string):
        return True
    else:
        return False

def FindNodeWithMaxBranch(parent, nodes = []):
        children = parent.xpath('child::*')
        if len(children) > 0:
            nodes.append(len(children))
            for child in children:
                FindNodeWithMaxBranch(child)
        return max(nodes)

dep_url = 'http://web.mit.edu/physics/people/faculty/index.html'

driver = webdriver.Firefox()
#open the main web browser
driver.get(dep_url)
time.sleep(random.randint(10,15))
#fac_number = len(driver.find_elements_by_xpath(general_xpath)) # number of the faculties
page_source = driver.page_source
if page_source != None:
    print("Found the HTML source")
source_tree = html.fromstring(page_source)
if source_tree != None:
    print("Html source tree established")
body = source_tree.xpath('//body')[0]
#find the number of faculty and the html element which is parent of table of the faculty
# The idea is that the html element which has the maximum children in the html
# is in fact the parent element for the list or table of faculty
#first we find the node with maximum child in the html body and set it to faculty number
fac_number = FindNodeWithMaxBranch(body)
print("faculty number is {}".format(fac_number))
#now we select the node with the maximum children 
fac_str = str(fac_number)
parent = body.xpath('//*[count(*) = '+fac_str+']')[0]
if parent != []:
    print("Found the parent node")

#We assume the children of the selected parent node is the one with each faculty information
children = parent.xpath('child::*')
assert fac_number == len(children), '''Number of the faculty should be equal to the number of children 
                                       of the node with max children in the HTML source'''
dep_faculty_data = [] #This gona be list of list of faculty information and will be passed to a panda data frame at end
for child in children:
    all_urls = child.xpath('*//@href')
    print("{} number of urls were selected".format(len(all_urls)))
    #Remove the duplicated urls so the we don't visit a webpage multiple times
    #We also remove the urls which doesn't start with http or https (eg. emails)
    urls = []
    [urls.append(x) for x in all_urls if (x not in urls and IsUrl(x))] 
    print("Number of filtered urls is: {}",format(len(urls)))
    print("Grabbed urls are {}".format(urls))
    #visit each link in faculty information to collect the faculty research intrest
    #We assume these links leads us to the faculty personal webpage
    research_intrest = ''
    for url in urls:
        print("scraping following url for faculty interests: {}".format(url))
        driver1 = webdriver.Firefox()
        driver1.get(url)
        time.sleep(random.randint(7,15))
        paragraphs = driver1.find_elements_by_xpath('//p')
        for paragraph in paragraphs:
            research_intrest += ' ' + paragraph.text
        driver1.close()

    #Now we scrap the faculty information on the main page, We may have done it first :) 
    #Some the scraped content may not be text and just tab or new line. We filter it as proceed 
    all_text = (child.xpath('descendant::text()'))
    faculty_data = []
    for text in all_text:
        result = (re.search(r"[a-z]|[A-Z]|[0-9]", text))
        if result != None:
            faculty_data.append(text)
    
    #Glue the faculty research intrests to faculty data
    faculty_data.append(research_intrest)
    #append the faculty data to the list of faculty data 
    dep_faculty_data.append(faculty_data)
#pass the list faculty information to a panda dataframe
df = pd.DataFrame(dep_faculty_data)
#save the data to a csv file
df.to_csv("faculty_information.csv", index=False, header=False)
#close the main web browser
driver.close()


# dep_url = 'http://web.mit.edu/physics/people/faculty/index.html'

# url_template_xpath = '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/+div[?]/div/div[1]/a'
# general_xpath = url_template_xpath.replace('+',r'/')
# general_xpath = general_xpath.replace('[?]','')
# url_xpath = url_template_xpath.replace('+','')
# url_xpath = '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[?]//*/a/@href'
# contents_xpath = '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[?]//*/text()'
# driver = webdriver.Firefox()
# driver.get(dep_url)
# time.sleep(random.randint(10,15))
# fac_number = len(driver.find_elements_by_xpath(general_xpath)) # number of the faculties
# print(fac_number)
# page_source = driver.page_source
# source_tree = html.fromstring(page_source)
# dep_faculty_data = []
# print("Got Source")
# for i in range(1,fac_number):
#     #time.sleep(random.randint(10,15))
#     research_intrest = ''
#     faculty_info = ''
#     contents = source_tree.xpath(MakeFacultyXpath(contents_xpath,i,'?'))
#     all_urls = source_tree.xpath(MakeFacultyXpath(url_xpath,i,'?'))
#     print("All urls are:{}".format(all_urls))
#     #filter duplicate urls
#     urls = []
#     [urls.append(x) for x in all_urls if x not in urls] 
#     for url in urls:       
#         # try:
#         if is_url(url):
#             print("Filtered url is {}".format(url))
#             driver1 = webdriver.Firefox()
#             driver1.get(url)
#             time.sleep(random.randint(7,15))
#             paragraphs = driver1.find_elements_by_xpath('//p')
#             for paragraph in paragraphs:
#                 research_intrest += ' ' + paragraph.text
#             driver1.close()
            
                
#         # except:
#         #     pass
#     #save the gathered information
#     faculty_data = []
#     for content in contents:
#         result = (re.search(r"[a-z]|[A-Z]|[0-9]", content))
#         if result != None:
#             faculty_data.append(content)
#     #save the reseach intrest data 
#     faculty_data.append(research_intrest)
#     dep_faculty_data.append(faculty_data)

# df = pd.DataFrame(dep_faculty_data)
# df.to_csv("faculty_information.csv", index=False, header=False)
# driver.close()


# time.sleep(5)
# #general_xpath = '//div[@class="person-listing__person-row"]'
# general_xpath = '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div//div/div/div[1]/a'
# link_xpath =    '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[?]/div/div[1]/a'
# name_xpath =    '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[?]/div/div[2]/a/span/span'
# position_xpath = ''
# email_xpath =   '/html/body/div/div[5]/div[2]/table/tbody/tr/td[1]/div[6]/div[2]/div[2]/div[2]/div/div[?]/div/div[5]/a/span'

# url = 'http://web.mit.edu/physics/people/faculty/index.html'

# driver = webdriver.Firefox()
# driver.get(url)
# driver.implicitly_wait(10)
# fac_number = len(driver.find_elements_by_xpath(general_xpath)) # number of the faculties
# print(fac_number)

# #f = open("information.csv", mode='w')
# #write header
# #f.write('name,email,position,research interest\n')
# #scrap the faculties data 
# data = []
# for i in range(1,fac_number):

#     research_intrest = ''
#     joined_xpath_link = MakeFacultyXpath(link_xpath,i,'?')
#     joined_xpath_name = MakeFacultyXpath(name_xpath,i,'?')
#     joined_xpath_position = MakeFacultyXpath(position_xpath,i,'?')
#     joined_xpath_email = MakeFacultyXpath(email_xpath,i,'?')

#     try:
#         name = driver.find_element_by_xpath(joined_xpath_name).text
#         print(name)
#     except:
#         name = 'None'
#     #f.write(name+',')
#     try:
#         email = driver.find_element_by_xpath(joined_xpath_email).text
#         print(email)
#     except:
#         email = 'None'
#     #f.write(email+',')
#     try:
#         position = driver.find_element_by_xpath(joined_xpath_position).text
#     except:
#         position = 'None'
#     #f.write(position+',')
#     try:
#         link = driver.find_element_by_xpath(joined_xpath_link)
#         link.click()
#         try:
#             paragraphs = driver.find_elements_by_xpath('//p')
#             for paragraph in paragraphs:
#                 research_intrest = research_intrest + ' ' + paragraph.text
            
#         finally:
#             driver.back()
#             driver.implicitly_wait(random.randint(5,8))
#     except:
#         research_intrest = 'None'
#     data.append([name,position,email,research_intrest])
#     #f.write(research_intrest)
#     #f.write('\n')

    

# df = pd.DataFrame(data, columns=['Name', 'Position', 'Email', 'Research_interest'])
# #f.close()
# driver.close()

# df.to_csv("faculty_information.csv", index=False, header=True)



