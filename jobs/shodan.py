"""A job to run a Shodan search."""
from botscheduler import *
from pybots import ShodanBot


class ShodanHostsCheckJob(JobBase):
    info = {
        'job_class_name': "Shodan - Hosts and open services check",
        'notes':          "This will perform a search on Shodan. You must specify an API key and a file with a list of "
                          "IP addresses or networks (in CIDR notation) to check for.",
        'arguments':      [{'type': 'string', 'description': 'Shodan API key'},
                           {'type': 'file', 'description': 'Path to the list of IP addresses or networks'}],
    }

    @report
    def run(self, api_key, ips_path, **kwargs):
        with ShodanBot(api_key) as bot:
            self._data = bot.hosts_from_file(ips_path)
        hosts = OrderedDict()
        for host, data in sorted(self._data.items(), key=lambda x: ip2int(x[0])):
            hosts[host] = data
        return [Section("Hosts found on Shodan"), Data(hosts)]

