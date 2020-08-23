import tornado.web
from ndscheduler import settings
from ndscheduler.server import handlers, server
from tinyscript import configparser

from .files import FilesHandler


class BotsSchedulerServer(server.SchedulerServer):
    VERSION = 'v1'
    singleton = None

    def __init__(self, scheduler_instance):
        # Start scheduler
        self.scheduler_manager = scheduler_instance
        scheduler_instance.get_datastore()._reset_datafiles()
        self.tornado_settings = {
            'debug': settings.DEBUG,
            'static_path': settings.STATIC_DIR_PATH,
            'template_path': settings.TEMPLATE_DIR_PATH,
            'scheduler_manager': self.scheduler_manager,
        }
        # Setup server
        URLS = [
            # Index page
            (r'/', handlers.index.Handler),
            # APIs
            (r'/api/%s/files' % self.VERSION, FilesHandler),
            (r'/api/%s/files/(.*)' % self.VERSION, FilesHandler),
            (r'/api/%s/executions' % self.VERSION, handlers.executions.Handler),
            (r'/api/%s/executions/(.*)' % self.VERSION, handlers.executions.Handler),
            (r'/api/%s/jobs' % self.VERSION, handlers.jobs.Handler),
            (r'/api/%s/jobs/(.*)' % self.VERSION, handlers.jobs.Handler),
            (r'/api/%s/logs' % self.VERSION, handlers.audit_logs.Handler),
        ]
        self.application = tornado.web.Application(URLS, **self.tornado_settings)


def run_server(namespace):
    """ This function configures and starts a scheduling server.
    
    :param namespace: options' namespace
    """
    ns = namespace
    # configure and run the server
    # 1. base settings
    settings.DEBUG = ns.debug
    settings.HTTP_ADDRESS = "127.0.0.1"
    settings.HTTP_PORT = ns.port + 1
    settings.JOB_CLASS_PACKAGES = ns.jobs
    settings.DATA_BASE_DIR = ns.data_dir
    settings.TIMEZONE = ns.timezone
    # NB: SCHEDULER_CLASS is not handled
    # 2. database settings
    settings.DATABASE_CLASS = "ndscheduler.core.datastore.providers.%s.Datastore%s" % (ns.dbms, ns.dbms.capitalize())
    settings.DATABASE_CONFIG_DICT = dict(ns.db_config[ns.db_profile])
    settings.JOBS_TABLENAME       = ns.jobs_table
    settings.EXECUTIONS_TABLENAME = ns.executions_table
    settings.FILES_TABLENAME      = ns.files_table
    settings.AUDIT_LOGS_TABLENAME = ns.logs_table
    # 3. other settings
    settings.THREAD_POOL_SIZE      = ns.tp_size
    settings.JOB_MAX_INSTANCES     = ns.job_max
    settings.JOB_COALESCE          = ns.job_coal
    settings.JOB_MISFIRE_GRACE_SEC = ns.job_misfire
    settings.TORNADO_MAX_WORKERS   = ns.tworkers
    # 4. layout settings
    # settings.APP_INDEX_PAGE left as default (index.html)
    settings.STATIC_DIR_PATH = settings.TEMPLATE_DIR_PATH = ns.static_path
    # 5. now start the server with the tuned settings
    from .tables import tables
    BotsSchedulerServer.run()

