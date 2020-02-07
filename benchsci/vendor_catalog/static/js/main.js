$(document).ready(function() {
    create_menu();
    $('#catalog_upload')
        .bind('change', function(ev) {
            ev.preventDefault();
            var file = $(this).val();
            var vendor = $("#vendor_selection").val();
            upload_file(file, vendor);
            ev.stopPropagation();
            return false;
        });
});

function create_menu() {
    $( "#main_menu" ).accordion(
        {
            collapsible: true,
            active: false
        }
    );
}
