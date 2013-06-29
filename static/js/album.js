$(document).ready(function(){
    $('#create-album-form').submit(function(e){
        var targetUrl = $(this).attr('action');
        $.post(targetUrl, $(this).serialize(), function(data){
            if(data){
                if(data['success']){
                    window.location.reload();
                }
                else{
                    alert('fail');
                }
            }
            else{
                alert('Sorry! Problem submitting your form, please try again.');
            }
        });
        return false;
    });
});