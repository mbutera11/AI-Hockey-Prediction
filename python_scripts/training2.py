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
# away = []
team_wins = []
opp_wins = []
team_streak = []
opp_streak = []
team_b2b = []
opp_b2b = []

winner = []

# select all predators games from db
cursor.execute("SELECT * FROM LastYear_Games WHERE home_id = 18 or away_id = 18");
result = cursor.fetchall()

# cursor.execute("SELECT * FROM LastYear_Games")
# result = cursor.fetchall()

for x in result:
    # if team is home
    if x[0] == 18:
        home.append(1)
        team_wins.append(x[2])
        opp_wins.append(x[3])
        team_streak.append(x[4])
        opp_streak.append(x[5])
        team_b2b.append(x[6])
        opp_b2b.append(x[7])
        if x[8] == 1:
            # team wins
            winner.append(1)
        else:
            # team loses
            winner.append(0)

    # if team is away
    else:
        home.append(0)
        team_wins.append(x[3])
        opp_wins.append(x[2])
        team_streak.append(x[5])
        opp_streak.append(x[4])
        team_b2b.append(x[7])
        opp_b2b.append(x[6])
        if x[8] == 1:
            # team loses
            winner.append(0)
        else:
            # team wins
            winner.append(1)

    # home.append(x[0])
    # away.append(x[1])
    # team_wins.append(x[2])
    # opp_wins.append(x[3])
    # team_streak.append(x[4])
    # opp_streak.append(x[5])
    # team_b2b.append(x[6])
    # opp_b2b.append(x[7])
    # winner.append(x[8])

# features = list(zip(home, away, home_wins, away_wins, home_streak, away_streak, home_b2b, away_b2b))
features = list(zip(home, team_wins, opp_wins, team_streak, opp_streak, team_b2b, opp_b2b))

model = KNeighborsClassifier(n_neighbors=3)
model.fit(features, winner)


cursor.execute("SELECT * FROM Games_ToDate WHERE home_id = 18 or away_id = 18")
result = cursor.fetchall()

randomGameIndex = random.randint(0, len(result))
randomGame = result[randomGameIndex]

randomGameValues = []

# if team is home
if randomGame[0] == 18:
    randomGameValues.append(1)
    randomGameValues.append(randomGame[2])
    randomGameValues.append(randomGame[3])
    randomGameValues.append(randomGame[4])
    randomGameValues.append(randomGame[5])
    randomGameValues.append(randomGame[6])
    randomGameValues.append(randomGame[7])

    if randomGame[8] == 1:
        # team wins
        randomGameValues.append(1)
    else:
        # team loses
        randomGameValues.append(0)

# if team is away
else:
    randomGameValues.append(0)
    randomGameValues.append(randomGame[3])
    randomGameValues.append(randomGame[2])
    randomGameValues.append(randomGame[5])
    randomGameValues.append(randomGame[4])
    randomGameValues.append(randomGame[7])
    randomGameValues.append(randomGame[6])

    if randomGame[8] == 1:
        # team loses
        randomGameValues.append(0)
    else:
        # team wins
        randomGameValues.append(1)

predicted = model.predict([[randomGameValues[0],
                            randomGameValues[1],
                            randomGameValues[2],
                            randomGameValues[3],
                            randomGameValues[4],
                            randomGameValues[5],
                            randomGameValues[6]]])

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
print("Actual Answer: " + str(randomGameValues[7]))
