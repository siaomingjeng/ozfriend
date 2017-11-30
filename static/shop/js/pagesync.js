/* Written by Xiaoming Zheng on 30AUG for my Lover */
(function($) {
    $("#items-group").change(function(){
        var aud=0;
        var rmb=0;
        $("#items-group tr.has_original").each(function(index,e){
            rmb+=$(this).children(".field-price").children("input").val()*$(this).children(".field-quantity").children("input").val();
            aud+=$(this).children(".field-expense").children("input").val()*$(this).children(".field-quantity").children("input").val();
        });
        $("#id_total_price").val(rmb.toFixed(2));
        $("#id_total_expense").val(aud.toFixed(2));
        });
})(django.jQuery);
