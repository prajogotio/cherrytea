// User Profile Pic

function loadProfilePic(src1){

    // src in img/ folder
    
    var img1 = "<img src=\"{{ url_for('static', filename='img/ " + src1 + " ') }}\"> ";
    $(".recently_backed_project").append(img1);
}


// User Profile 

function changeUsername(newusername){

    $("#username").html(newusername);
}

function changeJoinDate(newdate){
    $("#user-join-date").html(newdate);
}

function changeLocation(newloc){
    $("#user-location").html(newloc);
}


function changeAdvocate(newadvo){
    $("#user-advocate").html(newadvo);
}


function changeUserType(newtype){
    $("#user-type").html(newtype);
}


function changeProjectsBacked(newback){
    $("#user-projects-backed").html(newback);
}

// Biography
function changeBio(newbio){
    $(".user_biography_text").html(newbio);
}


// Recently Backed Projects Images



function loadImages(src1, src2, src3){

    // src in img/ folder
    
    var img1 = "<img src=\"{{ url_for('static', filename='img/ " + src1 + " ') }}\"> ";
    var img2 = "<img src=\"{{ url_for('static', filename='img/ " + src2 + " ') }}\"> ";
    var img3 = "<img src=\"{{ url_for('static', filename='img/ " + src3 + " ') }}\"> ";
    
    $(".recently_backed_project").append(img1);
    $(".recently_backed_project").append(img2);
    $(".recently_backed_project").append(img3);
    
}

function appendRecentlyBackedProjects(name, data) {
    var txt = '<span class="info-name">';
    txt += name;
    txt += '</span> donated <span class="info-money">$';
    txt += data.amount;
    txt += '</span> for <a href="';
    txt += '/project/'+data.proj_id;
    txt += '"><span class="info-title">';
    txt += data.proj_name;
    txt += '</span></a> on <span class="info-date">';
    txt += data.date_donated;
    txt += '.</span>';
    var div = document.createElement('div');
    div.setAttribute('class', 'info-item');
    $(div).html(txt);
    $('#recently_backed_project')[0].appendChild(div);
}

$(document).ready(function() {
    var name = $.trim($('input[name="full_name"]').first().val()) || $('input[name="username"]').first().val()
    var recent = $.parseJSON($('input[name="recent_backed_list"]').first().val());
    console.log(recent);
    for (var i = 0; i < recent.length; ++i) {
        appendRecentlyBackedProjects(name, recent[i]);
    }
});