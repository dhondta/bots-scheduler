"""Bots Scheduler's jobs.

Template:

```
from .base import *


class TestJob(JobBase):
    info = {
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
