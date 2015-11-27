(function() {

var step = 0;
var values = {};

function display(d) {
	$(d).css('display','block');
	setTimeout(function(){ $(d).css('opacity', '1'); }, 100);
}

function hide(d) {
	$(d).css('display', 'none');
}

$(document).ready(function() {

	$('#org-choice').click(function() {
		values.userType = 'org';
		hide('#regform-user-type');
		display('#regform-user-pass');
	});

	$('#person-choice').click(function() {
		values.userType = 'ind';
		hide('#regform-user-type');
		display('#regform-user-pass');
	})

	$('#regform-user-pass-next-button').click(function(){
		hide('#regform-user-pass');
		display('#regform-verif');
	});

	$('#regform-verif-next-button').click(function(){
		hide('#regform-verif');
		display('#regform-done');
	})

});


})()