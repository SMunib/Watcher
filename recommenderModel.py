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
    coldStart = None
    minimumVotes = 50
    minAVColdStart = 7.5
    minNumMoviesColdStart = 10
    recommendedMovies = []
    #


    # Checking for cold start problem
    dbCursor.execute("SELECT isFirstTime FROM users WHERE id = ?;", (userID, ))
    coldStart = dbCursor.fetchall()
    coldStart = coldStart[0][0]


    # Model Implementation
    if coldStart:
        dbCursor.execute("SELECT favGenres FROM users WHERE id = ?;", (userID, ))
        favGenres = dbCursor.fetchall()
        favGenres = convertTupleToList(favGenres)
        print(favGenres)

        if favGenres:
            dbCursor.execute("SELECT MovieID, Genres, Title, AvgVote, VoteCount FROM movies WHERE VoteCount > ? ORDER BY AvgVote DESC", (minimumVotes, ))
            results = dbCursor.fetchall()

            for genre in favGenres:
                count = 0

                for row in results:
                    favGenresMovies = row[1].split(", ")

                    if set([genre]).issubset(set(favGenresMovies)) and (row[3] > minAVColdStart): 
                        # print(row[0])
                        if not set([row[0]]).issubset(set(recommendedMovies)):
                            recommendedMovies.append(row[0])
                            count += 1
                    
                    if count >= minNumMoviesColdStart:
                        break
            
            return recommendedMovies
        else:
            return recommendedMovies
    
    else:
        print('not')



# Implementation
print(recommendMoives(2))