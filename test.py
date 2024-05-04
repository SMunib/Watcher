import sqlite3
import os

currentDir = os.getcwd()
dbFile = 'WatcherDB.db'
dbFolder = 'instance'

dbPath = os.path.join(currentDir, dbFolder)
dbPath = os.path.join(dbPath, dbFile)
dbConnection = sqlite3.connect(dbPath)
dbCursor = dbConnection.cursor()

###
row_count = 0
limit = 10
genre = ['Adventure', 'Action']
###

try:
    dbCursor.execute("SELECT MovieID, Title, AvgVote, VoteCount, Genres FROM movies WHERE VoteCount > 50 AND ProductionCountries = 'United States of America' ORDER BY AvgVote DESC;")
    results = dbCursor.fetchall()
    # dbConnection.commit()

    for row in results:
        if set(genre) <= set(row[4]):
            print(row)
            row_count += 1

        # if row_count >= limit:
        #     break
        
except sqlite3.Error as error:
    print("SQLite error: ", error)