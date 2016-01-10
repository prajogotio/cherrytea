(function($){
	var values = {};
	$(document).ready(function(){
		registerUploadPhotoCloudinary(values, 'proj_pic');
		$('#proj-pic-file').change(function(){
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
						$('#proj-pic-file-info').html("Uploading...");
					}
				}).done(function(msg){
					console.log('success', msg);
					values.proj_pic = msg.pic_id;
					$('#proj-pic-file-info').html("Project picture is uploaded!")
				}).fail(function(msg){
					console.log('fail', msg);
				})
			}
		});
		$('#submit-button').click(function() {
			values.proj_name = $('#proj-name-input').val();
			values.proj_desc = $('#proj-desc-input').val();
			values.category = $('#category-input').val();
			values.location = $('#location-input').val();
			values.other_info = $('#other-info-input').val();
			values.donation_goal = $('#donation-goal-input').val();
			values.charity_org = $('#charity-org-input').val();

			this.value = "Creating..."

			$.ajax({
				url:'http://'+location.host+'/create/project/submit',
				data:values,
				method:'POST'
			}).done(function(msg){
				console.log('success', msg);
				if (msg.success) {
					displayNotification("Project has been successfully created! Redirecting to the project profile...");
					setTimeout(function(){
						window.location.href = "/project/" + msg.proj_id;
					}, 1500);
				}
			}).fail(function(msg){
				console.log('fail', msg);
				// show failure
				displayNotification("Failed to create the project. Please try again later.");
			});
		});
	});
})(jQuery)

function registerUploadPhotoCloudinary(values, pic_id) {
	$('.form-upload').append($.cloudinary.unsigned_upload_tag("i9hka0um",  { cloud_name: 'ddkd4u5ja' }));
	$('.form-upload input').first().bind('cloudinarydone', function(e, data) {
		$('#form-upload-info').html('Uploaded!');
		$.ajax({
			url:'http://'+location.host+'/store/pic',
			method:'POST',
			data:{'pic_url':data.result.secure_url}
		}).done(function(msg) {
			values[pic_id] = msg.pic_id;
		});
	}).bind('cloudinaryprogress', function(e, data) { 
	  $('#form-upload-info').html('Uploading: ' +  
	    Math.round((data.loaded * 100.0) / data.total) + '%'); 
	});;
}