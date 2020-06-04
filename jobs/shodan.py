"""A job to run a Shodan search."""
from pybots import ShodanBot

from ._base import *


class ShodanJob(JobBase):
    info = {
        'notes': "This will perform a search on Shodan. You can specify as many arguments as you want. "
                 "This job will pass these arguments to the program in order.",
        'arguments': [{'type': 'string', 'description': 'Executable path'}],
        'example_arguments': '["/usr/local/my_program", "--file", "/tmp/abc"]',
    }

    @report
    def run(self, *args, **kwargs):

        return "## `%s`" % " ".join(args), Code(codecs.decode(out, "utf-8"))
