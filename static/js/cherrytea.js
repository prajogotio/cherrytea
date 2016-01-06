function appendProjectItem(list, title, type, backers, photo_url, project_url) {
	var div = document.createElement("div");
	var str = '<div class="project-item"><div class="project-photo"><img src="';
		str += photo_url;
		str += '"></div><div class="project-item-info"><div class="project-title">';
		str += title;
		str += '</div><div class="project-backing">';
		str += backers;
		str += '<span class="project-backing-caption"> donators</span></div><div class="project-type">';
		str += type;
		str += '</div></div></div>';
	div.innerHTML = str;
	div.addEventListener('click', function() {
		window.location.href = project_url || '/';
	});
	list.insertBefore(div, list.lastElementChild);
}


$(document).ready(function() {
	appendProjectItem(document.getElementById("recent-list"), "Donate your blood today!", "Donation", 311, "/static/img/t02.jpg", '/project/1');
	appendProjectItem(document.getElementById("recent-list"), "Donate your blood today!", "Donation", 123, "/static/img/t04.jpg");
	appendProjectItem(document.getElementById("popular-list"), "Donate your blood today!", "Donation", 222, "/static/img/t05.jpg");
	appendProjectItem(document.getElementById("popular-list"), "Donate your blood today!", "Donation", 341, "/static/img/t06.jpg");
	appendProjectItem(document.getElementById("popular-list"), "Donate your blood today!", "Donation", 912, "/static/img/t08.jpg");
})