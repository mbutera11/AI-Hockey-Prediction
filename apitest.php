<?php
    include "functions.php";
?>

<!DOCTYPE HTML>
<html>
<head>
    <title>Testing API...</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no"/>
    <link rel="stylesheet" href="assets/css/main.css"/>
</head>
<body class="subpage">
<div id="page-wrapper">

    <!-- Header -->
    <section id="header">
        <?php include "menuBar.php"; ?>
    </section>

    <!-- Content -->
    <section id="content">
        <div class="container">
            <div class="row">
                <div class="col-12">

                    <!-- Main Content -->
                    <section>
                        <header>
                            <h2>Getting Info</h2>
                        </header>

                        <p>
                            <?php
                                $conn = getConnection();

                                $url = "https://statsapi.web.nhl.com/api";
                                $next_game = "/v1/teams/18/?expand=team.schedule.next";
                                $team_stats = "/v1/teams/18/?expand=team.stats";
                                $all_games_lastYear = "/v1/schedule?startDate=2017-10-04&endDate=2018-04-10";

                                $todayDate = date('Y-m-d');
                                $all_games_today = "/v1/schedule?startDate=".$todayDate."&endDate=".$todayDate;

                                $all_games_5Years = "/v1/schedule?startDate=2013-10-01&endDate=2018-04-10";

                                $yesterdayDate = date('Y-m-d',strtotime("-1 days"));
                                $all_games_yesterday = "/v1/schedule?startDate=2018-10-03&endDate=".$yesterdayDate;

                                $jsonString = file_get_contents($url.$all_games_5Years);
                                echo prettyPrint($jsonString);

                            ?>
                        </p>

                    </section>

                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <section id="footer">
        <div class="container">
            <div class="row">
                <div class="col-8 col-12-medium">

                    <!-- Links -->
                    <section>
                        <h2>Links to Important Stuff</h2>
                        <div>
                            <div class="row">
                                <div class="col-3 col-12-small">
                                    <ul class="link-list last-child">
                                        <li><a href="#">Neque amet dapibus</a></li>
                                        <li><a href="#">Sed mattis quis rutrum</a></li>
                                        <li><a href="#">Accumsan suspendisse</a></li>
                                        <li><a href="#">Eu varius vitae magna</a></li>
                                    </ul>
                                </div>
                                <div class="col-3 col-12-small">
                                    <ul class="link-list last-child">
                                        <li><a href="#">Neque amet dapibus</a></li>
                                        <li><a href="#">Sed mattis quis rutrum</a></li>
                                        <li><a href="#">Accumsan suspendisse</a></li>
                                        <li><a href="#">Eu varius vitae magna</a></li>
                                    </ul>
                                </div>
                                <div class="col-3 col-12-small">
                                    <ul class="link-list last-child">
                                        <li><a href="#">Neque amet dapibus</a></li>
                                        <li><a href="#">Sed mattis quis rutrum</a></li>
                                        <li><a href="#">Accumsan suspendisse</a></li>
                                        <li><a href="#">Eu varius vitae magna</a></li>
                                    </ul>
                                </div>
                                <div class="col-3 col-12-small">
                                    <ul class="link-list last-child">
                                        <li><a href="#">Neque amet dapibus</a></li>
                                        <li><a href="#">Sed mattis quis rutrum</a></li>
                                        <li><a href="#">Accumsan suspendisse</a></li>
                                        <li><a href="#">Eu varius vitae magna</a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </section>

                </div>
                <div class="col-4 col-12-medium imp-medium">

                    <!-- Blurb -->
                    <section>
                        <h2>An Informative Text Blurb</h2>
                        <p>
                            Duis neque nisi, dapibus sed mattis quis, rutrum accumsan sed. Suspendisse eu
                            varius nibh. Suspendisse vitae magna eget odio amet mollis. Duis neque nisi,
                            dapibus sed mattis quis, sed rutrum accumsan sed. Suspendisse eu varius nibh
                            lorem ipsum amet dolor sit amet lorem ipsum consequat gravida justo mollis.
                        </p>
                    </section>

                </div>
            </div>
        </div>
    </section>

    <!-- Copyright -->
    <div id="copyright">
        &copy; Untitled. All rights reserved. | Design: <a href="http://html5up.net">HTML5 UP</a>
    </div>

</div>

<!-- Scripts -->
<script src="assets/js/jquery.min.js"></script>
<script src="assets/js/browser.min.js"></script>
<script src="assets/js/breakpoints.min.js"></script>
<script src="assets/js/util.js"></script>
<script src="assets/js/main.js"></script>

</body>
</html>

