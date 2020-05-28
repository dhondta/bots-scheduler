import sys
import traceback
from collections import OrderedDict
from ndscheduler.job import JobBase as OriginalJobBase
from tinyscript.report import *
from tinyscript.report import __features__


__all__ = ["JobBase", "OrderedDict", "report"] + __features__


DEFAULTS = {
    'job_class_string':  lambda c: "%s.%s" % (c.__module__, c.__name__),
    'job_class_name':    "New Job",
    'notes':             "",
    'arguments':         [],
    'example_arguments': "",
    'report_title':      None,
}


def report(f):
    """ Method decorator for producing a report from a list of report items from tinyscript.report. """
    def _wrapper(self, *args, **kwargs):
        items = f(self, *args, **kwargs)
        if not isinstance(items, (tuple, list)):
            items = [items]
        options = {'title': self.__class__.meta_info().get('report_title')}
        return Report(*items, **options).html()
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

