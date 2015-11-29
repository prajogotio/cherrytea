(function($){
	var values = {};

	function announceError(msg){
		$('#login-panel-notification').html(msg);
	}

	$(document).ready(function(){
		$('#login-panel-submit-button').click(function(){
			announceError("");
			values.username = $('#login-panel-username-input').val().trim();
			values.password = $('#login-panel-password-input').val();
			if (values.username == "" || values.password == "") {
				announceError("username and password required!")
				return;
			}
			this.value = "Logging in...";
			$.ajax({
				'url': 'http://'+location.host+'/user_login',
				'data': values,
				'method': "POST"
			}).done(function(msg) {
				if (msg.success) {
					// go to home page
					console.log("success");
					location = '/';
				} else {
					console.log("fail");
					announceError("username or password are incorrect");
					$('#login-panel-submit-button').val("Login")
				}
			})
		});
	});
})(jQuery)