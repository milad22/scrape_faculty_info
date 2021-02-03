import pandas as pd
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer 

#In this file I'm going to write a function which takes the content processes it and returns 
# a list of tokens which is noun phrases in the text and seprated noun phrases, 
# ready to pass to Tdfidf fit

def return_noun_phrases(content):
    """
        returns a list of noun phrases of the content
    """
    return TextBlob(content).noun_phrases

def noun_phrases_str(docs,sep_char):
    """
    returns the a list of noun phrases in from a list of documents
    """
    noun_phrases = []
    for doc in docs:
        noun_phrase_list = return_noun_phrases(doc)
        noun_phrases += noun_phrase_list
    noun_phrases_str = sep_char.join(noun_phrases)
    return noun_phrases_str

def chop_noun_phrases(noun_phrases):
    """
    gets list of noun phrases and returns a list of constituent words
    """
    words = []
    for noun_phrase in noun_phrases:
        words = words + noun_phrase.split(' ')
    return words

def lemmatizer(tokens):
    """
    returns list of stemed tokens
    ref: https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
    """
    lemmatized_tokens = []
    lemmatizer = WordNetLemmatizer()
    for token in tokens:
        #print("The token is {}\n".format(token))
        #print("Lemmantized token is {}\n".format(lemmatizer.lemmatize(token)))
        lemmatized_tokens += [lemmatizer.lemmatize(token)]
    print(lemmatized_tokens)
    return lemmatized_tokens


def process_contents(contents, sep_char):
    """
    returns a string formed of joined tokens seperated by the seperater character (sep_char) 
    """
    phrases = []
    for content in contents:
        #first find the noun phrases in the text
        noun_phrases = return_noun_phrases(content)
        words = chop_noun_phrases(noun_phrases)
        phrases += noun_phrases + words
    #Lemmatize the the token 
    lemmatized_phrases = lemmatizer(phrases)
    #print(stemed_phrases)
    #Make the string which is formed from the joining the phrases list by seprator charachtor sep_char
    #print(phrases)
    string = sep_char.join(lemmatized_phrases)
    
    return string

        
        
content = """ 
A black hole-neutron star simulation must adequately model the inspiral of the binary, its merger, outflows of ejected matter into interstellar space, and the accretion disk formed by the merger of hot nuclear matter swirling around the black hole.  Lately, my interest has mostly been on the last two issues.   With regard to outflows, the goal of our work is to track ejected matter far from the merger site to predict electromagnetic signals and final elemental abundances.  For accretion disks, we are studying the effects of magnetic fields and neutrino emission and applying simulations to test gamma ray burst models and to characterize the neutrino radiation.
"""

print(process_contents([content], ','))
