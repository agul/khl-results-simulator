/*
	KHL Matches Results Parser
	
	Parsing results from page https://www.icehockey24.com/russia/khl-2020-2021/results/
	Before run from the developers console expand all results by clicking "Show more matches v"

*/


var season_results = []
$(".event__match").each(function(index) {
    var match = $(this);
    var date_time = match.find(".event__time").first().text();
    const home_team = match.find(".event__participant--home").first().text();
    const away_team = match.find(".event__participant--away").first().text();
    const home_score = match.find(".event__score--home").first().text();
    const away_score = match.find(".event__score--away").first().text();
    const ot_so = match.find(".event__stage");
    var ot = false;
    var so = false;
    if (ot_so.length) {
        var value = ot_so.first().text();
        ot = (value == "AOT");
        so = (value == "Pen");
        date_time = date_time.slice(0, -3);  // remove AOT or Pen
    }
    const match_info = {
        "datetime": date_time,
       	"home": home_team,
        "away": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "ot": ot,
        "so": so
    };
    season_results.push(match_info);
});

JSON.stringify(season_results);
