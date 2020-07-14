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


def _load_mail_config(config_path, *profiles):
    """ SMTP configuration file load function. """
    global MAIL_CONFIG, MAIL_PROFILES
    MAIL_CONFIG = configparser.ConfigParser()
    MAIL_CONFIG.read(config_path)
    MAIL_PROFILES = profiles


def report(f):
    """ Method decorator for producing a report from a list of report items from tinyscript.report. """
    @wraps(f)
    def _wrapper(self, *args, **kwargs):
        items = f(self, *args, **kwargs)
        if not isinstance(items, (tuple, list)):
            items = [items]
        subject = self.__class__.meta_info().get('report_title')
        if subject:
            items.insert(0, Section(subject))
        else:
            subject = items[0]._data
        for profile in MAIL_PROFILES:
            try:
                from_mail = MAIL_CONFIG.get(profile, "from")
            except ini.NoSectionError:
                logger.error("No profile '%s'" % profile)
            try:
                to_mail   = MAIL_CONFIG.get(profile, "to")
                body = Report(*items[1:]).html()
                kwargs['server'] = (MAIL_CONFIG.get(profile, "hostname"), MAIL_CONFIG.get(profile, "port"))
                try:
                    kwargs['auth'] = (MAIL_CONFIG.get(profile, "user"), MAIL_CONFIG.get(profile, "password"))
                except ini.NoOptionError:
                    pass
                try:
                    kwargs['security'] = MAIL_CONFIG.get(profile, "security")
                except ini.NoOptionError:
                    pass
                send_mail(from_mail, to_mail, subject, body, **kwargs)
            except ini.Error:
                logger.error("Could not send email with profile '%s'" % profile)
        try:
            return Report(*items).html()
        except:
            logger.error("Could not generate report")
    return _wrapper


class JobBase(OriginalJobBase):
    """ JoBase enhancement for defining meta_info as a simple class attribute and handling default values. """
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

