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

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from parisfinalproject.Models.QueryFormStructure import UserRegistrationFormStructure
from parisfinalproject.Models.QueryFormStructure import LoginFormStructure

from parisfinalproject.Models.QueryFormStructure import QueryFormStructure 
from parisfinalproject.Models.QueryFormStructure import LoginFormStructure 
from parisfinalproject.Models.QueryFormStructure import UserRegistrationFormStructure 
from parisfinalproject.Models.QueryFormStructure import ExpandForm
from parisfinalproject.Models.QueryFormStructure import CollapseForm

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# -------------------------------------------------------
#Get the choices list of the players in in order of the abc
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
# data analysing of the datasets 
# quary
# -------------------------------------------------------
@app.route('/Query', methods=['GET', 'POST'])
def Query():

    Name = None
    Country = ''
    parametes_choices = ''

    form = QueryFormStructure(request.form)
    form.Players.choices = get_Players_choices() 
     
    if (request.method == 'POST' ):
        print('hello')

# creating the base to the graph

        df = df.set_index('Country')  
        df = df[(form.measures_mselect.data)]
        df = df.loc[(form.country_mselect.data)]

# the graph as picture form

        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'barh', figsize=(15, 5))
        chart = plot_to_img(fig)



    return render_template('Query.html', 
            form = form, 
            Country = Country,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
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
# database page
# -------------------------------------------------------
@app.route('/NBA_salary' , methods = ['GET' , 'POST'])
def NBA_salary():

    print("NBA_salary")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/NBA_salary.csv'))
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

