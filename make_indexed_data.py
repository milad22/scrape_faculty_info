import pandas as pd 
import random
import string


#Make indexed data base 

def create_random_id():
    """
    Creates a random string with length 8
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

#import spreadsheet with google scholar id's
data_df = pd.read_csv('faculty_info_for_google_scholar_with_scholar_id.csv')
#print data_df columns
print(data_df.columns)
#Make indexed spreadsheet
indexed_data = []
for index, row in data_df.iterrows():
    dict = {
        "id" : create_random_id(),
        "Affiliation" : row['Affiliation'],
        "Name" : row['Name'],
        "google_scholar_id" : row['google_scholar_id']
    }
    indexed_data.append(dict)

indexed_data_df = pd.DataFrame(indexed_data)
indexed_data_df.to_csv('indexed_data.csv', index = False)