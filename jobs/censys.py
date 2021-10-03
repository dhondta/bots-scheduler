"""A job to run a Censys search."""
from botscheduler import *
from pybots import CensysBot


class CensysHostsCheckJob(JobBase):
    info = {
        'job_class_name': "Censys - Hosts and open ports check",
        'notes':          "This will perform a search on Censys. You must specify API credentials (ID and secret) and a"
                          " file with a list of IP addresses or networks (in CIDR notation) to check for.",
        'arguments':      [{'type': 'string', 'description': 'Censys API identifier'},
                           {'type': 'string', 'description': 'Censys API secret'},
                           {'type': 'file', 'description': 'Path to the list of IP addresses or networks'}],
    }

    @report
    def run(self, api_id, api_secret, ips_path, **kwargs):
        with CensysBot(api_id, api_secret) as bot:
            self._data = bot.hosts_from_file(ips_path)
        hosts = OrderedDict()
        for host, data in sorted(self._data.items(), key=lambda x: ip2int(x[0])):
            hosts[host] = data
        return [Section("Hosts found on Censys"), Data(hosts)]


class CensysHostsEnumeration(JobBase):
    info = {
        'job_class_name': "Censys - Hosts enumeration from available certificates",
        'notes':          "This will perform a search on Censys for hostnames contained in public certificates. You "
                          "must specify API credentials (ID and secret) and a file with a list of domain names.",
        'arguments':      [{'type': 'string', 'description': 'Censys API identifier'},
                           {'type': 'string', 'description': 'Censys API secret'},
                           {'type': 'file', 'description': 'Path to the list of domain names'}],
    }

    @report
    def run(self, api_id, api_secret, domains_path, **kwargs):
        with CensysBot(api_id, api_secret) as bot:
            self._data = bot.hosts_from_domains_file(domains_path)
        hosts = OrderedDict()
        for host, data in sorted(self._data.items(), key=lambda x: x[0]):
            hosts[host] = data
        return [Section("Hosts found from certificates via Censys"), Data(hosts)]

