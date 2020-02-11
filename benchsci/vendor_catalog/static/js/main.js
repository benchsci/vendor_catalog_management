$(document).ready(function() {
    create_menu();
    connect_data_file_change();
    connect_upload_click();
    connect_vendor_select_change('vendor_download', 'vendor_files');
    connect_vendor_select_change('vendor_generate', 'vendor_generate_files');
    connect_download_click();
    connect_generate_click();
});

function create_menu() {
    $( "#main_menu" ).accordion(
        {
            collapsible: true,
            active: false
        }
    );
}

function connect_upload_click() {
    $('#upload').bind('click', function(ev) {
        ev.preventDefault();
        var file = $("#data_file")[0].files[0];
        var vendor = $("#vendor_upload").val();
        reset_progress(file.name);
        upload_file(file, vendor);
        ev.stopPropagation();
        return false;
    });
}

function connect_data_file_change() {
    $('#data_file').bind('change', function(ev) {
        ev.preventDefault();
        var file_name = $(this)[0].files[0].name;
        reset_progress(file_name);
        ev.stopPropagation();
        return false;
    });
}

function reset_progress(file_name) {
    $("#progress")
        .css('text-transform', '')
        .removeClass("succeeded failed")
        .addClass("uploading")
        .text("Ready to upload: " + file_name);
}

function connect_vendor_select_change(vendor_select_id, files_select_id) {
    $('#' + vendor_select_id).bind('change', function(ev) {
        ev.preventDefault();
        var vendor = $(this).val();
        var request = 
        $.ajax(
            create_ajax_request('get', '/vendor_files/?vendor=' + vendor)
        ).done(function( data, textStatus, jqXHR ){
            $('.' + files_select_id +'_item').remove()
            $.each(data.vendor_files, function(index, vendor_file) {
                $('#' + files_select_id).append('<option class="' + files_select_id + '_item" value="' + vendor_file + '">' + vendor_file + '</option>');
            });
        })
        ev.stopPropagation();
        return false;
    });
}

function connect_download_click() {
    $('#download').bind('click', function(ev) {
        ev.preventDefault();
        var vendor = $("#vendor_download").val();
        var file_name = $("#vendor_files").val();
        $.ajax(
            create_ajax_request('get', '/download/?vendor=' + vendor + '&file_name=' + file_name)
        ).done(function( data, textStatus, jqXHR ){
            window.location = data.signed_download_url;
        });
        ev.stopPropagation();
        return false;
    });
}

function connect_generate_click() {
    $('#generate').bind('click', function(ev) {
        ev.preventDefault();
        download_internal()
        ev.stopPropagation();
        return false;
    });
}

async function download_internal() {
    var vendor = $("#vendor_generate").val();
    var file_name = $("#vendor_generate_files").val();
    var url = '/download/?vendor=' + vendor + '&file_name=' + file_name + '&internal=true';
    var headers = { 'X-CSRFToken': Cookies.get('csrftoken') };
    notify("Starting download of catalog to processing area...");
    $.ajax(
        create_ajax_request('get', url, headers=headers)
    ).done(function( data, textStatus, jqXHR ){
        notify("Catalog downloaded to processing area. Generating translation lists...");
        generate_translation();
    }).fail(function(jqXHR, textStatus, errorThrown ) {
        notify(jqXHR.responseText || errorThrown);
    });
}

async function generate_translation() {
    var file_name = $("#vendor_generate_files").val();
    var data = new FormData();
    data.append('file_name', file_name);
    $.ajax(
        create_ajax_request('post', '/generate/', data, headers={ 'X-CSRFToken': Cookies.get('csrftoken') })
    ).done(function( data, textStatus, jqXHR ){
        notify("Catalog translation lists have been generated. Uploading translation lists to storage...");
        upload_internal();
    }).fail(function(jqXHR, textStatus, errorThrown ) {
        notify(jqXHR.responseText || errorThrown);
    });
}

async function upload_internal () {
    var vendor = $("#vendor_generate").val();
    var file_name = $("#vendor_generate_files").val() + '_translated';
    var data = new FormData();
    data.append('vendor', vendor);
    data.append('file_name', file_name);
    data.append('internal', 'true');
    $.ajax(
        create_ajax_request('post', '/upload/', data, headers={ 'X-CSRFToken': Cookies.get('csrftoken') })
    ).done(function( data, textStatus, jqXHR ){
        notify("Catalog translation lists have been uploaded to storage.");
    }).fail(function(jqXHR, textStatus, errorThrown ) {
        notify(jqXHR.responseText || errorThrown);
    });
}

function notify(message) {
    $("#generate_progress").text(message);
}
