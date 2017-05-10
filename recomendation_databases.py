#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:25:11 2017

@author: raja
"""

import sqlite3 as sql
import os

os.chdir('/home/raja/Recomendation_databse');

con_pro = sql.connect(r'programming.db');
cur_pro = con_pro.cursor();
cur_pro.execute('create table pro (url LONGVARCHAR)');

con_ent = sql.connect(r'entertainment.db');
cur_ent = con_ent.cursor();
cur_ent.execute('create table ent (url LONGVARCHAR)');

con_soc = sql.connect(r'social.db');
cur_soc = con_soc.cursor();
cur_soc.execute('create table soc (url LONGVARCHAR)');

con_spo = sql.connect(r'sports.db');
cur_spo = con_spo.cursor();
cur_spo.execute('create table spo (url LONGVARCHAR)');

con_sho = sql.connect(r'shopping.db');
cur_sho = con_sho.cursor();
cur_sho.execute('create table sho (url LONGVARCHAR)');

con_edu = sql.connect(r'education.db');
cur_edu = con_edu.cursor();
cur_edu.execute('create table edu (url LONGVARCHAR)');

con_oth = sql.connect(r'others.db');
cur_oth = con_oth.cursor();
cur_oth.execute('create table oth (url LONGVARCHAR)');

con_pro.close();
con_ent.close();
con_soc.close();
con_sho.close();
con_edu.close();
con_oth.close();
