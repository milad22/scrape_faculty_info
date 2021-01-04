from selenium import webdriver
import time
import random
import pandas as pd
from lxml import html 
import re 
import os
import csv 

def is_url(string):
    if ('http' in string) or ('https' in string):
        return True
    else:
        return False

def find_node_with_max_branch(parent):
    children = parent.xpath('child::*')
    if len(children) > 0:
        nodes.append(len(children))
        for child in children:
            find_node_with_max_branch(child)
    return max(nodes)

def fetch_faculty_page_content(url):
    content =''
    driver = webdriver.Firefox()
    try:
        driver.get(url)
        time.sleep(random.randint(4,7))
        #We assume the research interst content is in paragraph content
        try:
            paragraphs = driver.find_elements_by_xpath('//p')
            for paragraph in paragraphs:
                content += ' ' + paragraph.text
        except:
            pass
    except:
        pass
    driver.close()
    return content

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



#Make a list of universities to iterate over in the next 
unis_dataframe = pd.read_excel('Physics_departments_formatted_with_photo_counts.xlsx', na_values = 'None')
webpages_path = '/home/miliverse/pages/'
#Make the statistics file for scrapped univesities 
stat = UniScrappedDataStat()
stat_file = open('stat.csv', 'w')
stat_writer = csv.writer(stat_file)
stat_writer.writerow(stat.csv_heading_list())


dep_faculty_data = [] #This gonna be list of list of faculty information and will be passed to a panda data frame at end 
for index, row in unis_dataframe.iterrows():
    stat = UniScrappedDataStat()
    uni = row['University']
    stat.name = uni
    personal_image_number = row['directory_page_personal_photo_count']
    stat.image_count = personal_image_number
    read_from_images = (False or (personal_image_number > 0)) # This line is brilliant good job Mili
    logfile_name = uni + '_log.txt'
    logfile = open(logfile_name, mode='w')
    logfile.write("University is; {}\n".format(uni)) 
    print(uni)
    html_path = webpages_path + uni + '.html'
    page_source = '' 
    try:
        f = open(html_path, mode='r')
        for line in f.readlines():
            page_source += line
        print("Established the HTML source\n")
        logfile.write("Established the HTML source\n")
        f.close()
    #In case it couldn't read html, try to to open a web browser to read the html source 
    except:
        try:
            print("Couldn't read HTML source for {}\n".format(uni))
            print("Tries openning a webdriver to get the html source\n")
            directory_url = row['url']
            driver = webdriver.Firefox()
            #open the main web browser
            driver.get(directory_url)
            time.sleep(random.randint(10,15))
            page_source = driver.page_source
            driver.close()
        except:
            stat.fail_reason = "Couldn't read HTML source even with the web driver"
            stat_writer.writerow(stat.stat())
            logfile.close()
            continue
    source_tree = None
    source_tree = html.fromstring(page_source)
    if source_tree != None:
        print("Html tree established\n")
        logfile.write("Html tree established\n")
    body = []
    try:
        body = source_tree.xpath('//body')[0]
    except:
        stat.fail_reason = "Couldn't find HTML body"
        stat_writer.writerow(stat.stat())
        logfile.close()
        continue
    
    if read_from_images:
        print("Determines faculty info from images\n")
        children = body.xpath('*//img')
        stat.faculty_count = personal_image_number
    else:
        #find the number of faculty and the html element which is parent of table of the faculty
        # The idea is that the html element which has the maximum children in the html
        # is in fact the parent element for the list or table of faculty
        #first we find the node with maximum child in the html body and set it to faculty number
        nodes = []
        fac_number = find_node_with_max_branch(body)
        stat.faculty_count = fac_number
        print("Determines faculty info from maximum node with branch\n")
        print("faculty number is {}\n".format(fac_number))
        logfile.write("faculty number is {}\n".format(fac_number))
        #now we select the node with the maximum children 
        fac_str = str(fac_number)
        parent = []
        try:
            parent = body.xpath('//*[count(*) = '+fac_str+']')[0]
            print("Found the parent node\n")
            logfile.write("Found the parent node\n")
        except:
            print('Couldnt find the parent for {}\n'.format(uni))
            stat.fail_reason = "Couldnt find the parent"
            stat_writer.writerow(stat.stat())
            logfile.close()
            continue

        #We assume the children of the selected parent node is the one with each faculty information
        children = parent.xpath('child::*')
        assert fac_number == len(children), '''Number of the faculty should be equal to the number of children 
                                            of the node with max children in the HTML source'''
    
    for child in children:
        if read_from_images:
            parents = child.xpath('parent::node()')
            while len(parents) != 0:
                parent = parents[0]
                if len(parent.xpath('*//img')) > 3:
                    break
                else:
                    child = child.xpath('parent::node()')[0]
                parents = child.xpath('parent::node()')

            if len(parents) == 0:
                continue
            if len(parents[0].xpath('*//img')) > personal_image_number*11/10:
                continue

        #Some the scraped content may not be text and just tab or new line. We filter it as proceed
        faculty_data = []
        faculty_data.append(uni)
        all_text = ''
        try:
            all_text = (child.xpath('descendant::text()'))
            for text in all_text:
                #safeguard for not writing crazy long strings in a office cell
                #The maximum charachter length for libre office is 65535
                #ref:https://ask.libreoffice.org/en/question/22405/what-is-the-maximum-number-of-characters-in-a-calc-cell/#:~:text=For%20many%20versions%20the%20maximum,relevant%20limit%20to%20that%20number.
                if len(text) > 60000:
                    continue
                result = (re.search(r"[a-z]|[A-Z]|[0-9]", text))
                if result != None:
                    text = " ".join(text.split())
                    #change unicode to utf-8 if it's not 
                    text.encode()
                    faculty_data.append(text)
                #somtimes the number of text becomes overwhehlming
                #Usually it happens when the wrong data is grabbed. So we ignore them
                if len(faculty_data) > 10:
                    break
        except:
            all_text = ''
        all_urls = child.xpath('*//@href')
        logfile.write("{} number of urls were selected\n".format(len(all_urls)))
        #Remove the duplicated urls so the we don't visit a webpage multiple times
        #We also remove the urls which doesn't start with http or https (eg. emails)
        urls = []
        [urls.append(x) for x in all_urls if (x not in urls and is_url(x))] 
        #print("Number of filtered urls is: {}\n".format(len(urls)))
        logfile.write("Number of filtered urls is: {}\n".format(len(urls)))
        logfile.write("Grabbed urls are {}\n".format(urls))
        #visit each link in faculty information to collect the faculty research intrest
        #We assume these links leads us to the faculty personal webpage
        research_intrest = ''
        stat.url_count += len(urls)
        for url in urls:
            logfile.write("scraping following url for faculty interests: {}\n".format(url))
            #print("scraping following url for faculty interests: {}\n".format(url))
            #research_intrest += fetch_faculty_page_content(url)
            #time.sleep(random.randint(7,15))

        #Glue the faculty research intrests to faculty data
        faculty_data.append(research_intrest)
        #append the faculty data to the list of faculty data 
        dep_faculty_data.append(faculty_data)
        #pass the list faculty information to a panda dataframe
    logfile.close()
    df = pd.DataFrame(dep_faculty_data)
    #save the data to a csv file
    df.to_csv("faculty_info.csv", index=False, header=False)
    stat_writer.writerow(stat.stat())
stat_file.close()
os.system('rm -rf log_files stat scrapped_faculty_info')
os.system('mkdir log_files')
os.system('mv *_log.txt log_files')
os.system('mkdir stat')
os.system('mv stat.csv stat')
os.system('mkdir scrapped_faculty_info')
os.system('mv faculty_info.csv scrapped_faculty_info')