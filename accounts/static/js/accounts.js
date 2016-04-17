$(document).ready(

    function() {
        var transferForm = $('#transfer-form');
        transferForm.submit(function(event) {
            event.preventDefault();
            $.ajax({
                type: transferForm.attr('method'),
                url: transferForm.attr('action'),
                data: transferForm.serialize(),
                success: function(data) {
                    $('#messagediv').html(data['transferResultMessage']);
                    if(data.success) {
                        transferForm.find('.errorlist').remove();
                        transferForm[0].reset();
                    }
                    else {
                        transferForm.find('.errorlist').remove();
                        for (var key in data.errors) {
                            var error = data.errors[key][0]['message'];
                            var field = transferForm.find('#id_' + key);
                            field.before('<ul class="errorlist"><li>' + error + '</li></ul>');
                        }
                    }
                    $('#errors').html(data['errors']);
                },
                error: function(xhr, errmsg, err) {
                    console.log('Error: ' + xhr.status + ': ' + xhr.responseText);
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
