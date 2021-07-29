// parse KHL calendar from https://www.khl.ru/calendar/

calendar = []
$(".b-wide_tile_item").each(function() {
	var clubs = $(this).find(".m-club");
	var home = clubs.first().find(".e-club_name").text();
	var away = clubs.last().find(".e-club_name").text();

	calendar.push({"home": home, "away": away});
});
console.log(JSON.stringify(calendar));