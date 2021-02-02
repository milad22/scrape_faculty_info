import pandas as pd 

#merge the faculty information from different sources

data_df = pd.read_csv('indexed_data.csv')
#print data frame head()
print(data_df.head())
print(data_df.columns)
webpage_content_df = pd.read_json('faculty_research_interest.json', orient='split')
#remove duplicates
webpage_content_df.drop_duplicates()
#print columns
print(webpage_content_df.columns)

for index, row in data_df.iterrows():
    # if index > 4: break
    id = row['id']
    Name = row['Name']
    Affiliation = row['Affiliation']
    scholar_id = row['google_scholar_id']
    titles = []
    webpage_content = ''
    abstracts = []
    interests = []
    if scholar_id != 'None':
        fac_pubs_info_df = None
        #load abstracts and titles
        file_name = row['google_scholar_id'] + '_pubs.json'
        file_path = './google_scholar_data/' + file_name
        try:
            fac_pubs_info_df = pd.read_json(file_path, orient='split')
        except:
            print("Couldn't read the file for {} with scholar id {}".format(row['Name'], row['google_scholar_id']))
        try:    
            titles = fac_pubs_info_df['title']
            abstracts = fac_pubs_info_df['abstract']
        except:
            print("Couln't load titles and abstracts for *{}* from *{}*".format(Name, Affiliation))
        #load faculty interests
        file_name = row['google_scholar_id'] + '.json'
        file_path = './google_scholar_data/' + file_name
        try:
            fac_pubs_info_df = pd.read_json(file_path, orient='split')
            interests = fac_pubs_info_df['interests']
        except:
            print("Couldn't load interests for *{}* from *{}*".format(Name,Affiliation))

    try:
        webpage_content = webpage_content_df.loc[webpage_content_df['name'] == Name]['content']
    except:
        print("Coulnd't pull the content for {}".format(Name, Affiliation))
    
    dict = {
        "id" : id,
        "google_scholar_id" : scholar_id,
        "titles" : titles,
        "abstracts" : abstracts,
        "interests" : interests
    }
    #save the json file
    file_name = id
    file_path = './faculty_merged_info/' + file_name + '.json'
    df = pd.DataFrame([dict])
    df.to_json(file_path, orient= 'split', indent=4)
