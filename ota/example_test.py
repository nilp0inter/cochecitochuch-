import http.server
import multiprocessing
import os
import re
import socket
import ssl
import sys

server_cert = """-----BEGIN CERTIFICATE-----
MIIFZTCCA02gAwIBAgIUXK+WezXG7FUkQ9lav8yXftunBBswDQYJKoZIhvcNAQEL
BQAwQjELMAkGA1UEBhMCWFgxFTATBgNVBAcMDERlZmF1bHQgQ2l0eTEcMBoGA1UE
CgwTRGVmYXVsdCBDb21wYW55IEx0ZDAeFw0yMjA0MTUyMzAxMTBaFw0yMzA0MTUy
MzAxMTBaMEIxCzAJBgNVBAYTAlhYMRUwEwYDVQQHDAxEZWZhdWx0IENpdHkxHDAa
BgNVBAoME0RlZmF1bHQgQ29tcGFueSBMdGQwggIiMA0GCSqGSIb3DQEBAQUAA4IC
DwAwggIKAoICAQDUwOqSwngel8+/v4pLMZViT/eZ2TVA+63tvA1KM4h8pIXy6q5W
XWuFJD+moAMKafXYLYd+6kOtCDxg2zSBkdFmUnZpSk5LrBs3cc9RTLjTYy+ErEHZ
Z+LfhordgM7KF4d3UhD8EMqnumseAqPTASl6++6hrn5ZEUpIThJKF/aKHvLjDo+F
KUrdCCzQ6W/tnLIm+1n11rujHl8Rn4NkNYjHXCcv3DYwnqn8KLzu4eFY4gM3rEsx
lDDui/EIvVvMgYsEfWsR3j27jXdzXiCmTBZY3qq5NVw3TFftfztsli2N0HB0MFvm
O+ve3icZxKeZRhRatM4RtBJ2LiNGlDJ8mlrRl8SuTZz2N/qxAC3djlGAsXDcN4M4
JlQ0wymnmpFkgmysDOrVZMXgdQeF0Lbd0alAsnkZXX5VDkuAEy8fWWF7nYlR4dct
jBw++UrxB54Op/JOyPwFKq8lBBv4EvTmgzq61oxWII3uepc0QNr3NVWhBpyQgP1N
OFhXrOEI5l1aQAXkbl5qFPVp3Qgqc1x3OT98T0hJbN06C+8oiM+i39tfiqLoErUS
ddxey92JS8pEXXlT2sA7EzhytKDFRjXUrNebEZXwT6mNIn6YsiuVXm7YNC9mhMVj
0cOi1ex1YhAZJ7OYRMwGmChGcjP19dWXQqvDvUJ75lEqQxCCw/zvxd5lgQIDAQAB
o1MwUTAdBgNVHQ4EFgQUHcvIdMbdmOmVoedvK1cDDR/xlbIwHwYDVR0jBBgwFoAU
HcvIdMbdmOmVoedvK1cDDR/xlbIwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0B
AQsFAAOCAgEAkSKJhqLaZitWYmS7Aw+amU+ql7BruqCwCceCK+FITn7Q629gofvR
PeFZ2VhZwPOAmrBTuxPxHlLVrVOikdhiBOELsGGYrH8m4PMK414srzP+BpQY+lx+
FXAbiAGhHdO95j7KRgbbGQNs6Nmjgoc/dcXA19/JSncykRXdnMzDVPvsq4JnWNx8
+Qa3Y1fS+xBr/rkJ0shgtJ9/xKgvmxBbcdRXmqg0yRA7KCQBy4vBUVasQPM83Fx6
6Sn3ITXe6A3R2BGLr2JYcLhSJWtBPfiI1+1/fAht2nlnJIH9v9mUsnm29OAzvv9S
eUWFiEhymuzq5t9gztya6jKhIC7vanTCc9WCq4+ps15GN3j75m7BEhfVSty3vLkD
6XwuW9bb9q83x2JdYb2F4x8gtvTZVnuwXB1xu5cKk9+kM0NUdVgcWmSOMYJ5jpsH
V0HakzLtINI5fLUVMeyiJxerVszjy1xGrtmJC9VikaV5TH9DdwR8PP1HvgLDtsO6
Y6zlEhzoRWKVXzciFQPlwSRENi1JRf2fxjLGYK0BUk+lmXJmuBDxzxzxiPd/za+g
ZF9rqWcsBSOmf2TK5aK/HJDg8vMPw08egw+0l0kiB/7MW9ysFbVykHakf6e+mNsT
CBiSi58x4hI/dsAff04uaeHDc0ymKkMYJBJtIZ9i/vKEL+VIGPOTF70=
-----END CERTIFICATE-----"""

server_key = """-----BEGIN ENCRYPTED PRIVATE KEY-----
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
7w4IHWeidM0+ZvhNTVQ0SA==
-----END ENCRYPTED PRIVATE KEY-----"""

def get_my_ip():
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.connect(('8.8.8.8', 80))
    my_ip = s1.getsockname()[0]
    s1.close()
    return my_ip


def get_server_status(host_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_status = sock.connect_ex((host_ip, server_port))
    sock.close()
    if server_status == 0:
        return True
    return False


def start_https_server(ota_image_dir, server_ip, server_port, server_file=None, key_file=None):
    os.chdir(ota_image_dir)

    if server_file is None:
        server_file = os.path.join(ota_image_dir, 'server_cert.pem')
        cert_file_handle = open(server_file, 'w+')
        cert_file_handle.write(server_cert)
        cert_file_handle.close()

    if key_file is None:
        key_file = os.path.join(ota_image_dir, 'server_key.pem')
        key_file_handle = open('server_key.pem', 'w+')
        key_file_handle.write(server_key)
        key_file_handle.close()

    httpd = http.server.HTTPServer((server_ip, server_port), http.server.SimpleHTTPRequestHandler)

    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile=key_file,
                                   certfile=server_file, server_side=True)
    httpd.serve_forever()


if __name__ == '__main__':
    if sys.argv[2:]:    # if two or more arguments provided:
        # Usage: example_test.py <image_dir> <server_port> [cert_di>]
        this_dir = os.path.dirname(os.path.realpath(__file__))
        bin_dir = os.path.join(this_dir, sys.argv[1])
        port = int(sys.argv[2])
        cert_dir = os.path.join(this_dir, 'server_certs')  # optional argument
        print('Starting HTTPS server at "https://:{}"'.format(port))
        start_https_server(bin_dir, '0.0.0.0', port,
                           server_file=os.path.join(cert_dir, 'cert.pem'),
                           key_file=os.path.join(cert_dir, 'key.pem'))