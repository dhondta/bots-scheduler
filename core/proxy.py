import logging
from mitmproxy import addons
from mitmproxy.master import Master
from mitmproxy.tools import cmdline
from mitmproxy.tools.main import run
from multiprocessing import Process
from six import b


class AuthMaster(Master):
    """ Install the default addons and additional security features."""
    def __init__(self, opts):
        super().__init__(opts)
        self.addons.add(*addons.default_addons())  # this installs ProxyAuth
        self.addons.add(BlockHttp())
        self.addons.add(SecureHeaders())


class BlockHttp:
    """ Ensure that HTTP cannot be used. """
    def request(self, flow):
        if not flow.client_conn.tls_established:
            flow.reply.kill()


class SecureHeaders:
    """ Add HTTP secure headers to each response. """
    def response(self, flow):
        flow.response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        flow.response.headers['X-Content-Type-Options'] = "nosniff"
        flow.response.headers['X-Frame-Options'] = "DENY"
        flow.response.headers['X-XSS-Protection'] = "X-XSS-Protection: 1; mode=block"


def run_proxy(namespace):
    """ This function configures and starts a reverse authentication proxy.

    :param namespace: options' namespace
    """
    ns = namespace
    # configure and run the reverse proxy
    mitmlogger = logging.getLogger("mitmproxy.reverse.proxy")
    # 1. set the IP according to the chosen mode
    host = ["0.0.0.0", "127.0.0.1"][ns.local or ns.debug]
    # 2. if no htpasswd file provided, create one with the namespace._default_users
    if not ns.htpasswd:
        mitmlogger.debug("Generating the htpasswd file...")
        import bcrypt
        ns.htpasswd = ".htpasswd"
        with open(ns.htpasswd, 'wb') as f:
            for user in namespace.default_users:
                username, password = user.split(":")
                salt = bcrypt.gensalt()
                f.write(b("%s:%s") % (b(username), bcrypt.hashpw(b(password), salt)))
    # 3. setup the arguments for the proxy run function
    args = "--listen-host %s -p %d --proxyauth @%s --mode reverse:http://localhost:%d/" % \
           (host, ns.port, ns.htpasswd, ns.port + 1)
    if ns.certificate:
        args += " --certs %s" % ns.certificate
    # 4. now start the server as a separate process
    mitmlogger.info("Running proxy at {}:{} ...".format(host, ns.port))
    p = Process(target=run, args=(AuthMaster, cmdline.mitmproxy, args.split()))
    p.start()
    mitmlogger.info("*** You can access scheduler web ui at https://{}:{} ***".format(host, ns.port))
    return p

