$(document).ready(function() {
	var proj_id = parseInt($('input[name="proj_id"]').first().val());
    var goal = parseFloat($('input[name="goal"]').first().val());
    var donated = parseFloat($('input[name="donated"]').first().val());
    var goalCovered = donated/goal*70;
    $('#money-gauge').css('width', goalCovered+'%');
    if (goalCovered > 70) {
        $('#money-gauge').css('background-color', '#fb1')
    }
})