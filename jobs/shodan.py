"""A job to run a Shodan search."""
from pybots import ShodanBot

from ._base import *


class ShodanHostsCheckJob(JobBase):
    info = {
        'job_class_name': "Shodan - Hosts and open services check",
        'notes': "This will perform a search on Shodan. You must specify an API key and a file with a list of IP "
                 "addresses or networks (in CIDR notation) to check for.",
        'arguments': [{'type': 'string', 'description': 'Shodan API key'},
                      {'type': 'string', 'description': 'Path to the list of IP addresses or networks'}],
        'example_arguments': '["API_KEY", "/path/to/ips.list"]',
    }

    @report
    def run(self, api_key, ips_path, **kwargs):
        with ShodanBot(api_key) as bot:
            result = bot.hosts_from_file(ips_path)
        hosts = OrderedDict()
        for host, data in sorted(result.items(), key=lambda x: ip2int(x[0])):
            hosts[host] = data
        return [Section("Hosts found on Shodan"), Data(hosts)]

