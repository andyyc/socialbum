$(document).ready(function(){
    $('.add-user-btn').click(function(e){
        console.log($(this));
        parentRow = $(this).parent().parent();
        if(parentRow.hasClass('selected')) {
            $(this).html('Add');
            parentRow.removeClass('selected');
        }
        else {
            $(this).html('Remove');
            parentRow.addClass('selected');
        }
    });
});