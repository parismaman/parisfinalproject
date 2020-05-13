
##-----Imports-----##
##--imports all the ibraries for the forms---##
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectMultipleField, DateField, SelectField
from wtforms import validators, ValidationError

from wtforms.validators import DataRequired
### ----------------------------------------------------------- ###



##----------------------------QueryFormStructure------------------------##
## This class have the fields that are part of the nba-salary demonstration
## You can see two fields:
##   the 'Player' field - will be used to get the players in order to make a graph that presents the players he chose.
##   the 'Parameter' field - will be used to get a parameter for the comperhention
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class QueryFormStructure(FlaskForm):
    Players = SelectMultipleField('Choose players:', validators = [DataRequired()] )
    Parameters = SelectField('Choose parameter: ',  choices= [('G','G'),('MP','MP')])
    submit = SubmitField('Submit')
### ----------------------------------------------------------- ###


##--------------------------LoginFormStructure--------------------------------##
## This class have the fields that are part of the Login form.
##   This form will get from the user a 'username' and a 'password' and sent to the server
##   to check if this user is authorised to continue
## You can see three fields:
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')
### ----------------------------------------------------------- ###


##------------UserRegistrationFormStructure--------------------## 
## This class have the fields of a registration form
##   This form is where the user can register himself. It will have sll the information
##   we want to save on a user (general information) and the username ans PW the new user want to have
## You can see three fields:
##   the 'FirstName' field - will be used to get the first name of the user
##   the 'LastName' field - will be used to get the last name of the user
##   the 'PhoneNum' field - will be used to get the phone number of the user
##   the 'EmailAddr' field - will be used to get the E-Mail of the user
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')
### ----------------------------------------------------------- ###


##------------Expand buttom---------##
## builts the buttom that allows the user to open the table of the dataset 
class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"
### ----------------------------------------------------------- ###

##------------Collapse buttom---------##
## builts the buttom that allows the user to close the table of the dataset
class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"
### ----------------------------------------------------------- ###


