"""A job to run executable programs."""
import codecs
from subprocess import check_output, PIPE

from ._base import *


class ShellCommand(JobBase):
    info = {
        'job_class_name':    "Shell Command",
        'notes':             "This will run an OS command. The command is specified as a list of tokens. "
                             "Use at your own risk !",
        'arguments':         [{'type': 'list', 'description': 'tokenized command'}],
        'example_arguments': '["/usr/local/my_program", "--file", "/tmp/abc"]',
        'enabled':           False,
    }
    
    @report
    def run(self, *args, **kwargs):
        out = check_output(args, stderr=PIPE)
        return Section(cmd), Code(codecs.decode(out, "utf-8"))


class RawShellCommand(JobBase):
    info = {
        'job_class_name':    "Raw Shell Command",
        'notes':             "This will run an OS command. Use at your own risk !",
        'arguments':         [{'type': 'string', 'description': 'Executable path'}],
        'example_arguments': '["/usr/local/my_program", "--file", "/tmp/abc"]',
        'enabled':           False,
    }
    
    @report
    def run(self, *args, **kwargs):
        out = check_output(args[0], stderr=PIPE, shell=True)
        return Section(cmd), Code(codecs.decode(out, "utf-8"))

