import requests
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
        return resp.headers.get('location')

    SessionRedirectMixin.get_redirect_target = get_redirect_target

    response = requests.get("https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz")


   # ret = with_session()
   # while not ret.ok:
   #     with_session()

#   if not response.ok:
#        print(response)
#        print(response.status_code)
#        print(response.content)
#    os.system("curl -vL  https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz --output /tmp/kk")
