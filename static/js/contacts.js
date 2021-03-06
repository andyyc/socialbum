$(document).ready(function(){
    $('.add-user-btn').click(function(e){
        var user_id = $(this).attr('user_id');
        var parentRow = $(this).parent().parent();
        var checkbox = $('#user_friends_checkboxes input[name="users"]' + '[value=' + user_id + ']');

        if(parentRow.hasClass('selected')) {
            $(this).html('Add');
            parentRow.removeClass('selected');
            checkbox.prop("checked", false);
        }
        else {
            $(this).html('Remove');
            parentRow.addClass('selected');
            checkbox.prop("checked", true);
        }
    });

    $('.topic-cell').click(function(){
        var game_topic_id = $(this).attr('name');
        var game_topic_input = $('#id_game_topic');

        $('#topic-btn').removeAttr('disabled');
        $('.topic-cell').removeClass('selected');
        $(this).addClass('selected');
        game_topic_input.val(game_topic_id);
    });


});