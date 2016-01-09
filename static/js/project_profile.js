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



$(document).ready(function() {
    // set donation/goal bar
    var proj_id = parseInt($('input[name="proj_id"]').first().val());
    var goal = parseFloat($('input[name="goal"]').first().val());
    var donated = parseFloat($('input[name="donated"]').first().val());
    var goalCovered = donated/goal*70;
    $('#money-gauge').css('width', goalCovered+'%');
    if (goalCovered > 70) {
        $('#money-gauge').css('background-color', '#fb1')
    }

    var followed = $('input[name="followed"]').first().val() == 'true';
    if (followed) {
        $('#follow-button').hide();
        $('#unfollow-button').show();
    }

    $('#follow-button').click(function() {
        $.ajax({
            url:'http://'+location.host+'/ajax/follow',
            method:'POST',
            data:{'proj_id':proj_id}
        }).done(function(msg){
            if (msg.success) {
                displayNotification("Project has been successfully followed!")
                $('#follow-button').hide();
                $('#unfollow-button').show();
            }
        })
    });

    $('#unfollow-button').click(function() {
        $.ajax({
            url:'http://'+location.host+'/ajax/unfollow',
            method:'POST',
            data:{'proj_id':proj_id}
        }).done(function(msg){
            if (msg.success) {
                displayNotification("Project has been unfollowed.")
                $('#follow-button').show();
                $('#unfollow-button').hide();
            }
        })
    });

    registerListenerToPosts();
});


function registerListenerToPosts() {
    var posts = $('.post');
    for (var i = 0; i < posts.length; ++i) {
        var cur = posts[i];
        var broadcast_id = $(cur).find('input[name="broadcast_id"]').first().val();
        var like = $(cur).find('input[name="like"]').first().val();
        var textarea = $(cur).find('textarea')[0];
        var replyList = $(cur).find('.replies')[0];
        var likeButton = $(cur).find('.post_like')[0];
        var unlikeButton = $(cur).find('.post_unlike')[0];
        var replyButton = $(cur).find('.post_reply')[0];
        var counter = $(cur).find('.post_likes')[0];
        replyEventHandler(textarea, replyList, broadcast_id);
        if (like == 'true') {
            $(likeButton).hide();
        } else {
            $(unlikeButton).hide();
        }
        registerButtons(likeButton, unlikeButton, replyButton, broadcast_id, counter);
    }
}

function replyEventHandler(textarea, replyList, broadcast_id){
    var state = {
        processing : false,
    }
    $(textarea).keydown(function(e){
        if (state.processing) {
            e.preventDefault();
            return false;
        }
        if(e.which == 13) {
            state.processing = true;
            $.ajax({
                url:'http://'+location.host+'/post/reply',
                method:'POST',
                data:{broadcast_id:broadcast_id,
                      content:$(textarea).val()},
                beforeSend:function(){
                    $(textarea).css("color", "#555");
                }
            }).done(function(msg) {
                if(msg.success){
                    appendReply(replyList, $(textarea).val());
                    $(textarea).val('');
                }
            }).fail(function(msg) {
                displayNotification("Failed to send reply. Please try again later.");
            }).always(function(msg) {
                $(textarea).css("color", "black");
                state.processing = false;
            })
            e.preventDefault();
            return false;
        }
    });
}

function appendReply(replyList, msg) {
    $(replyList).find('.no-reply').first().hide();
    var div = document.createElement('div');
    div.setAttribute('class', 'reply-item');
    var txt = '<span><a href="/user">';
        txt += $('#session_user').val();
        txt +='</a><span> ';
        txt += msg;
        txt += '<br><span class="date-time">replied just now.</span>';
    div.innerHTML = txt;
    replyList.appendChild(div);
}


function registerButtons(likeButton, unlikeButton, replyButton, broadcast_id, counter) {
    $(likeButton).click(function(){
        $.ajax({
            'url':'http://'+location.host+'/post/like',
            'data':{broadcast_id:broadcast_id},
            'method':'POST',
        }).done(function(msg) {
            $(likeButton).hide();
            $(unlikeButton).show();
            $(counter).html(parseInt($(counter).html())+1);
        })
    });
    $(unlikeButton).click(function(){
        $.ajax({
            'url':'http://'+location.host+'/post/unlike',
            'data':{broadcast_id:broadcast_id},
            'method':'POST',
        }).done(function(msg) {
            $(likeButton).show();
            $(unlikeButton).hide();
            $(counter).html(parseInt($(counter).html())-1);
        })
    });
}