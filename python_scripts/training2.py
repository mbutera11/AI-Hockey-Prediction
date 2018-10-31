import mysql.connector
import random
from sklearn.neighbors import KNeighborsClassifier

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="hockey",
    port=3307
)
cursor = db.cursor()

home_wins = []
away_wins = []
home_streak = []
away_streak = []
home_b2b = []
away_b2b = []

winner = []

# select all predators games from db
cursor.execute("SELECT * FROM Games_Last5Years");
result = cursor.fetchall()

for x in result:
    home_wins.append(x[2])
    away_wins.append(x[3])
    home_streak.append(x[4])
    away_streak.append(x[5])
    home_b2b.append(x[6])
    away_b2b.append(x[7])

    winner.append(x[8])

features = list(zip(home_wins, away_wins, home_streak, away_streak, home_b2b, away_b2b))

model = KNeighborsClassifier(n_neighbors=3)
model.fit(features, winner)


cursor.execute("SELECT * FROM Games_ToDate")
result = cursor.fetchall()

# -------------- predict random game -----------------------

# randomGameIndex = random.randint(0, len(result))
# randomGame = result[randomGameIndex]
#
# predicted = model.predict([[randomGame[2],
#                             randomGame[3],
#                             randomGame[4],
#                             randomGame[5],
#                             randomGame[6],
#                             randomGame[7]]])
#
# print(randomGame)
# cursor.execute("SELECT name FROM teams WHERE id = " + str(randomGame[0]))
# homeTeam = cursor.fetchone()
#
#
# cursor.execute("SELECT name FROM teams WHERE id = " + str(randomGame[1]))
# awayTeam = cursor.fetchone()
#
# print("Game: " + homeTeam[0] + " vs. " + awayTeam[0])
#
# print("Estimated Answer: " + str(predicted))
# print("Actual Answer: " + str(randomGame[8]))


# get prediction accuracy
total = len(result)
correct = 0

for y in result:
    predicted = model.predict([[y[2],
                                y[3],
                                y[4],
                                y[5],
                                y[6],
                                y[7]]])
    if str(predicted[0]) == str(y[8]):
        correct += 1

accuracy = correct/total

print("Accuracy: " + str(accuracy))
