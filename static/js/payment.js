(function(){
	var state = {
		inProcess : false
	};

	$(document).ready(function(){
		$('#payment-confirm').click(function(){
			if (state.inProcess) return;
			state.inProcess = true;
			var donation = $('#payment-amount').val();
			$.ajax({
				url: 'http://' + location.host + '/record/donation',
				data: {'proj_id':parseInt($('input[name="proj_id"]').first().val()),
					   'donation_amount':$('#payment-amount').val()},
				method: 'POST',
				beforeSend: function() {
					displayNotification("Donation is being processed...");
					displayWaitingBox();
				}
			}).done(function(msg){
				console.log('success', msg);
				displayNotification("Donation is successfully processed!");
				if (msg.success) {
					$('#completed-screen').show();
				}
			}).fail(function(msg){
				console.log('fail', msg);
				displayNotification("Payment failed. Please try again later.");

			}).always(function(msg) {
				closeWaitingBox();
			});
		});
	});
})();