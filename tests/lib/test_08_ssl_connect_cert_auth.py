# Test whether a client produces a correct connect and subsequent disconnect when using SSL.
# Client must provide a certificate.
import pytest

import tests.paho_test as paho_test
from tests.paho_test import ssl

# The client should connect with keepalive=60, clean session set,
# and client id 08-ssl-connect-crt-auth
# It should use the CA certificate ssl/all-ca.crt for verifying the server.
# The test will send a CONNACK message to the client with rc=0. Upon receiving
# the CONNACK and verifying that rc=0, the client should send a DISCONNECT
# message. If rc!=0, the client should exit with an error.

connect_packet = paho_test.gen_connect("08-ssl-connect-crt-auth", keepalive=60)
connack_packet = paho_test.gen_connack(rc=0)
disconnect_packet = paho_test.gen_disconnect()


@pytest.mark.skipif(ssl is None, reason="no ssl module")
def test_08_ssl_connect_crt_auth(ssl_server_socket, start_client):
    start_client("08-ssl-connect-cert-auth.py")

    (conn, address) = ssl_server_socket.accept()
    conn.settimeout(10)

    paho_test.expect_packet(conn, "connect", connect_packet)
    conn.send(connack_packet)

    paho_test.expect_packet(conn, "disconnect", disconnect_packet)

    conn.close()
