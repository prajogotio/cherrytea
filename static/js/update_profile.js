(function($){
	var values = {};
	$(document).ready(function(){
		$('#prof_pic').change(function(){
			if (this.files.length > 0){
				var f = this.files[0];
				var formData = new FormData();
				formData.append('file', f);
				$.ajax({
					url:'http://'+location.host+'/upload',
					data: formData,
					method: 'POST',
					contentType:false,
					processData:false,
					beforeSend: function() {
						$('#prof_pic_info').html("Uploading...");
					}
				}).done(function(msg){
					console.log('success', msg);
					values.profile_pic_id = msg.pic_id;
					$('#prof_pic_info').html("Profile picture is uploaded!")
				}).fail(function(msg){
					console.log('fail', msg);
				})
			}
		});
		$('#submit').click(function() {
			values.first_name = $('#first_name').val();
			values.last_name = $('#last_name').val();
			values.advocate = $('#advocate').val();
			values.address = $('#address').val();
			values.bio = $('#bio').val();
			values.date_of_birth = $('#date_of_birth').val();

			this.value = "Updating..."

			$.ajax({
				url:'http://'+location.host+'/update/user_profile/submit',
				data:values,
				method:'POST'
			}).done(function(msg){
				console.log('success', msg);
				displayNotification("Profile is updated!")
			}).fail(function(msg){
				console.log('fail', msg);
			}).always(function(msg){
				$('#submit').attr('value', "update");
			});
		});
	});
})(jQuery)