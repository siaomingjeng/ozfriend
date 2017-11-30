$(document).ready(function(){
    $(".js-ajax-submit").click(function(e){
        var form = $(this).closest("form");
        e.preventDefault();
        image=form.siblings().children("img");
   /*     console.log(form.siblings("#js-item-price_rmb").text()); */
        $.ajax({
            url: form.attr("action"),
            method: 'post',
            data: form.serialize(),
            success: function(data){
                if($('#subheader span.hide')){$('#subheader span.hide').removeClass('hide');}
                if ('success'==data){
                    $("p#js-item-number").text(Number($("p#js-item-number").text())+1);
                    $("p#js-price-total").text((Number($("p#js-price-total").text())+Number(form.siblings("#js-item-price_rmb").text())).toFixed(2));
                image.animate({
                     height:'-=45px'
                },'fast',function(){
                    image.animate({
                        height:'+=45px'
                    },'fast');
                });
            }else{alert("You have added 8 this item!")}}
        });
    });

    $("#search-text").keyup(function(){
        if ($(this).val().length > 1){
            $.get($(this).parent("form").attr("action"), {'q':$(this).val()},function(data){
                $('#search-result').html('');
                for (var i = data.length-1;i>=0;i--){
                    if (data[i] != ""){
                        $('#search-result').append($("<div></div>").text(data[i]));
                    }
                };
                $('#search-result').find('div').bind('click', function(){
                    $("#search-text").val($(this).text());  /*this.innerHTML*/
                    $("#search-result").empty();
                });
                $('#search-result').find('div').hover(function(){
                    $('#search-result').find('div').removeClass("hover");
                    $(this).addClass("hover");
                });
            });}
        else{
            $("#search-result").empty();
        }
    }); 
/*  $("#search-text").blur(function(){
 *          $("#search-result").empty();
 *              });
 *                  $("#search-text").keydown(function(){
 *                          $("#search-result").empty();
 *                              });*/
});
