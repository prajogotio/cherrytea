(function($){
	var values = {};
	$(document).ready(function(){
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
					$('#proj-pic-file-info').html("Project picture uploaded!")
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
			values.other_info = $('#other-info-input').html();
			values.donation_goal = $('#donation-goal-input').val();
			values.charity_org = $('#charity-org-input').val();

			this.value = "Creating..."

			$.ajax({
				url:'http://'+location.host+'/create_project_submission',
				data:values,
				method:'POST'
			}).done(function(msg){
				console.log('success', msg);
			}).fail(function(msg){
				console.log('fail', msg);
			});
		});
	});
})(jQuery)