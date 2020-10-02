from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, union, distinct, desc
from core.database_connection.sqlalchemy_create_engine import SQLALCHEMY_DATABASE_URI
from core.crud.sqlalchemy import get_compiled_raw_mysql

from core.models.datasource import DataSource
from core.models.playlist_datasource import PlaylistDataSource
from core.models.usernarrative import UserNarrative
from itertools import chain

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_datasourceid_from_youtube_url_and_trackid(youtube_url: str, trackid: str) -> DataSource:
    datasourceid = (db_session.query(DataSource.id)
                    .select_from(DataSource)
                    .filter(DataSource.valid == 1,
                            DataSource.track_id == trackid,
                            DataSource.source_uri == youtube_url)
                    )
    return datasourceid


def remove_datasourceid():
    datasourceid = (db_session.query(PlaylistDataSource.playlist_id, UserNarrative.id.label('narrative_id'))
                    .select_from(DataSource)
                    .outerjoin(PlaylistDataSource,
                               PlaylistDataSource.datasource_id == DataSource.id)
                    .outerjoin(UserNarrative,
                               UserNarrative.content_json.like("%"+ DataSource.id + "%"))
                    .filter(DataSource.id.in_(joy))
                    )
    return datasourceid


if __name__ == "__main__":
    joy = get_datasourceid_from_youtube_url_and_trackid('https://www.youtube.com/watch?v=oOIJecsnaWg','3CC450E5DE2D4E8BB18264375A8C9816')
    # joy_xinh = remove_datasourceid().all()

    # k = list(chain.from_iterable(joy_xinh))
    print(joy_xinh)

