# import pandas as pd
# from textblob import TextBlob
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn import feature_extraction

# sep_char = ','
# def return_noun_phrases(content):
#     """
#         returns a list of noun phrases of the content
#     """
#     return TextBlob(content).noun_phrases

# def tokenizer(doc):
#     """
#     dummy function defined to feed the TfidfVectorizer
#     """
#     phrase_list  = doc.split(sep_char)
#     return phrase_list

# def noun_phrases_str(docs):
#     """
#     returns the a list of noun phrases in from a list of documents
#     """
#     noun_phrases = []
#     for doc in docs:
#         noun_phrase_list = return_noun_phrases(doc)
#         noun_phrases += noun_phrase_list
#     noun_phrases_str = sep_char.join(noun_phrases)
#     return noun_phrases_str


# # First find the title similarity 
# data_df = pd.read_csv('faculty_info_for_google_scholar_with_scholar_id.csv', keep_default_na=False, usecols = [0,1,2,3])
# noun_phrases_dict_list = []
# missing_fac_info_dict_list = []
# for index, row in data_df.iterrows():
#     if row['google_scholar_id'] == 'None' or row['google_scholar_id'] == '': 
#         continue
#     file_name = row['google_scholar_id'] + '_pubs.json'
#     file_path = './google_scholar_data/' 
#     fac_pubs_info_df = None
#     try:
#         fac_pubs_info_df = pd.read_json(file_path+file_name, orient='split')
#     except:
#         print("Couldn't read the file for {} with scholar id {}".format(row['Name'], row['google_scholar_id']))
#     try:
#         titles = fac_pubs_info_df['title']
#         titles_noun_phrases_str = noun_phrases_str(titles)
#         abstracts = fac_pubs_info_df['abstract']
#         abstracts_noun_phrases_str = noun_phrases_str(abstracts)
#         noun_phrases_dict = {
#         "Name": row['Name'], "Affiliation": row['Affiliation'], 
#         "google_scholar_id": row['google_scholar_id'], 
#         "titles_noun_phrases_str": titles_noun_phrases_str,
#         "abstracts_noun_phrases_str": abstracts_noun_phrases_str,
#         }
#         noun_phrases_dict_list.append(noun_phrases_dict)
#     except:
#         print("Found missing info for {} from {}".format(row['Name'], row['Affiliation']))
#         missing_fac_info_dict = {
#         "Name": row['Name'], "Affiliation": row['Affiliation'], 
#         "google_scholar_id": row['google_scholar_id'], 
#         }
#         missing_fac_info_dict_list.append(missing_fac_info_dict)

# #construct the noun phrases dataframe
# noun_phrases_df = pd.DataFrame(noun_phrases_dict_list)
# missing_fac_info_df = pd.DataFrame(missing_fac_info_dict_list)
# missing_fac_info_df.to_csv('missing_fac_info_from_google_scholar.csv')

# # print(noun_phrases_df.shape)
# # print(noun_phrases_df.head())

# from sklearn.feature_extraction.text import TfidfVectorizer
# import scipy.sparse
# tfidf_vectorizer = TfidfVectorizer(max_df=1.0, max_features=200000,
#                                  min_df=0.0, stop_words='english',
#                                  use_idf=True, tokenizer=tokenizer, token_pattern=None,
#                                 smooth_idf=True, norm = 'l2')
# #print((noun_phrases_df['noun_phrases_str']).shape)
# tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['titles_noun_phrases_str'])
# # vocab = tfidf_vectorizer.vocabulary_
# # print(vocab)
# # for term in vocab:
# #     print(term)
# # print(len(tfidf_vectorizer.vocabulary_))
# # print(tfidf_matrix.shape)
# #save the tfidf_matrix
# scipy.sparse.save_npz('titles_tfidf_matrix.npz', tfidf_matrix)

# tfidf_vectorizer = TfidfVectorizer(max_df=1.0, max_features=200000,
#                                  min_df=0.0, stop_words='english',
#                                  use_idf=True, tokenizer=tokenizer, token_pattern=None,
#                                 smooth_idf=True, norm = 'l2')
# #print((noun_phrases_df['noun_phrases_str']).shape)
# tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['abstracts_noun_phrases_str'])
# print(tfidf_vectorizer.vocabulary_)
# print(len(tfidf_vectorizer.vocabulary_))
# print(tfidf_matrix.shape)
# #save the tfidf_matrix
# scipy.sparse.save_npz('abstracts_tfidf_matrix.npz', tfidf_matrix)


#################################################################################
import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction
from process_content import process_contents
import random
import string

sep_char = ','
# def return_noun_phrases(content):
#     """
#         returns a list of noun phrases of the content
#     """
#     return TextBlob(content).noun_phrases

def tokenizer(doc):
    """
    dummy function defined to feed the TfidfVectorizer
    """
    phrase_list  = doc.split(sep_char)
    return phrase_list

def create_random_string():
    """
    Creates a random string with length 8
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def sort_tuple(tup):  
  
    # reverse = None (Sorts in Ascending order)  
    # key is set to sort using second element of  
    # sublist lambda has been used  
    tup.sort(key = lambda x: x[1])  
    return tup 

# def noun_phrases_str(docs):
#     """
#     returns the a list of noun phrases in from a list of documents
#     """
#     noun_phrases = []
#     for doc in docs:
#         noun_phrase_list = return_noun_phrases(doc)
#         noun_phrases += noun_phrase_list
#     noun_phrases_str = sep_char.join(noun_phrases)
#     return noun_phrases_str

# content = """ 
# A black hole-neutron star simulation must adequately model the inspiral of the binary, its merger, outflows of ejected matter into interstellar space, and the accretion disk formed by the merger of hot nuclear matter swirling around the black hole.  Lately, my interest has mostly been on the last two issues.   With regard to outflows, the goal of our work is to track ejected matter far from the merger site to predict electromagnetic signals and final elemental abundances.  For accretion disks, we are studying the effects of magnetic fields and neutrino emission and applying simulations to test gamma ray burst models and to characterize the neutrino radiation.
# """

# print(process_contents([content], ','))


# First find the title similarity 
data_df = pd.read_csv('indexed_data.csv', keep_default_na=False, usecols = [0,1,2,3])
#print(data_df['id'][0])
noun_phrases_dict_list = []
missing_fac_info_dict_list = []
# for index, row in data_df.iterrows():
#     # if index < 2: continue
#     # if index > 10: break
#     #intilize the contents with a random string so if any of them are missing the process still proceed
#     #initilizing them with same string artificilly make them the research interest similar
#     # if they are missing for two person
#     webpage_contents = [create_random_string()]
#     interests = [create_random_string()]
#     titles = [create_random_string()]
#     abstracts = [create_random_string()]
#     file_name = row['id'] + '.json'
#     file_path = './faculty_merged_info/' + file_name
#     fac_pubs_info_df = None
#     try:
#         fac_pubs_info_df = pd.read_json(file_path, orient='split')
#     except:
#         print("Couldn't read the file for {} with id {}".format(row['Name'], row['id']))
#     try:
#         titles = fac_pubs_info_df['titles'].iloc[0]
#     except:
#         print("Found missing *titles* for {} with id {}".format(row['Name'], row['id']))
#     try:
#         abstracts = fac_pubs_info_df['abstracts'].iloc[0]
#     except:
#         print("Found missing *abstracts* for {} with id {}".format(row['Name'], row['id']))
#     try:
#         interests = fac_pubs_info_df['interests'].iloc[0][0]
#     except:
#         print("Found missing *interests* for {} with id {}".format(row['Name'], row['id']))
#     try:
#         webpage_contents = fac_pubs_info_df['personal_page_content'].iloc[0]
#     except:
#         print("Found missing *webpage contents* for {} with id {}".format(row['Name'], row['id']))

#     noun_phrases_dict = {
#     "Name": row['Name'], 
#     "Affiliation": row['Affiliation'], 
#     "id": row['id'],
#     "titles_noun_phrases_str": process_contents(titles, sep_char, find_noun_phrases = False),
#     "abstracts_noun_phrases_str": process_contents(abstracts, sep_char, find_noun_phrases = False),
#     "interests_noun_phrases_str": process_contents(interests, sep_char,find_noun_phrases = False),
#     "webpage_contents_noun_phrases_str": process_contents(webpage_contents, sep_char, find_noun_phrases = False)
#     }
#     # print(noun_phrases_dict)
#     noun_phrases_dict_list.append(noun_phrases_dict)


# #construct the noun phrases dataframe
# noun_phrases_df = pd.DataFrame(noun_phrases_dict_list)
#save the dataframe
# noun_phrases_df.to_pickle('fac_research_data.pkl')
noun_phrases_df = pd.read_pickle('fac_research_data.pkl')

# print(noun_phrases_df.shape)
# print(noun_phrases_df.head())
#************************************
print("Began making the model")
search_terms = ['string theory']
search_terms_dict = {
"Name": 'dummy', 
"Affiliation": 'dummy', 
"id": 'dummy',
"titles_noun_phrases_str": process_contents(search_terms, sep_char, find_noun_phrases = False),
"abstracts_noun_phrases_str": process_contents(search_terms, sep_char, find_noun_phrases = False),
"interests_noun_phrases_str": process_contents(search_terms, sep_char,find_noun_phrases = False),
"webpage_contents_noun_phrases_str": process_contents(search_terms, sep_char, find_noun_phrases = False)
}
#append search terms dict to the dataframe
noun_phrases_df = noun_phrases_df.append(search_terms_dict, ignore_index=True)
print(noun_phrases_df.tail(2))
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse
tfidf_vectorizer = TfidfVectorizer(max_df=0.5, max_features=200000,
                                 min_df=0.0, stop_words='english',
                                 use_idf=True, tokenizer=tokenizer, token_pattern=None,
                                smooth_idf=True, norm = 'l2')
#print((noun_phrases_df['noun_phrases_str']).shape)
titles_tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['titles_noun_phrases_str'])
vocab = tfidf_vectorizer.vocabulary_
print(vocab)
# for term in vocab:
#     print(term)
# print(len(tfidf_vectorizer.vocabulary_))
# print(tfidf_matrix.shape)
#save the tfidf_matrix
scipy.sparse.save_npz('titles_tfidf_matrix.npz', titles_tfidf_matrix)
################################################################
################################################################

tfidf_vectorizer = TfidfVectorizer(max_df=0.5, max_features=200000,
                                 min_df=0.0, stop_words='english',
                                 use_idf=True, tokenizer=tokenizer, token_pattern=None,
                                smooth_idf=True, norm = 'l2')
#print((noun_phrases_df['noun_phrases_str']).shape)
abstracts_tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['abstracts_noun_phrases_str'])
print(tfidf_vectorizer.vocabulary_)
print(len(tfidf_vectorizer.vocabulary_))
print(abstracts_tfidf_matrix.shape)
#save the tfidf_matrix
scipy.sparse.save_npz('abstracts_tfidf_matrix.npz', abstracts_tfidf_matrix)
################################################################
################################################################

tfidf_vectorizer = TfidfVectorizer(max_df=0.5, max_features=200000,
                                 min_df=0.0, stop_words='english',
                                 use_idf=True, tokenizer=tokenizer, token_pattern=None,
                                smooth_idf=True, norm = 'l2')
#print((noun_phrases_df['noun_phrases_str']).shape)
interests_tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['interests_noun_phrases_str'])
vocab = tfidf_vectorizer.vocabulary_
print(vocab)
# for term in vocab:
#     print(term)
# print(len(tfidf_vectorizer.vocabulary_))
# print(tfidf_matrix.shape)
#save the tfidf_matrix
scipy.sparse.save_npz('interests_tfidf_matrix.npz', interests_tfidf_matrix)
################################################################
################################################################

tfidf_vectorizer = TfidfVectorizer(max_df=0.5, max_features=200000,
                                 min_df=0.0, stop_words='english',
                                 use_idf=True, tokenizer=tokenizer, token_pattern=None,
                                smooth_idf=True, norm = 'l2')
#print((noun_phrases_df['noun_phrases_str']).shape)
webpage_contents_tfidf_matrix = tfidf_vectorizer.fit_transform(noun_phrases_df['webpage_contents_noun_phrases_str'])
print(tfidf_vectorizer.vocabulary_)
print(len(tfidf_vectorizer.vocabulary_))
print(webpage_contents_tfidf_matrix.shape)
#save the tfidf_matrix
scipy.sparse.save_npz('webpage_contents_tfidf_matrix.npz', webpage_contents_tfidf_matrix)


from sklearn.metrics.pairwise import cosine_similarity
titles_cosine_similarity = cosine_similarity(titles_tfidf_matrix)[-1,:]
abstracts_cosine_similarity = cosine_similarity(abstracts_tfidf_matrix)[-1,:]
interests_cosine_similarity = cosine_similarity(interests_tfidf_matrix)[-1,:]
webpage_contents_cosine_similarity = cosine_similarity(webpage_contents_tfidf_matrix)[-1,:]


from operator import add 
total_similarity = [(titles_cosine_similarity[i] + abstracts_cosine_similarity[i] + interests_cosine_similarity[i] + webpage_contents_cosine_similarity[i]) for i in range(len(interests_cosine_similarity))]
print(total_similarity[-1])

#Make list of tuples
tup_list = []
for i in range(len(total_similarity)-1):
    tup_list.append((i,total_similarity[i]))
#sort the tuples based on similarity
selected_tuples = sort_tuple(tup_list)[-10:-1]
for tuple in selected_tuples:
    print(data_df['id'][tuple[0]])
