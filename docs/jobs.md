!!! note "This page is for users"
    
    This page presents the available jobs and their parameters. It is aimed to show to a user of the WUI how to use these jobs.
    
    If you want sysadmin-oriented information, please consult [the related page](server.html). For developer-oriented information, please consult [the other related page](howto.html).

-----

## Shell

!!! danger "Not enabled by default"
    
    Due to the obvious dangerousness of letting a user trigger OS commands, the following jobs are **disabled by default**. These can be enabled by editing the jobs and setting the `info` key `enabled` to `True`.


This module contains two jobs:

- *Shell Command*: It runs an OS command tokenized into a list of arguments.

<p align="center"><img src="img/job_shell-command.png" alt="Shell Command"></p>

- *Raw Shell Command*: It runs a raw OS command.

<p align="center"><img src="img/job_raw-shell-command.png" alt="Raw Shell Command"></p>

-----

## Censys

This module contains one job:

- *Censys - Hosts and open ports check*: It checks a list of IP addresses and networks (in CIDR notation) for publicly accessible ports.

<p align="center"><img src="img/job_censys-hosts-ports-check.png" alt="Censys - Hosts and open ports check"></p>

!!! warning "API ID and secret required"
    
    This job requires that you subscribe on [Censys](https://censys.io/) and that you ask for an API identifier and secret.

## GhostProject

This module contains one job:

- *GhostProject - Emails check for known passwords*: It checks a list of email addresses for publicly associated passwords.

<p align="center"><img src="img/job_ghostproject-emails-check.png" alt="GhostProject - Emails check for known passwords"></p>

## Have I Been Pwned?

This module contains two jobs:

- *Have I Been Pwned? - Breached domains check*: It checks a list of email addresses or domains for known data breaches (having leaked addresses and passwords).

<p align="center"><img src="img/job_hibp-emails-check.png" alt="Have I Been Pwned? - Breached domains check"></p>

- *Have I Been Pwned? - Pwned passwords check*: It checks a list of passwords for publicly known ones.

<p align="center"><img src="img/job_hibp-emails-check.png" alt="Have I Been Pwned? - Pwned passwords check"></p>

!!! note "k-Anonymity"
    
    This [service](https://haveibeenpwned.com/API/v3#PwnedPasswords) uses [k-anonymity](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/) to preserve privacy and prevent linking submitted passwords by only using the first 5 characters of the SHA1 hash.

## Have I Been Sold?

This module contains one job:

- *Have I Been Sold - Emails check*: It checks a list of email addresses against a database of publicly sold emails (e.g. for advertising).

<p align="center"><img src="img/job_hibs-emails-check.png" alt="Have I Been Sold - Emails check"></p>


## Nuclear Leaks

This module contains one job:

- *NuclearLeaks - Breached domains check*: It checks a list of domains for known data breaches (having leaked addresses and passwords).

<p align="center"><img src="img/job_nuclearleaks-domains-check.png" alt="NuclearLeaks - Breached domains check"></p>

## Shodan

This module contains one job:

- *Shodan - Hosts and open services check*: It checks a list of IP addresses and networks (in CIDR notation) for publicly accessible services. It is more detailed than the job *Censys - Hosts and open ports check*.

<p align="center"><img src="img/job_shodan-hosts-ports-check.png" alt="Shodan - Hosts and open services check"></p>

!!! warning "API key required"
    
    This job requires that you subscribe on [Shodan](https://shodan.io/) and that you purchase an API key.

