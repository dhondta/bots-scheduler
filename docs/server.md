!!! note "This page is for system administrators"
    
    This page presents some options of the launcher script for tuning the parameters of the application components.
    
    If you want user-oriented information, please consult [the related page](jobs.html). For developer-oriented information, please consult [the other related page](howto.html).

!!! warning "Performance and tuning"
    
    This project uses components based on popular projects. This documentation is not aimed to compare the performance while tuning the component parameters. For more information about their tuning, please refer to the related documentations.

-----

## Overview

The application is architectured as follows:

<p align="center"><img src="img/botscheduler-internals.png" alt="Bots Scheduler's internals"></p>

- Scheduling: [APScheduler](https://apscheduler.readthedocs.io/en/stable/)
- Web server: [Tornado](https://www.tornadoweb.org/en/stable/)
- Web frontend: [Backbone.js](https://backbonejs.org/)
- Backend DB: SQLite, MySQL or PostgreSQL
- Reverse proxy: [mitmproxy](https://mitmproxy.org/)

Application's options are organized per component. You can see it by invoking `--help`:

```sh
$ ./bots-scheduler run --help
[...]
usage: ./bots-scheduler run [-h] [--help] [--debug] [-j JOBS] [-d DATA_DIR]
                            [-l] [-p PORT] [--smtp-config SMTP_CONFIG]
                            [--smtp-profile [SMTP_PROFILE [SMTP_PROFILE ...]]]
                            [--db-config DB_CONFIG] [--db-profile DB_PROFILE]
                            [--executions-table EXECUTIONS_TABLE]
                            [--jobs-table JOBS_TABLE]
                            [--files-table FILES_TABLE]
                            [--logs-table LOGS_TABLE] [--job-coalesce]
                            [--job-max-instances JOB_MAX]
                            [--job-misfire JOB_MISFIRE]
                            [--threadpool-size TP_SIZE] [--timezone TIMEZONE]
                            [--max-workers TWORKERS]
                            [--certificate CERTIFICATE] [--htpasswd HTPASSWD]

```

-----

## Server

The server can be run locally or not and its basic parameters, host IP address and port, are tunable. You can also tune the location where it searches for job classes. Note that this last parameter is a list, meaning that `--jobs` can be used multiple times to include multiple paths.

```sh
[...]
base options:
  --debug               run the server in debug mode (default: False)
  -j JOBS, --jobs JOBS  folder with jobs to be imported (default: ['jobs'])
  -d DATA_DIR, --data-dir DATA_DIR
                        folder with the data files to be used (default: data)
  -l, --local           force running the server locally (default: False)
  -p PORT, --port PORT  server's port number (default: 8888)
                         NB: this will be the listening port of the proxy, this of the scheduler will be port+1
[...]
```

## Notifications

The scheduler can be tuned to send email notifications when tasks give an output. You can tune this by specifying an SMTP configuration in the INI format and one or more SMTP profiles, as defined in the SMTP configuration. These profiles are the section titles of the INI configuration.

```sh
[...]
notification options:
  --smtp-config SMTP_CONFIG
                        SMTP INI configuration file (default: conf/smtp.ini)
  --smtp-profile [SMTP_PROFILE [SMTP_PROFILE ...]]
                        SMTP profile to be selected from the configuration file (default: None)
[...]
```

!!! note "SMTP INI configuration fields"
    
    The format supports 7 fields, like shown in the example below.
    
        [my-profile]
        hostname = localhost
        port     = 25
        security = unencrypted
        user     = changeme
        password = changeme
        from     = changeme@mydomain.com
        to       = changeme@mydomain.com
    
    For the sake of simplicity, a template configuration is provided in the `conf` folder of the project.
    
    Note that, for the `security` field, using a default port sets it to the appropriate value such as in the following list. Setting this value is thus, in most cases, not required.
    
    - 25: `unencrypted`
    - 465: `ssl`
    - 587: `starttls`

## Backend database

Thanks to [NdScheduler](https://github.com/Nextdoor/ndscheduler), 3 different classical backends can be selected: SQLite, MySQL and PostgreSQL. The table names can all be tuned for a better flexibility into a production DBMS.

```sh
[...]
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
[...]
```

## Scheduler

The scheduler has multiple parameters that can be tuned as the timezone or coalescing missed job executions. It can limit concurrent executing instances of a same job and applies a grace time for job misfire for preventing the scheduler from being overwhelmed.

```sh
[...]
APScheduler options:
  --job-coalesce        Coalesce missed executions of a job (default: True)
  --job-max-instances JOB_MAX
                        Maximum number of concurrently executing instances of a job (default: 3)
  --job-misfire JOB_MISFIRE
                        Job misfire grace time in seconds (default: 3600)
  --threadpool-size TP_SIZE
                        Threadpool size (default: 2)
  --timezone TIMEZONE   server's timezone (default: UTC)
[...]
```

## Web server

The Web server has only one option for tuning its number of workers.

```sh
[...]
Tornado options:
  --max-workers TWORKERS
                        Maximum number of workers (default: 8)
[...]
```

## Reverse proxy

The reverse authentication proxy is started as a separate process just before starting the scheduling server and stops right after this last one. It can be tuned with a certificate (then avoiding annoying warning messages or blocking due to an unregistered certificate) and a `.htpasswd` credentials file (beware to configure it with relevant permissions).

```sh
[...]
Mitmproxy options:
  --certificate CERTIFICATE
                        TLS private certificate file (default: None)
                         NB: if None, the default certificate of mitmproxy is used
  --htpasswd HTPASSWD   authentication file (default: None)
                         NB: if None, .htpasswd is automatically created with the DEFAULT_USERS
[...]
```

