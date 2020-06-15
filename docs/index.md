## Introduction

Bots Scheduler is a scheduling system based on [Nextdoor Scheduler](https://github.com/Nextdoor/ndscheduler) that uses jobs templated upon [PyBots](https://github.com/dhondta/pybots). It especially focuses on tasks derived from security-related Web services like Shodan or Censys. See the [*Available jobs* page](jobs.html) for a complete list of the available jobs.


### NdScheduler variations

This project implements a launcher for the [NdScheduler](https://github.com/Nextdoor/ndscheduler) server relying on [Tinyscript](https://github.com/dhondta/tinyscript) that uses a virtual environment. It also provides an alternate version of the Web User Interface for enhancing job results and their flexibility to provide formatted reports. Also, in-memory code mutation is achieved using [Tinyscript](https://github.com/dhondta/tinyscript) to adapt/fix some places in the code base of [NdScheduler](https://github.com/Nextdoor/ndscheduler).


### Security features

This project also uses [mitmproxy](https://github.com/mitmproxy/mitmproxy) to protect the original Web server with:

- an authentication proxy (currently relying on HTTP Basic Auth)
- HTTPS enforcement
- HTTP security headers

### Documentation overview

The remainder of this documentation is structured as follows:

- [*Server tuning*](server.html): this section is more sysadmin-oriented and presents application's running options.
- [*Available jobs*](jobs.html): this section is for users that want to manage job tasks in the Web user interface.
- ]*How to make a job*](howto.html): this section is developer-oriented for defining a new job class.
