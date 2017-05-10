# ReGX
ReGX is a recommendation engine which recommends websites to the user based on the current search by user. 
The machine learns according to the new database after every two days by analyzing the whole of the data of the user browse history.

# The hierarchy of the files are as follow (in accordance with their execution):
## 1. data_extract_mozilla.py:
This script runs collects the user history form PC and assign them some categories.
Lastly it creates a .csv file.

## 2. recomendation_databses.py:
It creates the databases for the categories to recommend.

## 3. google_search_classifier.py:
This script scraps web according to the current user searcha nd then gives top results from google.

## 4. k_neigbhour_classifer.py

This script classifies the search and then assign a category and gives recomendation.
