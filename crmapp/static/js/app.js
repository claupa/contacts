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

function delete_contact() {
    var result = confirm('Está seguro que desea eliminar el contacto?');
    if (result) {
        // $('#delete-contact-form').submit();
        return true;
    } else {
        return false;
    }
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

    // $('#id_estado_civil option').each(function(index) {
    //     if (index != 0) {
    //         this.label = this.label + 'o';
    //     }
    // });
    // $('#id_sexo').click(function(e) {});

    // Account - Use AJAX to get the Account Edit form and
    // display it on the page w/out a refresh
    $('#gi-container').delegate('.edit-account', 'click', function(e) {
        e.preventDefault();
        $('#gi-container').load($(this).attr('href'));
    });

    // ------------- ADD  PHONE NUMBER ------------------------------------------------------------

    $('.delete-phone-holder').each(function(index) {
        var e = $(this);

        e.attr('id', e.attr('id') + index);
        if (index == 0) {
            e.parents('#telefonos-table>div').children('.label-phone').text('Número de Teléfono*:');
        }
    });
    $('.delete-phone-holder').last().show();
    $('.delete-phone-holder').first().hide();
    $('#telefonos-persona #id_phones-TOTAL_FORMS').val($('.delete-phone-holder').length);

    var phone_index = $('.delete-phone-holder').length;
    $('#anadir-phone').click(function(e) {
        e.preventDefault();
        var new_phone = '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-phone">Número de Teléfono:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_phones-' + phone_index + '-number" maxlength="100" name="phones-' + phone_index + '-number" placeholder="+53 55555555 (casa)" type="text" value="">' +
            '</div>' +
            '<div class="text-right col-xs-12 col-md-2 col-lg-2" id="delete-phone-' + phone_index + '">' +
            ' <a href="#" class="delete-phone">Eliminar <i class="fa fa-times"></i></a>' +
            '</div>' +
            '</div>' +
            '</div>';
        $('#telefonos-table').append(new_phone);
        $('#telefonos-persona #id_phones-TOTAL_FORMS').val(phone_index + 1);
        if (phone_index - 1 > 0)
            $('#delete-phone-' + (phone_index - 1)).hide();
        phone_index++;

    });

    $('#telefonos-table').on('click', '.delete-phone', function(e) {
        e.preventDefault();
        phone_index--;
        if (phone_index - 1 > 0)
            $('#delete-phone-' + (phone_index - 1)).show();
        $(e.currentTarget.parentElement.parentElement.parentElement).detach();
        $('#telefonos-persona #id_phones-TOTAL_FORMS').val(phone_index);

    });

    // ------------- ADD   EMAIL ------------------------------------------------------------
    $('.delete-email-holder').each(function(index) {
        var e = $(this);
        e.attr('id', e.attr('id') + index);
        if (index == 0) {
            e.parents('#emails-table>div').children('.label-email').text('Correo Electrónico*:');
        }
    });
    $('.delete-email-holder').last().show();
    $('.delete-email-holder').first().hide();


    var email_index = $('.delete-email-holder').length;
    $('#anadir-email').click(function(e) {
        e.preventDefault();
        var new_email = '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-email">Correo Electrónico:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_email-' + email_index + '-email" maxlength="100" name="email-' + email_index + '-email" placeholder="correo@algo.com" type="text" value="">' +
            '</div>' +
            '<div class="text-right col-xs-12 col-md-2 col-lg-2 delete-email-holder" id="delete-email-' + email_index + '">' +
            ' <a href="#" class="delete-email">Eliminar <i class="fa fa-times"></i></a>' +
            '</div>' +
            '</div>' +
            '</div>';
        $('#emails-table').append(new_email);
        $('#email-group #id_email-TOTAL_FORMS').val(email_index + 1);
        if (email_index - 1 > 0)
            $('#delete-email-' + (email_index - 1)).hide();
        email_index++;

    });
    $('#emails-table').on('click', '.delete-email', function(e) {
        e.preventDefault();
        email_index--;
        if (email_index - 1 > 0)
            $('#delete-email-' + (email_index - 1)).show();
        $(e.currentTarget.parentElement.parentElement.parentElement).detach();
        $('#email-group #id_email-TOTAL_FORMS').val(email_index);
    });

    // ------------- ADD   Address ------------------------------------------------------------

    $('.delete-addr-holder').each(function(index) {
        var e = $(this);
        e.attr('id', e.attr('id') + index);
        if (index == 0) {
            e.parents('#addrs-table>div').children('.label-addr').text('Dirección*:');
        }
    });
    $('.delete-addr-holder').last().show();
    $('.delete-addr-holder').first().hide();


    var addr_index = $('.delete-addr-holder').length;
    $('#anadir-addr').click(function(e) {
        e.preventDefault();
        var new_addr = '<div class="addr">' +
            '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-addr">Dirección:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_addr-' + addr_index + '-address" maxlength="200" name="addr-' + addr_index + '-address" placeholder="Calle 0 e/ 0 y 0 #000, Municipio, Provincia" type="text">' +
            '</div>' +
            '<div class="text-right col-xs-12 col-md-2 col-lg-2 delete-addr-holder" id="delete-addr-' + addr_index + '">' +
            '<a href="#" class="delete-addr">Eliminar<i class="fa fa-times"></i></a>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-addr">País:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_addr-' + addr_index + '-pais" maxlength="50" name="addr-' + addr_index + '-pais" type="text" value="Cuba">' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>';

        $('#addrs-table').append(new_addr);

        $('#addr-group #id_addr-TOTAL_FORMS').val(addr_index + 1);
        if (addr_index - 1 > 0)
            $('#delete-addr-' + (addr_index - 1)).hide();
        addr_index++;

    });
    $('#addrs-table').on('click', '.delete-addr', function(e) {
        e.preventDefault();
        addr_index--;
        if (addr_index - 1 > 0)
            $('#delete-addr-' + (addr_index - 1)).show();
        $(e.currentTarget.parentElement.parentElement.parentElement.parentElement).detach();
        $('#addr-group #id_addr-TOTAL_FORMS').val(addr_index);

    });
    // ------------- ADD CONTACTPERSON -----------------------------------------
    $('.delete-contact-holder').each(function(index) {
        var e = $(this);
        e.attr('id', e.attr('id') + index);
        if (index == 0) {
            e.parents('#contacts-table>div').children('.label-contact').text('Persona de Contacto*:');
        }
    });
    $('.delete-contact-holder').last().show();
    $('.delete-contact-holder').first().hide();


    var contact_index = $('.delete-contact-holder').length;
    $('#anadir-contact').click(function(e) {
        e.preventDefault();
        var new_contact = '<div class="contactos">' +
            '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-contact">Persona de Contacto:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_contact-' + contact_index + '-persona" maxlength="200" name="contact-' + contact_index + '-persona" placeholder="Nombre y Apellidos" type="text">' +
            '</div>' +
            '<div class="text-right col-xs-12 col-md-2 col-lg-2 delete-contact-holder" id="delete-contact-' + contact_index + '">' +
            '<a href="#" class="delete-contact">Eliminar<i class="fa fa-times"></i></a>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-contact">Cargo:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_contact-' + contact_index + '-cargo" maxlength="50" name="contact-' + contact_index + '-cargo" type="text" placeholder="Cargo">' +
            '</div>' +
            '</div>' +
            '</div>' +
            '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-contact">Número(s) de Teléfono:</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_contact-' + contact_index + '-numbers" maxlength="50" name="contact-' + contact_index + '-numbers" type="text" placeholder="+555 5555 (casa), +555 5555 (movil), ...">' +
            '</div>' +
            '</div>' +
            '</div>' +
            '<div class="row create-contact-inputs">' +
            '<div class="col-xs-12 col-md-3 col-lg-3 label-contact">Correo(s) Electrónico(s):</div>' +
            '<div class="col-xs-12 col-md-9 col-lg-9">' +
            '<div class="text-left form-input">' +
            '<input id="id_contact-' + contact_index + '-emails" maxlength="50" name="contact-' + contact_index + '-emails" type="text" placeholder="correo1@correo.com, correo2@correo.com, ...">' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>';

        $('#contacts-table').append(new_contact);

        $('#contact-group #id_contact-TOTAL_FORMS').val(contact_index + 1);
        if (contact_index - 1 > 0)
            $('#delete-contact-' + (contact_index - 1)).hide();
        contact_index++;

    });
    $('#contacts-table').on('click', '.delete-contact', function(e) {
        e.preventDefault();
        contact_index--;
        if (contact_index - 1 > 0)
            $('#delete-contact-' + (contact_index - 1)).show();
        $(e.currentTarget.parentElement.parentElement.parentElement.parentElement).detach();
        $('#contact-group #id_contact-TOTAL_FORMS').val(contact_index);

    });

    $('#staff-table-pagination').pagination({
        dataSource: $.makeArray($('.contact-staff')),
        pageSize: 5,
        callback: function(data, pagination) {
            // template method of yourself
            var html = data;
            $('#staff-table').html(html);
        }
    });
    $('#contact-table-pagination').pagination({
        dataSource: $.makeArray($('.contact-list')),
        pageSize: 5,
        callback: function(data, pagination) {
            // template method of yourself
            var html = data;
            $('#contact-table').html(html);
        }
    });

});