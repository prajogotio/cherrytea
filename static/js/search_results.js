
function requestSearch(search_term, offset, size) {
	$.ajax({
		url:'http://'+location.host+'/ajax/search',
		method:'GET',
		data: {'search_term':search_term,
			   'offset':offset,
			   'size':size},
		beforeSend: function() {
			displayWaitingBox('Searching...');
		}
	}).done(function(msg) {
		console.log(msg)
		$('#search-results').html("");
		for (var i = 0; i < msg.result.length; ++i) {
			appendSearchResult(msg.result[i]);
		}
		$('#result-total').html(msg.num_of_matches);
		$('#result-range').html((msg.offset+1) + ' to ' + (msg.offset+msg.result.length));
		renderPager(msg.offset, msg.size, msg.num_of_matches, msg.search_term);
	}).always(function(msg) {
		closeWaitingBox();
	});
}

function appendPagerButton(caption, offset, size, search_term, currentPage) {
	var a = document.createElement('a');
	$(a).click(function() {
		requestSearch(search_term, offset, size);
	});
	$(a).html(caption);
	$(a).addClass('no-select')
	if (currentPage) {
		$(a).css('background-color', '#a11');
	}
	$('#search-pager').append(a);
}

function renderPager(offset, size, total, search_term){
	var containers = Math.ceil(total/size);
	var cur = Math.ceil((offset+1)/size);
	var NUM_OF_PAGERS = 4;
	$('#search-pager').html('');
	if (cur != 1) {
		appendPagerButton('prev', size*(cur-2), size, search_term);
	}
	for (var i = Math.max(1,cur-2); i < Math.min(containers,cur+NUM_OF_PAGERS); ++i) {
		appendPagerButton(i, size*(i-1), size, search_term, i==cur);
	}
	if (cur+1 < containers) {
		appendPagerButton('next', size*cur, size, search_term);
	}
}


function appendSearchResult(data) {
	var div = document.createElement('div');
	div.setAttribute('class', 'result-item');
	var txt = '<div class="result-thumbnail float-left"><img src="';
		txt += data.proj_pic_url || '/static/img/no_poster.jpg';
		txt += '" onclick=\'window.location.href="';
		txt += '/project/' + data.proj_id;
		txt += '"\'></div><div class="result-info float-left"><div class="result-name"><a href="';
		txt += '/project/' + data.proj_id;
		txt += '">';
		txt += data.proj_name;
		txt += '</a></div><div class="result-owner"><a href="';
		txt += '/user/'+data.owner_id;
		txt += '">';
		txt += data.username;
		txt += '</a></div><div class="result-desc">';
		txt += data.proj_desc;
		txt += '</div><div class="result-category">';
		txt += data.category;
		txt += '</div><div class="result-metadata"><div class="result-donation float-left">';
		txt += data.num_of_donations;
		txt += ' donations</div><div class="result-date float-right">Created on ';
		txt += data.date_created;
	 	txt += '</div><div class="clear-fix"></div></div></div><div class="clear-fix"></div>';
	
	$(div).append(txt);
	$('#search-results').append(div);
}

$(document).ready(function() {
		
	$('#search_button').click(function() {
		requestSearch($('#search_bar').val(), 0, 5)
	});
});

