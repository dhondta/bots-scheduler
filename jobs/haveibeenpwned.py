"""A job to run a search on emails or domains using HaveIBeenPwned?."""
from pybots import HaveIBeenPwnedBot

from ._base import *


class HaveIBeenPwnedJob(JobBase):
    info = {
        'job_class_name':    "Have I Been Pwned? - Breached domains check",
        'notes':             "This will perform a search on HaveIBeenPwned? against the provided file with a list of "
                             "emails or domains that could have been involved in recent data breaches.",
        'arguments':         [{'type': 'string', 'description': 'Path to the list of emails and/or domains'}],
        'example_arguments': '["path/to/emails_or_domains.list"]',
    }

    @report
    def run(self, emails_domains_path, **kwargs):
        with HaveIBeenPwnedBot() as bot:
            results = bot.breaches_from_file(emails_domains_path)
        report = [Section("Breaches found on HaveIBeenPwned?")]
        for domain, breaches in results.items():
            report.append(Subsection(Code(domain, size=20)))
            for breach in breaches:
                report.append(Title(breach.pop('Title'), "h4"))
                d = OrderedDict()
                d['Description'] = breach.pop('Description')
                d['Breach date'] = breach.pop('BreachDate')
                d['Date added to HIBP'] = breach.pop('AddedDate').split("T")[0]
                d['Compromised accounts'] = breach.pop('PwnCount')
                d['Compromised data'] = ", ".join(breach.pop('DataClasses'))
                for k in ['Domain', 'ModifiedDate']:
                    breach.pop(k)
                flags = []
                for k in list(breach.keys()):
                    if k.startswith("Is"):
                        if breach.pop(k):
                            flags.append(k[2:].lower())
                d['Flags'] = ", ".join(flags).capitalize()
                img = Image(breach.pop('LogoPath'), width="80%")
                report.append(Table([[img, Data(d, size=12)]], column_headers=None))
        return report

