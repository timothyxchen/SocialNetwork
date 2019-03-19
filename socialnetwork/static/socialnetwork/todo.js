// Sends a new request to update the to-do list
var isotime = new Date('2000-02-27T01:26:33.870Z');

function getList() {
    var refreshTextElement = isotime.toISOString();
    $.ajax({
        url: "/socialnetwork/refresh-global",
        type: 'GET',
        data: "last_refresh="+refreshTextElement+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updateList
    });
}

function updateList(lists) {
    $(lists).each(function() {
        if(this.model == "socialnetwork.post"){
            $("en_"+this.pk).remove();
            $("newpost").prepend(
            '<en_'+this.pk+'><a href="profile/'+this.fields.post_creator+'"%}">Posted by'
            +this.fields.post_creator+'</a>'
            +"<span id='id_post_text_"+this.pk+"'>"+sanitize(this.fields.content)+"</span>"
            +"<span>"+sanitize(this.fields.post_time)+"</span><br>"
            + '<ol id="todo-list_'+this.pk+'"></ol>'
            + '<label>Comment:</label>'
            + '<input id="comment_'+this.pk+'" type="text" name="comment">'
            + '<button onclick="addComment('+this.pk+')">Comment</button>'
            + '<span id="error" class="error"></span><br></en_"'+this.pk+'">'
            );
        }else{
            $("em_"+this.pk).remove();
            $("#todo-list_"+this.fields.post_id).prepend(
            '<em_'+this.pk+'><a href="profile/'+this.fields.creator_id+'"%}">Commented by'
            +this.fields.comment_creator+'</a>'
            +"<span id='id_comment_text_"+this.pk+"'>"+sanitize(this.fields.content)+"</span>"
            +"<span>"+sanitize(this.fields.comment_time)+"</span><br></em_"+this.pk+">"
            );
        }
    });
    isotime=new Date();
}

function getFollowerList() {
    var refreshTextElement = isotime.toISOString();
    $.ajax({
        url: "/socialnetwork/refresh-global",
        type: 'GET',
        data: "last_refresh="+refreshTextElement+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updateList
    });
}

function updateFollowerList(lists) {
    $(lists).each(function() {
        if(this.model == "socialnetwork.comment"){
            $("em_"+this.pk).remove();
            $("#todo-list_"+this.fields.post_id).prepend(
            '<em_'+this.pk+'><a href="profile/'+this.fields.creator_id+'"%}">Commented by'
            +this.fields.comment_creator+'</a>'
            +"<span id='id_comment_text_"+this.pk+"'>"+sanitize(this.fields.content)+"</span>"
            +"<span>"+sanitize(this.fields.comment_time)+"</span><br></em_"+this.pk+">"
            );

        }else{
            $("en_"+this.pk).remove();
            $("newpost").prepend(
            '<en_'+this.pk+'><a href="profile/'+this.fields.post_creator+'"%}">Posted by'
            +this.fields.post_creator+'</a>'
            +"<span id='id_post_text_"+this.pk+"'>"+sanitize(this.fields.content)+"</span>"
            +"<span>"+sanitize(this.fields.post_time)+"</span><br></en_"+this.pk+">"
            +   '<ol id="todo-list_'+this.pk+'"></ol>'
            + '<label>Comment:</label>'
            + '<input id="comment_'+this.pk+'" type="text" name="comment">'
            + '<button onclick="addComment('+this.pk+')">Comment</button>'
            + '<span id="error" class="error"></span><br>'
            );
        }
        isotime=new Date();

    });

}

function updateComments(comments) {
    // Removes the old to-do list items
    // Adds each new todo-list item to the list
    $(comments).each(function() {
        $("em_"+this.pk).remove();
        $("#todo-list_"+this.fields.post_id).prepend(
            '<em_'+this.pk+'><a href="profile/'+this.fields.creator_id+'"%}">Commented by'
            +this.fields.comment_creator+'</a>'
            +"<span id='id_comment_text_"+this.pk+"'>"+sanitize(this.fields.content)+"</span>"
            +"<span>"+sanitize(this.fields.comment_time)+"</span><br></em_"+this.pk+">"
        );
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function addComment(id) {
    var commentTextElement = $("#comment_"+id);
    var commentTextValue   = commentTextElement.val();

    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment",
        type: "POST",
        data: "comment_text="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken()+"&id="+id,
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateComments(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getList;
window.onload =getFollowerList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);
window.setInterval(getFollowerList,5000);