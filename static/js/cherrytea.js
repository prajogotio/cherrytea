function appendProjectItem(list, title, type, donations, photo_url, project_url) {
	var div = document.createElement("div");
	if (photo_url == null) {
		photo_url = '/static/img/no_poster.jpg';
	}
	var str = '<div class="project-item"><div class="project-photo"><img src="';
		str += photo_url;
		str += '"></div><div class="project-item-info"><div class="project-title">';
		str += title;
		str += '</div><div class="project-backing">';
		str += donations;
		str += '<span class="project-backing-caption"> donations</span></div><div class="project-type">';
		str += type;
		str += '</div></div></div>';
	div.innerHTML = str;
	div.addEventListener('click', function() {
		window.location.href = project_url || '/';
	});
	list.insertBefore(div, list.lastElementChild);
}


$(document).ready(function() {
	// populate lists
	var recentList = $('#recent-list')[0];
	var popularList = $('#popular-list')[0];
	var recommendedList = $('#recommendation-list')[0];
	var allList = [recentList, popularList]
	var ajaxUrl = ['/ajax/recent_project','/ajax/popular_project']
	for(var k = 0; k < allList.length;++k){
		(function(url, theList){
			$.ajax({
				url : 'http://'+location.host+url,
				method : 'GET',
				data : {'size':3}
			}).done(function(msg){
				for (var i = 0; i < msg.length; ++i) {
					var proj = msg[i];
					appendProjectItem(theList, proj.proj_name, proj.category, proj.donations, proj.proj_pic_url, '/project/'+proj.proj_id);
				}
			});
		})(ajaxUrl[k],allList[k]);
	}
});