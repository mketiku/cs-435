import datetime, os, socket, sys

time_format = '%a, %d %b %Y %H:%M:%S'
req_time_format = '%Y-%m-%d %H:%M:%S.%f'
wwwroot = os.getcwd() + '/www'
allowed_types = {
    'html' : 'text/html',
    'css' : 'text/css',
    'js' : 'application/x-javascript',
    'jpg' : 'image/jpeg',
    'gif' : 'image/gif',
    'png' : 'image/png'
}

allowed_methods = {
    'GET'
}

def strip_headers(req):
    headers = {}
    for line in req.split('\n')[1:]:
        if line == '\r':
            break
        head_line = line.partition(':')
        headers[head_line[0].lower()] = head_line[2].strip()
    return headers

def file_modified(f):
    return os.path.getmtime(f)

def get_response(req):
    r = req.split('\n')[0]
    h = strip_headers(req)
    date = datetime.datetime.today().strftime(time_format)

    print('>  Request type:  {}'.format(r))

    if r != '':
        method = r.split(' ')[0]
        print(method)
        path = r.split(' ')[1]
    else:
        method = 'GET'
        path = '/'

    if path.endswith('/'):
        path = path + 'index.html'

    fullpath = wwwroot + path
    print('>  Requested path: www' + path)

    if method in allowed_methods:
        try:
            # Get Content-Type
            requested_file_type = os.path.splitext(fullpath)[1].replace('.','')
            if requested_file_type in allowed_types:
                content_type = allowed_types[requested_file_type]
            else:
                print('>  File type not found for: {}'.format(requested_file_type))
                content_type = allowed_types['html']

            # Get content
            with open(fullpath) as f:
                # Get modification date of requested path
                modify_date = datetime.datetime.fromtimestamp(file_modified(fullpath))

                # Check for 'if-modified-since' header
                if 'if-modified-since' in h:
                    try:
                        check_date = datetime.datetime.strptime(h['if-modified-since'], req_time_format)
                    except ValueError:
                        check_date = datetime.datetime.strptime(h['if-modified-since'], time_format)

                    # Check if file has changed
                    if ((check_date - modify_date) > datetime.timedelta(seconds=0)):
                        code = '304 Not Modified'
                        content = ''

                    # If not, send file
                    else:
                        code = '200 OK'
                        content = f.read()

                # If no 'if-modified-since' header, send file
                else:
                    check_date = date
                    code = '200 OK'
                    content = f.read()

        # If file is not found...
        except (IOError, OSError) as e:
            code = '404 Not Found'
            modify_date = date
            content_type = allowed_types['html']
            content = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>Not Found</h1>\n<p>The requested URL {} was not found on this server.</p>\n</body>\n</html>'.format(path)

    # If method is not allowed...
    else:
        code = '405 Method Not Allowed'
        modify_date = date
        content_type = allowed_types['html']
        content = ''

    # Combine all of the above and return response object
    print(">  Response code: {}\n".format(code))
    resp = 'HTTP/1.1 {}\nDate: {}\nLast-Modified: {}\nContent-Type: {}\n\n{}'.format(code, date, modify_date, content_type, content)
    # print('\n>  Response to send:\n' + resp)
    return resp

def main(argv):
    port = int(argv[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    print('Listening on port {} for connections...\n'.format(port))

    # Main loop
    while(True):
        connection, address = s.accept()
        message = connection.recv(1024).decode('UTF-8')

        # decode the message and send response
        resp = get_response(message)
        connection.send(resp)
        connection.close()

    # Cleanup
    s.shutdown(socket.SHUT_RDWR)
    s.close()

if __name__ == '__main__':
    # Check if port is specified
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        # If not, run on port 8080
        main([8080])
