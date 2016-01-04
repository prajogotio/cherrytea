// First Part
// All the descriptions of the project, title, etc. 

function changeProjectName(newname){
    $("#project-title").html(newname);   
}

function changeProjectDescption(newdes){
    $("#project-description").html(newdes);
}

function changeProjectLocation(newloc){
    $("#project-location").html(newloc);
}


function changeProjectCategory(newcat){
    $("#project-category").html(newcat);
}

function changeProjectOwner(newown){
    $("#project-owner").html(newown);    
}

function changeProjectOrganization(neworg){
    $("#project-charity-org").html(neworg);
}





// Donation Goal, Collected, Donors

function changeDonationGoal(newgoal){
    $("#donation-goal").html(newgoal);
}

function changeDonationCollected(newcollect){
    $("#donation-collected").html(newcollect);
}

function changeNumDonor(newdonor){
    $("#number-of-donor").html(newdonor);
}






// Create Update Post

function createUpdatePost(title, updateText, date){

    var adddiv = "<div class=\"post\"><div class=\"post_title\">" + title + "</div><div class=\"post_post\">" + updateText + "</div><div class=\"post_date\">" + date + "</div></div>";
                                
    $(".project_update").append(adddiv);
    
}



// Create Comment

function createComment(user, commentText, date){

    var adddiv = "<div class=\"comment\"><div class=\"comment_user\">" + user + "</div><div class=\"comment_text\">" + commentText + "</div><div class=\"comment_date\">" + date + "</div></div>";
                                
    $(".comments").append(adddiv);
    
}



// Posting New Comment

function postComment(){
    
    var commentText = $(".new_comment_data").val();
    var commentUser = $(".user_comment").val();
    console.log(commentUser);
    var date = new Date();
    
    var datePosted = "Commented on " + date.getDay() + "/" + date.getMonth() + "/" +date.getFullYear();
    
    createComment(commentUser, commentText, datePosted);
    
}











