// This is for Django's CSRF protection; see https://docs.djangoproject.com/en/1.5/ref/contrib/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
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

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Helpful snippet from http://stackoverflow.com/questions/680241/resetting-a-multi-stage-form-with-jquery
function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
        .removeAttr('checked').removeAttr('selected');
}

// Main App
$(document).ready(function() {

    // Account - Use AJAX to get the Account Edit form and
    // display it on the page w/out a refresh
    $('#gi-container').delegate('.edit-account', 'click', function(e) {
        e.preventDefault();
        $('#gi-container').load($(this).attr('href'));
    });

    var address_index = 0;
    $('#anadir-direccion').click(function(e) {
        e.preventDefault();
        $('#direcciones-table').append('<div class="new-address-' + address_index + '">' +
            ' <div class="text-right" id="delete-address-' + address_index + '"><a href="#" class="delete-address">Eliminar <i class="fa fa-times"></i></a></div>' +
            '<div class="row address-row "><span class = "col-lg-6" > Dirección </span><span class = "col-lg-6" > Municipio </span></div>' +
            '<div class = "row address-row" ><span class = "col-lg-6" >' +
            '<input id = "id-direccion-' + address_index + '" maxlength = "100" name = "direccion" type = "text" value = " " >' +
            '</span><span class = "col-lg-6" >' +
            '<input id = "id-municipio-' + address_index + '" maxlength = "50" name = "municipio" type = "text" value = " " >' +
            '</span></div ><div class = "row address-row" ><span class = "col-lg-6" > Provincia </span>' +
            '<span class = "col-lg-6" > Descripción </span></div>' +
            '<div class = "row address-row"><span class = "col-lg-6" >' +
            '<input id = "id-provincia-' + address_index + '" maxlength = "50" name = "provincia" type = "text" value = " " >' +
            '</span><span class = "col-lg-6" >' +
            '<input id = "id-descripcion-' + address_index + '" maxlength = "100" name = "descripcion" type = "text" value = " " >' +
            '</span></div></div>');
        address_index++;
    });
    $('body').on('click', '.delete-address', function(e) {
        e.preventDefault();
        console.log(e.currentTarget);
        e.toElement.parentNode.parentNode.remove();
        console.log('hola');
    });
    $('#id_estado_civil option').each(function(index) {
        if (index != 0) {
            console.log(this.label);
            this.label = this.label + 'o';
        }
    });
    $('#id_sexo').click(function(e) {
        console.log(e);
        console.log($(this));
    });
});