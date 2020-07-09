"""A job to run executable programs."""
import codecs
from botscheduler import *
from subprocess import check_output, PIPE


class ShellCommand(JobBase):
    info = {
        'job_class_name':    "Shell Command",
        'notes':             "This will run an OS command. The command is specified as a list of tokens. "
                             "Use at your own risk !",
        'arguments':         [{'type': 'list', 'description': 'Tokenized OS command'}],
        'example_arguments': '["/usr/local/my_program", "--file", "/tmp/abc"]',
        'enabled':           True,
    }
    
    @report
    def run(self, *args, **kwargs):
        out = check_output(args, stderr=PIPE)
        return Section(" ".join(args)), Code(codecs.decode(out, "utf-8"))


class RawShellCommand(JobBase):
    info = {
        'job_class_name':    "Raw Shell Command",
        'notes':             "This will run an OS command. Use at your own risk !",
        'arguments':         [{'type': 'string', 'description': 'OS command as a string'}],
        'example_arguments': "/usr/local/my_program --file /tmp/abc",
        'enabled':           False,
    }
    
    @report
    def run(self, *args, **kwargs):
        out = check_output(args[0], stderr=PIPE, shell=True)
        return Section(args[0]), Code(codecs.decode(out, "utf-8"))

