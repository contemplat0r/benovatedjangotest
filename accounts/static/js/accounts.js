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
                    if(data.success) {
                        transferForm[0].reset();
                    }
                    else {
                        transferForm.find('.errorField').remove();
                        for (var key in data.errors) {
                            var error = data.errors[key];
                            var field = transferForm.find('id_' + key);
                            field.before('<p class="errorField"><em></em>' + error + '</p>');
                        }
                    }
                    $('#errors').html(data['errors']);
                },
                error: function(xhr, errmsg, err) {
                    console.log('Error: ' + xhr.status + ': ' + xhr.responseText);
                    //$('#messagediv').html('Error message');
                    $('#messagediv').html(errmsg);
                }
            });
            return false;
        });
        
        function getCookie(name) {
            var cookieValue = null;
            var i = 0;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (i; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
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
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }
);
