import sqlalchemy
from ndscheduler import settings, utils
from ndscheduler.core.datastore import tables


tables.DATAFILES = sqlalchemy.Table(
    settings.FILES_TABLENAME, tables.METADATA,
    sqlalchemy.Column('filename', sqlalchemy.Text, nullable=False, primary_key=True),
    sqlalchemy.Column('user', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('created_time', sqlalchemy.DateTime(timezone=True), nullable=False,
                      default=utils.get_current_datetime),
    sqlalchemy.Column('entries', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('description', sqlalchemy.Text, nullable=True))

