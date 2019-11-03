"""A job to run executable programs."""
import codecs
from subprocess import check_output, PIPE

from .base import *


class Shell(JobBase):
    info = {
        'notes': "This will run an executable program. You can specify as many "
                 "arguments as you want. This job will pass these arguments to "
                 "the program in order.",
        'arguments': [{'type': 'string', 'description': 'Executable path'}],
        'example_arguments': '["/usr/local/my_program", "--file", "/tmp/abc"]',
    }
    
    @report
    def run(self, *args, **kwargs):
        out = check_output(args, stderr=PIPE)
        return "## `%s`" % " ".join(args), Code(codecs.decode(out, "utf-8"))
