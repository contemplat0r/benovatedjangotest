$(document).ready(

    function() {
        var transferForm = $('#transfer-form');
        transferForm.submit(function(event) {
            event.preventDefault();
            console.log('Entry in transferForm.submit');
            console.log(transferForm.serialize());
            $.ajax({
                type: transferForm.attr('method'),
                url: transferForm.attr('action'),
                data: transferForm.serialize(),
                success: function(data) {
                    console.log('Success');
                    console.log(data);
                    //$('#messagediv').html(data);
                    $('#messagediv').html(data['transferResultMessage']);
                },
                error: function(xhr, errmsg, err) {
                    console.log('Error: ' + xhr.status + ': ' + xhr.responseText);
                    //$('#messagediv').html('Error message');
                    $('#messagediv').html(errmsg);
                }
            });
            return false;
        });
    }
);
