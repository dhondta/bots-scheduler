<h1 align="center">Bots Scheduler <a href="https://twitter.com/intent/tweet?text=Bots Scheduler%20-%20A%20Web%20interface%20for%20scheduling%20cron-style%20OSINT%20tasks%20relying%20on%20Web%20services%20like%20Shodan,%20Censys%20or%20HaveIBeenPwned.%0D%0Ahttps%3a%2f%2fgithub%2ecom%2fdhondta%2fbots-scheduler%0D%0A&hashtags=python,cybersecurity,bots,infosec,webserver,cron,osint,taskscheduler,shodan,censys,haveibeenpwned"><img src="https://img.shields.io/badge/Tweet--lightgrey?logo=twitter&style=social" alt="Tweet" height="20"/></a></h1>
<h3 align="center">Schedule your OSINT task the Cron way with a Web interface.</h3>

[![Read The Docs](https://readthedocs.org/projects/bots-scheduler/badge/?version=latest)](https://bots-scheduler.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/dhondta/bots-scheduler.svg?branch=master)](https://travis-ci.com/dhondta/bots-scheduler)
[![Requirements Status](https://requires.io/github/dhondta/bots-scheduler/requirements.svg?branch=master)](https://requires.io/github/dhondta/bots-scheduler/requirements/?branch=master)
[![Known Vulnerabilities](https://snyk.io/test/github/dhondta/bots-scheduler/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/dhondta/bots-scheduler?targetFile=requirements.txt)
[![License](https://img.shields.io/badge/license-AGPL%20v3-lightgrey.svg)](https://github.com/dhondta/bots-scheduler/blob/master/LICENSE)

This application is a scheduling system based on [Nextdoor Scheduler](https://github.com/Nextdoor/ndscheduler/) that uses jobs templated upon [PyBots](https://github.com/dhondta/pybots/). It especially focuses on tasks derived from security-related Web services like Shodan or Censys. Additionally, it protects the original Web server from Nextdoor with an authentication proxy based on [mitmproxy](https://github.com/mitmproxy/mitmproxy/).

```sh
$ git clone https://github.com/dhondta/bots-scheduler.git
$ cd bots-scheduler
$ ./bots-scheduler reset
<<< adapt conf/db.ini and conf/smtp.ini >>>
```

## :sunglasses: Demonstrations

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/running-the-server.gif" alt="Running the server from the command line"></p>

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/auth-proxy.gif" alt="Authenticating with the reverse proxy"></p>

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/presentation.gif" alt="Browsing the WUI panels"></p>

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/adding-and-running-jobs.gif" alt="Adding and running a job, inspecting the report"></p>


## :clap:  Supporters

[![Stargazers repo roster for @dhondta/bots-scheduler](https://reporoster.com/stars/dark/dhondta/bots-scheduler)](https://github.com/dhondta/bots-scheduler/stargazers)

[![Forkers repo roster for @dhondta/bots-scheduler](https://reporoster.com/forks/dark/dhondta/bots-scheduler)](https://github.com/dhondta/bots-scheduler/network/members)

<p align="center"><a href="#"><img src="https://img.shields.io/badge/Back%20to%20top--lightgrey?style=social" alt="Back to top" height="20"/></a></p>
