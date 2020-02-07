function upload_file(file, vendor) {
    if (!file || !vendor)
        return;    
    var chunk_size = 1048576;
    start_upload(file, vendor, chunk_size);
}

function create_ajax_request(method, url, data, headers, status_code_map) {
    return {
        url: url,
        type: method,
        data: data,
        dataType: 'json',
        headers: headers,
        cache: false,
        contentType: false,
        processData: false,
        statusCode: status_code_map
    }
}

function start_upload_headers() {
    var headers = {
        'X-CSRFToken': Cookies.get('csrftoken'),
    }
    return headers;
}

function resume_upload_headers(file) {
    var headers = {
        'Content-Length': file.size,
        'Content-Type': 'application/octet-stream',
        'Content-Range': '*/' + file.size,
    }
    return headers;
}

function continue_upload_headers(file, range_start, range_ends) {
    var headers = {
        'Content-Length': file.size,
        'Content-Type': 'application/octet-stream',
    }
    if (range_start !== undefined && range_ends !== undefined) {
        headers['Content-Range'] = 'bytes ' + range_start + '-' + (range_ends - 1) + '/' + file.size;
    }
    return headers;
}

function start_upload(file, vendor, chunk_size) {
    var data = new FormData();
    data.append('file_size', file.size);
    data.append('vendor', vendor);
    data.append('catalog_name', file.name);
    var headers = start_upload_headers();
    var request = create_ajax_request('post', '/upload', data, headers, {});
    $.ajax(
        request
    ).done(function( data, textStatus, jqXHR ){
        send_file_chunk(data.resumable_upload_url, file, 0, chunk_size, 0);
    }).fail(function(jqXHR, textStatus, errorThrown ) {
        update_status('failed', jqXHR.responseText || errorThrown);
    });
}

function get_resume_upload_function(resumable_upload_url, file, start, chunk_size) {
    return function(data, textStatus, jqXHR ) {
        var content_range = jqXHR.getResponseHeader("Content-Range");
        var new_start = content_range.split("-")[1];
        if (new_start > start) {
            start = new_start;
        }
        send_file_chunk(resumable_upload_url, file, start, chunk_size, 0);
    }
}

function slice(file, start, end) {
    var slice = file.mozSlice ? file.mozSlice :
                file.webkitSlice ? file.webkitSlice :
                file.slice ? file.slice : function() {};
    return slice.bind(file)(start, end);
}

async function send_file_chunk(resumable_upload_url, file, start, chunk_size, retries) {
    update_percentage(start, file.size);
    var file_size = file.size
    var end = start + chunk_size;
    if (end >= file_size) {
        end = file_size;
    }
    var data = slice(file, start, end);
    var headers = continue_upload_headers(file, start, end);
    var status_code_map = { 308: get_resume_upload_function(url, file, end, chunk_size) };
    var request = create_ajax_request('put', resumable_upload_url, data, headers, status_code_map);
    $.ajax(
        request
    ).done(function(data, textStatus, jqXHR){
        update_status('succeeded', JSON.stringify(data));
    }).fail(function(jqXHR, textStatus, errorThrown ) {
        if (jqXHR.status != 308) {
            resume_upload(resumable_upload_url, file, start, chunk_size, retries++);
        }
    });
}

async function resume_upload(resumable_upload_url, file, start, chunk_size, retries) {
    var headers = resume_upload_headers(file);
    var status_code_map = { 308: get_resume_upload_function(url, file, start, chunk_size) };
    var request = create_ajax_request('put', resumable_upload_url, '', headers, status_code_map);
    $.ajax(
        request
    ).done(function(data, textStatus, jqXHR){
        update_status('succeeded', JSON.stringify(data));
    }).fail(function(jqXHR, textStatus, errorThrown ) {
        if (retries >= 3) {
            update_status('failed', jqXHR.responseText || errorThrown);
        } else if (jqXHR.status != 308) {
            send_file_chunk(resumable_upload_url, file, start, chunk_size, retries++);
        }
    });
} 

function update_status(message, console_message) {
    console.log(console_message);
    $('#upload_progress').removeClass('uploading').addClass(message).text(message + '!').css('text-transform', 'capitalize');
}

function update_percentage(last_byte, file_size) {
    var percentage = Math.floor(last_byte / file_size * 100) ;
    $('#upload_progress').text('Uploading...' + percentage + '%');
}
