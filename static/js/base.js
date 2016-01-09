var state = {
	offset_id:0,
	justLoaded:true,
	newNotification:[],
}

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


function displayWaitingBox(txt) {
	$('#waiting-box-content').html(txt);
	$('#waiting-box').show();
}

function closeWaitingBox() {
	$('#waiting-box').hide();
}


$(document).ready(function() {
	$('#head-menu-icon').click(function() {
		$('#menu-options-layer').show();
	});

	$('#menu-options-layer').click(function() {
		$(this).hide();
	});

	$('#news').click(function() {
		$('#news-layer').show()
		unhighlightnewsButton();
		markAllNotificationRead();
	});

	$('#news-layer').click(function() {
		$(this).hide();
	});

	checkNotification();
	setInterval(function() {
		checkNotification();
	}, 15000);
});


function checkNotification() {
	$.ajax({
		url:'http://'+location.host+'/ajax/notif',
		method:'GET',
		data:{offset_id:state.offset_id}
	}).done(function(msg) {
		msg = msg.reverse();
		for (var i = 0; i < msg.length; ++i) {
			state.offset_id = Math.max(msg[i].notif_id, state.offset_id);
			if (!state.justLoaded) {
				displayNotification(msg[i].content);
			}
			appendNewsTray(msg[i]);
		}
		state.justLoaded = false
	});
}

function appendNewsTray(msg) {
	var div = document.createElement('div');
	$(div).addClass('news-item');
	if (msg.status == 0) {
		$(div).addClass('unread-news');
		highlightNewsButton();
		state.newNotification.push(msg.notif_id);
	}
	var str = '<div>';
		str += msg.content;
		str += '</div><div class="date">';
		str += msg.date_created;
		str += '</div>';
	$(div).html(str);
	$('#news-tray')[0].insertBefore(div, $('#news-tray')[0].firstChild);
}

function highlightNewsButton() {
	$('#news').addClass('got-unread-news');
	$('#news').html('News!');
}

function unhighlightnewsButton() {
	$('#news').removeClass('got-unread-news');
	$('#news').html('News');
}

function markAllNotificationRead() {
	for (var i = 0; i < state.newNotification.length; ++i) {
		var cur = state.newNotification[i];
		$.ajax({url:'http://'+location.host+'/ajax/notif/read', data:{notif_id:cur}})
	}
	state.newNotification = [];
	setTimeout(function() {
		var news = $('#news-tray').children();
		for (var i = 0; i < news.length; ++i) {
			$(news[i]).removeClass('unread-news');
		}
	}, 1000);
}