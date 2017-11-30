/* Written by Xiaoming Zheng on 30AUG for my Lover */
(function($) {
$(document).ready(function() {
    function reCalculateSum(){
        var expense_aud=0;
        var price_rmb=0;
        var expense_rmb=0;
        var price_aud=0;
        $("#items-group tr.form-row").each(function(index,e){
            price_rmb+=$(this).children(".field-price_rmb").children("input").val()*$(this).children(".field-quantity").children("input").val();
            expense_aud+=$(this).children(".field-expense_aud").children("input").val()*$(this).children(".field-quantity").children("input").val();
            expense_rmb+=$(this).children(".field-expense_rmb").children("input").val()*$(this).children(".field-quantity").children("input").val();
            price_aud+=$(this).children(".field-price_aud").children("input").val()*$(this).children(".field-quantity").children("input").val();
        });
        $("#id_total_price_rmb").val(price_rmb.toFixed(2));
        $("#id_total_expense_aud").val(expense_aud.toFixed(2));
        $("#id_total_expense_rmb").val(expense_rmb.toFixed(2));
        $("#id_total_price_aud").val(price_aud.toFixed(2));
    }

    $(".field-price_rmb, .field-quantity, .field-expense_aud, .field-expense_rmb, .field-price_aud").change(reCalculateSum);
    $(".field-delivered input#id_delivered").click(function(){
        /*jquery checked state doesnot work here, so use js instead: [this] insteadof [$("this")] */
        if (this.checked){
            if (!($(".field-delivered_date input#id_delivered_date").val())){
                function appendZero(obj){if(obj<10){return "0"+obj;}else{return obj;}}
                var mydate = new Date();
                var cd = mydate.getFullYear()+'-'+appendZero(mydate.getMonth()+1)+'-'+appendZero(mydate.getDate());
                $(".field-delivered_date input#id_delivered_date").val(cd);
                }
            }
        else{
            $(".field-delivered_date input#id_delivered_date").val("");
            }
    });

    if (!(document.getElementById('id_delivered').checked)){$('#id_delivered').siblings('label').css('color','red');}
    if (!(document.getElementById('id_paid').checked)){$('#id_paid').siblings('label').css('color','red');}
    
    $("#id_total_expense_rmb").parent().hide();
    $("#id_total_price_aud").parent().hide();
    $("#items-group > div > fieldset > table > thead > tr > th:nth-child(3)").hide();
    $("td.field-price_aud").hide();
    $("td.field-expense_rmb").hide();
    $("#items-group > div > fieldset > table > thead > tr > th:nth-child(8)").hide();
    $("#id_total_expense_aud").parent().after('<input type="button" value="Show All" id="ozfriend_show_all">');
    $("#id_total_expense_aud").parent().after('<input type="button" value="Hide Some" id="ozfriend_hide_some">');

    $("#ozfriend_show_all").click(function(){
        $("#id_total_expense_rmb").parent().show();
        $("#id_total_price_aud").parent().show();
        $("#items-group > div > fieldset > table > thead > tr > th:nth-child(3)").show();
        $("td.field-price_aud").show();
        $("td.field-expense_rmb").show();
        $("#items-group > div > fieldset > table > thead > tr > th:nth-child(8)").show();
        $("#ozfriend_hide_some").show();
        $("#ozfriend_show_all").hide();
    });

    $("#ozfriend_hide_some").click(function(){
        $("#id_total_expense_rmb").parent().hide();
        $("#id_total_price_aud").parent().hide();
        $("#items-group > div > fieldset > table > thead > tr > th:nth-child(3)").hide();
        $("td.field-price_aud").hide();
        $("td.field-expense_rmb").hide();
        $("#items-group > div > fieldset > table > thead > tr > th:nth-child(8)").hide()
        $("#ozfriend_hide_some").hide();
        $("#ozfriend_show_all").show();
    });
    if($("#id_total_expense_rmb").val()>0 || $("#id_total_price_aud").val()>0){$("#ozfriend_show_all").trigger("click");};
    
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

    $(".field-product input").keyup(function(){
        $('#search-result').remove();
        if ($(this).val().length > 1){
            $(this).after('<div id="search-result"></div>')
            $.get('/shop/inner/', {'q':$(this).val()}, function(data){
                for (var i = data.length-1;i>=0;i--){
                    if (data[i] != ""){
                        $('#search-result').append($("<div></div>").text(data[i]));
                    }
                };
                $('#search-result').find('div').bind('click', function(){
                    var search_text = $(this).text();
                    var insertp = $(this).closest('tr');
                    var ch = '<strong><a href="/admin/shop/product/{ID}/change/">'+$(this).text()+'</a></strong>';
                    /*'csrfmiddlewaretoken':csrftoken*/
                    $.post('/shop/inner/',{'search_text':search_text},function(res){
                        insertp.children('.field-price_rmb').children("input").val(res.price_rmb);
                        insertp.children('.field-expense_aud').children("input").val(res.expense_aud);
                        insertp.children('.field-price_aud').children("input").val(res.price_aud);
                        insertp.children('.field-expense_rmb').children("input").val(res.expense_rmb);
                        insertp.children('.field-product').children("input").val(res.id);
                        var add_content = ch.replace("{ID}", res.id);
                        insertp.children('.field-product').children('strong').remove();
                        insertp.children('.field-product').children('.related-lookup').after(add_content);
                        reCalculateSum();
                    });
                    $('#search-result').remove();
                });
                $('#search-result').find('div').hover(function(){
                    $('#search-result').find('div').removeClass("hover");
                    $(this).addClass("hover");
                });
            });
        }
        else{
            $("#search-result").remove();
        };
    });

    $(".field-receiver #id_receiver").keyup(function(e){
        if (e.which == 32){
            $(this).val($.trim($(this).val()));
            $.post('/orders/inner/',{'receiver':$.trim($(this).val())},function(res){
                if(res.status){
                    $(".field-receiver #id_phone").val(res.phone);
                    $(".field-address #id_address").val(res.address);
                };
            });
        };
    });
});
})(django.jQuery);
