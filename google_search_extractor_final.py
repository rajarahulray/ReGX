# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sqlite3 as sql
import os

page = requests.get("https://www.google.co.in/search?q=Life after Engineering")
soup = BeautifulSoup(page.content)
links = soup.find_all("a");


url_lists = [];
                   
for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
    url_lists.append(re.split(":(?=(^http))",link["href"].replace("/url?q=","")));                

print(len(url_lists));
         
extract_pattern = re.compile("'(.*)&sa");
extract_pattern2 = re.compile("'(.*)J:");
for url_lists_index in range(len(url_lists)):
    g = extract_pattern.search(str(url_lists[url_lists_index]));
    g2 = extract_pattern.search(str(url_lists[url_lists_index]));
    print(url_lists_index);
    if g :                              
        url_lists[url_lists_index] = g.group(1);                     
    #not working yet..
    elif g2:
        url_lists[url_lists_index] = g2.group(1);                     
        
#for url in url_lists:
#    print(url);

os.chdir('/home/raja/Recomendation_databse');

con = sql.connect('others.db');
print("Connection Established")
for url in url_lists:
    print([url]);
    con.execute("INSERT INTO oth (url) VALUES (?)", [url]);

con.commit();
cur = con.execute("select * from oth;");
data_all = cur.fetchall();
for row in cur:
    print(type(row))
    print(row);
con.close();
print("Connection Closed...");
    
