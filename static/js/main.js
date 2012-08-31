$(function() {
    $('#file_upload').uploadify({
        'swf'      : '/static/uploadify/uploadify.swf',
        'uploader' : '',
        'formData':{},
        'cancelImage' : '/static/uploadify/cancel.png',
        'fileTypeExts'   : '*.jpg;*.png',
        'multi'		: true,
        'auto'    : true,
        'buttonText': '添加照片',
        'height':20,
        'width':72,
        // Put your options here
    });
},
function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            $.each(data.result, function (index, file) {
                $('<p/>').text(file.name).appendTo(document.body);
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
                'width',
                progress + '%'
            );
        }
    });
});
