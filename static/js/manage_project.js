$(document).ready(function() {
	var proj_id = parseInt($('input[name="proj_id"]').first().val());
    var goal = parseFloat($('input[name="goal"]').first().val());
    var donated = parseFloat($('input[name="donated"]').first().val());
    var goalCovered = donated/goal*70;
    $('#money-gauge').css('width', goalCovered+'%');
    if (goalCovered > 70) {
        $('#money-gauge').css('background-color', '#fb1')
    }


    $.ajax({
    	url:'/ajax/donation_stats',
    	data:{proj_id:proj_id},
    	method:'GET'
    }).done(function(msg){
    	drawGraph($('#graph')[0], msg.reverse(), 600, 400);
    });
});

function drawGraph(container, points, width, height) {
	var canvas = document.createElement('canvas');
	canvas.width = width;
	canvas.height = height;
	var g = canvas.getContext('2d');

	var padding = 30;
	var max = -1e30;

	for (var i = 0; i < points.length; ++i) {
		max = Math.max(max, points[i].y);
	}

	var level = Math.floor(Math.log(max)/Math.log(10));
	var order = Math.pow(10,level)
	var divisor = Math.ceil(max/order);
	if (max == 0) {
		$(container).html("Currently there is not enough data.")
		return;
	}

	var barWidth = 27;
	var step = (width-2*(padding)-points.length*barWidth)/(points.length+1);
	
	for (var i = 0; i <= divisor; ++i) {
		if (i!=divisor){
			g.strokeStyle = "black";
			g.lineWidth = 0.5;
			g.strokeRect(padding, padding + (height-2*padding)/divisor * i, width-2*padding ,(height-2*padding)/divisor)
		}
		g.fillStyle="black";
		g.font="18px Helvetica";
		g.fillText('$'+(i * order), 0,  height - padding - (height-2*padding)/divisor * i);
	}
	for (var i = 0; i < points.length; ++i) {
		g.fillStyle="#679";
		g.fillRect((i+1)*step + i*barWidth + padding, height - padding - (height-2*padding)/(order*divisor)*points[i].y, barWidth, (height-2*padding)/(order*divisor)*points[i].y);
		g.fillStyle="black";
		g.font="18px Helvetica";
		g.fillText(points[i].x, (i+1)*step + i*barWidth + padding, height-padding+20);
	}

	container.appendChild(canvas);
}