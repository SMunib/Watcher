import os
import math
import sqlite3
import numpy
import matplotlib as plt


# Helping functions to manipulate data
def convertTupleToList(tuple):
    List = tuple[0][0]
    List = List.split(', ')
    return List

def convertTupleToString(tuple):
    Str = tuple[0][0]
    Str = Str.replace("'", "")
    return Str

def relativeRating(avg, userrating):
    xRelative = avg - userrating
    return xRelative

def scaleRelativeRating(minRR, maxRR, relativeRating, scaler = 10):
    xScaled = ((relativeRating - minRR) / (maxRR - minRR)) * scaler
    return xScaled

def recommendMoives(userID):
    # Determining directory for accesing WatcherDB.db in /instance folder
    currentDir = os.getcwd()
    dbFile = 'WatcherDB.db'
    dbFolder = 'instance'
    dbPath = os.path.join(currentDir, dbFolder)
    dbPath = os.path.join(dbPath, dbFile)

    # Establishing DB connection
    try:
        dbConnection = sqlite3.connect(dbPath)
        dbCursor = dbConnection.cursor()

    except sqlite3.Error as error:
        return 'Database connection failed!'
    
    # Variables needed by model
    #


    # Checking for cold start problem
    dbCursor.execute("SELECT isFirstTime FROM users WHERE id = ?;", (userID, ))



# Implementation
recommendMoives(1)