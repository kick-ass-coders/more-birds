# import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import json

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
          'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
          'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
          'WI', 'WY']

def get_st_list(state):

    # store url for page with list of us birds
    stateURL = "https://ebird.org/region/US-"+state+"/media?yr=all&m="
    # get html
    result=requests.get(stateURL)
    # create beautiful soup object
    soup = bs(result.text, 'html.parser')
    # get all h3 tags
    h3 = soup.findAll('h3')
    # get all text from h3 tags
    state_birds = [tag.text for tag in h3]
    checklist = {state: state_birds} 
    return(checklist)

checklists = {}
for state in states:
    state_list = get_st_list(state)
    checklists.update(state_list)

checklists_j = json.dumps(checklists)

with open('state_checklists.txt', 'w') as outfile:
    json.dump(checklists, outfile)