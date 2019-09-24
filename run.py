from urllib.parse import urlparse, urljoin

import requests
from requests import *
from requests.exceptions import *
from requests._internal_utils import *
from requests.cookies import *
from requests.utils import *
import logging
import os


def with_session():
    class UTF8RedirectingSession(requests.Session):
        def get_redirect_target(self, resp):
            if resp.is_redirect:
                # print(resp.headers['location'])
                #print("\n\n return modified \n\n")
                #print(resp.headers['location'])
                #print(resp.headers['location'].__class__)
                tmp = resp.headers['location'].encode("ASCII").decode("utf-8") 
                print("HOLAAA")
                print(tmp)
                return tmp #.replace("%7E", "~").encode("latin1").decode("utf-8")
            return None

    with UTF8RedirectingSession() as session:
        headers = {}
        headers["Pragma"] = "Pragma: akamai-x-get-client-ip, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id"
        return session.get("https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz", headers=headers)

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    
    
    #response = requests.get("https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz")

    from requests.sessions import SessionRedirectMixin

    def get_redirect_target(self, resp):
        tmp = resp.headers.get('location')
        if tmp:
            print("TIPO: {}".format(tmp.__class__))
            print("VALOR: {}".format(tmp))
            return tmp


    def resolve_redirects(self, resp, req, stream=False, timeout=None,
                          verify=True, cert=None, proxies=None, yield_requests=False,
                          **adapter_kwargs):
        """Receives a Response. Returns a generator of Responses or Requests."""

        hist = []  # keep track of history

        print(".........")
        print(resp.headers.get("location"))
        url = self.get_redirect_target(resp)
        print(url)
        previous_fragment = urlparse(req.url).fragment
        while url:
            prepared_request = req.copy()

            # Update history and keep track of redirects.
            # resp.history must ignore the original request in this loop
            hist.append(resp)
            resp.history = hist[1:]

            try:
                resp.content  # Consume socket so it can be released
            except (ChunkedEncodingError, ContentDecodingError, RuntimeError):
                resp.raw.read(decode_content=False)

            if len(resp.history) >= self.max_redirects:
                raise TooManyRedirects('Exceeded %s redirects.' % self.max_redirects,
                                       response=resp)

            # Release the connection back into the pool.
            resp.close()

            # Handle redirection without scheme (see: RFC 1808 Section 4)
            if url.startswith('//'):
                parsed_rurl = urlparse(resp.url)
                url = '%s:%s' % (to_native_string(parsed_rurl.scheme), url)

            # Normalize url case and attach previous fragment if needed (RFC 7231 7.1.2)
            parsed = urlparse(url)
            if parsed.fragment == '' and previous_fragment:
                parsed = parsed._replace(fragment=previous_fragment)
            elif parsed.fragment:
                previous_fragment = parsed.fragment
            url = parsed.geturl()

            # Facilitate relative 'location' headers, as allowed by RFC 7231.
            # (e.g. '/path/to/resource' instead of 'http://domain.tld/path/to/resource')
            # Compliant with RFC3986, we percent encode the url.
            if not parsed.netloc:
                url = urljoin(resp.url, requote_uri(url))
            else:
                url = requote_uri(url)

            prepared_request.url = to_native_string(url)

            self.rebuild_method(prepared_request, resp)

            # https://github.com/requests/requests/issues/1084
            if resp.status_code not in (codes.temporary_redirect, codes.permanent_redirect):
                # https://github.com/requests/requests/issues/3490
                purged_headers = ('Content-Length', 'Content-Type', 'Transfer-Encoding')
                for header in purged_headers:
                    prepared_request.headers.pop(header, None)
                prepared_request.body = None

            headers = prepared_request.headers
            try:
                del headers['Cookie']
            except KeyError:
                pass

            # Extract any cookies sent on the response to the cookiejar
            # in the new request. Because we've mutated our copied prepared
            # request, use the old one that we haven't yet touched.
            extract_cookies_to_jar(prepared_request._cookies, req, resp.raw)
            merge_cookies(prepared_request._cookies, self.cookies)
            prepared_request.prepare_cookies(prepared_request._cookies)

            # Rebuild auth and proxy information.
            proxies = self.rebuild_proxies(prepared_request, proxies)
            self.rebuild_auth(prepared_request, resp)

            # A failed tell() sets `_body_position` to `object()`. This non-None
            # value ensures `rewindable` will be True, allowing us to raise an
            # UnrewindableBodyError, instead of hanging the connection.
            rewindable = (
                    prepared_request._body_position is not None and
                    ('Content-Length' in headers or 'Transfer-Encoding' in headers)
            )

            # Attempt to rewind consumed file-like object.
            if rewindable:
                rewind_body(prepared_request)

            # Override the original request.
            req = prepared_request

            if yield_requests:
                yield req
            else:

                resp = self.send(
                    req,
                    stream=stream,
                    timeout=timeout,
                    verify=verify,
                    cert=cert,
                    proxies=proxies,
                    allow_redirects=False,
                    **adapter_kwargs
                )

                extract_cookies_to_jar(self.cookies, prepared_request, resp.raw)

                # extract redirect url, if any, for the next loop
                url = self.get_redirect_target(resp)
                print(url)
                yield resp

    SessionRedirectMixin.get_redirect_target = get_redirect_target
    SessionRedirectMixin.resolve_redirects = resolve_redirects

    response = requests.get("https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz")


   # ret = with_session()
   # while not ret.ok:
   #     with_session()

#   if not response.ok:
#        print(response)
#        print(response.status_code)
#        print(response.content)
#    os.system("curl -vL  https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz --output /tmp/kk")
