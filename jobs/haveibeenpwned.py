"""A job to run a search on emails or domains using HaveIBeenPwned?."""
from botscheduler import *
from pybots import HaveIBeenPwnedBot, PwnedPasswordsBot


class HaveIBeenPwnedJob(JobBase):
    info = {
        'job_class_name': "Have I Been Pwned? - Breached domains check",
        'notes':          "This will perform a search on HaveIBeenPwned? against the provided file with a list of "
                          "emails or domains that could have been involved in recent data breaches.",
        'arguments':      [{'type': 'file', 'description': 'Path to the list of emails and/or domains'}],
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
                report.append(Table([[Data(d, size=12)]], row_headers=[img], column_headers=None))
        return report


class PwnedPasswordsJob(JobBase):
    info = {
        'job_class_name': "Have I Been Pwned? - Pwned passwords check",
        'notes':          "This will perform a search in the PwnedPasswords database on HaveIBeenPwned? against the "
                          "given passwords file for checking if they could have been involved in recent data breaches.",
        'arguments':      [{'type': 'file', 'description': 'Path to the list of passwords'}],
    }

    @report
    def run(self, passwords_path, **kwargs):
        with PwnedPasswordsBot() as bot:
            pwned = bot.check_from_file(passwords_path)
        return [Section("Pwned passwords found on HaveIBeenPwned?"), List(*pwned)]

