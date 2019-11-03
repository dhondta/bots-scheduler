from ndscheduler.job import JobBase as OriginalJobBase
from tinyscript.report import *
from tinyscript.report import __features__


__all__ = ["JobBase", "report"] + __features__


DEFAULTS = {
    'job_class_string':  lambda c: "%s.%s" % (c.__module__, c.__name__),
    'notes':             "",
    'arguments':         [],
    'example_arguments': "",
    'report_title':      None,
}


def report(f):
    """ Method decorator for producing a report from a list of report items from
         tinyscript.report. """
    def _wrapper(self, *args, **kwargs):
        title = None
        for a in args:
            if isinstance(a, Title):
                title = a.html()
        title = title or self.__class__.meta_info().get('report_title')
        items = f(self, *args, **kwargs)
        if not isinstance(items, (tuple, list)):
            items = [items]
        options = {}
        if title:
            options['title'] = title
        return Report(*items, **options).html().replace("\n", "")
    return _wrapper


class JobBase(OriginalJobBase):
    """ JoBase enhancement for defining meta_info as a simple class attribute
         and handling default values. """
    @classmethod
    def meta_info(cls):
        d = getattr(cls, "info", {})
        for k, v in DEFAULTS.items():
            if k not in d.keys():
                d[k] = v(cls) if callable(v) else v
        return d
