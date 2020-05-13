"""
Routes and views for the flask application.
"""

##-------------------------Imports-----------------------##
##-------imports all the ibraries for the views.py--------#
### --------------------------------------------------- ###

from datetime import datetime
from flask import render_template
from parisfinalproject import app
from parisfinalproject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
 

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path


from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
# allows the user to select multiple feilds or one, and to move to other page from the datamodel page
from wtforms import ValidationError

from parisfinalproject.Models.QueryFormStructure import QueryFormStructure 
from parisfinalproject.Models.QueryFormStructure import LoginFormStructure 
from parisfinalproject.Models.QueryFormStructure import UserRegistrationFormStructure 
from parisfinalproject.Models.QueryFormStructure import ExpandForm
from parisfinalproject.Models.QueryFormStructure import CollapseForm

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# -------------------------------------------------------##
# Get the choices list of the players in in order of the abc
# -------------------------------------------------------##

def get_Players_choices():
    df = pd.read_csv(path.join(path.join(__file__),"..\\static\\Data\\NBA_salary.csv" ))
    # קורא את קובץ ה-csv
    l=df['Player'].tolist()
    # מאפשרת למשתמש לבחור שחקנים מן הרשימה בקטגוריה
    l.sort()
    # ממיינת את הרשימה לפי סדר a-z
    l=list(zip(l,l))
    return l
    # מחזירה את רשימת השחקנים עם אפשרות לבחירת שחקנים ללא הגבלה של המשתמש


###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 
app.config['SECRET_KEY'] = 'All You Need Is Love Ta ta ta ta ta'
# secret key- נועד להגן על פרטי המשתמש: שם, סיסמה לאתר, טלפון, מייל וכו'
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# מייבא מאפליקציית bootst

# -------------------------------------------------------
# Home page
# -------------------------------------------------------

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

# -------------------------------------------------------
# contact page
# -------------------------------------------------------
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
     
    )

# -------------------------------------------------------
# About page
# -------------------------------------------------------

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
    
    )

# -------------------------------------------------------
# photo album page
# -------------------------------------------------------

@app.route('/Album')
def Album():
    """Renders the about page."""
    return render_template(
        'PictureAlbum.html',
        title='Pictures',
        year=datetime.now().year,
    )

# -------------------------------------------------------
# data model page
# -------------------------------------------------------
@app.route('/DataModel')
def DataModel():

    print("DataModel")

    """Renders the about page."""
    return render_template(
        'DataModel.html',
        title='DataModel',
        year=datetime.now().year,
        message='My data page.',
    )


# -------------------------------------------------------
# database page
# -------------------------------------------------------
@app.route('/NBA_salary' , methods = ['GET' , 'POST'])
def NBA_salary():

    print("NBA_salary")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    #ייבוא מעמוד ה- QueryFormStructure
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/NBA_salary.csv'))
    # קורא את קובץ ה-csv
    df=df[['Player','Salary','NBA_Country','Age', 'Tm','G','MP', 'TS%']]
    # מוריד מהטבלה את כל העמודות מקובץ הדאטא המקורי שלא רלוונטיות לי ומשאיר רק את הרלוונטיות
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
     # הפעולה תפתח את הטבלה המלאה, כשיבקש המשתמש באמצעות לחיצת כפתור
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
     # הפעולה תסגור את הטבלה מתצוגה, כשיבקש המשתמש באמצעות לחיצת כפתור

    

    return render_template(
        'NBA_salary.html',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )



# -------------------------------------------------------
# data analysing of the datasets 
# quary page
# -------------------------------------------------------
@app.route('/Query', methods=['GET', 'POST'])
def Query():

    chart= ''


    form = QueryFormStructure(request.form)
    form.Players.choices = get_Players_choices() 
     
    if (request.method == 'POST' ):
        category = form.Parameters.data
        # יוצר משתנה חדש
        player_names = form.Players.data
        # יוצר משתנה חדש
        df = pd.read_csv(path.join(path.join(__file__),"..\\static\\Data\\NBA_salary.csv" ))
        df=df[['Player','Salary','G','MP']]
        # מגדיר טבלה חדשה בה נמצאים רק הפרמטרים הרלוונטים לי
        df=df[['Player','Salary',category]]
        # מגדיר מחדש את הטבלהת רק שבמקום שמות הקטגוריות יצרתי משתנה שכולל את שניהם שבהמשך יהפוך לקטגוריה dollarper ויבצע את הפעולה המבוקשת לקווארי שלי
        df=df.dropna()
        # מוריד את כל השחקנים שיש להם בטבלה שדות ריקים
        df['Salary']= df['Salary'].astype(int)
        # הופך את הסטרינג לאינדקס על מנת שיהיה ניתן לחלק את הקטגוריה וליצור מספר מממוצע חדש
        df[category]= df[category].astype(int)
        # הופך את הסטרינג לאינדקס על מנת שיהיה ניתן לחלק את הקטגוריה וליצור מספר מממוצע חדש
        df['DollarPer']= df['Salary']/df[category]
        # יוצר קטגוריה חדשה בשם dollarper. היא מועדת לחשב מצוצע עם קטגוריות שאיתם ירצה המשתמש להשוות. לדוגמא, 
        # אם ירצה המשתמש להשוות בעזרת הפרמטר כמות משחקים אז הפעולה שיצרתי תחלק את המשכורת הכוללת של אוותו שחקן בכמות המשחקים ששיחק בעונה
        #    ) דולר פר משחק) ובכך תציג כמה מרוויח השחקן בממוצע בכל משחק
        df=df.drop('Salary',1)
        # מוריד את הקטגוריה מאחר ויצרנו אחת חדשה בשם dollarper שמבוססת על הקטגוריות המשכורת
        df=df.drop(category,1)
        # מוריד את הקטגוריה מאחר ויצרנו אחת חדשה בשם dollarper שמבוססת על הקטגוריות ועל המשכורת
        df=df.set_index('Player')
        df=df[df.index.isin(player_names)]
        # בודקת אם ערכי שחקנים אלו נמצאים ברשימה
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'barh', figsize=(15, 5), color='pink', fontsize= 20)
        chart = plot_to_img(fig)
        # עיצוב הגרף, עצב, גודל טקס, צורה.. + הופך את הגרף לתמונה



    return render_template('Query.html', 
            form = form, 
            year=datetime.now().year,
            message='This page will use the web forms to get user input',
            chart = chart
        )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # אם הרשימה ממולאת כמו שצריך, האתר יציג הודעה "תודה שנרשמת"
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            # אם אחד הפרטים שהזין המשתמש כבר קיים במערכת, האתר יציג הודעה בה רשום: "שגיאה: שם משתמש זה כבר קיים במערכת"
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)
 
    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query')
        else:
            flash('Error in - Username and/or password')
   # אם שם המשתמש והסיסמה שהכניס המשתמש תואמים ונכונים, האתר יאשר זאת ויעביר אותו ישירות לעמוד ה-query
   # אם לא, האתר יחזיר הודעת שגיאה בה כתוב שם משתמש/ סיסמה אינם נכונים
    return render_template(
        'login.html',
        form=form,
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Turns the graph into a picture
# -------------------------------------------------------

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


