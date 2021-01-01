
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
    $('body').mouseup(function (e) {
        var selection = $.trim(getSelected());
        if (!btnSave && selection != '') {
            btnSave = $('<button>')
                .attr({
                    type: 'button',
                    id: 'btnsave'
                })
                .html('+')
                .css({
                    'color': 'red'
                }).hide();
            $(document.body).append(btnSave);

            $('#btnsave').click(function save(event) {
                event.preventDefault();
                var txt = $.trim(getSelected());

                var request = new XMLHttpRequest();
                request.open("POST", URL + "notes");
                request.setRequestHeader("Content-Type", "text/plain");
                request.overrideMimeType("text/plain");
                request.onload = function () {
                    console.log("Response received: " + request.responseText);
                };
                try {
                    request.send(JSON.stringify({ "user_id": "1", "text": txt, "source": window.location.href }));
                }
                catch (err) {
                    console.log(err);
                }
                document.getElementById("btnsave").style.display = "none";
            });
        }



        if (selection != '') {
            btnSave.css({
                top: e.pageY - 0,
                left: e.pageX - 3,
                position: 'absolute'
            })
                .fadeIn();
        }
        else {
            if (document.getElementById("btnsave")) {
                document.getElementById("btnsave").style.display = "none";
            }
        }
    });

});

