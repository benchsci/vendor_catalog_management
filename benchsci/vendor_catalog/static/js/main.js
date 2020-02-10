$(document).ready(function() {
    create_menu();
    connect_data_file_change();
    connect_upload_click();  
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
        var vendor = $("#vendor").val();
        upload_file(file, vendor);
        ev.stopPropagation();
        return false;
    });
}

function connect_data_file_change() {
    $('#data_file').bind('change', function(ev) {
        ev.preventDefault();
        var file_name = $(this)[0].files[0].name;
        $("#progress").text("Ready to upload: " + file_name);
        ev.stopPropagation();
        return false;
    });
}
