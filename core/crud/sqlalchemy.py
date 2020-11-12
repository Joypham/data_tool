from core.models.pointlog import PointLog
from core.models.album_track import Album_Track
from core.models.track import Track
from core.models.album import Album
from core.models.crawlingtask import Crawlingtask

from sqlalchemy.dialects import mysql
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, union, distinct, desc
from core.database_connection.sqlalchemy_create_engine import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_compiled_raw_mysql(query):
    """
    # chú ý: muốn chạy get_compiled_raw_mysql phải bỏ .all() trong query
    :param cmd: SQLAlchemy query or statement
    :rtype: str
    """

    if hasattr(query, 'statement'):
        stmt = query.statement
    else:
        stmt = query
    return stmt.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})



