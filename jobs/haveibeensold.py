"""A job to run a search on sold email using HaveIBeenSold."""
from pybots import HaveIBeenSoldBot

from ._base import *


class HaveIBeenSoldJob(JobBase):
    info = {
        'job_class_name':    "Have I Been Sold - Emails check",
        'notes':             "This will perform a search on HaveIBeenSold? against the provided file with a list of "
                             "emails that could have been sold to third parties.",
        'arguments':         [{'type': 'string', 'description': 'Path to the list of emails'}],
        'example_arguments': '"path/to/emails.list" or ["path/to/list1", "path/to/list2", ...]',
    }

    @report
    def run(self, emails_path, **kwargs):
        with HaveIBeenSoldBot() as bot:
            result = bot.check_from_file(emails_path)
        report = [Section("Email addresses found on HaveIBeenSold?")]
        report.append(List(*result) if len(result) > 0 else Text("None", color="green"))
        return report 

