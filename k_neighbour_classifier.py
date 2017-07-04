# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import cross_validation, neighbors
import sqlite3 as sql
import os
from tkinter import Label, Tk, Button, Toplevel
import webbrowser
from random import randint

cat_dict = {
        '1' : 'programming',
        '2' : 'education',
        '3' : 'sports',
        '4' : 'entertainment',
        '5' : 'social',
        '6' : 'shop',
        '7' : 'others',
        };

ABOUT_TEXT = """About

This is an auto-generated window to show you some recomendations based on your searches"""

DISCLAIMER = """
Disclaimer

These recomendations are generated based on your searches on web.
Use it on your own risk"""

rec_list = [];

def callback(event):
    try:
        webbrowser.open_new(event.widget.cget("text"));
        print("Recomendation Showed");
    except Exception as e:
        print('Some Error: {}'.format(str(e)));

def clickAbout():
    toplevel = Toplevel()
    toplevel.configure(background = 'white');
    label1 = Label(toplevel, text=ABOUT_TEXT, height=0, width=100)
    label1.pack()
    label1.configure(background = 'white');
    label2 = Label(toplevel, text=DISCLAIMER, height=0, width=100)
    label2.configure(background = 'white');
    label2.pack();
    
    i = randint(0, len(rec_list));
    label3 = Label(toplevel, text = rec_list[i], fg="blue", cursor="hand2");
    
    label3.pack();
    label3.bind("<Button-1>", callback);
    label3.configure(background = 'white');
    toplevel.mainloop();

data_frame = pd.read_csv('/home/raja/Documents/output.csv');
data_frame.drop(['title'], 1, inplace = True);
data_frame.drop(['id'], 1, inplace = True);

train= np.array(data_frame.drop(['category'],1));
test = np.array(data_frame['category']);
                
x_train, x_test, y_train, y_test = cross_validation.train_test_split(train, test, test_size = 0.4);

clf = neighbors.KNeighborsClassifier()
clf.fit(x_train, y_train);

accuracy = clf.score(x_test, y_test);
print('Accuracy: {}'.format(accuracy));


#Predicting Test Data...
ld = os.listdir("/home/raja/.mozilla/firefox/");
        
for i in ld:
    if i.endswith(".default"):
        os.chdir("/home/raja/.mozilla/firefox/{}".format(i));

con = sql.connect("places.sqlite");
                 
cur = con.cursor();
test_data = [];    
#cur.execute("select * from moz_historyvisits limit 10");
cur.execute('select visit_count, max(last_visit_date) from moz_places where title != "None" and length(title) <=25');
for row in cur:
    test_data.append(list(row));
    print(row);

con.close();
print(test_data);

pre_data = np.array(test_data);
pre_data = pre_data.reshape(len(pre_data),-1);
prediction = clf.predict(pre_data);

'''Prediction....'''
print(prediction);
#print(type(data_frame['abs(mrp)']));     
#data_frame['abs(mrp)'].plot();
#pyplot.scatter(pre_data[0],pre_data[1] , color = 'red');

os.chdir('/home/raja/Recomendation_databse');
for k,v in cat_dict.items():
    if str(prediction[0]) == k:
        db = cat_dict[k];
    
print(db)
con = sql.connect('{}.db'.format(db));
print('Connection established');
cur = con.execute('select url from {}'.format(db[0:3]));
for row in cur:
    rec_list.append(row);
#con.close();
app = Tk()

app.title("Recomendation_App")
app.geometry("250x100+1100+590");
app.resizable(0,0);
app.configure(background = 'white');
label = Label(app, text = "Your Recomendations are here", height=0, width=100);
label.configure(background = 'white');
label2 = Label(app, text = "Want to view ?");
label2.configure(background = 'white');
b = Button(app, text="No", width=20, command=app.destroy)
button1 = Button(app, text="Yes, show me", width=20, command=clickAbout)
label.pack();
label2.pack();
b.pack(side='bottom',padx=0,pady=0)
button1.pack(side='bottom',padx=5,pady=5);

app.mainloop();
