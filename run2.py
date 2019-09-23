import requests
import logging
import os
import http.client 

http.client.HTTPConnection.debuglevel = 5

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(1)
requests_log.propagate = True

requests.get("https://api.bintray.com:443/conan/conan/conan-center/v1/files/conan/OpenSSL/1.1.1c/stable/0/package/8f5c5dedfae9faebaa2d65d5c8f43d2ec7d219de/0/conan_package.tgz")

