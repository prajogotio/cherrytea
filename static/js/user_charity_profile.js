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


// Current Project Images



function loadImages(src1, src2, src3){

    // src in img/ folder
    
    var img1 = "<img src=\"{{ url_for('static', filename='img/ " + src1 + " ') }}\"> ";
    var img2 = "<img src=\"{{ url_for('static', filename='img/ " + src2 + " ') }}\"> ";
    var img3 = "<img src=\"{{ url_for('static', filename='img/ " + src3 + " ') }}\"> ";
    
    $(".recently_backed_project").append(img1);
    $(".recently_backed_project").append(img2);
    $(".recently_backed_project").append(img3);
    
    


}