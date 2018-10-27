<?php

//    $next_game = "/v1/teams/18/?expand=team.schedule.next";
//    $team_stats = "/v1/teams/18/?expand=team.stats";
//    $all_games = "/v1/schedule?startDate=2017-10-04&endDate=2018-04-04";


    // helps with pushing value to associative arrays used in insertLastYearGames()
    function array_push_assoc($array, $key, $value){
        $array[$key] = $value;
        return $array;
    }

    // returns connection to hockey db
    function getConnection() {
        $host = "localhost";
        $username = "root";
        $pass = "";
        $db = "hockey";

        $connection = mysqli_connect($host, $username, $pass, $db);

        return $connection;

    }

    // insert current teams to db
    function insertTeams() {
        $conn = getConnection();

        $url = "https://statsapi.web.nhl.com/api";

        $jsonString = file_get_contents($url);
        $jsonObject = json_decode($jsonString);

        $sql = "INSERT INTO teams VALUES ";
        for($i = 0; $i < sizeof($jsonObject->teams); $i++) {
            $sql .= "(".$jsonObject->teams[$i]->id.", '".$jsonObject->teams[$i]->name."', '".$jsonObject->teams[$i]->abbreviation."', '".$jsonObject->teams[$i]->locationName."', '".$jsonObject->teams[$i]->conference->name."', '".$jsonObject->teams[$i]->division->name."'),";
        }
        $sql = substr($sql, 0, -1).";";

        $conn -> query($sql);
    }

    // insert training data from last years hockey games
    function insertLastYearGames() {

        $conn = getConnection();

        $url = "https://statsapi.web.nhl.com/api";
        $all_games = "/v1/schedule?startDate=2017-10-04&endDate=2018-04-04";

        $jsonString = file_get_contents($url.$all_games);
        $jsonObject = json_decode($jsonString);
        $sql = "INSERT INTO LastYear_Games VALUES ";
        $jsonObject = $jsonObject -> dates;

        // populate associative array of win streaks for teams
        $streakArray = array();
        $dayBeforeGames = array();
        $dayOfGames = array();
        $teams_from_db = $conn -> query("SELECT name FROM teams");
        while($row = $teams_from_db -> fetch_assoc()) {
            $streakArray = array_push_assoc($streakArray, $row['name'], 0);
            $dayBeforeGames = array_push_assoc($dayBeforeGames, $row['name'], 0);
            $dayOfGames = array_push_assoc($dayOfGames, $row['name'], 0);
        }

        // loop through json object of all games from last year
        foreach($jsonObject as $key => $item) {
            $date = $item->date;

            // move values from dayOfGames to dayBeforeGames
            // the make all day of games 0
            foreach($dayOfGames as $key => $value) {
                $dayBeforeGames[$key] = $value;
                $dayOfGames[$key] = 0;
            }

            for($i = 0; $i < sizeof($item->games); $i++) {
                // store home and away teams
                $home = $item->games[$i]->teams->home->team->name;
                $away = $item->games[$i]->teams->away->team->name;

                // loop through day of games and update values to 1 of teams playing
                foreach($dayOfGames as $key => $value) {
                    if(strcmp($value, $home) == 0) {
                        $dayOfGames[$key] = 1;
                    }elseif(strcmp($key, $away) == 0) {
                        $dayOfGames[$key] = 1;
                    }
                }

                // ignore games from all star weekend
                if(strcmp($home, "Team Pacific") == 0 || strcmp($home, "Team Atlantic") == 0 ||
                    strcmp($home, "Team Metropolitan") == 0 || strcmp($home, "Team Central") == 0) {
                    continue;
                }

                // score of the game to determine winner
                $homeScore = $item->games[$i]->teams->home->score;
                $awayScore = $item->games[$i]->teams->away->score;

                // store current streaks for teams
                $homeStreak = $streakArray[$home];
                $awayStreak = $streakArray[$away];

                // determine winner and store winner
                // store wins for home and away teams
                // winning team is wins -1 because api store wins based on outcome of current game
                if($homeScore > $awayScore) {
                    $winner = $home;

                    // update streaks for both teams
                    $streakArray[$winner]++;
                    $streakArray[$away] = 0;
                    $home_wins = $item->games[$i]->teams->home->leagueRecord->wins - 1;
                    $away_wins = $item->games[$i]->teams->away->leagueRecord->wins;
                } else {
                    $winner = $away;

                    // update streaks for both teams
                    $streakArray[$winner]++;
                    $streakArray[$home] = 0;
                    $away_wins = $item->games[$i]->teams->away->leagueRecord->wins - 1;
                    $home_wins = $item->games[$i]->teams->home->leagueRecord->wins;
                }
                // add game states to sql for insert
                $sql .= "('".$home."', '".$away."', ".$home_wins.", ".$away_wins.", ".$homeStreak.", ".$awayStreak.", ".$dayBeforeGames[$home].", ".$dayBeforeGames[$away].", '".$winner."', '".$date."'),";
            }
        }
        // replace last comma with a semicolon
        $sql = substr($sql, 0, -1).";";

        // insert to db
        $conn -> query($sql);
    }

    function prettyPrint($jsonString) {

        $jsonObject = json_decode($jsonString);

        return "<pre>".json_encode($jsonObject, JSON_PRETTY_PRINT)."</pre>";
    }




?>