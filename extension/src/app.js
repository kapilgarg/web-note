
function getSelected() {
    if (window.getSelection) {
        return window.getSelection();
    }
    else if (document.getSelection) {
        return document.getSelection();
    }
    else {
        var selection = document.selection && document.selection.createRange();
        if (selection.text) {
            return selection.text;
        }
        return false;
    }
}

$(document).ready(function () {
    console.debug('loading...');
    var btnSave = null;
    $('body').mouseup(function(e){
        var selection = $.trim(getSelected());
        if(!btnSave && selection!=''){
            btnSave = $('<button>')
            .attr({
                type : 'button',
                id : 'btnsave'
            })
            .html('+')
            .css({
                'color' : 'red'
            }).hide();
            $(document.body).append(btnSave);
        }

        $('#btnsave').click(function  save() {
            var txt = $.trim(getSelected());
            document.getElementById("btnsave").style.display="none";
        });

        if(selection !=''){
            btnSave.css({
                top : e.pageY-0,
                left : e.pageX -3,
                position:'absolute'
            })
            .fadeIn();
        }
    });
    
});

