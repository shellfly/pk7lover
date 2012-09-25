$(function(){
    $('.7photo-box ').hover(function(){
        $(this).css({'filter':'alpha(opacity=81)','opacity':0.81});
    },function(){
        $(this).css({'filter':'alpha(opacity=100)','opacity':1})
    });  
   
    $('.7activity').hover(function(){
        $(this).css('background','#EFEFEF');
    },function(){
        $(this).css('background','');
    });

    $('#id_username').focus();
    $('.helptext').addClass('muted');
    $('.7minigravatar').css({'width':'48px','margin-left':'10px'}) 
});

$(function() {
    $('.carousel').carousel({
        interval: 7000
    });
});

$(function(){
    $('.vDateField').datePicker().val(new Date().asString()).trigger('change');
})

$(function(){
    var $photoboxs = $('.7photo-boxs')
    $photoboxs.imagesLoaded(function(){
        $photoboxs.masonry({
            itemSelector : '.7photo-box',
            columnWidth : 10,
            isAnimated: true,
        });
    });
});

