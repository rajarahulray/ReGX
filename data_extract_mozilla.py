# -*- coding: utf-8 -*-

import os
import sqlite3 as sql
import csv
import re
#from sklearn import 

'''Category dictionary'''
cat_dict = {
'1' : ['Mozilla', 'Python', 'Java', 'Perl', 'IDE', 'Spyder', 'Eclipse', 'Maven', 'spring','SQL', 'Swagger', 'Google'],
'2' : ['UPTU', 'AKTU', 'Dr.A.P.J.Abdul Kalam Technical University', 'IPU', 'Indraprastha University', 'MIT'],
'3' : ['IPL', 'Indian Premier League', 'Barclays Priemier League', 'Europa Cup', 'Cricket', 'Football', 'Olympics',\
          'Taek-wondo', 'Swimming'],
'4' : ['Bollywood', 'Hollywood', 'Top Movies', 'Movies', 'Songs', 'Actors', 'Netflix', 'Trending'],
'5' : ['Facebook', 'Twitter', 'Linkedin', 'Squarespace', 'Whatsappweb', 'Instagram', 'Telegram', 'Snapchat', 'Skype'],
'6' : ['Amazon', 'Flipkart', 'eBay', 'Snapdeal', 'Alibaba'],
}
##if nothing matches from above category it is appended in others category.....need to think a little bit more..
#others = [];

'''loading mozilla database moz_places...'''

ld = os.listdir("/home/raja/.mozilla/firefox/");
        
for i in ld:
    if i.endswith(".default"):
        os.chdir("/home/raja/.mozilla/firefox/{}".format(i));

con = sql.connect("places.sqlite");
                 
cur = con.cursor();
    
#cur.execute("select * from moz_historyvisits limit 10");
cur.execute('select id, title, visit_count, last_visit_date from moz_places where title != "None" and length(title) <=25');

#data_list;
#dl = [['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash']];    
dl = [['id', 'title', 'visit_count', 'last_visit_date', 'category']];    
for row in cur:
    print(row); 
    #row.append(" ");
    list_row = list(row)
    list_row.append(" ");
    dl.append(list_row);

#extracting titles from fetched data to a temporary location...
temp = [];
for rec in dl:
    temp.append(rec[1]);
    
#assigning categories to the searches....
for i in range(1, len(dl)):
    if type(dl[i][4] is str):
        dl[i][4] = 7;
        
for k,v in cat_dict.items():
    for i in cat_dict[k]:
        for j in range(1,len(temp)):
            if re.search(r'\b{}\b'.format(i), temp[j]):
                dl[j][4] = int(k);
            

#temp is empty now...
temp = [];
                
con.close();        
'''saving information into .csv file'''
with open("/home/raja/Documents/output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(dl) 

             
