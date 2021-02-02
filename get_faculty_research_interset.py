import pandas as pd 
from selenium import webdriver
import time
import random
import json

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def is_url(string):
    if ('http' in string) or ('https' in string):
        return True
    else:
        return False

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    #return u" ".join(t.strip() for t in visible_texts)
    return visible_texts

def find_matching_text(text_list1, text_list2):
    matching_text = []
    for text in text_list1:
        if text in text_list2:
            matching_text.append(text)
    return matching_text

def grab_content(df, number_of_records):
    visited_urls = []
    data = []
    for index, row in df.iterrows():
        if index > number_of_records:
            break
        # if index < 600:
        #     continue
        affiliation = ''
        name = ''
        content = []
        if (index % 100) == 0:
            visited_urls = []
        urls = []
        if row[0] != '' and row[1] != '':
            affiliation = row[0]
            name = row[1]
            for i in range(2,10):
                if is_url(row[i]):
                    urls.append(row[i])
            if urls != []:
                for url in urls:
                    if url not in visited_urls:
                        try: 
                            time.sleep(random.randint(4,7))
                            html = urllib.request.urlopen(url).read()
                            visible_content_list = text_from_html(html)
                            for text in visible_content_list:
                                content.append(text)
                            print("Scrapped data for the url: {}\n".format(url)) 
                        except:
                            print("Couldn't open url for {} with affiliation {}\n".format(name, affiliation))
            data.append([name, affiliation, content])
    data_df = pd.DataFrame(data, columns= ['name','affiliation','content'])
    return data_df

def find_shared_text(df, affiliations):
    matching_text_list_of_list = []
    for affiliation in affiliations:
        row_count = len((df.loc[df['affiliation'] == affiliation]).index)
        matching_text_list = []
        if row_count < 2:
            print("Couldn't find shared text for {}".format(affiliation))
        else:
            n = min(6,row_count)
            uni_data_df = (df.loc[df['affiliation'] == affiliation]).head(n)
            matching_text_list_with_dup_list = []
            for i in range(0,n-1):
                text_list1 = uni_data_df['content'].iloc[i]
                text_list2 = uni_data_df['content'].iloc[i+1]
                matching_text_list_with_dup_list.append(find_matching_text(text_list1, text_list2))
            #flaten the 2D-array
            matching_text_list_with_dup = [x for item in matching_text_list_with_dup_list for x in item]
            #remove the duplicate element of the list
            [matching_text_list.append(x) for x in matching_text_list_with_dup if (x not in matching_text_list)]
            matching_text_list_of_list.append([affiliation, matching_text_list])
    shared_texts_df = pd.DataFrame(matching_text_list_of_list, columns=['affiliation', 'shared_text'])
    return shared_texts_df

def remove_shared_content(df):
    for index, row in df.iterrows():
        affiliation = row['affiliation']
        content = row['content']
        try:
            shared_text_list = (shared_texts_df[shared_texts_df['affiliation']  == affiliation]).iloc[0,1]
            cleaned_content = []
            [cleaned_content.append(x) for x in content if x not in shared_text_list]
            research_interest = u" ".join(t.strip() for t in cleaned_content)
        except:
            print("gave up cleaning for the {}".format(affiliation))
            research_interest = u" ".join(t.strip() for t in content)
        row['content'] = research_interest
    return df

file_path = 'faculty_info_cleaned_by_hand.csv'
fac_info_df = pd.read_csv(file_path,skip_blank_lines=True,
                 keep_default_na=False, usecols = [0,1,2,3,4,5,6,7,8,9])
#drop duplicate rows
fac_info_df_no_dup = fac_info_df.drop_duplicates()
#indicate how many records want to analyse 
number_of_records = 8200
data_df = grab_content(fac_info_df_no_dup,number_of_records)
#save the data here so if anything wrong happend in future we don't start from scrach
json_string = data_df.to_json(orient="split")
parsed = json.loads(json_string)
f = open("faculty_research_interest_without_proccessing.json", mode='w')
f.write(json.dumps(parsed, indent = 4))
f.close()
#get the list of universities 
affiliations = data_df.affiliation.unique()
#find shared text for each university
shared_texts_df = find_shared_text(data_df, affiliations) 
#remove the matching text from the content of 
# the data frame and make the research interest text for each faculty member
cleaned_data_df = remove_shared_content(data_df)

json_string = cleaned_data_df.to_json(orient="split")
parsed = json.loads(json_string)
f = open("faculty_research_interest.json", mode='w')
f.write(json.dumps(parsed, indent = 4))
f.close()


# data_df = pd.read_json('faculty_research_interest_without_proccessing.json', orient='split')
# #get the list of universities 
# affiliations = data_df.affiliation.unique()
# #find shared text for each university
# shared_texts_df = find_shared_text(data_df, affiliations) 
# #remove the matching text from the content of 
# # the data frame and make the research interest text for each faculty member
# cleaned_data_df = remove_shared_content(data_df)

# json_string = cleaned_data_df.to_json(orient="split")
# parsed = json.loads(json_string)
# f = open("faculty_research_interest.json", mode='w')
# f.write(json.dumps(parsed, indent = 4))
# f.close()