"""A job to run executable programs."""
import codecs
from subprocess import check_output, PIPE

from ._base import *


class Shell(JobBase):
    info = {
        'job_class_name':    "Shell Command",
        'notes':             "This will run an executable program. You can specify a list of arguments.",
        'arguments':         [{'type': 'string', 'description': 'Executable path'}],
        'example_arguments': '["/usr/local/my_program", "--file", "/tmp/abc"]',
        'enabled':           False,  # enable at own risk
    }
    
    @report
    def run(self, *args, **kwargs):
        cmd = args[0]
        out = check_output(cmd, stderr=PIPE, shell=True)
        return Section(cmd), Code(codecs.decode(out, "utf-8"))

