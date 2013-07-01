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
});