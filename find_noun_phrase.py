import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
from nltk import Tree
import pandas as pd

#ref:https://stackoverflow.com/questions/33587667/extracting-all-nouns-from-a-text-file-using-nltk
from textblob import TextBlob

# blob = TextBlob(text)
# print(blob.noun_phrases)
# list = [[1,3,2],[4,3,2],[1,6,7]]
# flaten_list = [x for item in list for x in item] 
# print(flaten_list)

fran = """ 
Francois Foucart is an Assistant Professor in the Physics Department at UNH. He is originally from Brussels, Belgium, and obtained undegraduate engineering degrees from the Free University of Brussels (ULB) and the Ecole Centrale Paris (ECP). He moved to the United States for a Ph.D in Physics, graduating from Cornell University in 2011. He was then a postdoctoral fellow for 3 years at the Canadian Institute for Theoretical Astrophysics (CITA) in Toronto, and a NASA Einstein fellow at the Lawrence Berkeley National Lab (LBL) for another 3 years, before moving to UNH in 2017.

Francois Foucart works on computational astrophysics, with a particular focus on studies of black holes and neutron stars, general relativistic hydrodynamics, radiation transport, and nuclear astrophysics. In particular, he studies merging black holes and neutron stars, and models the gravitational wave and electromagnetic signals (gamma-ray bursts, optical/infrared transients) that these mergers power, as well as their role in the production of heavy atoms such as gold and platinum. He also studies the evolution of accretion disks both as remnants of binary mergers and in the neighborhood of supermassive black holes. 

Simulations of merging compact objects are especially important in order to interpret observations of gravitational waves by the LIGO and Virgo detectors, as well as the electromagnetic signals detectable by ground-based and space-based observatories which accompany these events (if one of the merging objects is a neutron star). Observations of binary mergers can also help us ellucidate open problems in nuclear physics: the properties of cold, neutron-rich matter at the extremely large densities existing in the core of a neutron star, and the origin of elements produced by rapid neutron capture (r-process) nucleosynthesis (incl. gold, platinum, uranium,...).

In August 2017, the LIGO and Virgo detectors observed for the first time gravitational waves powered by the collision of two neutron stars. These gravitational waves were followed by observations of the post-merger remnant across the entire electromagnetic spectrum. After this first detection, it now seems likely that dozens of neutron star mergers will be observed over the next decade. If we have reliable models to interpret these observations, we can use neutron star mergers to study gravity, nuclear physics, the life and death of massive stars, the mechanisms powering the observed population of short gamma-ray bursts, and the origin of many of the heavy elements observed in the solar system today! An important objective of my research is thus to use numerical simulations to develop and test models of the gravitational wave and electromagnetic signals powered by neutron star mergers.

Simulations of accretion disks around supermassive black holes, on the other hand, will help us understand the impact of the disk's inflows and outflows on the formation and evolution of the surrounding galaxy, and will also play an important role in the interpretation of observations of Sgr A* (the supermassive black hole at the center of the Milky Way) by the Event Horizon Telescope. These observations will, for the first time, provide us with images resolving the event horizon of a black hole!
"""
matt = """
My research focuses on the dynamics of hot nuclear matter in strongly curved spacetime.  Most of my published work concerns black hole-neutron star binary mergers, which are potentially important sources of gravitational waves, kilonovae, short duration gamma ray bursts (GRBs), and r-process elements.  Much of our black hole-neutron star work has been devoted to exploring the large parameter space of possible binaries.  There are two interesting (from a fluid dynamics/GRB perspective) regions of this space, where the neutron star is ripped apart before being swallowed by the black hole:  systems with low black hole mass and systems with high black hole spin.  We’ve focused a lot on binaries with high-spin, moderate-to-high mass  black holes both because they’ve gotten less attention from other groups and because SpEC is very good at handling high-spin black holes.

A black hole-neutron star simulation must adequately model the inspiral of the binary, its merger, outflows of ejected matter into interstellar space, and the accretion disk formed by the merger of hot nuclear matter swirling around the black hole.  Lately, my interest has mostly been on the last two issues.   With regard to outflows, the goal of our work is to track ejected matter far from the merger site to predict electromagnetic signals and final elemental abundances.  For accretion disks, we are studying the effects of magnetic fields and neutrino emission and applying simulations to test gamma ray burst models and to characterize the neutrino radiation.

I’m also very interested in the extension of SXS research to studies of binary neutron stars, newborn neutron stars, black hole accretion in general, and other strong-gravity nuclear matter systems that involve the sort of physics we’ve been playing with in our black hole-neutron star mergers.  To me, the fascination of non-vacuum numerical relativity is that 1) all of these other exotic areas of physics come into play in addition to strong gravity, 2) simulations are still so immature that major pieces of physics have yet to be included and qualitative surprises may be in store, and 3) the existence of a special frame picked out by the fluid flow makes it much easier to convert simulation data into intelligible narratives.

Biography

I got my PhD in 2005 at the University of Illinois at Urbana-Champaign working with Prof. Stuart Shapiro on the effects of viscous and magnetic angular momentum transport on binary neutron star merger remnants.  I then went to Cornell as a postdoc working under Prof. Saul Teukolsky.  My main task during these years was to add hydrodynamics to the Spectral Einstein Code and carry out our first black hole-neutron star simulations.  I next began working on adding more realistic modeling of the neutron star matter to these simulations.  In 2010, I joined the faculty of Washington State University as an assistant professor.
"""
def dummy_fun(doc):
    return doc

def tokenize_text(doc):
    return doc.split(sep)

sep = ','
matt_blob = TextBlob(matt).noun_phrases
fran_blob = TextBlob(fran).noun_phrases

matt_term_list = [t for term in matt_blob for t in term.split(' ')]
#matt_term_list += matt_blob
fran_term_list = [t for term in fran_blob for t in term.split(' ')]
#fran_term_list += fran_blob





matt_text = sep.join(matt_blob)
fran_text = sep.join(fran_blob)
#print(tokenize_text(matt_text))

# matt_text = "I love you very much. How are doing"
# fran_text = "I'm doing well I love you too"
#docs = [matt_text,fran_text]
#docs = [matt_blob, fran_blob]
docs = [matt_term_list, fran_term_list]

print(fran_blob)
print(matt_blob)
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(
    max_df=1.0, max_features=200000,
    min_df = 0.0,
    analyzer='word',
    tokenizer=dummy_fun,
    preprocessor=dummy_fun,
    #tokenizer=tokenize_text,
    #preprocessor=dummy_fun,
    token_pattern=None,
    use_idf = True,
    smooth_idf=True,
    norm = 'l2')  
X = tfidf.fit_transform(docs)

print(len(tfidf.get_feature_names()))
print(X.shape)
print(X[0,:])
print(X[1,:])
# print(tfidf_matrix[1,:])
print(tfidf.vocabulary_)
# print(tfidf.inverse_transform(X))

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(X)
print(similarity)
