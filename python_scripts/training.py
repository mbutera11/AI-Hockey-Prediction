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

home = []
away = []
home_wins = []
away_wins = []
home_streak = []
away_streak = []
home_b2b = []
away_b2b = []

winner = []

cursor.execute("SELECT * FROM LastYear_Games")
result = cursor.fetchall()

for x in result:
    home.append(x[0])
    away.append(x[1])
    home_wins.append(x[2])
    away_wins.append(x[3])
    home_streak.append(x[4])
    away_streak.append(x[5])
    home_b2b.append(x[6])
    away_b2b.append(x[7])

    winner.append(x[8])

features = list(zip(home, away, home_wins, away_wins, home_streak, away_streak, home_b2b, away_b2b))

model = KNeighborsClassifier(n_neighbors=3)
model.fit(features, winner)


cursor.execute("SELECT * FROM Games_ToDate")
result = cursor.fetchall()

randomGameIndex = random.randint(0, len(result))
randomGame = result[randomGameIndex]
predicted = model.predict([[randomGame[0],
                            randomGame[1],
                            randomGame[2],
                            randomGame[3],
                            randomGame[4],
                            randomGame[5],
                            randomGame[6],
                            randomGame[7]]])

print(randomGame)
cursor.execute("SELECT name FROM teams WHERE id = " + str(randomGame[0]))
homeTeam = cursor.fetchall()


cursor.execute("SELECT name FROM teams WHERE id = " + str(randomGame[1]))
awayTeam = cursor.fetchall()

for x in homeTeam:
    print(x)

print(" vs. ")

for y in awayTeam:
    print(y)

print("Estimated Answer: " + str(predicted))
print("Actual Answer: " + str(randomGame[8]))
