import mysql.connector
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import svm
import graphviz


def predictionAccuracy():
    home_wins = []
    away_wins = []
    home_streak = []
    away_streak = []
    home_b2b = []
    away_b2b = []

    winner = []
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="hockey",
        port=3307
    )
    cursor = db.cursor()

    # select all games from db
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

    # model = KNeighborsClassifier(n_neighbors=3)
    # model.fit(features, winner)

    model = tree.DecisionTreeClassifier()
    model.fit(features, winner)

    # model = svm.SVC(kernel='linear')
    # model.fit(features, winner)

    cursor.execute("SELECT * FROM Games_ToDate")
    result = cursor.fetchall()
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

    accuracy = correct / total

    print("Accuracy: " + str(accuracy))


def trainTestSplit():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="hockey",
        port=3307
    )
    cursor = db.cursor()

    cursor.execute("SELECT * FROM LastYear_Games");
    result = cursor.fetchall()

    features = []
    target = []

    for y in result:
        features.append([y[2], y[3], y[4], y[5], y[6], y[7]])
        target.append(y[8])

    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.3)

    # model = KNeighborsClassifier(n_neighbors=3)
    # model.fit(x_train, y_train)

    model = tree.DecisionTreeClassifier()
    model.fit(x_train, y_train)

    data = tree.export_graphviz(model, out_file=None)
    graph = graphviz.Source(data)
    graph.render("hockey")


    # model = svm.SVC(kernel='linear')
    # model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    print("Score: " + str(model.score(x_test, y_test)))


def predictRandomGame():
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

    # select all games from db
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

    # model = KNeighborsClassifier(n_neighbors=3)
    # model.fit(features, winner)

    model = tree.DecisionTreeClassifier()
    model.fit(features, winner)

    # model = svm.SVC(kernel='linear')
    # model.fit(features, winner)

    cursor.execute("SELECT * FROM Games_ToDate")
    result = cursor.fetchall()
    randomGameIndex = random.randint(0, len(result))
    randomGame = result[randomGameIndex]

    predicted = model.predict([[randomGame[2],
                                randomGame[3],
                                randomGame[4],
                                randomGame[5],
                                randomGame[6],
                                randomGame[7]]])

    print(randomGame)
    cursor.execute("SELECT name FROM teams WHERE id = " + str(randomGame[0]))
    homeTeam = cursor.fetchone()

    cursor.execute("SELECT name FROM teams WHERE id = " + str(randomGame[1]))
    awayTeam = cursor.fetchone()

    print("Game: " + homeTeam[0] + " vs. " + awayTeam[0])

    print("Estimated Answer: " + str(predicted))
    print("Actual Answer: " + str(randomGame[8]))
