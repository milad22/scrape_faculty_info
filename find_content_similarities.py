import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction

sep_char = ','
def return_noun_phrases(content):
    """
        returns a list of noun phrases of the content
    """
    return TextBlob(content).noun_phrases

def tokenizer(doc):
    """
    dummy function defined to feed the TfidfVectorizer
    """
    phrase_list  = doc.split(sep_char)
    return phrase_list

def noun_phrases_str(docs):
    """
    returns the a list of noun phrases in from a list of documents
    """
    noun_phrases = []
    for doc in docs:
        noun_phrase_list = return_noun_phrases(doc)
        noun_phrases += noun_phrase_list
    noun_phrases_str = sep_char.join(noun_phrases)
    return noun_phrases_str


# First find the title similarity 
data_df = pd.read_csv('faculty_info_for_google_scholar_with_scholar_id.csv', keep_default_na=False, usecols = [0,1,2,3])
noun_phrases_dict_list = []
missing_fac_info_dict_list = []
for index, row in data_df.iterrows():
    if row['google_scholar_id'] == 'None' or row['google_scholar_id'] == '': 
        continue
    file_name = row['google_scholar_id'] + '_pubs.json'
    file_path = './google_scholar_data/' 
    fac_pubs_info_df = None
    try:
        fac_pubs_info_df = pd.read_json(file_path+file_name, orient='split')
    except:
        print("Couldn't read the file for {} with scholar id {}".format(row['Name'], row['google_scholar_id']))
    try:
        titles = fac_pubs_info_df['title']
        titles_noun_phrases_str = noun_phrases_str(titles)
        abstracts = fac_pubs_info_df['abstract']
        abstracts_noun_phrases_str = noun_phrases_str(abstracts)
        noun_phrases_dict = {
        "Name": row['Name'], "Affiliation": row['Affiliation'], 
        "google_scholar_id": row['google_scholar_id'], 
        "titles_noun_phrases_str": titles_noun_phrases_str,
        "abstracts_noun_phrases_str": abstracts_noun_phrases_str,
        }
        noun_phrases_dict_list.append(noun_phrases_dict)
    except:
        print("Found missing info for {} from {}".format(row['Name'], row['Affiliation']))
        missing_fac_info_dict = {
        "Name": row['Name'], "Affiliation": row['Affiliation'], 
        "google_scholar_id": row['google_scholar_id'], 
        }
        missing_fac_info_dict_list.append(missing_fac_info_dict)

#construct the noun phrases dataframe
noun_phrases_df = pd.DataFrame(noun_phrases_dict_list)
missing_fac_info_df = pd.DataFrame(missing_fac_info_dict_list)
missing_fac_info_df.to_csv('missing_fac_info_from_google_scholar.csv')

# print(noun_phrases_df.shape)
# print(noun_phrases_df.head())

from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse
tfidf_vectorizer = TfidfVectorizer(max_df=1.0, max_features=200000,
                                 min_df=0.0, stop_words='english',
                                 use_idf=True, tokenizer=tokenizer, token_pattern=None,
                                smooth_idf=True, norm = 'l2')
#print((noun_phrases_df['noun_phrases_str']).shape)
tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['titles_noun_phrases_str'])
# vocab = tfidf_vectorizer.vocabulary_
# print(vocab)
# for term in vocab:
#     print(term)
# print(len(tfidf_vectorizer.vocabulary_))
# print(tfidf_matrix.shape)
#save the tfidf_matrix
scipy.sparse.save_npz('titles_tfidf_matrix.npz', tfidf_matrix)

tfidf_vectorizer = TfidfVectorizer(max_df=1.0, max_features=200000,
                                 min_df=0.0, stop_words='english',
                                 use_idf=True, tokenizer=tokenizer, token_pattern=None,
                                smooth_idf=True, norm = 'l2')
#print((noun_phrases_df['noun_phrases_str']).shape)
tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['abstracts_noun_phrases_str'])
print(tfidf_vectorizer.vocabulary_)
print(len(tfidf_vectorizer.vocabulary_))
print(tfidf_matrix.shape)
#save the tfidf_matrix
scipy.sparse.save_npz('abstracts_tfidf_matrix.npz', tfidf_matrix)
