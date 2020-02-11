function create_ajax_request(method, url, data={}, headers={}, status_code_map={}) {
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