"""
Used structures and classes
"""
##---------------------------Imports-----------------------------##
##--imports all the ibraries---##
### ----------------------------------------------------------- ###

from os import path
import json
import pandas as pd

def create_LocalDatabaseServiceRoutines():
    return LocalDatabaseServiceRoutines()

class LocalDatabaseServiceRoutines(object):
    def __init__(self):
        self.name = 'Data base service routines'
        self.index = {}
        self.UsersDataFile = path.join(path.dirname(__file__), '..\\static\\Data\\users.csv')

# -------------------ReadCSVUsers------------------------------------#
        # Read users data into a dataframe #
# -------------------------------------------------------------------#

    def ReadCSVUsersDB(self):
        df = pd.read_csv(self.UsersDataFile)
        return df

# ------------------WriteCSVToFile-------------------------#
# Saves the DataFrame (input parameter) into the users csv #
# ---------------------------------------------------------#

    def WriteCSVToFile_users(self, df):
        df.to_csv(self.UsersDataFile, index=False)


# --------------------IsUserExist-----------------------------------#
#        Check if username is already exist in the data file        #
# ------------------------------------------------------------------#

    def IsUserExist(self, UserName):
        # Load the database of users
        df = self.ReadCSVUsersDB()
        df = df.set_index('username')
        return (UserName in df.index.values)


# ---------------------------------------IsLoginGood-----------------------------------#
#-- chek if the UserName/Password are correct(exist in users.csv) and return boolean --#
# -------------------------------------------------------------------------------------#

    def IsLoginGood(self, UserName, Password):
        # Load the database of users
        df = self.ReadCSVUsersDB()
        df=df.reset_index()
        selection = [UserName]
        df = df[pd.DataFrame(df.username.tolist()).isin(selection).any(1)]

        df = df.set_index('password')
        return (Password in df.index.values)
     
# -------------------AddNewUser--------------------------#
# Add a new user to the DB
# -------------------------------------------------------#

    def AddNewUser(self, User):
        # Load the database of users
        df = self.ReadCSVUsersDB()
        dfNew = pd.DataFrame([[User.FirstName.data, User.LastName.data, User.PhoneNum.data, User.EmailAddr.data, User.username.data, User.password.data]], columns=['FirstName', 'LastName', 'PhoneNum', 'EmailAddr',  'username', 'password'])
        dfComplete = df.append(dfNew, ignore_index=True)
        self.WriteCSVToFile_users(dfComplete)

