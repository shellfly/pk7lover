$(function(){
    $('.7tucao').click(function(){
        $('.7tucao form textarea').attr('rows',2);
        if ($('.7tucao form .btn').length == 0){
            $('<input class="btn btn-success pull-right" type="submit" value="吐嘈" />').appendTo('.7tucao form') 
        }
    });

    $('.7photo-image > a ').css({'filter':'alpha(opacity=81)','opacity':0.81}).hover(function(){
        $(this).css({'filter':'alpha(opacity=100)','opacity':1});
    },function(){
        $(this).css({'filter':'alpha(opacity=81)','opacity':0.81})
    }); 

  //  $('<a href="#edit"><i class="icon-pencil"></i></a>').appendTo('.7photo-desc p')
    $('ul li').css('display','inline');
    $('header').css('margin-bottom','13px');
    $('.thislink').css({'color':'white','background':'#83BF73'})
    $('#id_username').focus()
});

$(function() {
    $('.carousel').carousel({
        interval: 3600
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

