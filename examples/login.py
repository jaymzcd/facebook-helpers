from wsgiref.simple_server import make_server
from fbhelpers import FBHelper

def login_test(environ, start_response):
    if code is None:
        fb.start_login(permissions='publish_stream')
    else:
        errors = _check_errors()
        access_token = fb.post_authorize(code)
        return access_token
    return

httpd = make_server('', '8000', login_test)
httpd.serve_forever()
