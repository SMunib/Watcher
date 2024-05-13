import os
import math
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

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


# AI Model
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
    minAvgVote = 6.5
    minNumMoviesColdStart = 10
    recommendedMovies = []
    userWatchedMovies = []
    X = 0
    Y = 0
    allRelativeRatings = []
    allAvgRatings = []
    allMovieIDs = []
    numClusters = 4
    acceptingSimilarity = 0.015
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

        if favGenres:
            dbCursor.execute("SELECT MovieID, Genres, Title, AvgVote, VoteCount FROM movies WHERE VoteCount > ? ORDER BY AvgVote DESC", (minimumVotes, ))
            results = dbCursor.fetchall()

            for genre in favGenres:
                count = 0

                for row in results:
                    favGenresMovies = row[1].split(", ")

                    if set([genre]).issubset(set(favGenresMovies)) and (row[3] > minAVColdStart): 
                        if not set([row[0]]).issubset(set(recommendedMovies)):
                            recommendedMovies.append(row[0])
                            count += 1
                    
                    if count >= minNumMoviesColdStart:
                        break
            
            return recommendedMovies
        else:
            return recommendedMovies
    
    else:
        # Getting all movies user has watched
        dbCursor.execute("SELECT watchedMovies FROM users WHERE id = ?", (userID, ))
        userWatchedMovies = dbCursor.fetchall()
        userWatchedMovies = convertTupleToList(userWatchedMovies)

        # iterating for each movie Collaborative then Content based filtering and generating recommendations based on each movie
        for movie in userWatchedMovies:
            clusteringCoordinates = []

            # Getting the rating user has given to it
            dbCursor.execute("SELECT rating FROM user_rating WHERE userID = ? and movieID = ?", (userID, movie))
            userMovieRating = dbCursor.fetchall()
            userMovieRating = userMovieRating[0][0]
            X = userMovieRating

            # Getting the avg rating given to it
            dbCursor.execute("SELECT AvgVote FROM movies WHERE movieID = ?", (movie, ))
            userMovieAvgRating = dbCursor.fetchall()
            userMovieAvgRating = userMovieAvgRating[0][0]
            Y = userMovieAvgRating

            # Creating coordinate for user movie
            clusteringCoordinates.append((X, Y))
            allMovieIDs.append(movie)

            # Now, getting coordinates for all movies with similar genres
            dbCursor.execute("SELECT Genres FROM movies WHERE MovieID = ?", (movie, ))
            userMovieGenres = dbCursor.fetchall()
            userMovieGenres = convertTupleToList(userMovieGenres)
            # print(userMovieGenres)
            
            # Getting high rated movies for each genre
            dbCursor.execute("SELECT MovieID, Genres, Title, AvgVote, VoteCount FROM movies WHERE VoteCount > ? ORDER BY AvgVote DESC", (minimumVotes, ))
            results = dbCursor.fetchall()

            for genre in userMovieGenres:
                count = 0

                for row in results:
                    moviesGenres = row[1].split(", ")

                    # Getting highest rated n movies for the genre
                    if set([genre]).issubset(set(moviesGenres)) and not(row[0] in userWatchedMovies) :
                        allRelativeRatings.append(relativeRating(row[3], userMovieRating))
                        allAvgRatings.append(row[3])
                        allMovieIDs.append(row[0])

            # Creating coordinates for the choosen movies    
            for x in range(len(allRelativeRatings)):
                X = scaleRelativeRating(min(allRelativeRatings), max(allRelativeRatings), allRelativeRatings[x], 10)
                Y = allAvgRatings[x]
                clusteringCoordinates.append((X, Y))        
            
            # Converting coordinates from list of tuples to 2D numpy array
            clusteringCoordinates = np.array(clusteringCoordinates)

            
            # plt.figure(figsize=(8, 6))
            plt.scatter(clusteringCoordinates[:, 0], clusteringCoordinates[:, 1], color='blue', label='Movies from same genre')
            plt.scatter(clusteringCoordinates[0][0], clusteringCoordinates[0][1], color='red')
            # plt.annotate('User Movie', (clusteringCoordinates[0][0], clusteringCoordinates[0][1]), textcoords="offset points", xytext=(0, 10), ha='center')
            # print(clusteringCoordinates[0])
            

            # Applying KMeans on cluster coordinates created
            kmeans = KMeans(n_clusters = numClusters)
            kmeans.fit(clusteringCoordinates)
            clusterCenters = kmeans.cluster_centers_
            plt.scatter(clusterCenters[:, 0], clusterCenters[:, 1], color='red', marker='x', s=100, label='Cluster Centers')
            
            for i in range(numClusters):
                clusterPoints = clusteringCoordinates[kmeans.labels_ == i]
                plt.scatter(clusterPoints[:, 0], clusterPoints[:, 1], label=f'Cluster {i+1}')
            
            movieClusterNo = 0
            for i in range(numClusters):
                clusterIndices = np.where(kmeans.labels_ == i)[0]
                clusterPoints = clusteringCoordinates[clusterIndices]
                # print(clusterPoints)
                for j in clusterPoints:
                    if np.array_equal(clusteringCoordinates[0], j):
                        movieClusterNo = i

            # print(movieClusterNo + 1)
            clusterIndices = np.where(kmeans.labels_ == movieClusterNo)[0]
            clusterPoints = clusteringCoordinates[clusterIndices]
            moviesSelected = [allMovieIDs[i] for i in clusterIndices]
            # print(moviesSelected)
            # print(kmeans.labels_)

            # plt.title('K-Means Clustering')
            # plt.xlabel('X-coordinate')
            # plt.ylabel('Y-coordinate')
            # plt.legend()
            # plt.show()

            count = 0
            clusterMovieSynopsis = []
            userMovieSynopsis = []
            dbCursor.execute("SELECT MovieID, Synopsis, Title FROM movies WHERE MovieID = ?;", (movie, ))
            results = dbCursor.fetchall()
            userMovieSynopsis = results[0][1]
            # print([userMovieSynopsis])

            for clusterMovie in moviesSelected:
                count += 1
                dbCursor.execute("SELECT MovieID, Synopsis, Title FROM movies WHERE MovieID = ?;", (clusterMovie, ))
                results = dbCursor.fetchall()

                if count <= 1:
                    continue

                clusterMovieSynopsis = results[0][1]
                rawText = []
                rawText.append(userMovieSynopsis)
                rawText.append(clusterMovieSynopsis)
            
                tfidfVectorizer = TfidfVectorizer(stop_words = 'english')
                tfidfMatrix = tfidfVectorizer.fit_transform(rawText)
                # print(tfidfMatrix)

                cosineSimilarity = linear_kernel(tfidfMatrix, tfidfMatrix)
                # break

                if cosineSimilarity[0][1] > acceptingSimilarity:
                    # print(cosineSimilarity[0][1])
                    recommendedMovies.append(clusterMovie)
                
            # Testing to run once!
            # break;
        
        
        dbConnection.close()
        return recommendedMovies

def recommendMoviesOnLastWatched(userID):
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
    recommendedMovies = []
    userWatchedMovies = []
    X = 0
    Y = 0
    allRelativeRatings = []
    allAvgRatings = []
    allMovieIDs = []
    numClusters = 4
    acceptingSimilarity = 0.015
    #


    # Checking for cold start problem
    dbCursor.execute("SELECT isFirstTime FROM users WHERE id = ?;", (userID, ))
    coldStart = dbCursor.fetchall()
    coldStart = coldStart[0][0]


    # Model Implementation
    # Getting all movies user has watched
    dbCursor.execute("SELECT watchedMovies FROM users WHERE id = ?", (userID, ))
    userWatchedMovies = dbCursor.fetchall()
    userWatchedMovies = convertTupleToList(userWatchedMovies)
    print(userWatchedMovies.pop())
    movie = userWatchedMovies.pop()
    # iterating for each movie Collaborative then Content based filtering and generating recommendations based on each movie
    
    clusteringCoordinates = []

    # Getting the rating user has given to it
    dbCursor.execute("SELECT rating FROM user_rating WHERE userID = ? and movieID = ?", (userID, movie))
    userMovieRating = dbCursor.fetchall()
    userMovieRating = userMovieRating[0][0]
    X = userMovieRating

    # Getting the avg rating given to it
    dbCursor.execute("SELECT AvgVote FROM movies WHERE movieID = ?", (movie, ))
    userMovieAvgRating = dbCursor.fetchall()
    userMovieAvgRating = userMovieAvgRating[0][0]
    Y = userMovieAvgRating

    # Creating coordinate for user movie
    clusteringCoordinates.append((X, Y))
    allMovieIDs.append(movie)

    # Now, getting coordinates for all movies with similar genres
    dbCursor.execute("SELECT Genres FROM movies WHERE MovieID = ?", (movie, ))
    userMovieGenres = dbCursor.fetchall()
    userMovieGenres = convertTupleToList(userMovieGenres)
    # print(userMovieGenres)
    
    # Getting high rated movies for each genre
    dbCursor.execute("SELECT MovieID, Genres, Title, AvgVote, VoteCount FROM movies WHERE VoteCount > ? ORDER BY AvgVote DESC", (minimumVotes, ))
    results = dbCursor.fetchall()

    for genre in userMovieGenres:
        count = 0

        for row in results:
            moviesGenres = row[1].split(", ")

            # Getting highest rated n movies for the genre
            if set([genre]).issubset(set(moviesGenres)) and not(row[0] in userWatchedMovies) :
                allRelativeRatings.append(relativeRating(row[3], userMovieRating))
                allAvgRatings.append(row[3])
                allMovieIDs.append(row[0])

    # Creating coordinates for the choosen movies    
    for x in range(len(allRelativeRatings)):
        X = scaleRelativeRating(min(allRelativeRatings), max(allRelativeRatings), allRelativeRatings[x], 10)
        Y = allAvgRatings[x]
        clusteringCoordinates.append((X, Y))        
    
    # Converting coordinates from list of tuples to 2D numpy array
    clusteringCoordinates = np.array(clusteringCoordinates)

    
    # plt.figure(figsize=(8, 6))
    plt.scatter(clusteringCoordinates[:, 0], clusteringCoordinates[:, 1], color='blue', label='Movies from same genre')
    plt.scatter(clusteringCoordinates[0][0], clusteringCoordinates[0][1], color='red')
    # plt.annotate('User Movie', (clusteringCoordinates[0][0], clusteringCoordinates[0][1]), textcoords="offset points", xytext=(0, 10), ha='center')
    # print(clusteringCoordinates[0])
    

    # Applying KMeans on cluster coordinates created
    kmeans = KMeans(n_clusters = numClusters)
    kmeans.fit(clusteringCoordinates)
    clusterCenters = kmeans.cluster_centers_
    plt.scatter(clusterCenters[:, 0], clusterCenters[:, 1], color='red', marker='x', s=100, label='Cluster Centers')
    
    for i in range(numClusters):
        clusterPoints = clusteringCoordinates[kmeans.labels_ == i]
        plt.scatter(clusterPoints[:, 0], clusterPoints[:, 1], label=f'Cluster {i+1}')
    
    movieClusterNo = 0
    for i in range(numClusters):
        clusterIndices = np.where(kmeans.labels_ == i)[0]
        clusterPoints = clusteringCoordinates[clusterIndices]
        # print(clusterPoints)
        for j in clusterPoints:
            if np.array_equal(clusteringCoordinates[0], j):
                movieClusterNo = i

    # print(movieClusterNo + 1)
    clusterIndices = np.where(kmeans.labels_ == movieClusterNo)[0]
    clusterPoints = clusteringCoordinates[clusterIndices]
    moviesSelected = [allMovieIDs[i] for i in clusterIndices]
    # print(moviesSelected)
    # print(kmeans.labels_)

    # plt.title('K-Means Clustering')
    # plt.xlabel('X-coordinate')
    # plt.ylabel('Y-coordinate')
    # plt.legend()
    # plt.show()

    count = 0
    clusterMovieSynopsis = []
    userMovieSynopsis = []
    dbCursor.execute("SELECT MovieID, Synopsis, Title FROM movies WHERE MovieID = ?;", (movie, ))
    results = dbCursor.fetchall()
    userMovieSynopsis = results[0][1]
    # print([userMovieSynopsis])

    for clusterMovie in moviesSelected:
        count += 1
        dbCursor.execute("SELECT MovieID, Synopsis, Title FROM movies WHERE MovieID = ?;", (clusterMovie, ))
        results = dbCursor.fetchall()

        if count <= 1:
            continue

        clusterMovieSynopsis = results[0][1]
        rawText = []
        rawText.append(userMovieSynopsis)
        rawText.append(clusterMovieSynopsis)
    
        tfidfVectorizer = TfidfVectorizer(stop_words = 'english')
        tfidfMatrix = tfidfVectorizer.fit_transform(rawText)
        # print(tfidfMatrix)

        cosineSimilarity = linear_kernel(tfidfMatrix, tfidfMatrix)
        # break

        if cosineSimilarity[0][1] > acceptingSimilarity:
            # print(cosineSimilarity[0][1])
            recommendedMovies.append(clusterMovie)
        
    # Testing to run once!
    # break;


    dbConnection.close()
    return recommendedMovies


# Implementation #
# print("Recommended Movies: ", len(recommendMoives(4)))
# print(len(recommendMoviesOnLastWatched(4)))