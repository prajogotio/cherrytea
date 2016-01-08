(function() {
	var state = {
		posting : false
	};

	$(document).ready(function(){
		state.proj_id = parseInt($('input[name="proj_id"]').first().val());
		$('#submit').click(function() {
			if (state.posting) return;
			state.posting = true;
			$.ajax({
				url:'http://'+location.host+'/ajax/post',
				method:'POST',
				data:{'proj_id':state.proj_id,
					  'title':$('#title').val(),
					  'entry':$('#entry').val()},
				beforeSend:function() {
					displayWaitingBox('Posting...');
				}
			}).done(function(msg) {
				if (msg.success){
					displayNotification("Post has been successfully published. Redirecting to project page...");
					setTimeout(function() {
						window.location.href = '/project/' + state.proj_id;
					}, 1500);
				}
			}).fail(function(msg) {
				displayNotification("Posting failed. Try again later.");
			}).always(function(msg) {
				closeWaitingBox();
			})
		});
	});

})();
