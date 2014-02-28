from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.utils import DNS_NAME
import smtplib
from smtplib import SMTPException
from smtplib import _have_ssl
from smtplib import SSLFakeFile
import ssl


class SMTPExt(smtplib.SMTP):
    """
    This class extends smtplib.SMTP and overrides the starttls method
    allowing extra parameters and forwarding them to ssl.wrap_socket.
    """

    def starttls(self, keyfile=None, certfile=None, **kwargs):
        self.ehlo_or_helo_if_needed()
        if not self.has_extn("starttls"):
            raise SMTPException("STARTTLS extension not supported by server.")
        (resp, reply) = self.docmd("STARTTLS")
        if resp == 220:
            if not _have_ssl:
                raise RuntimeError("No SSL support included in this Python")
            self.sock = ssl.wrap_socket(self.sock, keyfile, certfile,
                                        **kwargs)
            self.file = SSLFakeFile(self.sock)
            # RFC 3207:
            # The client MUST discard any knowledge obtained from
            # the server, such as the list of SMTP service extensions,
            # which was not obtained from the TLS negotiation itself.
            self.helo_resp = None
            self.ehlo_resp = None
            self.esmtp_features = {}
            self.does_esmtp = 0
        return (resp, reply)


class SSLv3EmailBackend(EmailBackend):
    """
    Extends default EmailBackend and overrides open method to use
    SMTPExt.starttls() method, together with custom ssl.wrap_socket params
    """

    WRAP_SOCKET_PARAMS = {
        'ssl_version': ssl.PROTOCOL_SSLv3
    }

    def open(self):
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            # If local_hostname is not specified, socket.getfqdn() gets used.
            # For performance, we use the cached FQDN for local_hostname.
            self.connection = SMTPExt(self.host, self.port,
                                           local_hostname=DNS_NAME.get_fqdn())
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls(**self.WRAP_SOCKET_PARAMS)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise


class SSLv23EmailBackend(SSLv3EmailBackend):
    WRAP_SOCKET_PARAMS = {
        'ssl_version': ssl.PROTOCOL_SSLv23
    }


class SSLv2EmailBackend(SSLv3EmailBackend):
    WRAP_SOCKET_PARAMS = {
        'ssl_version': ssl.PROTOCOL_SSLv2
    }


class TLSv1EmailBackend(SSLv3EmailBackend):
    WRAP_SOCKET_PARAMS = {
        'ssl_version': ssl.PROTOCOL_TLSv1
    }
