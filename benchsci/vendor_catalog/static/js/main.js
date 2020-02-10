$(document).ready(function() {
    create_menu();
    connect_data_file_change();
    connect_upload_click();
    connect_vendor_download_change();
    connect_download_click();
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
        upload_file(file, vendor);
        ev.stopPropagation();
        return false;
    });
}

function connect_data_file_change() {
    $('#data_file').bind('change', function(ev) {
        ev.preventDefault();
        var file_name = $(this)[0].files[0].name;
        $("#progress").css('text-transform', '').removeClass("succeeded failed").addClass("uploading").text("Ready to upload: " + file_name);
        ev.stopPropagation();
        return false;
    });
}

function connect_vendor_download_change() {
    $('#vendor_download').bind('change', function(ev) {
        ev.preventDefault();
        var vendor = $(this).val();
        $.ajax({
                url: '/vendor_files/?vendor=' + vendor,
                type: 'get',
                dataType: 'json',
        }).done(function( data, textStatus, jqXHR ){
            $.each(data.vendor_files, function(index, vendor_file) {
                $('#vendor_files').append('<option value="' + vendor_file + '">' + vendor_file + '</option>');
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
        $.ajax({
            url: '/download/?vendor=' + vendor + '&file_name=' + file_name,
            type: 'get',
            dataType: 'json',
        }).done(function( data, textStatus, jqXHR ){
            window.location = data.signed_download_url;
        });
        ev.stopPropagation();
        return false;
    });
}