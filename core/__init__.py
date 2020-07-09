from ndscheduler import constants, utils
from ndscheduler.core.scheduler_manager import SchedulerManager
from ndscheduler.core.scheduler.base import SingletonScheduler
from ndscheduler.server import handlers
from tinyscript import code

from .proxy import run_proxy
from .server import run_server


# monkey-patch constants
constants.DEFAULT_JOBS_TABLENAME = 'scheduler_jobs'
constants.DEFAULT_EXECUTIONS_TABLENAME = 'scheduler_executions'
constants.DEFAULT_FILES_TABLENAME = 'scheduler_files'
constants.DEFAULT_AUDIT_LOGS_TABLENAME = 'scheduler_jobauditlogs'
constants.AUDIT_LOG_FILE_ADDED = __fa = 6
constants.AUDIT_LOG_DICT[__fa] = "file added"
constants.AUDIT_LOG_FILE_DELETED = __fd = 7
constants.AUDIT_LOG_DICT[__fd] = "file deleted"


# this modification prevents disabled jobs from being triggered by the scheduler
code.replace(SingletonScheduler.run_job, "datastore = utils.get_datastore_instance()", """
    datastore = utils.get_datastore_instance()
    try:
        if not utils.import_from_path(job_class_path).meta_info()['enabled']: return
    except: pass""")

# this modification allows to define proxy job classes without catching these as valid templates in the WUI
code.replace(utils.get_all_available_jobs, "if issubclass(module_property, job.JobBase):",
             "if issubclass(module_property, job.JobBase) and len(module_property.__subclasses__()) == 0 and "
             "type(module_property) != job.JobBase and module_property.meta_info().get('enabled', True)"
             " and module_property.meta_info().get('job_class_name', 'New Job') != 'New Job':")

# this modification leverages the modification on utils.get_all_available_jobs to filter jobs at the scheduler level
code.replace(SchedulerManager.get_jobs, "return self.sched.get_jobs()", """
    enabled_jobs = [j['job_class_string'] for j in utils.get_all_available_jobs()]
    return [j for j in self.sched.get_jobs() if utils.get_job_name(j) in enabled_jobs]""")

# this modification leverages the modification on utils.get_all_available_jobs to filter executions
code.replace(handlers.executions.Handler._get_executions, "return executions", """
    jobs = [j['job_class_string'] for j in utils.get_all_available_jobs()]
    return {'executions': [e for e in executions['executions'] if e.get('job', {}).get('task_name') in jobs]}
    """)

# this modification leverages the modification on utils.get_all_available_jobs to filter audit logs
code.replace(handlers.audit_logs.Handler._get_logs,
    "logs = self.datastore.get_audit_logs(time_range_start, time_range_end)", """
    import json
    from ndscheduler import utils
    enabled_job_ids = [j.id for j in self.scheduler_manager.get_jobs()]
    enabled_jobs = [j['job_class_string'] for j in utils.get_all_available_jobs()]
    logs_list = []
    for log in self.datastore.get_audit_logs(time_range_start, time_range_end)['logs']:
        try:
            if json.loads(log['description'])['job_class_string'] in enabled_jobs:
                logs_list.append(log)
        except ValueError:
            if log['job_id'] in enabled_job_ids:
                logs_list.append(log)
    logs = {'logs': logs_list}""")

# this modification joins settings.DATA_BASE_DIR to arguments of type "file" just before running a job
code.replace(SingletonScheduler.run_scheduler_job, "job_class.run_job(job_id, execution_id, *args, **kwargs)", """
    newargs = []
    for a1, a2 in zip(job_class.meta_info()['arguments'], args):
        if a1['type'] == "file":
            import os
            a2 = os.path.join(settings.DATA_BASE_DIR, a2)
        newargs.append(a2)
    job_class.run_job(job_id, execution_id, *newargs, **kwargs)
    """)

# this modification adapts the default time ranges for API requests of executions and logs
code.replace(handlers.executions.Handler._get_executions, "ten_minutes_ago = now - timedelta(minutes=10)",
                                                          "ten_minutes_ago = now - timedelta(days=1)")
code.replace(handlers.audit_logs.Handler._get_logs, "ten_minutes_ago = now - timedelta(minutes=10)",
                                                    "ten_minutes_ago = now - timedelta(days=1)")

