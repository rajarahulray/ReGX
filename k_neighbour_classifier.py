# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import cross_validation, neighbors
import sqlite3 as sql
import os
from tkinter import Label, Tk, Button, Toplevel
import webbrowser
from random import randint

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

cat_dict = {
        '1' : 'programming',
        '2' : 'education',
        '3' : 'sports',
        '4' : 'entertainment',
        '5' : 'social',
        '6' : 'shop',
        '7' : 'ecommerce',
        '8' : 'others',
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
        print("Recomendation Shown");
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

#loading the json data andconverting it to pandas data frame.
data_frame = pd.read_json('/home/raja/Documents/json_output.json');

##renamed all json data lables as id, title, visit_count, last_visit_data, and category.
data_frame.columns = ['id', 'title', 'visit_count', 'last_visit_date', 'category'];
data_frame = data_frame.dropna();
data_frame.drop(['title'], 1, inplace = True);
data_frame.drop(['id'], 1, inplace = True);
data_frame = data_frame.drop(data_frame.index[0]);

train= np.array(data_frame.drop(['category'],1));
test = np.array(data_frame['category']);
                
x_train, x_test, y_train, y_test = cross_validation.train_test_split(train, test, test_size = 0.4);
x_train = x_train.astype('int');
y_train = y_train.astype('int');
y_train = y_train.astype('int');
y_test = y_test.astype('int');

# Test options and evaluation metric
seed = 7
scoring = 'accuracy'# Test options and evaluation metric

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, x_test, y_test, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)

#training data with k-NN_classifier.
clf = neighbors.KNeighborsClassifier()
clf.fit(x_train, y_train);

#mean accuracy based on test_data..
accuracy = clf.score(x_test, y_test);
print('Accuracy: {}'.format(accuracy));


#Predicting Test Data...
ld = os.listdir("/home/raja/.mozilla/firefox/");
print('Entered "/home/raja/.mozilla/firefox/" directory');
        
for i in ld:
    if i.find(".default") != -1:
        os.chdir("/home/raja/.mozilla/firefox/{}".format(i));

con = sql.connect("places.sqlite");
print('used places.sqlite table');
                 
cur = con.cursor();
test_data = [];    
#cur.execute("select * from moz_historyvisits limit 10");

cur.execute('select visit_count, max(last_visit_date) from moz_places where title != "None" and length(title) <=25');
for row in cur:
    test_data.append(list(row));
    print(row);

con.close();
#print(test_data);

pre_data = np.array(test_data);
pre_data = pre_data.reshape(len(pre_data),-1);
prediction = clf.predict(pre_data);

'''Prediction....'''
print("Your Recommended Category : ",cat_dict[str(prediction[0])]);
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
con.close();
print('Conncetion Closed')

#GUI for recommender:
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
