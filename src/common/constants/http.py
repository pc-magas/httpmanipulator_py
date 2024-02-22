# Redirect status Codes
http_redirect = [300, 301, 302, 303, 304, 305, 306, 307, 308]

success_status_codes = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209]

error_status_codes = [
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
    410, 411, 412, 413, 414, 415, 416, 417, 418, 421,
    422, 423, 424, 425, 426, 427, 428, 429, 431, 451,
    500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
]

http_status_code = [
    100, 101, 102, 103,
    *success_status_codes,
    *http_redirect,
    305, 306,
    *error_status_codes
]

http_methods = ['GET', 'PUT', 'POST', 'PATCH', 'HEAD', 'OPTIONS', 'DELETE']

http_status_code_as_string = ','.join(map(str, http_status_code))
http_methods_as_string_quoted = ','.join(map(lambda x: f"'{x}'", http_methods))

no_301_302_http_methods = ['PUT', 'POST', 'PATCH']

# Exporting variables
http_status_code,
http_redirect,
success_status_codes,
error_status_codes,
http_status_code_as_string,
http_methods,
http_methods_as_string_quoted,
no_301_302_http_methods