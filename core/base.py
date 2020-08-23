import logging
import socket
import struct
import sys
import traceback
from collections import OrderedDict
from functools import wraps
from ndscheduler.job import JobBase as OriginalJobBase
from tinyscript import configparser
from tinyscript.helpers import send_mail
from tinyscript.report import *
from tinyscript.report import __features__
try:
    import ConfigParser as ini
except ImportError:
    import configparser as ini


__all__ = ["JobBase", "OrderedDict", "ip2int", "report"] + __features__


DEFAULTS = {
    'job_class_string':  lambda c: "%s.%s" % (c.__module__, c.__name__),
    'job_class_name':    "New Job",
    'notes':             "",
    'arguments':         [],
    'example_arguments': "",
    'report_title':      None,
    'enabled':           True,
}
MAIL_CONFIG = None
MAIL_PROFILES = []


ip2int = lambda a: struct.unpack("!I", socket.inet_aton(a))[0]

logger = logging.getLogger(__name__)


def _load_mail_config(config, *profiles):
    """ SMTP configuration file load function. """
    global MAIL_CONFIG, MAIL_PROFILES
    MAIL_CONFIG = config
    MAIL_PROFILES = profiles


def email(profile, items):
    """ Function for sending a notification email. """
    global MAIL_CONFIG
    c = MAIL_CONFIG
    if not c.has_section(profile):
        logger.error("No profile '%s'" % profile)
        return
    # mandatory parameters
    for option in ["from", "to", "hostname", "port"]:
        if not c.has_option(profile, option):
            logger.error("Missing option '%s'" % option)
            return
    kwargs = {}
    kwargs['server'] = (c.get(profile, "hostname"), int(c.get(profile, "port")))
    kwargs['content_type'] = "html"
    # optional SMTP parameters
    try:
        kwargs['security'] = c.get(profile, "security")
    except ini.NoOptionError:
        pass
    try:
        kwargs['auth'] = (c.get(profile, "user"), c.get(profile, "password"))
    except ini.NoOptionError:
        pass
    try:
        send_mail(c.get(profile, "from"), c.get(profile, "to"), items[0]._data, Report(*items[1:]).html(), **kwargs)
    except Exception as e:
        logger.error("Could not send email with profile '%s' (%s)" % (profile, str(e)))


def report(f):
    """ Method decorator for producing a report from a list of report items from tinyscript.report. """
    @wraps(f)
    def _wrapper(self, *args, **kwargs):
        global MAIL_PROFILES
        items = f(self, *args, **kwargs)
        if not isinstance(items, (tuple, list)):
            items = [items]
        title = self.__class__.meta_info().get('report_title')
        if title:
            items.insert(0, Section(title))
        # trigger email notification based on an explicit flag or on non-empty data set as an attribute to the job
        if getattr(self, "_notify", len(getattr(self, "_data", [])) > 0):
            for profile in MAIL_PROFILES:
                email(profile, items)
        try:
            return Report(*items).html()
        except:
            logger.error("Could not generate report")
    return _wrapper


class JobBase(OriginalJobBase):
    """ JobBase enhancement for defining meta_info as a simple class attribute and handling default values. """
    @classmethod
    def get_failed_result(cls):
        error = "".join(traceback.format_exception(*sys.exc_info()))
        return Report(Title("Unexpected Error", color="red"), Code(error, size=11)).html()
    
    @classmethod
    def get_scheduled_error_result(cls):
        return JobBase.get_failed_result()
    
    @classmethod
    def meta_info(cls):
        d = getattr(cls, "info", {})
        for k, v in DEFAULTS.items():
            if k not in d.keys():
                d[k] = v(cls) if callable(v) else v
        return d

