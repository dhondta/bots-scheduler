import dateutil.parser
import dateutil.tz
import os
import string
import tornado.concurrent
import tornado.gen
import tornado.web
from datetime import datetime
from datetime import timedelta
from ndscheduler import constants, settings, utils
from ndscheduler.core.datastore import tables
from ndscheduler.core.datastore.providers import base
from ndscheduler.server.handlers.base import BaseHandler
from sqlalchemy import desc, select
from tinyscript import b, code, codecs, ensure_str
from tinyscript.helpers.data.types import *


def _abspath(filename):
    return os.path.join(settings.DATA_BASE_DIR, filename)


def get_file_metadata(filename):
    """Get the description and lines count of a data file."""
    c, d = 0, ""
    with open(filename) as f:
        for i, l in enumerate(f):
            if i == 0 and l.startswith("#"):
                d = l[1:].strip()
            if len(l.strip()) > 0 and not l.startswith("#"):
                c += 1
    return d, c


class FilesHandler(BaseHandler):
    def __check_data_dir(self, path):
        """Method for checking that the given path is relative to settings.DATA_BASE_DIR."""
        if path.startswith(settings.DATA_BASE_DIR) and os.path.isfile(path):
            self.set_status(200)
        else:
            raise tornado.web.HTTPError(404)

    def _get_files(self):
        """Returns a list of all available data files.

        It's a blocking operation.
        """
        now = datetime.utcnow()
        time_range_end = self.get_argument('time_range_end', now.isoformat())
        one_month_ago = now - timedelta(seconds=2592000)
        time_range_start = self.get_argument('time_range_start', one_month_ago.isoformat())
        return self.datastore.get_datafiles(time_range_start, time_range_end)

    @tornado.concurrent.run_on_executor
    def get_files(self):
        """Wrapper to run _get_data() on a thread executor.

        :return: list for data files
        :rtype:  list
        """
        return self._get_files()

    @tornado.gen.engine
    def get_files_yield(self):
        """Wrapper for get_data in async mode."""
        return_dict = yield self.get_files()
        self.finish(return_dict)

    @tornado.web.removeslash
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        """Returns the list of available data files.

        Handles only one endpoint:
            GET /api/v1/data
        """
        self.get_files_yield()

    @tornado.web.removeslash
    def post(self):
        """Adds a data file.

        add_data() is a non-blocking operation, but audit log is a blocking operation.

        Handles an endpoint:
            POST /api/v1/data
        """
        self.json_args = self.request.files['file'][0]
        # only allowed input format: {"filename":"...","content":"..."}
        for field in ['filename', 'body', 'content_type']:
            if field not in self.json_args:
                raise tornado.web.HTTPError(400, reason='Required field: %s' % field)
        for field in self.json_args.keys():
            if field not in ['filename', 'body', 'content_type']:
                raise tornado.web.HTTPError(400, reason='Unexpected field: %s' % field)
        fn, cont, ctype, descr = self.json_args['filename'], self.json_args['body'], self.json_args['content_type'], ""
        if self.datastore.get_datafile(fn) is not None:
            raise tornado.web.HTTPError(400, reason='File exists')
        path = _abspath(self.json_args['filename'])
        # create the directory tree if it does not exist
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        # filter bad content type
        if ctype != "text/plain":
            raise tornado.web.HTTPError(400, reason='Bad data file content type: %s' % ctype)
        # filter bad extensions
        if os.path.splitext(path)[1] not in [".dat", ".lst", ".raw", ".txt"]:
            raise tornado.web.HTTPError(400, reason='Bad data file extension: %s' % path)
        # this is aimed to mitigate directory traversal ; only paths relative to settings.DATA_BASE_DIR are allowed
        if not path.startswith(settings.DATA_BASE_DIR):
            raise tornado.web.HTTPError(400, reason='Bad data file path: %s' % path)
        # filter content not in printable characters or invalid content
        prefix = b("")
        for i, line in enumerate(cont.splitlines()):
            line = ensure_str(line)
            if i == 0 and line.startswith("#"):
                prefix = b(line[1:].strip())
            if any(ensure_str(c) not in string.printable for c in line):
                raise tornado.web.HTTPError(400, reason='Bad character at line: %s' % string.shorten(line, 40))
            #if not any(f(line) for f in [is_asn, is_domain, is_email, is_hash, is_ip, is_mac, is_port, is_url]):
            #    raise tornado.web.HTTPError(400, reason='Bad content format: %s' % string.shorten(line, 40))
        # then write the file
        with open(path, 'wb') as f:
            f.write(prefix + cont)
        # Blocking operation.
        self.datastore.add_datafile(fn, descr)
        self.datastore.add_audit_log("main", "Data files", constants.AUDIT_LOG_FILE_ADDED, user=self.username,
                                     description="Added data file '{}'".format(fn))
        self.set_status(201)
        self.write({'file': fn})

    def _delete_file(self, filename):
        """Deletes a data file.

        It's a blocking operation.

        :param str filename: Path to the data file, relative to settings.DATA_BASE_DIR.
        """
        path = _abspath(filename)
        self.__check_data_dir(path)
        os.remove(path)
        self.datastore.remove_datafile(filename)
        self.datastore.add_audit_log("main", "Data files", constants.AUDIT_LOG_FILE_DELETED, user=self.username,
                                     description="Deleted data file '{}'".format(filename))

    @tornado.concurrent.run_on_executor
    def delete_file(self, filename):
        """Wrapper for _delete_data() to run on a threaded executor."""
        self._delete_file(filename)

    @tornado.gen.engine
    def delete_file_yield(self, filename):
        yield self.delete_file(filename)

    @tornado.web.removeslash
    def delete(self, filename):
        """Deletes a data file.

        Handles an endpoint:
            DELETE /api/v1/data/filename

        :param str filename: Path to the data file, relative to settings.DATA_BASE_DIR.
        """
        filename = codecs.decode(filename, "url")
        self.delete_file_yield(filename)
        self.finish({'file': filename})

    @tornado.web.removeslash
    def options(self, filename):
        """Checks if a data file exists.

        Handles an endpoint:
            OPTIONS /api/v1/data/filename

        :param str filename: Path to the data file, relative to settings.DATA_BASE_DIR.
        """
        filename = codecs.decode(filename, "url")
        self.__check_data_dir(_abspath(filename))


def __add_datafile(self, filename, description="", **kwargs):
    """Insert a data file.
    :param str filename: string for the relative path to the data file.
    :param str description: string for describing the data file.
    """
    descr, entries = get_file_metadata(_abspath(filename))
    description = description or descr
    datafile = {
        'filename': filename,
        'description': description,
        'entries': entries,
    }
    datafile.update(kwargs)
    data_insert = tables.DATAFILES.insert().values(**datafile)
    self.engine.execute(data_insert)
base.DatastoreBase.add_datafile = __add_datafile


def __build_datafile(self, row):
    """Return datafile from a row of scheduler_datafiles table.
    :param obj row: A row instance of scheduler_datafiles table.
    :return: A dictionary of data file.
    :rtype: dict
    """
    try:
        created_time = self.get_time_isoformat_from_db(row.created_time)
    except:
        created_time = row.created_time.isoformat()
    return_dict = {
        'filename': row.filename,
        'user': row.user,
        'created_time': created_time,
        'entries': row.entries,
        'description': row.description}
    return return_dict
base.DatastoreBase._build_datafile = __build_datafile


def __get_datafile(self, filename):
    """Return a data file dictionary.

    :param str filename: name of the data file.
    :return: data file
    :rtype: dict
    """
    select_file = tables.DATAFILES.select().where(tables.DATAFILES.c.filename == filename)
    rows = self.engine.execute(select_file)
    for row in rows:
        return self._build_datafile(row)
base.DatastoreBase.get_datafile = __get_datafile


def __get_datafiles(self, time_range_start, time_range_end):
    """Return a list of data files.

    :param str time_range_start: ISO format for time range starting point.
    :param str time_range_end: ISO for time range ending point.
    :return: A dictionary with all data files, e.g.,
        {
            'logs': [
                {
                    'filename': ...
                    'user': ...
                    'created_time': ...
                    'entries': ...
                    'description': ...
                }
            ]
        }
        Sorted by created_time.
    :rtype: dict
    """
    utc = dateutil.tz.gettz('UTC')
    start_time = dateutil.parser.parse(time_range_start).replace(tzinfo=utc)
    end_time = dateutil.parser.parse(time_range_end).replace(tzinfo=utc)
    selectable = select('*').where(
        tables.DATAFILES.c.created_time.between(
            start_time, end_time)).order_by(desc(tables.DATAFILES.c.created_time))
    rows = self.engine.execute(selectable)
    return {'files': [self._build_datafile(row) for row in rows]}
base.DatastoreBase.get_datafiles = __get_datafiles


def __remove_datafile(self, filename):
    """Remove a data file.
    :param str filename: string for the relative path to the data file.
    """
    data_delete = tables.DATAFILES.delete().where(tables.DATAFILES.c.filename == filename)
    self.engine.execute(data_delete)
base.DatastoreBase.remove_datafile = __remove_datafile


def __reset_datafiles(self):
    """Reset the table of data files according to the base directory."""
    for row in self.engine.execute(tables.DATAFILES.select()):
        if not os.path.isfile(_abspath(row.filename)):
            data_delete = tables.DATAFILES.delete().where(tables.DATAFILES.c.filename == row.filename)
            self.engine.execute(data_delete)
    for root, _, files in os.walk(settings.DATA_BASE_DIR):
        for f in files:
            f = os.path.relpath(os.path.join(root, f), settings.DATA_BASE_DIR)
            select_file = tables.DATAFILES.select().where(tables.DATAFILES.c.filename == f)
            if len(list(self.engine.execute(select_file))) == 0:
                self.add_datafile(f)
base.DatastoreBase._reset_datafiles = __reset_datafiles

