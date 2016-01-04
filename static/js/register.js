(function() {

var step = 0;
var values = {};

function display(d) {
	$(d).css('display','block');
	setTimeout(function(){ $(d).css({
		'opacity': '1',
		'top': '0'})}, 100);
}

function hide(d) {
	$(d).css('display', 'none');
}

$(document).ready(function() {

	display('#regform-user-type');

	$('#org-choice').click(function() {
		values.user_type = 'org';
		hide('#regform-user-type');
		display('#regform-user-pass');
	});

	$('#person-choice').click(function() {
		values.user_type = 'ind';
		hide('#regform-user-type');
		display('#regform-user-pass');
	});

	$('#regform-user-pass-next-button').click(function(){
	    var checksPassed = true;
        var pass_err = $('#regform-password-match-error');
        var filled_err = $('#regform-user-pass-error');

	    if (!checkInputsFilled('regform-user-pass')){
            setVisible(filled_err, true);
            checksPassed = false;
            }
        else
            setVisible(filled_err, false);

        if (!passwordsMatch($('#regform-password-input').val(),
                            $('#regform-password-conf-input').val())){

            setVisible(pass_err, true);
            checksPassed = false;
            }
        else
            setVisible(pass_err, false);

        if (checksPassed){
            values.username = $('#regform-username-input').val();
            values.password = $('#regform-password-input').val();
            hide('#regform-user-pass');
            display('#regform-verif');
        }
	});

/*
	$('#regform-password-conf-input').keyup(function(e) {
        if ($('#regform-password-input').val().length == this.value.length) {
		    $('#regform-user-pass-next').css({'visibility': 'visible'});
			setTimeout(function(){
				$('#regform-user-pass-next').css({'opacity': '1'});
			}, 100);
		    }
		else {
			$('#regform-user-pass-next').css({'visibility': 'hidden',
												 'opacity': '0'});
		}
	});
	*/

	$('#regform-verif-next-button').click(function(){
	    var checksPassed = true;
	    var filled_err = $('#regform-verif-error');

        if (!checkInputsFilled('regform-verif')){
            setVisible(filled_err, true);
            checksPassed = false;
        }
        else
            setVisible(filled_err, false);

	    if (checksPassed){
            values.email = $('#regform-email-input').val();
            values.charity_number = $('#regform-char-num-input').val();

            createUserAccount(values);

            hide('#regform-verif');
            display('#regform-done');
		}
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

function checkInputsFilled(page_id){
    //Check all inputs that are child of #page_id
    var success = true;
    var inputs = $('#'+page_id + " .transparent-input");

    inputs.each(function(){
        if (this.value.trim() == "")
            success = false;
    });
    return success;
}

function setVisible(jq, set){
    if (!set) {
        jq.css('display', 'none');
        setTimeout(function(){
            jq.css({
                'opacity' : '0',
                'visibility' : 'hidden'});
        }, 100);

        }
    else {
        jq.css('display', 'block');
        setTimeout(function(){
            jq.css({
                'opacity' : '1',
                'visibility' : 'visible'});
        }, 100);
    }
}

function passwordsMatch(text1, text2){
    if (text1 == text2)
        return true;
    else
        return false;
}

})()