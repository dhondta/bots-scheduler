"""A job to run a search on sold email using HaveIBeenSold."""
from pybots import GhostProjectBot

from ._base import *


class GhostProjectJob(JobBase):
    info = {
        'job_class_name':    "GhostProject - Emails check for known passwords",
        'notes':             "This will perform a search on GhostProject against the provided file with a list of "
                             "emails whose passwords may be publicly known.",
        'arguments':         [{'type': 'string', 'description': 'Path to the list of emails'}],
        'example_arguments': '"path/to/emails.list" or ["path/to/list1", "path/to/list2", ...]',
    }

    @report
    def run(self, emails_path, **kwargs):
        with GhostProjectBot() as bot:
            result = bot.check_from_file(emails_path)
        result = {k: ", ".join(_ for _ in v if _ != "") for k, v in result.items()}
        return [Section("Email addresses with known passwords found on GhostProject"), Data(result)] 

