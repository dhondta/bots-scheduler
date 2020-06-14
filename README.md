[![Read The Docs](https://readthedocs.org/projects/bots-scheduler/badge/?version=latest)](https://bots-scheduler.readthedocs.io/en/latest/?badge=latest)
[![Requirements Status](https://requires.io/github/dhondta/bots-scheduler/requirements.svg?branch=master)](https://requires.io/github/dhondta/bots-scheduler/requirements/?branch=master)
[![Known Vulnerabilities](https://snyk.io/test/github/dhondta/bots-scheduler/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/dhondta/bots-scheduler?targetFile=requirements.txt)
[![License](https://img.shields.io/badge/license-AGPL%20v3-lightgrey.svg)](https://github.com/dhondta/bots-scheduler/blob/master/LICENSE)

# Bots Scheduler

This application is a scheduling system based on [Nextdoor Scheduler](https://github.com/Nextdoor/ndscheduler) that uses jobs templated upon [PyBots](https://github.com/dhondta/pybots). It especially focuses on tasks derived from security-related Web services like Shodan or Censys. Additionally, it protects the original Web server from Nextdoor with an authentication proxy based on [mitmproxy](https://github.com/mitmproxy/mitmproxy).

## Installation

```sh
$ git clone https://github.com/dhondta/bots-scheduler.git
$ cd bots-scheduler
```

## Demonstrations

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/running-the-server.gif" alt="Running the server from the command line"></p>

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/auth-proxy.gif" alt="Authenticating with the reverse proxy"></p>

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/presentation.gif" alt="Browsing the WUI panels"></p>

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/bots-scheduler/master/docs/demos/adding-and-running-jobs.gif" alt="Adding and running a job, inspecting the report"></p>

## Usage

```sh
$ ./bots-scheduler --help
BotsScheduler 1.1.2
Author   : Alexandre D'Hondt
Copyright: © 2020 A. D'Hondt
License  : GNU Affero General Public License v3.0
Reference: https://github.com/Nextdoor/ndscheduler
Source   : https://github.com/dhondta/bots-scheduler

This tool is a launcher for the Nextdoor Scheduler with a set of jobs based on robots made with PyBots
 (https://github.com/dhondta/python-pybots).
Moreover, it provides authentication through the use of an integrated reverse proxy.

usage: ./bots-scheduler [-h] [--help] [-v] {run,clean} ...

positional arguments:
  {run,clean}  command to be executed
    run        run the server
    clean      remove server's virtual environment


extra arguments:
  -h             show usage message and exit
  --help         show this help message and exit
  -v, --verbose  verbose mode (default: False)

```

This help shows 2 commands:

1. `run`: for running the application
2. `clean`: for cleaning the virtual environment

```sh
BotsScheduler 1.1.2
Author   : Alexandre D'Hondt
Copyright: © 2020 A. D'Hondt
License  : GNU Affero General Public License v3.0
Reference: https://github.com/Nextdoor/ndscheduler
Source   : https://github.com/dhondta/bots-scheduler

This tool is a launcher for the Nextdoor Scheduler with a set of jobs based on robots made with PyBots
 (https://github.com/dhondta/python-pybots).
Moreover, it provides authentication through the use of an integrated reverse proxy.

usage: ./bots-scheduler run [-h] [--help] [-d] [-j JOBS] [-l] [-p PORT]
                            [--dbms {sqlite,postgresql,mysql}]
                            [--db-config DB_CONFIG]
                            [--executions-table EXECUTIONS_TABLE]
                            [--jobs-table JOBS_TABLE]
                            [--logs-table LOGS_TABLE] [--job-coalesce]
                            [--job-max-instances JOB_MAX]
                            [--job-misfire JOB_MISFIRE]
                            [--threadpool-size TP_SIZE] [--timezone TIMEZONE]
                            [--max-workers TWORKERS]
                            [--certificate CERTIFICATE] [--htpasswd HTPASSWD]



extra arguments:
  -h      show usage message and exit
  --help  show this help message and exit

base options:
  -d, --debug           run the server in debug mode (default: False)
  -j JOBS, --jobs JOBS  folder with jobs to be imported (default: ['jobs'])
  -l, --local           force running the server locally (default: False)
  -p PORT, --port PORT  server's port number (default: 8888)
                         NB: this will be the listening port of the proxy, this of the scheduler will be port+1

database options:
  --dbms {sqlite,postgresql,mysql}
                        database management system (default: sqlite)
  --db-config DB_CONFIG
                        database INI configuration file (default: db.conf)
  --executions-table EXECUTIONS_TABLE
                        executions table name (default: scheduler_execution)
  --jobs-table JOBS_TABLE
                        jobs table name (default: scheduler_jobs)
  --logs-table LOGS_TABLE
                        logs table name (default: scheduler_jobauditlog)

APScheduler options:
  --job-coalesce        Coalesce missed executions of a job (default: True)
  --job-max-instances JOB_MAX
                        Maximum number of concurrently executing instances of a job (default: 3)
  --job-misfire JOB_MISFIRE
                        Job misfire grace time in seconds (default: 3600)
  --threadpool-size TP_SIZE
                        Threadpool size (default: 2)
  --timezone TIMEZONE   server's timezone (default: UTC)

Tornado options:
  --max-workers TWORKERS
                        Maximum number of workers (default: 8)

Mitmproxy options:
  --certificate CERTIFICATE
                        TLS private certificate file (default: None)
                         NB: if None, the default certificate of mitmproxy is used
  --htpasswd HTPASSWD   authentication file (default: None)
                         NB: if None, .htpasswd is automatically created with the DEFAULT_USERS

```
