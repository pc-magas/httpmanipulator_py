from common.constants.http import http_status_code_as_string

def up(conn):
    print(http_status_code_as_string)

def down(conn):
    print("DOWN "+http_status_code_as_string)
