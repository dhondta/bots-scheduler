"""A job to run a search against the list of data breaches of NuclearLeaks."""
from botscheduler import *
from pybots import NuclearLeaksBot


class NuclearLeaksJob(JobBase):
    info = {
        'job_class_name': "NuclearLeaks - Breached domains check",
        'notes':          "This will perform a search on NuclearLeaks' list against the provided file with a list of"
                          " emails or domains that could have been involved in data breaches.",
        'arguments':      [{'type': 'file', 'description': 'Path to the list of emails and/or domains'}],
    }

    @report
    def run(self, emails_domains_path, **kwargs):
        with NuclearLeaksBot() as bot:
            self._data = bot.breaches_from_file(emails_domains_path)
        report = [Section("Breaches found on NuclearLeaks")]
        for domain, breaches in self._data.items():
            report.append(Subsection(Code(domain, size=20)))
            for breach in breaches:
                report.append(Title(breach.pop('database'), "h4"))
                d = OrderedDict()
                for k in ['entries', 'hashing_algorithm', 'category', 'dump_date', 'acknowledged']:
                    d[k.replace("_", " ").title()] = breach.pop(k)
                report.append(Data(d, size=12))
        return report

