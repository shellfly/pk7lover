$(function(){
    $('.7tucao').click(function(){
        $('.7tucao form textarea').attr('rows',2);
        if ($('.7tucao form .btn').length == 0){
            $('<input class="btn btn-success pull-right" type="submit" value="吐嘈" />').appendTo('.7tucao form') 
        }
    });

    $('.7photo-box ').hover(function(){
        $(this).css({'filter':'alpha(opacity=81)','opacity':0.81});
    },function(){
        $(this).css({'filter':'alpha(opacity=100)','opacity':1})
    }); 

  //  $('<a href="#edit"><i class="icon-pencil"></i></a>').appendTo('.7photo-desc p')
    $('ul li').css('display','inline');
    $('header').css('margin-bottom','13px');
    $('.thislink a').css({'color':'white','background':'#83BF73'});
    $('#id_username').focus();
    $('.helptext').css('display','none');
    $('.7minigravatar').css({'width':'48px','margin-left':'10px'})
});

$(function() {
    $('.carousel').carousel({
        interval: 7000
    });
    
});

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

