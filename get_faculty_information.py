from selenium import webdriver
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

unis_dataframe = pd.read_excel('Physics_departments.xlsx', na_values = 'None')
general_log_file = open('log_file_txt', mode='w')
dep_faculty_data = [] #This gonna be list of list of faculty information and will be passed to a panda data frame at end
for index, row in unis_dataframe.iterrows():
    uni = row['University']
    logfile_name = uni + 'log.txt'
    logfile = open(logfile_name, mode='w')
    logfile.write("University is; {}\n".format(uni))
    general_log_file.write("University is; {}\n".format(uni))
    url_prefix = ''
    dep_url = row['url'] 
    print(uni)
    if uni == 'empty':
        logfile.close()
        continue

    driver = webdriver.Firefox()
    #open the main web browser
    driver.get(dep_url)
    time.sleep(random.randint(10,15))
    #fac_number = len(driver.find_elements_by_xpath(general_xpath)) # number of the faculties
    try:
        page_source = driver.page_source
        logfile.write("Found the HTML source\n")
        general_log_file.write("Found the HTML source for uni {}\n".format(uni))
    except:
        general_log_file.write("Couldn't find HTML source for {}\n".format(uni))
        logfile.close()
        driver.close()
        continue
    source_tree = html.fromstring(page_source)
    if source_tree != None:
        logfile.write("Html source tree established\n")
        general_log_file.write("Html source tree established for {}\n".format(uni))
    body = source_tree.xpath('//body')[0]
    #find the number of faculty and the html element which is parent of table of the faculty
    # The idea is that the html element which has the maximum children in the html
    # is in fact the parent element for the list or table of faculty
    #first we find the node with maximum child in the html body and set it to faculty number
    fac_number = FindNodeWithMaxBranch(body)
    logfile.write("faculty number is {}\n".format(fac_number))
    general_log_file.write("faculty number for {} is {}\n".format(uni,fac_number))
    #now we select the node with the maximum children 
    fac_str = str(fac_number)
    try:
        parent = body.xpath('//*[count(*) = '+fac_str+']')[0]
    except:
        general_log_file.write('Couldnt parse the page for {}'.format(uni))
        logfile.close()
        driver.close()
        continue

    if parent != []:
        logfile.write("Found the parent node\n")
        general_log_file.write("Found the parent node for {}\n".format(uni))

    #We assume the children of the selected parent node is the one with each faculty information
    children = parent.xpath('child::*')
    assert fac_number == len(children), '''Number of the faculty should be equal to the number of children 
                                        of the node with max children in the HTML source'''
    
    for child in children:
        all_urls = child.xpath('*//@href')
        logfile.write("{} number of urls were selected\n".format(len(all_urls)))
        #Some website urls missing one part of urls. It usually comes fro aurl wrapper
        #We need to add it here 
        for url in all_urls:
            url = url_prefix + url 
        #Remove the duplicated urls so the we don't visit a webpage multiple times
        #We also remove the urls which doesn't start with http or https (eg. emails)
        urls = []
        [urls.append(x) for x in all_urls if (x not in urls and IsUrl(x))] 
        logfile.write("Number of filtered urls is: {}\n".format(len(urls)))
        logfile.write("Grabbed urls are {}\n".format(urls))
        
        general_log_file.write("Number of links feched for faculty is {}\n".format(len(urls)))
        #visit each link in faculty information to collect the faculty research intrest
        #We assume these links leads us to the faculty personal webpage
        research_intrest = ''
        for url in urls:
            logfile.write("scraping following url for faculty interests: {}\n".format(url))
            driver1 = webdriver.Firefox()
            try:
                driver1.get(url)
                time.sleep(random.randint(7,15))
                #We assume the research interst content is in paragraph content
                try:
                    paragraphs = driver1.find_elements_by_xpath('//p')
                    for paragraph in paragraphs:
                        research_intrest += ' ' + paragraph.text
                except:
                    pass
            except:
                pass
            driver1.close()
        #Now we scrap the faculty information on the main page, We may have done it first :) 
        #Some the scraped content may not be text and just tab or new line. We filter it as proceed
        faculty_data = []
        faculty_data.append(uni)
        try:
            all_text = (child.xpath('descendant::text()'))
            for text in all_text:
                result = (re.search(r"[a-z]|[A-Z]|[0-9]", text))
                if result != None:
                    faculty_data.append(text)
        except:
            all_text = ''
        
        #Glue the faculty research intrests to faculty data
        faculty_data.append(research_intrest)
        #append the faculty data to the list of faculty data 
        dep_faculty_data.append(faculty_data)
        #pass the list faculty information to a panda dataframe
        #close the main web browser
    driver.close()
    logfile.close()
    
    df = pd.DataFrame(dep_faculty_data)
    #save the data to a csv file
    df.to_csv("faculty_info.csv", index=False, header=False) 
general_log_file.close()
