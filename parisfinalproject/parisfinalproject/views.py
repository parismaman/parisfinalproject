"""
Routes and views for the flask application.
"""

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

# -------------------------------------------------------
# import from the environment and from requirment.txt
# -------------------------------------------------------

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

# -------------------------------------------------------
# Get the choices list of the players in in order of the abc
# -------------------------------------------------------
def get_Players_choices():
    df = pd.read_csv(path.join(path.join(__file__),"..\\static\\Data\\NBA_salary.csv" ))
    l=df['Player'].tolist()
    l.sort()
    l=list(zip(l,l))
    return l



###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 
app.config['SECRET_KEY'] = 'All You Need Is Love Ta ta ta ta ta'
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

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
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/NBA_salary.csv'))
    df=df[['Player','Salary','NBA_Country','Age', 'Tm','G','MP', 'TS%']]
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

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
        player_names = form.Players.data
        df = pd.read_csv(path.join(path.join(__file__),"..\\static\\Data\\NBA_salary.csv" ))
        df=df[['Player','Salary','G','MP']]
        df=df[['Player','Salary',category]]
        df=df.dropna()
        df['Salary']= df['Salary'].astype(int)
        df[category]= df[category].astype(int)
        df['DollarPer']= df['Salary']/df[category]
        df=df.drop('Salary',1)
        df=df.drop(category,1)
        df=df.set_index('Player')
        df=df[df.index.isin(player_names)]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'barh', figsize=(15, 5), color='pink', fontsize= 20)
        chart = plot_to_img(fig)



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
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
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


