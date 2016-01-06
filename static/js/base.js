function displayNotification(txt) {
	var div = document.createElement('div');
	div.innerHTML = txt;
	$('#notif-list').append(div);
	setTimeout(function() {
		$(div).fadeOut("slow", function() {
			$(div).remove();
		});
	}, 2000);
}