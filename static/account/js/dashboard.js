$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".customer-order-id").click(function(e){
        $('#dashboard-orderitems').remove()
        loc=$(this).parents("tr")
        console.log($.trim($(this).text()))
        $.post('/account/orderitem/',{'orderid':$.trim($(this).text())},function(res){
            console.log(res)
            if(res){
                loc.after('<tr id="dashboard-orderitems"><td></td><td colspan="2" id="td-dashboard-orderitems"></td></tr>');
                var data=""
                for (var i = res.length-1;i>=0;i--){data += '['+res[i]+']'+' ';};
                $('#td-dashboard-orderitems').text(data);
                };


            });
        console.log(loc)
    });
    $(document).click(function(){
        $('#dashboard-orderitems').remove()
    });
    if($('.suborder').text()==$('th.suborder').text()){$('.suborder').hide();}
});
