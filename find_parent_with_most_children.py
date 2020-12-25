from typing import Text
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
from lxml import html 
import re
# parent = '//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div'
# all_links_in_parent = '//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div//@href'
# all_children_of_parent = '//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div/*'
# #itrate over childeren 


def find_max_node_branch(parent, nodes = []):
        children = parent.xpath('child::*')
        if len(children) > 0:
            nodes.append(len(children))
            for child in children:
                find_max_node_branch(child)
        return max(nodes)






url = 'http://web.mit.edu/physics/people/faculty/index.html'

doc = open('MIT_Department_of_Physics.html', mode='r')
page = doc.read()

tree = html.fromstring(page)
parent = tree.xpath('//*[@id="middle-column"]/div[6]/div[2]/div[2]/div[2]/div')[0]

# children = parent.xpath('child::*')
# for child in children:
#     print(child.xpath('descendant::text()')) #selecr all descendant text od current node 
#     #print(child.xpath('*//@href'))
body = tree.xpath('//body')[0]

parent2 = body.xpath('//*[count(*) = 89]')[0]
children = parent2.xpath('child::*')
# for child in children:
    #print(child.xpath('descendant::text()')) #selecr all descendant text od current node 
    #print(child.xpath('*//@href'))

print(find_max_node_branch(body))

# N = 89
# def find_node_with_n_branch(parent):
#         children = parent.xpath('child::*')
        
#         if len(children) == N:
#             return parent
            
#         else:
#             for child in children:
#                 parent = child
#                 find_node_with_n_branch(parent)

        

# print(find_node_with_n_branch(body).xpath('descendant::text()'))


# children = parent.xpath('child::*')
# for child in children:
#     print(child.xpath('descendant::text()')) #selecr all descendant text od current node





