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
		values.user_type = 'org';
		hide('#regform-user-type');
		display('#regform-user-pass');
	});

	$('#person-choice').click(function() {
		values.user_type = 'ind';
		hide('#regform-user-type');
		display('#regform-user-pass');
	})

	$('#regform-user-pass-next-button').click(function(){
		values.username = $('#regform-username-input').val();
		values.password = $('#regform-password-input').val();
		hide('#regform-user-pass');
		display('#regform-verif');
	});

	$('#regform-password-conf-input').keyup(function(e) {
		if ($('#regform-username-input').val().trim() != ""
		    && $('#regform-password-input').val() == this.value) {
			$('#regform-user-pass-next').css({'visibility': 'visible'});
			setTimeout(function(){
				$('#regform-user-pass-next').css({'opacity': '1'});
			}, 100)
		} else {
			$('#regform-user-pass-next').css({'visibility': 'hidden',
												 'opacity': '0'});
		}
	});

	$('#regform-verif-next-button').click(function(){
		values.email = $('#regform-email-input').val();
		values.charity_number = $('#regform-char-num-input').val();

		createUserAccount(values);

		hide('#regform-verif');
		display('#regform-done');
	});

});

function createUserAccount(values) {
	$.ajax({
		url: 'http://'+location.host+'/create_user',
		data: values,
		method: 'POST'
	}).done(function(msg) {
		console.log(msg);
	}).fail(function(msg) {
		console.log(msg);
	});
}


})()