"""Bots Scheduler's jobs.

Template:

```
from ._base import *


class TestJob(JobBase):
    info = {
        'job_class_name':    "This will be displayed as the job class name",
        'notes':             "This will do something",
        'arguments':         [],
        'example_arguments': "",
        'report_title':      "An example report",
    }

    @report
    def run(self, *args, **kwargs):
        # do something
        # compute report_items here
        return item1, item2, ...
```
"""
