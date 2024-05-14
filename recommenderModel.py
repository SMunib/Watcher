import os
import json
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


class Trainer:

    def __init__(self, settingsPath):
        self.settingsFilePath = settingsPath

        with open(self.settingsFilePath, 'r') as settings:
            data = json.load(settings)

        self.minVotes = data["minVotes"] 
        self.minAvgRating = data["minAvgRating"] 
        self.clustersNo = data["clustersNo"] 
        self.acceptingSimilarity = data["acceptingSimilarity"]
        

    def saveSettings(self):
        data = {
                "minVotes": self.minVotes,
                "minAvgRating": self.minAvgRating,
                "clustersNo": self.clustersNo,
                "acceptingSimilarity": self.acceptingSimilarity
            }

        with open(self.settingsFilePath, "w") as settings:
            json.dump(data, settings)

    def fit(self, cursor, userID):
        watchedMovies = []
        recommendedMoives = []
        movieCount = 0
        ratingSum = 0

        cursor.execute("SELECT watchedMovies FROM users WHERE id = ?", (userID, ))
        results = cursor.fetchall()
        watchedMovies = convertTupleToList(results)
        
        cursor.execute("SELECT recommendedMovies FROM users WHERE id = ?", (userID, ))
        results = cursor.fetchall()
        recommendedMoives = convertTupleToList(results)

        for movie in recommendedMoives:
            if set([movie]).issubset(set(watchedMovies)):
                cursor.execute("SELECT AvgVote FROM movies WHERE movieID = ?", (movie, ))
                results = cursor.fetchall()

                ratingSum = ratingSum + results[0][0]
                movieCount += 1
        
        accuracy = (ratingSum / movieCount)

        if accuracy < self.minAvgRating and (self.minAvgRating - accuracy) < 1:
            self.minAvgRating += 0.2
        elif accuracy < self.minAvgRating and (self.minAvgRating - accuracy) > 1:
            self.minAvgRating += 0.4
            self.acceptingSimilarity += 0.01
        elif accuracy > self.minAvgRating and (accuracy - self.minAvgRating) < 1:
            self.minAvgRating -= 0.2
            self.acceptingSimilarity -= 0.002
        elif accuracy > self.minAvgRating and (accuracy - self.minAvgRating) > 1:
            self.minAvgRating -= 0.4
            self.acceptingSimilarity -= 0.004

        self.saveSettings()


# Helping functions to manipulate data
def convertTupleToList(tuple):
    List = tuple[0][0]
    List = List.split(', ')
    return List

def convertTupleToString(tuple):
    Str = tuple[0][0]
    Str = Str.replace("'", "")
    return Str

def convertListToString(list):
    string = ', '.join(str(num) for num in list)
    return string

def relativeRating(avg, userrating):
    xRelative = avg - userrating
    return xRelative

def scaleRelativeRating(minRR, maxRR, relativeRating, scaler = 10):
    xScaled = ((relativeRating - minRR) / (maxRR - minRR)) * scaler
    return xScaled


# AI Model
def recommendMovies(userID):
    # Determining directory for accesing WatcherDB.db in /instance folder
    currentDir = os.getcwd()
    dbSettings = 'dbSettings.json'
    dbFile = 'WatcherDB.db'
    dbFolder = 'instance'
    dbPath = os.path.join(currentDir, dbFolder)
    dbPath = os.path.join(dbPath, dbFile)
    settingsPath = os.path.join(currentDir, dbFolder)
    settingsPath = os.path.join(settingsPath, dbSettings)
    
    # Establishing DB connection
    try:
        dbConnection = sqlite3.connect(dbPath)
        dbCursor = dbConnection.cursor()

    except sqlite3.Error as error:
        return 'Database connection failed!'
    
    trainer = Trainer(settingsPath)
    trainer.fit(dbCursor, userID)

    # Variables needed by model
    coldStart = None
    minAVColdStart = 7.5
    minNumMoviesColdStart = 10
    minimumVotes = trainer.minVotes
    numClusters = trainer.clustersNo
    acceptingSimilarity = trainer.acceptingSimilarity
    minAvgVote = trainer.minAvgRating
    X = 0
    Y = 0
    recommendedMovies = []
    userWatchedMovies = []
    allRelativeRatings = []
    allAvgRatings = []
    allMovieIDs = []
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
            
            recommendedMovies = list(set(recommendedMovies))
            dbCursor.execute("UPDATE users SET recommendedMovies = ? WHERE id = ?", (convertListToString(recommendedMovies), userID))
            dbConnection.commit()
            return list(set(recommendedMovies))
        else:
            return list(set(recommendedMovies))
    
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
                    if set([genre]).issubset(set(moviesGenres)) and not(row[0] in userWatchedMovies) and row[3] > minAvgVote:
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

        recommendedMovies = list(set(recommendedMovies))
        dbCursor.execute("UPDATE users SET recommendedMovies = ? WHERE id = ?", (convertListToString(recommendedMovies), userID))
        dbConnection.commit()
        dbConnection.close()
        # convertListToString(recommendedMovies)
        # print(recommendedMovies)
        return list(set(recommendedMovies))

def recommendMoviesOnLastWatched(userID):
    # Determining directory for accesing WatcherDB.db in /instance folder
    currentDir = os.getcwd()
    dbSettings = 'dbSettings.json'
    dbFile = 'WatcherDB.db'
    dbFolder = 'instance'
    dbPath = os.path.join(currentDir, dbFolder)
    dbPath = os.path.join(dbPath, dbFile)
    settingsPath = os.path.join(currentDir, dbFolder)
    settingsPath = os.path.join(settingsPath, dbSettings)

    # Establishing DB connection
    try:
        dbConnection = sqlite3.connect(dbPath)
        dbCursor = dbConnection.cursor()

    except sqlite3.Error as error:
        return 'Database connection failed!'
    
    trainer = Trainer(settingsPath)
    trainer.fit(dbCursor, userID)

    # Variables needed by model
    minimumVotes = trainer.minVotes
    minAvgVote = trainer.minAvgRating
    numClusters = trainer.clustersNo
    acceptingSimilarity = trainer.acceptingSimilarity
    X = 0
    Y = 0
    recommendedMovies = []
    userWatchedMovies = []
    allRelativeRatings = []
    allAvgRatings = []
    allMovieIDs = []
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
            if set([genre]).issubset(set(moviesGenres)) and not(row[0] in userWatchedMovies) and row[3] > minAvgVote:
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
    recommendedMovies = list(set(recommendedMovies))
    dbCursor.execute("UPDATE users SET lastMovieRecommendations = ? WHERE id = ?", (convertListToString(recommendedMovies), userID))
    dbConnection.commit()
    dbConnection.close()
    return list(set(recommendedMovies))









############################## TESTING AND IMPLEMENTATION ##############################
# print("Recommended Movies: ", recommendMovies(4))
# print("No. Movies: ", len(recommendMoives(4)))
# recommendMoviesOnLastWatched(4)

# currentDir = os.getcwd()
# dbFile = 'WatcherDB.db'
# dbSettings = 'dbSettings.json'
# dbFolder = 'instance'
# dbPath = os.path.join(currentDir, dbFolder)
# dbPath = os.path.join(dbPath, dbFile)
# settingsPath = os.path.join(currentDir, dbFolder)
# settingsPath = os.path.join(settingsPath, dbSettings)

# minVotes = 40

# data = {
#     "minVotes": 50,
#     "minAvgRating": 7.0,
#     "clustersNo": 4,
#     "acceptingSimilarity": 0.015
# }

# with open(settingsPath, "w") as settings:
#     json.dump(data, settings)

# # Establishing DB connection
# try:
#     dbConnection = sqlite3.connect(dbPath)
#     dbCursor = dbConnection.cursor()

# except sqlite3.Error as error:
#     print('Database connection failed!')

# t = Trainer(settingsPath)
# print(t.minAvgRating, t.acceptingSimilarity)
# t.fit(dbCursor, 4)
# print(t.minAvgRating, t.acceptingSimilarity)