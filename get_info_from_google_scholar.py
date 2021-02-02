from scholarly import scholarly
import pandas as pd

# faculty_data_df = pd.read_csv('faculty_info_for_google_scholar.csv',skip_blank_lines=True,
#                  keep_default_na=False, usecols = [0,1,2,3])
faculty_data_df = pd.read_csv('missing_fac_info_from_google_scholar.csv',skip_blank_lines=True,
                 keep_default_na=False, usecols = [0,1,2,3])

for index, row in faculty_data_df.iterrows():
    if index < 11:
         continue

    print(index)
    name = row['Name']
    affiliation = row['Affiliation']
    search_query = scholarly.search_author(name)
    try:
        author = scholarly.fill(next(search_query))
        scholar_id = author['scholar_id']
        faculty_data_df['google_scholar_id'].iloc[index] = scholar_id
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
            author_df.to_json(file_path+file_name, orient = 'split', indent = 4)

        author_pubs = []
        try:
            for i in range(10):
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
        except:
            pass
        pubs_df = pd.DataFrame(author_pubs)
        file_name = scholar_id + '_pubs' + '.json'
        with open(file_path+file_name, mode='w') as f:
            pubs_df.to_json(file_path+file_name, orient = 'split', indent = 4)
    except:
        faculty_data_df['google_scholar_id'].iloc[index] = 'None'
    #faculty_data_df.to_csv('faculty_info_for_google_scholar_with_scholar_id.csv', index = False)

