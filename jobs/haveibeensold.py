"""A job to run a search on sold email using HaveIBeenSold."""
from botscheduler import *
from pybots import HaveIBeenSoldBot


class HaveIBeenSoldJob(JobBase):
    info = {
        'job_class_name': "Have I Been Sold - Emails check",
        'notes':          "This will perform a search on HaveIBeenSold? against the provided file with a list of "
                          "emails that could have been sold to third parties.",
        'arguments':      [{'type': 'file', 'description': 'Path to the list of emails'}],
    }

    @report
    def run(self, emails_path, **kwargs):
        with HaveIBeenSoldBot() as bot:
            result = bot.check_from_file(emails_path)
        report = [Section("Email addresses found on HaveIBeenSold?")]
        report.append(List(*result) if len(result) > 0 else Text("None", color="green"))
        return report 

